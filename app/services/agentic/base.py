import os
from typing import Dict, Any

class PromptManager:
    """Unified manager for loading and formatting prompt templates."""
    
    def __init__(self, base_dir: str = "app/services/agentic/prompts"):
        self.base_dir = base_dir

    def load_prompt(self, agent_name: str, prompt_name: str, args: Dict[str, Any] = None) -> str:
        """Loads a prompt template and replaces placeholders with provided args."""
        file_path = os.path.join(self.base_dir, agent_name, f"{prompt_name}.md")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Prompt template not found at {file_path}")
            
        with open(file_path, 'r', encoding='utf-8') as f:
            template = f.read()
            
        if args:
            for key, value in args.items():
                template = template.replace(f"{{{key}}}", str(value))
                
        return template

# Global instance for easy access
prompt_manager = PromptManager()
