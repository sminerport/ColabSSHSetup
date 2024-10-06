# setup_ssh.py

import os

def setup_ssh():
    # Mount Google Drive
    from google.colab import drive
    drive.mount('/content/drive')

    # Create SSH keys if not already generated
    if not os.path.exists('/content/drive/MyDrive/colab_ssh/id_rsa'):
        os.system('ssh-keygen -t rsa -b 4096 -C "scottminer1205@gmail.com" -f /content/drive/MyDrive/colab_ssh/id_rsa -N ""')

    # Load the SSH keys
    os.system('mkdir -p ~/.ssh')
    os.system('cp /content/drive/MyDrive/colab_ssh/id_rsa ~/.ssh/id_rsa')
    os.system('cp /content/drive/MyDrive/colab_ssh/id_rsa.pub ~/.ssh/id_rsa.pub')
    os.system('chmod 600 ~/.ssh/id_rsa')

    # Add SSH key to ssh-agent
    os.system('eval $(ssh-agent -s)')
    os.system('ssh-add ~/.ssh/id_rsa')

    # Output the public key for GitHub
    os.system('cat ~/.ssh/id_rsa.pub')

if __name__ == "__main__":
    setup_ssh()
