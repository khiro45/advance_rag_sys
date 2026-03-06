from app.services.agentic.base import prompt_manager

def prompt_loader(agent_name: str, prompt_name: str, prompt_args: dict = None):
    """Bridge for the legacy prompt_loader using the new prompt_manager."""
    return prompt_manager.load_prompt(agent_name, prompt_name, prompt_args)
