import sys
import os
from pathlib import Path
from dotenv import load_dotenv


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

try:
    from src.utils.llm_provider import LLMProvider
except ImportError:
    print("❌ Error: Could not import LLMProvider. Make sure you updated src/utils/llm_provider.py!")
    sys.exit(1)

load_dotenv()

def test_api():
    print("🔍 DIAGNOSTIC: Checking API Keys...")
    
    gemini_key = os.getenv("MY_SECRET_KEY")
    groq_key = os.getenv("MY_SECRET_KEY")

    print(f"   [1] GEMINI_API_KEY found?  -> {'✅ YES' if gemini_key else '❌ NO'}")
    print(f"   [2] GROQ_API_KEY found?    -> {'✅ YES' if groq_key else '❌ NO'}")

    print("\n📡 NETWORK TEST (Sending 'Hello' to models)...")

    
    if gemini_key:
        print("\n👉 Asking Google Gemini (gemini-1.5-flash)...")
        try:
            res = LLMProvider.generate("Reply with only one word: 'Working'", "gemini-1.5-flash")
            if res and "Working" in res:
                print(f"   ✅ SUCCESS! Response: {res.strip()}")
            else:
                print(f"   ⚠️ Connected, but weird response: {res}")
        except Exception as e:
            print(f"   ❌ FAILED: {e}")
    else:
        print("   ⏭️ Skipping Gemini (No Key)")

    
    if groq_key:
        print("\n👉 Asking Groq (llama3-70b-8192)...")
        try:
            res = LLMProvider.generate("Reply with only one word: 'Working'", "llama3-70b-8192")
            if res and "Working" in res:
                print(f"   ✅ SUCCESS! Response: {res.strip()}")
            else:
                print(f"   ⚠️ Connected, but weird response: {res}")
        except Exception as e:
            print(f"   ❌ FAILED: {e}")
    else:
        print("   ⏭️ Skipping Groq (No Key)")

if __name__ == "__main__":
    test_api()
