"""
cli_utils.py — Utilities for terminal interaction
"""

def prompt_for_backend(default_backend: str) -> str:
    """
    Prompt the user to select an AI backend.
    """
    print("\n" + "="*40)
    print("  🤖 AI BACKEND SELECTION")
    print("="*40)
    print(f"Current default: {default_backend.upper()}")
    print("-" * 40)
    print("Choose your model:")
    print("  1. Ollama (Local Llama 3.2)")
    print("  2. Google Gemini (Cloud)")
    print("-" * 40)
    
    choice = input("Enter choice (1 or 2, Enter for default): ").strip()
    
    if choice == "1":
        return "ollama"
    elif choice == "2":
        return "gemini"
    else:
        print(f"Using default: {default_backend.upper()}")
        return default_backend
