import os
import subprocess
import json
import sys
from pathlib import Path
import shutil

CONFIG_PATH = os.path.expanduser("~/.gitcommit.json")
INSTALL_PATH = "/usr/local/bin/gitcommit"
VENV_PATH = os.path.expanduser("~/.gitcommit-venv")

def create_config():
    """Create or update the configuration file."""
    print("Setting up gitcommit...")
    api_key = input("Enter your OpenAI API Key: ").strip()
    model = input("Enter the OpenAI model to use (default: gpt-4o): ").strip() or "gpt-4o"
    max_tokens = input("Enter max tokens for the response (default: 300): ").strip() or "300"

    config = {
        "api_key": api_key,
        "model": model,
        "max_tokens": int(max_tokens)
    }

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)
    print(f"Configuration saved to {CONFIG_PATH}.")

def create_virtual_env():
    """Create a virtual environment for gitcommit."""
    if not os.path.exists(VENV_PATH):
        print(f"Creating virtual environment at {VENV_PATH}...")
        subprocess.run([sys.executable, "-m", "venv", VENV_PATH], check=True)

    pip_path = Path(VENV_PATH) / "bin" / "pip"
    print(f"Installing required packages in the virtual environment...")
    subprocess.run([str(pip_path), "install", "--upgrade", "pip"], check=True)
    subprocess.run([str(pip_path), "install", "openai"], check=True)

def install_script():
    """Install the gitcommit script."""
    script_source = os.path.abspath(__file__).replace('setup.py', 'gitcommit.py')
    venv_python = Path(VENV_PATH) / "bin" / "python"

    if not os.path.exists(script_source):
        raise FileNotFoundError(f"Cannot find gitcommit.py at {script_source}.")

    try:
        # Write the script with the virtual environment shebang
        script_content = f"#!{venv_python}\n" + open(script_source).read()
        with open(INSTALL_PATH, "w") as f:
            f.write(script_content)
        os.chmod(INSTALL_PATH, 0o755)
    except PermissionError:
        print("Permission denied. Retrying with sudo...")
        temp_path = "/tmp/gitcommit.py"
        with open(temp_path, "w") as f:
            f.write(script_content)
        subprocess.run(["sudo", "mv", temp_path, INSTALL_PATH], check=True)
        subprocess.run(["sudo", "chmod", "755", INSTALL_PATH], check=True)

    print(f"gitcommit installed successfully at {INSTALL_PATH}.")

def main():
    try:
        create_config()
        create_virtual_env()
        install_script()
        print("\nSetup complete! Use `gitcommit` to generate commit messages.")
    except Exception as e:
        print(f"Error during setup: {e}")

if __name__ == "__main__":
    main()
