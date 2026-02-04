import os
from typing import Dict, Any
import re

class PromptLoader:
    def __init__(self, base_path: str = None):
        if base_path is None:
            # Default to the directory where this file resides + 'prompts_data'
            base_path = os.path.join(os.path.dirname(__file__), "prompts_data")
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def load_prompt(self, workflow_name: str, prompt_name: str, **kwargs) -> str:
        """
        Loads a .md prompt file from a workflow directory and formats it with kwargs.
        Example: load_prompt("research_agent", "system_step", user_name="John")
        """
        file_path = os.path.join(self.base_path, workflow_name, f"{prompt_name}.md")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Prompt file not found at: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Format the content with provided parameters
        try:
            return content.format(**kwargs)
        except KeyError as e:
            raise KeyError(f"Missing parameter for prompt '{prompt_name}': {e}")
        except Exception as e:
            raise Exception(f"Error formatting prompt '{prompt_name}': {e}")

    def list_workflows(self):
        """Lists available workflow directories."""
        return [d for d in os.listdir(self.base_path) if os.path.isdir(os.path.join(self.base_path, d))]

# Global instance for use in the app
prompt_loader = PromptLoader()
