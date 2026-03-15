import sys
import os

# === 1. FORCE LOAD .ENV (На всяк випадок дублюємо логіку) ===
print("🔑 SYSTEM: Loading environment variables manually...")
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')

if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            os.environ[key.strip()] = value.strip().strip('"').strip("'")
    print("✅ SYSTEM: Environment loaded.")
else:
    print("❌ SYSTEM ERROR: .env file not found!")

# === 2. SETUP PATHS ===
# Додаємо поточну папку в Python Path, щоб він бачив 'src'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# === 3. RUN EVOLUTION ===
try:
    from src.core.evolution import run_evolution
except ImportError as e:
    print(f"❌ IMPORT ERROR: {e}")
    sys.exit(1)

if __name__ == "__main__":
    try:
        run_evolution()
    except KeyboardInterrupt:
        print("\n🛑 Evolution stopped by user.")
