import sys
import os

print("🔑 SYSTEM: Loading environment variables manually...")
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')

if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            
            key, value = line.split('=', 1)
            clean_key = key.strip()
            clean_value = value.strip().strip('"').strip("'")
            
            os.environ[clean_key] = clean_value
    print("✅ SYSTEM: Environment loaded.")
else:
    print("❌ SYSTEM ERROR: .env file not found in root!")



if not os.getenv("GEMINI_API_KEY"):
    print("⚠️ WARNING: GEMINI_API_KEY is missing in environment after loading!")
else:
    print("✅ KEY CHECK: Gemini Key is present.")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from src.core.orchestrator import run_simulation
except ImportError as e:
    print(f"❌ IMPORT ERROR: {e}")
    sys.exit(1)

if __name__ == "__main__":
    try:
        run_simulation()
    except KeyboardInterrupt:
        print("\n🛑 Simulation stopped by user.")
