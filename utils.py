import os
import pyfiglet
import subprocess
import readline
import glob
import shutil
import platform
from colorama import Fore, Style


def clear():
    os.system('cls' if os.name=='nt' else 'clear')

NMAP_FLAGS = ["-sS", "-sT", "-sU", "-A", "-O", "-p", "-Pn", "-v", "-T4", "--script"]

def complete(text, state):
    """Autocomplete function for commands, files, and Nmap options."""
    options = []

    # If text starts with "-", suggest Nmap flags
    if text.startswith("-"):
        options = [flag for flag in NMAP_FLAGS if flag.startswith(text)]

    # If text looks like a file path, autocomplete files/folders
    elif "/" in text or "." in text:
        options = glob.glob(text + "*")  # Suggest matching files/folders

    # Otherwise, suggest system commands
    else:
        try:
            commands = subprocess.getoutput('compgen -c').split()  # Get all Linux commands
            options = [cmd for cmd in commands if cmd.startswith(text)]
        except Exception:
            options = []

    return options[state] if state < len(options) else None

def is_tmux_running():
    """Check if the script is running inside a tmux session."""
    return "TMUX" in os.environ

def get_script_directory():
    """Get the directory where the Python script is located."""
    return os.path.dirname(os.path.abspath(__file__))

def open_command_in_new_terminal(command):
    """Opens a Linux or macOS terminal window and runs the command."""

    system_platform = platform.system()  # Detect OS
    script_dir = get_script_directory()

    if is_tmux_running():
        # If inside tmux, split the screen vertically and run the command
        os.system(f'tmux split-window -v "cd {script_dir} && {command} ; bash"')

    elif system_platform == "Darwin":  # macOS
        try:
            print(f"Opening command in a new macOS Terminal at {script_dir}: {command}")
            apple_script = f'''
            tell application "Terminal"
                do script " cd {script_dir} && {command}; exec bash"
                activate
            end tell
            '''
            subprocess.run(["osascript", "-e", apple_script])
        except Exception as e:
            print(f"Error opening macOS Terminal: {e}")

    elif system_platform == "Linux":
        # List of terminal emulators to try on Linux
        terminal_options = [
            "gnome-terminal -- bash -c",
            "konsole -e",
            "xfce4-terminal -e",
            "x-terminal-emulator -e",
            "mate-terminal -- bash -c",
            "terminator -x",
            "alacritty -e bash -c",
            "kitty -e bash -c",
            "urxvt -e bash -c",
            "st -e bash -c",
            "lxterminal -e bash -c",
            "tilix -e bash -c",
        ]

        for term in terminal_options:
            terminal_cmd = f'{term} "cd {script_dir} && {command} ; exec bash"'
            if shutil.which(term.split()[0]):  # Check if terminal exists
                os.system(terminal_cmd)
                return

        print("No compatible terminal emulator found. Please install a terminal such as gnome-terminal or konsole.")

    else:
        print(f"Unsupported operating system: {system_platform}")

# Enable tab completion globally
def enable_autocomplete():
    """Activates global autocomplete for Linux commands, files, and Nmap options."""
    readline.set_completer(complete)
    readline.parse_and_bind("tab: complete")

def banner_nmap(*words, username):
    titles = [pyfiglet.figlet_format(word).split("\n") for word in words]

    # Find the max number of lines across all words
    max_lines = max(len(title) for title in titles)

    # Normalize the number of lines for each word (padding with empty lines)
    for title in titles:
        title += [""] * (max_lines - len(title))

    # Assign different colors dynamically
    colors = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA, Fore.WHITE]

    # Print the words side by side, line by line
    for lines in zip(*titles):
        print("  ".join(color + line for color, line in zip(colors, lines[:len(words)])) + Style.RESET_ALL)

def run_command(command):
    """Execute a Linux command inside the menu interface."""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"{Fore.RED}{result.stderr}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error executing command: {e}{Style.RESET_ALL}")