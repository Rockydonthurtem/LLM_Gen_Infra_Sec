# mock_llm.py
def call_llm(prompt: str):
    """
    Safe mock LLM that simulates output for testing.
    Detects 'malicious' patterns.
    """
    forbidden_phrases = [
        "ignore previous instructions",
        "reveal secrets",
        "print hidden",
        "delete_all_accounts",
    ]
    
    if any(phrase in prompt.lower() for phrase in forbidden_phrases):
        return "⚠️ Security warning: malicious prompt detected."
    
    # Simulate normal LLM response
    #print(f"LLM Response: processed your prompt safely.\nPrompt was: {prompt[:50]}...")
    return f"LLM Response: processed your prompt safely.\nPrompt was: {prompt[:50]}..."
