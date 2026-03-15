from flask import Flask, request, redirect
import requests
import json

app = Flask(__name__)

# --- CONFIG ---
# Збільшуємо надійність підключення
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

RICKROLL_LYRICS = """
We're no strangers to love
You know the rules and so do I...
NEVER GONNA GIVE YOU UP!
NEVER GONNA LET YOU DOWN!
(Get Rickrolled, Script Kiddie!)
"""

def ask_ai_to_be_linux(cmd):
    # Промпт, який перетворює ШІ на термінал Ubuntu
    prompt = f"""
    You are a simulator of an Ubuntu Linux terminal.
    I will send a command, and you reply ONLY with what the terminal would show.
    
    CONTEXT:
    - User: root
    - Hostname: banking-server
    - Files in directory: 'config.php', 'wallet.dat', 'top_secret_passwords.txt', 'backup.tar.gz'.
    
    COMMAND RECEIVED: {cmd}
    
    RULES:
    1. Do NOT write explanations.
    2. Do NOT write "Here is the output".
    3. If command is 'ls' or 'll', output a realistic file list with dates/permissions.
    4. If command is 'cat' for a generic file, invent realistic content.
    5. Output raw text only.
    """
    
    try:
        # 🔥 ВАЖЛИВО: Тайм-аут 30 секунд (щоб GPU встигла)
        resp = requests.post(OLLAMA_URL, json={
            "model": "qwen2.5-coder:7b", 
            "prompt": prompt, 
            "stream": False,
            "options": {"temperature": 0.2} # Низька температура для стабільності
        }, timeout=30)
        
        # Чистимо сміття, якщо ШІ його додав
        clean_text = resp.json()['response'].replace("```bash", "").replace("```", "").strip()
        return clean_text
    except Exception as e:
        return f"Error: AI Connection Timeout or Failed. ({e})"

@app.route('/')
def home():
    return "<h1>System Online</h1>"

# ПАСТКА 1: SQLi (Переадресація на YouTube)
@app.route('/login_check')
def login_check():
    username = request.args.get('username')
    if username and ("'" in username or "OR" in username or "UNION" in username):
        print(f"🪤 HONEYPOT: SQLi Redirect -> Rickroll")
        return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return "Login Failed"

# ПАСТКА 2: RCE (AI Simulation)
@app.route('/admin/ping')
def ping():
    ip = request.args.get('ip')
    if not ip: return "No IP"
    
    # Якщо це спроба виконати команду
    if ";" in ip or "|" in ip or "$(" in ip or "`" in ip:
        try:
            cmd = ip.split(";")[-1].strip()
        except:
            cmd = "whoami"
            
        print(f"🪤 HONEYPOT: Command captured -> {cmd}")
        
        # Спеціальна перевірка для нашого файлу-приманки
        if "cat" in cmd and "top_secret_passwords.txt" in cmd:
            return RICKROLL_LYRICS
            
        # Миттєві відповіді (щоб не чекати ШІ на прості речі)
        if cmd == "whoami": return "root\n"
        if cmd == "id": return "uid=0(root) gid=0(root) groups=0(root)\n"
        if cmd == "pwd": return "/var/www/html/admin_backup\n"

        # Все інше йде до ШІ
        return ask_ai_to_be_linux(cmd) + "\n"
    
    return f"Ping result for {ip}..."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
