# agent_module.py
def execute_action(action: str):
    """
    Simulated agent execution with whitelist
    """
    allowed_actions = ["send_email", "generate_report"]
    
    if action not in allowed_actions:
        return f"⚠️ Unsafe action blocked: {action}"
    return f"✅ Action executed safely: {action}"
