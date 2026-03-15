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
    
    # === FIX: OS COMMAND INJECTION ===
    # Construct the command as a list of arguments.
    # This is crucial for preventing shell injection when shell=False.
    cmd_args = ["ping", "-c", "1", ip]
    
    try:
        # subprocess.run is the recommended and secure way to run external commands.
        # shell=False prevents the command from being interpreted by a shell,
        # treating 'ip' as a literal argument to 'ping'.
        # capture_output=True captures stdout and stderr.
        # text=True decodes the output as text (UTF-8 by default).
        result = subprocess.run(cmd_args, capture_output=True, text=True, shell=False)
        
        # The original os.popen().read() would return the output even if ping failed
        # (e.g., "ping: unknown host"). We mimic this behavior by returning stdout.
        return result.stdout
    except FileNotFoundError:
        # This exception occurs if the 'ping' command itself is not found on the system.
        return "Error: 'ping' command not found. Please ensure it's installed and in your system's PATH."
    except Exception as e:
        # Catch any other unexpected errors during the execution of subprocess.run.
        return f"An unexpected error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)