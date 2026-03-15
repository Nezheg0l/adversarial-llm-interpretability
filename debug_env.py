import os

print("🔍 DEBUGGING .ENV FILE...")

env_path = ".env"

if not os.path.exists(env_path):
    print(f"❌ FATAL: File '{env_path}' does not exist in current directory!")
    print(f"   Current Directory: {os.getcwd()}")
    exit(1)

print(f"✅ File '{env_path}' found.")

try:
    with open(env_path, "r") as f:
        lines = f.readlines()
        print(f"   Lines in file: {len(lines)}")
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"): continue
            
            if "=" in line:
                key, value = line.split("=", 1)
                
                masked_value = value[:5] + "*" * 5
                print(f"   🔑 Found Key: {key} = {masked_value}")
                
                
                os.environ[key] = value

    print("\n✅ Manual loading complete. Testing access...")
    print(f"   GEMINI_API_KEY inside Python: {'OK' if os.environ.get('MY_SECRET_KEY') else 'MISSING'}")
    print(f"   GROQ_API_KEY inside Python:   {'OK' if os.environ.get('MY_SECRET_KEY') else 'MISSING'}")

except Exception as e:
    print(f"❌ Error reading file: {e}")
