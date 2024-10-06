# setup_ssh.py

import os
import subprocess

def setup_ssh():
    # Check if running in Google Colab and if it's an interactive session
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

    # Define paths for keys
    key_path = '/content/drive/MyDrive/colab_ssh/id_rsa' if in_colab else os.path.expanduser('~/colab_ssh/id_rsa')
    ssh_dir = os.path.expanduser('~/.ssh')

    # Check if the key exists
    if os.path.exists(key_path):
        print("SSH key found. Copying key to ~/.ssh directory...")
        # Load the SSH keys
        os.makedirs(ssh_dir, exist_ok=True)
        subprocess.run(['cp', key_path, f'{ssh_dir}/id_rsa'], check=True)
        subprocess.run(['cp', f'{key_path}.pub', f'{ssh_dir}/id_rsa.pub'], check=True)
        os.chmod(f'{ssh_dir}/id_rsa', 0o600)

        # Add SSH key to ssh-agent
        try:
            # Start the SSH agent and set environment variables
            agent = subprocess.run(['ssh-agent', '-s'], capture_output=True, text=True, check=True)
            agent_output = agent.stdout.splitlines()
            for line in agent_output:
                if line.startswith("SSH_AUTH_SOCK"):
                    ssh_auth_sock = line.split(";")[0].split("=")[1]
                    os.environ["SSH_AUTH_SOCK"] = ssh_auth_sock
                elif line.startswith("SSH_AGENT_PID"):
                    ssh_agent_pid = line.split(";")[0].split("=")[1]
                    os.environ["SSH_AGENT_PID"] = ssh_agent_pid
            
            # Add the key to the SSH agent
            subprocess.run(['ssh-add', f'{ssh_dir}/id_rsa'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to start SSH agent or add key: {e}")

        # Output the public key for GitHub
        subprocess.run(['cat', f'{ssh_dir}/id_rsa.pub'], check=True)
    else:
        print("SSH key not found. Please ensure the key is present in the specified location.")

if __name__ == "__main__":
    setup_ssh()
