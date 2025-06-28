# src/guardian_ai/data_processing/sanitizer.py

import re
import json
from transformers import pipeline

class DataSanitizer:
    def __init__(self, config):
        """
        Initializes the sanitizer based on a configuration dictionary.
        """
        self.config = config
        self.enabled = config.get("enable", False)

        # Setup PII detection
        if self.enabled and "pii_detection" in self.config:
            # In a real implementation, we might use a library like 'presidio-analyzer'
            # For this example, we'll simulate it.
            self.pii_entities = self.config["pii_detection"]["entities"]
            self.pii_redaction_token = self.config["pii_detection"]["redaction_token"]
            print(f"✅ PII Sanitizer enabled for: {self.pii_entities}")

        # Setup secrets detection
        if self.enabled and "secrets_detection" in self.config:
            patterns_file = self.config["secrets_detection"]["patterns_file"]
            with open(patterns_file, 'r') as f:
                self.secrets_patterns = json.load(f)
            self.secrets_redaction_token = self.config["secrets_detection"]["redaction_token"]
            print(f"✅ Secrets Sanitizer enabled with patterns from: {patterns_file}")
        
        # Setup toxicity filter
        if self.enabled and self.config.get("toxicity_filtering", {}).get("enable", False):
            tox_conf = self.config["toxicity_filtering"]
            self.toxicity_classifier = pipeline("text-classification", model=tox_conf["model"])
            self.toxicity_threshold = tox_conf["threshold"]
            print(f"✅ Toxicity filter enabled with model: {tox_conf['model']}")


    def sanitize_text(self, text_sample):
        """
        Applies all configured sanitization steps to a single piece of text.
        """
        if not self.enabled:
            return text_sample, True # Return original text and 'is_clean' flag

        # 1. PII Redaction (example with simple regex)
        if "EMAIL_ADDRESS" in self.pii_entities:
            text_sample = re.sub(r'\S+@\S+', self.pii_redaction_token, text_sample)
        # ... add more regex for other entities

        # 2. Secrets Redaction
        if hasattr(self, 'secrets_patterns'):
            for pattern_name, regex in self.secrets_patterns.items():
                text_sample = re.sub(regex, self.secrets_redaction_token, text_sample)

        # 3. Toxicity Check
        if hasattr(self, 'toxicity_classifier'):
            results = self.toxicity_classifier(text_sample)
            # Assuming the model returns {'label': 'toxic', 'score': 0.9}
            # This logic depends on the specific model used
            for result in results:
                if result['label'].lower() == 'toxic' and result['score'] > self.toxicity_threshold:
                    print(f"⚠️ High toxicity detected (score: {result['score']}). Discarding sample.")
                    return None, False # Indicate sample should be dropped
        
        return text_sample, True

    def sanitize_batch(self, batch):
        """
        Takes a batch of data (e.g., a dictionary of lists) and applies sanitization.
        This is what the Hugging Face `dataset.map()` function would call.
        """
        clean_texts = []
        # Assuming the text data is in a column named 'text'
        for text in batch["text"]:
            sanitized_text, is_clean = self.sanitize_text(text)
            if is_clean:
                clean_texts.append(sanitized_text)
            # If not clean, we effectively drop it by not adding it to the new list

        batch["text"] = clean_texts
        return batch