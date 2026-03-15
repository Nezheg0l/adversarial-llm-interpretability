from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Vulnerable Target Online</h1>"

@app.route('/ping')
def ping():
    ip = request.args.get('ip')
    if not ip:
        return "Error: No IP provided"
    
    cmd_args = ["ping", "-c", "1", ip]
    
    try:
        result = subprocess.run(cmd_args, capture_output=True, text=True, shell=False)
        
        return result.stdout
    except FileNotFoundError:
        return "Error: 'ping' command not found. Please ensure it's installed and in your system's PATH."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)