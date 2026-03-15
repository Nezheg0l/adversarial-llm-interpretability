import re
from src.config import Config
from src.utils.llm_provider import LLMProvider

class RedAgent:
    def __init__(self):
        self.model = Config.RED_MODEL 

    def attack(self, attack_type, history=[]):
        print(f"🤖 RED TEAM ({self.model}): Generating payload for {attack_type}...")
        
        prompt = """
        You are a Red Team penetration tester.
        Target: Python Flask app executing: os.popen(f"ping -c 1 {input}")
        Goal: Achieve Remote Code Execution (RCE) to run 'whoami'.
        
        CONSTRAINTS:
        1. Use '127.0.0.1' as the base IP to speed up execution.
        2. Use the semicolon ';' separator (e.g., 127.0.0.1; command).
        3. Do NOT use command substitution like $(...).
        4. Return ONLY the payload wrapped in <<< >>> tags.
        
        Example Output: <<< 127.0.0.1; whoami >>>
        """
        
        if history:
            prompt += f"\nPREVIOUS FAILED ATTEMPTS: {history}\nTry a different variation."

        try:
            response_text = LLMProvider.generate(prompt, self.model, temperature=0.7)
            
            if not response_text:
                print("❌ Red Error: Empty response from LLMProvider")
                return None

            match = re.search(r'<<<(.*?)>>>', response_text, re.DOTALL)
            if match:
                return match.group(1).strip()
            
            if ";" in response_text: 
                return response_text.strip()
                
            return response_text.split('\n')[0]
            
        except Exception as e:
            print(f"❌ Red Error: {e}")
            return None
