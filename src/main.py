import os
import re
import subprocess
from dotenv import load_dotenv

def find_env_file():
    """Attempt to locate the .env file within Google Drive."""
    drive_path = '/content/drive/MyDrive'
    env_filename = ".env"
    
    for root, dirs, files in os.walk(drive_path):
        if env_filename in files:
            return os.path.join(root, env_filename)
    return None

def setup_ssh():
    # Check if running in Google Colab
    in_colab = 'COLAB_GPU' in os.environ or 'COLAB_TPU_ADDR' in os.environ

    # Mount Google Drive if in an interactive Colab session
    if in_colab:
        print("Running in Google Colab.")
        try:
            from google.colab import drive
            drive_path = '/content/drive'
            if not os.path.ismount(drive_path):
                print("Mounting Google Drive...")
                drive.mount(drive_path)
            else:
                print("Google Drive is already mounted.")
        except ImportError:
            print("Google Colab environment not detected properly. Unable to mount Google Drive.")
    else:
        print("Not running in an interactive Google Colab session. Skipping Google Drive mount.")

    # Locate the .env file automatically
    dotenv_path = find_env_file()
    if dotenv_path:
        load_dotenv(dotenv_path)
        print(f"Loaded .env file from {dotenv_path}")
    else:
        print("No .env file found, proceeding without predefined SSH path.")

    # Attempt to load SSH key path from environment, prompt if not set
    key_path = os.getenv("SSH_KEY_PATH")
    while not key_path or not os.path.exists(key_path):
        key_path = input("Enter the path to your SSH key: ")
        if os.path.exists(key_path):
            print("SSH key found.")
            break
        else:
            print("SSH key not found at the specified path. Please try again or press Ctrl+C to exit.")

    # Set up SSH directory
    print("Copying SSH key to ~/.ssh directory...")
    ssh_dir = os.path.expanduser('~/.ssh')
    os.makedirs(ssh_dir, exist_ok=True)
    subprocess.run(['cp', key_path, f'{ssh_dir}/id_rsa'], check=True)
    subprocess.run(['cp', f'{key_path}.pub', f'{ssh_dir}/id_rsa.pub'], check=True)
    os.chmod(f'{ssh_dir}/id_rsa', 0o600)

    # Add SSH key to ssh-agent
    try:
        agent = subprocess.run(['ssh-agent', '-s'], capture_output=True, text=True, check=True)
        agent_output = agent.stdout.splitlines()
        for line in agent_output:
            if line.startswith("SSH_AUTH_SOCK"):
                ssh_auth_sock = line.split(";")[0].split("=")[1]
                os.environ["SSH_AUTH_SOCK"] = ssh_auth_sock
            elif line.startswith("SSH_AGENT_PID"):
                ssh_agent_pid = line.split(";")[0].split("=")[1]
                os.environ["SSH_AGENT_PID"] = ssh_agent_pid
        subprocess.run(['ssh-add', f'{ssh_dir}/id_rsa'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to start SSH agent or add key: {e}")

    # Output the public key for GitHub
    subprocess.run(['cat', f'{ssh_dir}/id_rsa.pub'], check=True)

    # Prompt user for Git user email with basic validation
    email_pattern = r"[^@]+@[^@]+\.[^@]+"
    while True:
        git_email = input("Enter your Git email: ")
        if re.match(email_pattern, git_email):
            break
        else:
            print("Invalid email format. Please enter a valid email.")

    # Prompt user for Git username with non-empty check
    while True:
        git_name = input("Enter your Git username: ")
        if git_name.strip():
            break
        else:
            print("Username cannot be empty. Please enter a valid username.")

    try:
        subprocess.run(['git', 'config', '--global', 'user.email', git_email], check=True)
        subprocess.run(['git', 'config', '--global', 'user.name', git_name], check=True)
        print("Git user identity has been set successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set Git user identity: {e}")

if __name__ == "__main__":
    setup_ssh()