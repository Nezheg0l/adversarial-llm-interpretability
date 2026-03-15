import os
import requests

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                os.environ[k.strip()] = v.strip().strip('"').strip("'")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ Key missing")
    exit()

print(f"🔑 Using Key: {api_key[:5]}...")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
resp = requests.get(url)

if resp.status_code == 200:
    print("\n✅ AVAILABLE MODELS:")
    models = resp.json().get('models', [])
    for m in models:
        if "generateContent" in m.get("supportedGenerationMethods", []):
            print(f"   - {m['name'].replace('models/', '')}")
else:
    print(f"❌ Error: {resp.text}")

