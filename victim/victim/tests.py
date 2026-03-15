import requests
import sys

# Адреса контейнера
BASE_URL = "http://localhost:5000"

def test_homepage():
    try:
        r = requests.get(BASE_URL)
        if r.status_code == 200 and "Login" in r.text:
            return True
        print(f"❌ Homepage Failed: Status {r.status_code}")
        return False
    except:
        return False

def test_valid_login():
    try:
        # Спроба входу з правильним паролем (з init_db.py)
        # user: user, pass: 123456
        r = requests.get(f"{BASE_URL}/login_check", params={"username": "user", "password": "123456"})
        if "Welcome, user!" in r.text:
            return True
        print(f"❌ Valid Login Failed. Output: {r.text[:50]}...")
        return False
    except:
        return False

def test_ping_functionality():
    try:
        # Перевірка, чи пінг взагалі працює (для адміна)
        # Спочатку треба "обійти" авторизацію (в нашому демо коді адмінка відкрита, це ок)
        r = requests.get(f"{BASE_URL}/admin/ping", params={"ip": "127.0.0.1"})
        if r.status_code == 200 and "bytes from" in r.text:
            return True
        print(f"❌ Ping Function Failed. Output: {r.text[:50]}...")
        return False
    except:
        return False

def run_all_tests():
    print("🧪 RUNNING REGRESSION TESTS...")
    if not test_homepage(): return False
    if not test_valid_login(): return False
    if not test_ping_functionality(): return False
    print("✅ ALL TESTS PASSED. App is healthy.")
    return True

if __name__ == "__main__":
    success = run_all_tests()
    if not success:
        sys.exit(1) # Повертаємо помилку для системи
