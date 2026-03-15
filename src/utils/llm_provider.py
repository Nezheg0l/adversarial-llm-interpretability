import os
import requests
import json

# МИ ПРИБРАЛИ load_dotenv(). Файл вже завантажений через run.py!

class LLMProvider:
    @staticmethod
    def generate(prompt, model_name, temperature=0.5):
        
        # === DEBUG: Щоб ми точно бачили, що відбувається ===
        # (Розкоментуй рядок нижче, якщо знову буде помилка)
        # print(f"DEBUG: Requesting {model_name}. Gemini Key present? {'Yes' if os.getenv('GEMINI_API_KEY') else 'No'}")

        # === GOOGLE GEMINI ===
        if "gemini" in model_name:
            api_key = os.getenv("GEMINI_API_KEY")
            
            if not api_key: 
                # Якщо ключа немає, спробуємо знайти його серед усіх змінних (дебаг)
                print("❌ ERROR: Gemini Key missing in os.environ!")
                return None
            
            # Чистимо ключ ще раз на випадок сміття
            api_key = api_key.strip()
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}
            data = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": temperature}
            }
            
            try:
                resp = requests.post(url, headers=headers, json=data)
                
                if resp.status_code != 200:
                    print(f"❌ Google API Error ({resp.status_code}): {resp.text}")
                    return None
                    
                return resp.json()['candidates'][0]['content']['parts'][0]['text']
            except Exception as e:
                print(f"❌ Gemini Connection Error: {e}")
                return None

        # === GROQ ===
        elif "groq" in model_name or "llama3-70b" in model_name:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key: 
                print("❌ ERROR: Groq Key missing!")
                return None
            
            api_key = api_key.strip()
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}"}
            data = {
                "model": "llama3-70b-8192",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature
            }
            try:
                resp = requests.post(url, headers=headers, json=data)
                return resp.json()['choices'][0]['message']['content']
            except Exception as e:
                print(f"❌ Groq Error: {e}")
                return None

        # === OLLAMA (Local) ===
        else:
            url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
            data = {
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": temperature}
            }
            try:
                resp = requests.post(url, json=data)
                return resp.json()['response']
            except:
                return None
