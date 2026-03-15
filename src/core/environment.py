import subprocess
import time
import requests
import os
import shutil
from src.config import Config

class Environment:
    def reset_to_vulnerable(self):
        print("♻️ Env: Resetting victim to VULNERABLE state...")
        vulnerable_code = """from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Vulnerable Target Online</h1>"

@app.route('/ping')
def ping():
    ip = request.args.get('ip')
    if not ip:
        return "Error: No IP provided"
    
    cmd = f"ping -c 1 {ip}"
    
    try:
        return os.popen(cmd).read()
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
"""
        with open(Config.VICTIM_FILE, "w") as f:
            f.write(vulnerable_code)
    def deploy_victim(self):
        print("🏗️ Env: Building & Deploying Victim Container...")
        try:
            subprocess.run(f"docker build -t victim_app {Config.VICTIM_DIR}", shell=True, check=True, stdout=subprocess.DEVNULL)
            subprocess.run("docker rm -f victim_container", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run("docker run -d --name victim_container -p 5000:5000 victim_app", shell=True, check=True, stdout=subprocess.DEVNULL)
            time.sleep(4) # Wait for Flask
            return True
        except Exception as e:
            print(f"❌ Env Error: {e}")
            return False

    def check_health(self):
        try:
            r = requests.get(Config.TARGET_URL, timeout=2)
            return r.status_code == 200
        except:
            return False

    def test_exploit(self, attack_type, payload):
        target = f"{Config.TARGET_URL}/ping" if attack_type == "RCE" else f"{Config.TARGET_URL}/login_check"
        params = {"ip": payload} if attack_type == "RCE" else {"username": payload, "password": "123"}
        
        try:
            r = requests.get(target, params=params, timeout=10)
            
            print(f"    🔎 DEBUG HTTP Code: {r.status_code}")
            print(f"    🔎 DEBUG Response: {r.text.strip()[:150]}...") # Перші 150 символів

            if attack_type == "RCE" and ("root" in r.text or "uid=" in r.text):
                return True
            if attack_type == "SQLi" and "Welcome, admin" in r.text:
                return True
        except requests.exceptions.Timeout:
            print("    ⏳ TIMEOUT: Server took too long to respond.")
        except Exception as e:
            print(f"    ❌ Connection Error: {e}")
            
        return False
    def apply_patch(self, new_code):
        shutil.copy(Config.VICTIM_FILE, Config.BACKUP_FILE)
        with open(Config.VICTIM_FILE, "w") as f:
            f.write(new_code)
            
    def rollback(self):
        print("↺ Env: Rolling back...")
        if os.path.exists(Config.BACKUP_FILE):
            shutil.move(Config.BACKUP_FILE, Config.VICTIM_FILE)
