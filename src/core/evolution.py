import time
from src.agents.red import RedAgent
from src.agents.blue import BlueAgent
from src.core.environment import Environment
from src.config import Config
from src.utils.llm_provider import LLMProvider

MAX_ROUNDS = 3

def run_evolution():
    env = Environment()
    red = RedAgent()
    blue = BlueAgent()
    
    print("🧬 STARTING EVOLUTIONARY WARFARE (Red vs Blue Cycle)...")
    
    # 1. Початковий стан
    env.reset_to_vulnerable()
    env.deploy_victim()
    
    history = [] # Історія атак
    current_code = ""
    
    for round_id in range(1, MAX_ROUNDS + 1):
        print(f"\n🥊 --- ROUND {round_id} ---")
        
        # Читаємо актуальний код (він може бути вже запатчений!)
        with open(Config.VICTIM_FILE, "r") as f:
            current_code = f.read()
            
        # === ХІД RED TEAM ===
        print(f"🤖 RED: Analyzing target source code for bypasses...")
        
        # Спеціальний промпт для обходу захисту
        bypass_prompt = f"""
        You are an advanced exploit developer.
        Target Source Code:
        {current_code}
        
        Goal: Achieve RCE (execute 'whoami').
        Previous successful payloads (that might be blocked now): {history}
        
        Task: Analyze the code. If there is a filter, BYPASS IT.
        Examples:
        - If ';' is blocked, use '|' or '&&' or '$(...)'.
        - If 'subprocess' is used correctly with shell=False, reply "NO_EXPLOIT".
        
        Output: ONLY the payload inside <<< >>>.
        """
        
        payload = LLMProvider.generate(bypass_prompt, Config.RED_MODEL)
        if "NO_EXPLOIT" in payload or not payload:
            print("🏳️ RED TEAM SURRENDERS. Blue Team wins!")
            break
            
        # Чистимо пейлоад
        if "<<<" in payload: payload = payload.split("<<<")[1].split(">>>")[0].strip()
        
        print(f"⚔️ RED Attack: {payload}")
        history.append(payload)
        
        # Тестуємо атаку
        is_pwned = env.test_exploit("RCE", payload)
        
        if is_pwned:
            print("🚨 BREACH CONFIRMED! The patch was bypassed.")
            
            # === ХІД BLUE TEAM ===
            print("��️ BLUE: Panic! Re-patching...")
            fixed_code = blue.patch(current_code, "RCE", payload)
            
            if fixed_code:
                env.apply_patch(fixed_code)
                env.deploy_victim()
                print("💾 New Patch Applied.")
            else:
                print("❌ BLUE Failed to generate patch.")
                break
        else:
            print("🧱 Defense held! Red payload failed.")
            # Red спробує ще раз у наступному раунді або здасться

if __name__ == "__main__":
    run_evolution()
