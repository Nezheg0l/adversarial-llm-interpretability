from src.config import Config
from src.utils.llm_provider import LLMProvider

class BlueAgent:
    def __init__(self):
        self.model = Config.BLUE_MODEL 

    def patch(self, source_code, vulnerability_type, exploit_used):
        print(f"🛡️ BLUE TEAM ({self.model}): Analyze & Patching...")
        
        prompt = f"""
        Role: Senior Security Engineer.
        Task: Fix a {vulnerability_type} vulnerability in the Python code below.
        Context: The attacker successfully used the payload: "{exploit_used}".
        
        VULNERABLE CODE:
        {source_code}
        
        REQUIREMENTS:
        1. Replace insecure functions (like os.popen/os.system) with 'subprocess.run'.
        2. Set 'shell=False'.
        3. Return ONLY the complete, fixed Python code. 
        4. Do NOT use Markdown formatting (no ```python blocks).
        """
        
        try:
            code = LLMProvider.generate(prompt, self.model, temperature=0.1)
            
            if code:
                clean_code = code.replace("```python", "").replace("```", "").strip()
                return clean_code
            return None
            
        except Exception as e:
            print(f"❌ Blue Error: {e}")
            return None
