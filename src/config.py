import os

def load_env_manually():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_file = os.path.join(base_dir, '.env')
    
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                
                
                key, value = line.split('=', 1)
                
                clean_key = key.strip()
                clean_value = value.strip().strip('"').strip("'")
                
                os.environ[clean_key] = clean_value
              
load_env_manually()

class Config:
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    
    GEMINI_API_KEY = os.getenv("MY_SECRET_KEY")
    GROQ_API_KEY = os.getenv("MY_SECRET_KEY")
    
    RED_MODEL = "gemini-2.5-flash"
    BLUE_MODEL = "gemini-2.5-flash"
    
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    VICTIM_DIR = os.path.join(BASE_DIR, "victim")
    VICTIM_FILE = os.path.join(VICTIM_DIR, "app.py")
    BACKUP_FILE = os.path.join(VICTIM_DIR, "app.py.bak")

    TARGET_HOST = "localhost"
    TARGET_PORT = 5000
    TARGET_URL = f"http://{TARGET_HOST}:{TARGET_PORT}"
