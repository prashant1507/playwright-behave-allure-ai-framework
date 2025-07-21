import os
import json
import re

import ollama

from datetime import datetime

from behave.runner import Context
from playwright.sync_api import Page

from helpers.constants.framework_constants import SCREENSHOTS_DIR
from utils.logger import log_info_emoji, log_error
from utils.misc import load_config


class AISelectorHealer:

    def __init__(self):
        self.model = load_config()['ai_model']
        self.selector_map_file = "selector_map.json"
        self.log_file = "selector_log.json"
        self._load_selector_map()

    def _load_selector_map(self):
        if os.path.exists(self.selector_map_file):
            with open(self.selector_map_file, "r") as f:
                self.selector_map = json.load(f)
        else:
            self.selector_map = {}

    def _save_selector_map(self):
        with open(self.selector_map_file, "w") as f:
            json.dump(self.selector_map, f, indent=2)

    def _log_result(self, entry: dict):
        existing = []
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as f:
                try:
                    existing = json.load(f)
                except:
                    existing = []

        existing.append(entry)
        with open(self.log_file, "w") as f:
            json.dump(existing, f, indent=2)

    def update_selector(self, original_selector, new_selector):
        self.selector_map[original_selector] = new_selector
        self._save_selector_map()

    def _query_ai(self, prompt, screenshot_path):
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            images=[screenshot_path],
            stream=False,
            # keep_alive=0,
            system="You are an expert Quality Assurance Engineer automation expert.",
            options={
                'temperature': 0.1,  # More focused responses
            }
        )

        return response.response

    def stop_model(self):
        res = ollama.generate(
            model=self.model,
            stream=False,
            keep_alive=0,
        )
        if str(res.done_reason) == "unload":
            log_info_emoji("🧠 ", f"AI Model Stopped| {self.model}...")

    def heal_selector(self, original_selector: str, label: str, context: Context) -> str:
        screenshot_path = f"{SCREENSHOTS_DIR}/ai-{str(context.bdd_step).replace(' ', '_')}.png"
        context.page.screenshot(path=screenshot_path)

        # if original_selector in self.selector_map:
        #     return self.selector_map[original_selector]

        html_snippet = context.page.content()[:8000]
        prompt = f"""
            A web automation test failed because the selector `{original_selector}` no longer matches anything in the DOM.

            You are given:
            - The full HTML source of the page  
            - A label that describes the target element: `{label}`  
            - A screenshot of the webpage  
            - BDD Step which failed: `{context.bdd_step}`

            Your tasks:
            1. Inspect the HTML and screenshot to identify the correct element that matches the label `{label}`.  
            2. Check if the original selector `{original_selector}` has a typo or is outdated. If so, correct it.  
            3. If the target element has an `id or data-testid or any other unique property`, **prefer using that for the selector**. Otherwise, construct a reliable **xpath** selector.  
            4. Estimate your confidence level in the new selector, as a percentage.  
            5. Return only the selector and your confidence level in this format:

            Return your answer in the following JSON format:

              "selector": "your proposed xpath selector",
              "confidence": "your confidence percentage with % sign",
              "selector_type": "xpath"
            
            Previously Healed Selectors:\n{json.dumps(self.selector_map, indent=4)}
            HTML:\n{html_snippet}
            
            Tip: If a similar label already exists in the 'Previously Healed Selectors', consider using that selector or adapting it.
        """

        log_info_emoji("🧠 ", f"Querying AI Model | {self.model}...")
        ai_response = self._query_ai(prompt, screenshot_path)
        log_info_emoji("🤖 ", f"AI Response:\n{ai_response}")

        suggested_selector, confidence, selector_type = extract_selector_and_confidence(ai_response)

        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "original_selector": original_selector,
            "suggested_selector": suggested_selector,
            "confidence": confidence,
            "selector_type": selector_type,
            "valid": False
        }

        if suggested_selector:
            is_valid = validate_selector(context.page, suggested_selector, selector_type)
            log_entry["valid"] = is_valid

            if is_valid:
                log_info_emoji("✅ ", f"Selector validated with confidence {confidence}%")
                self.update_selector(original_selector, suggested_selector)
                self._log_result(log_entry)
                return suggested_selector
            else:
                log_info_emoji("❌ ", "Selector suggested by AI did not match anything on the page.")

        self._log_result(log_entry)
        return suggested_selector


def extract_selector_and_confidence(ai_response):
    try:
        # Try to parse JSON block first
        json_match = re.search(r'```json\s*({.*?})\s*```', ai_response, re.DOTALL)
        if json_match:
            json_data = json.loads(json_match.group(1))
            selector = json_data.get("selector")
            confidence = json_data.get("confidence")
            selector_type = str(json_data.get("selector_type")).lower()
            return selector, confidence, selector_type

        # Fallback regex patterns
        selector_patterns = [
            r'Selector:\s*`([^`]+)`',
            r'Selector:\s*([^\n]+)',
            r'text="([^"]+)"',
            r'```(?:css|xpath|text)?\s*([^`]+)```',
            r'//[^\n]+',
            r'h2:-soup-contains\("([^"]+)"\)',
        ]

        confidence_patterns = [
            r'Confidence:\s*(\d+%)',
            r'Confidence:\s*(\d+)',
            r'(\d+)%'
        ]

        selector_type_patterns = [
            r'Selector Type:\s*([^\n]+)',
            r'Type:\s*([^\n]+)',
            r'```(css|xpath|text)',
        ]

        selector = None
        confidence = None
        selector_type = None

        for pattern in selector_patterns:
            match = re.search(pattern, ai_response, re.IGNORECASE)
            if match:
                selector = match.group(1).strip()
                break

        for pattern in confidence_patterns:
            match = re.search(pattern, ai_response)
            if match:
                conf_value = match.group(1)
                confidence = conf_value if conf_value.endswith('%') else f"{conf_value}%"
                break

        for pattern in selector_type_patterns:
            match = re.search(pattern, ai_response, re.IGNORECASE)
            if match:
                selector_type = match.group(1).strip().lower()
                break

        # Auto-detect selector type if still unknown
        if not selector_type and selector:
            if selector.startswith('//') or selector.startswith('./'):
                selector_type = 'xpath'
            elif 'text=' in selector or selector.startswith('text="'):
                selector_type = 'text'
            elif any(c in selector for c in ['.', '#', '[', ':', '>']):
                selector_type = 'css'
            else:
                selector_type = 'unknown'

        return selector, confidence, selector_type

    except Exception as e:
        log_error(f"Error extracting selector info: {e}")
        return None, None, None

def validate_selector(page: Page, selector: str, selector_type: str) -> bool:
    try:
        if selector_type == "xpath":
            return len(page.query_selector_all(f'xpath={selector}')) > 0
        return False
    except Exception:
        return False