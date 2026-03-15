from src.agents.red import RedAgent
from src.agents.blue import BlueAgent
from src.core.environment import Environment
from src.config import Config
from src.utils.logger import ExperimentLogger
import time

def run_simulation():
    env = Environment()
    red = RedAgent()
    blue = BlueAgent()
    logger = ExperimentLogger() 
    
    print("🚀 INITIALIZING RESEARCH LAB...")
    if not env.deploy_victim():
        return

    env.reset_to_vulnerable() 
    
    attack_type = "RCE" 
    
    
    start_time = time.time()
    payload = red.attack(attack_type)
    print(f"⚔️ Attack Payload: {payload}")
    
    vuln_confirmed = env.test_exploit(attack_type, payload)
    patch_duration = 0
    defense_success = False

    if vuln_confirmed:
        print("🚨 VULNERABILITY CONFIRMED!")
      
        patch_start = time.time()
        with open(Config.VICTIM_FILE, "r") as f:
            vuln_code = f.read()
            
        fixed_code = blue.patch(vuln_code, attack_type, payload)
        
        if fixed_code:
            env.apply_patch(fixed_code)
            env.deploy_victim()
            patch_duration = time.time() - patch_start 
            
            print("🕵️ Verifying Patch...")
            if env.check_health():
                if not env.test_exploit(attack_type, payload):
                    print(f"✅ SUCCESS: Patch blocked the attack (Time: {patch_duration:.2f}s)")
                    defense_success = True
                else:
                    print("❌ FAILURE: Patch didn't fix the vuln.")
                    env.rollback()
            else:
                print("❌ FAILURE: Patch broke the app.")
                env.rollback()
    else:
        print("🤷 Attack failed (False Negative).")

    logger.log_result(attack_type, payload, vuln_confirmed, round(patch_duration, 2), defense_success)
    logger.print_stats()

if __name__ == "__main__":
    run_simulation()
