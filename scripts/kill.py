"""
Script to kill the running FastAPI server process.
Usage: python kill.py
"""
import os
import signal
import subprocess
import sys
import platform

def find_uvicorn_pid():
    """Find the PID of the running uvicorn process"""
    system = platform.system()
    try:
        if system == "Windows":
            # Use tasklist on Windows
            output = subprocess.check_output("tasklist /FI \"IMAGENAME eq python.exe\" /FO CSV", shell=True).decode()
            lines = output.strip().split('\n')
            for line in lines[1:]:  # Skip header
                parts = line.strip('"').split('","')
                if len(parts) >= 2 and "uvicorn" in line:
                    return int(parts[1])
        else:
            # Use ps on Unix-like systems
            output = subprocess.check_output("ps -ef | grep uvicorn | grep -v grep", shell=True).decode()
            if output:
                return int(output.split()[1])
    except subprocess.CalledProcessError:
        pass
    return None

def kill_uvicorn():
    """Kill the running uvicorn process"""
    pid = find_uvicorn_pid()
    if pid:
        try:
            system = platform.system()
            if system == "Windows":
                subprocess.call(f"taskkill /F /PID {pid}", shell=True)
            else:
                os.kill(pid, signal.SIGTERM)
            print(f"Killed uvicorn process with PID {pid}")
            return True
        except Exception as e:
            print(f"Error killing process: {e}")
    else:
        print("No running uvicorn process found")
    return False

if __name__ == "__main__":
    if not kill_uvicorn():
        print("Checking for port 8000 usage...")
        try:
            system = platform.system()
            if system == "Windows":
                # Find process using port 8000 on Windows
                output = subprocess.check_output("netstat -ano | findstr :8000", shell=True).decode()
                if output:
                    parts = output.strip().split()
                    for part in parts:
                        if part.isdigit() and int(part) > 1000:
                            pid = int(part)
                            subprocess.call(f"taskkill /F /PID {pid}", shell=True)
                            print(f"Killed process using port 8000 with PID {pid}")
                            break
            else:
                # Find process using port 8000 on Unix-like systems
                output = subprocess.check_output("lsof -i:8000 -t", shell=True).decode()
                if output:
                    pid = int(output.strip())
                    os.kill(pid, signal.SIGTERM)
                    print(f"Killed process using port 8000 with PID {pid}")
        except subprocess.CalledProcessError:
            print("No process found using port 8000")
        except Exception as e:
            print(f"Error: {e}")
