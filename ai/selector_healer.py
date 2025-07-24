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

    def update_selector(self, selector_identifier, new_selector):
        self.selector_map[selector_identifier] = new_selector
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

    def heal_selector(self, context: Context, exception: str, original_selector: str = "") -> str:

        # if original_selector in self.selector_map:
        #     return self.selector_map[original_selector]

        screenshot_path = f"{SCREENSHOTS_DIR}/ai-{str(context.bdd_step).replace(' ', '_')}.png"
        context.page.screenshot(path=screenshot_path)
        html_snippet = context.page.content()[:8000]

        prompt = f"""
            You’re helping debug a failed Playwright web automation test. Here's what you have:

                - The full HTML source of the page: {html_snippet}
                - A screenshot of the webpage
                - The Playwright exception: {exception}
                - The BDD step that failed: {context.bdd_step}
                - The original selector used (may be empty): {original_selector}
                - Previously healed selectors (JSON): {json.dumps(self.selector_map, indent=4)}
                
                Your job is to figure out what went wrong and fix it.
                
                Tasks:
                    1. Inspect the HTML and screenshot to find the correct element the test is trying to interact with.
                    2. If the element has a unique attribute like id, data-testid, or similar, use that.
                    3. If not, write a reliable XPath for it.
                    4. Estimate your confidence level in the new selector (as a percentage).
                    5. Suggest a name for the selector (this will be used as the JSON key).
                    6. Return your result as a single JSON block, and do not include any explanation, reasoning, or commentary. Only return valid JSON.
                    
                      "selector_identifier": "your proposed identifier name",
                      "selector": "your proposed xpath or attribute-based selector",
                      "confidence": "your confidence percentage with %",
                      "selector_type": "xpath"
                    
                
                Notes:
                    - Check if a similar selector already exists in the previously healed selectors. If so, reuse or adapt it.
                    - Be accurate but keep the XPath as simple and stable as possible.

        """

        log_info_emoji("🧠 ", f"Querying AI Model | {self.model}...")
        ai_response = self._query_ai(prompt, screenshot_path)
        log_info_emoji("🤖 ", f"AI Response:\n{ai_response}")

        suggested_selector, confidence, selector_type, selector_identifier = extract_selector_and_confidence(ai_response)

        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "exception": exception,
            "suggested_selector_identifier": selector_identifier if original_selector == "" else original_selector,
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
                self.update_selector(selector_identifier, suggested_selector)
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
            selector_identifier = str(json_data.get("selector_identifier")).lower()
            return selector, confidence, selector_type, selector_identifier

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

        # Auto-detect a selector type if still unknown
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