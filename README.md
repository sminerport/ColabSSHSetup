# SSH Setup Script for Google Colab

This repository contains a Python script designed to set up SSH access for use in Google Colab environments. The script handles SSH key setup, Git configuration, and the addition of the SSH key to the SSH agent, making it easier to authenticate with GitHub or other Git servers while working in Colab.

## Files

- **main.py**: The primary setup script. Prompts users for the SSH key path, Git email, and username, then configures Git and SSH settings accordingly.
- **.env.example**: A sample environment file to securely store the SSH key path.
- **LICENSE**: Open source license for this project.

## Requirements

This script assumes:

- You’re using Google Colab or a similar environment.
- You have an SSH key available, either in Google Drive or a custom directory.
- (Optional) You store the path to the SSH key in a `.env` file for convenience and security.

## Usage

1. **Google Drive Mounting (in Colab)**:

   - The script automatically detects if it’s running in Google Colab. If so, it attempts to mount Google Drive at `/content/drive`. Ensure your SSH key is saved in Google Drive or another accessible location.

2. **Environment Variables**:

   - You can create a `.env` file to securely store the path to your SSH key, reducing the need for manual entry.
   - Place the `.env` file in your Google Drive, and the script will automatically locate it within `/content/drive/MyDrive`.
   - Use the provided `.env.example` file as a template. Copy `.env.example` to `.env` and enter the SSH key path under `SSH_KEY_PATH`.

3. **Running the Script**:

   - Execute the script using:
     ```bash
     python main.py
     ```
   - You’ll be prompted to enter:
     - **Path to your SSH key** (if not specified in `.env`): The script will prompt you for this if no valid path is detected.
     - **Git email**: Your email for Git commits (e.g., `username@example.com`).
     - **Git username**: Your GitHub username or other identifier.

4. **Error Handling**:
   - If the specified SSH key path isn’t found, the script will prompt you to re-enter the path.
   - If the Git email format is invalid, it will ask for a correct format.

## Security Notes

- **No sensitive information**: The script doesn’t save or expose any sensitive information by itself.
- **SSH Key Management**: Ensure your SSH private key is securely stored in Google Drive or another safe location.
- **Environment Variables**: The script sets up `SSH_AUTH_SOCK` and `SSH_AGENT_PID` for the current session, which allows secure SSH access within the environment.

## License

This project is licensed under the terms of the included [LICENSE](./LICENSE) file.
