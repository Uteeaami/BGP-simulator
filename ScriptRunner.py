import subprocess
import atexit

script1_path = './scripts/create-interfaces.sh'
script2_path = './scripts/update-toml.sh'
script3_path = './scripts/terminate-interfaces.sh'

def run_startup_scripts():
    try:
        subprocess.run(['sudo', 'bash', script1_path])
    except Exception as e:
        print(f"Error running script1: {e}")

    try:
        subprocess.run(['bash', script2_path])
    except Exception as e:
        print(f"Error running script2: {e}")

def run_exit_script():
    try:
        subprocess.run(['bash', script3_path])
    except Exception as e:
        print(f"Error running script3: {e}")

atexit.register(run_exit_script)
