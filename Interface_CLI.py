import sys
import os
from colorama import Fore, Style, init
from utils import clear, banner_nmap, enable_autocomplete

# Initialize colorama for Windows compatibility
init(autoreset=True)

def check_sudo():
    """Ensure the script is running with sudo privileges."""
    if os.geteuid() != 0:  # Check if the script is NOT running as root
        print(f"\n{Fore.RED}This script requires sudo privileges!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Restarting with sudo...{Style.RESET_ALL}\n")
        try:
            # Relaunch the script with sudo
            command = ["sudo", sys.executable] + sys.argv
            os.execvp("sudo", command)
        except Exception as e:
            print(f"{Fore.RED}Failed to restart with sudo: {e}{Style.RESET_ALL}")
            sys.exit(1)

enable_autocomplete()

def initial_banner():
    """ Display the CLI banner """
    print(Fore.MAGENTA + Style.BRIGHT + "~~~~~~~~ PENTESTING TOOL ~~~~~~~~".center(50))

def get_username():
    """ Ask for the user's name and return it """
    username = input(Fore.CYAN + "Enter your username: " + Style.RESET_ALL)
    return username

def show_menu_principal(username):
    check_sudo()
    """ Display the main menu with options """
    while True:
        clear()
        print(f"\n{Fore.YELLOW}{username} >>{Style.RESET_ALL} What do you want to do?\n")
        options = [
            f"{Fore.GREEN}[1] Active Information Gathering{Style.RESET_ALL}",
            f"{Fore.GREEN}[2] Explotation & Vuln. Scanns{Style.RESET_ALL}",
            f"{Fore.RED}[3] Exit{Style.RESET_ALL}"
        ]
        for option in options:
            print(option)

        choice = input("\nEnter your choice: ").strip()

        match choice:
            case '1':
                show_menu_AIG(username)
            case '2':
                show_menu_EVS(username)
            case '3':
                print("\nExiting...")
                break
            case _:
                print(f"{Fore.RED}Invalid choice, please try again.{Style.RESET_ALL}")
                input("\nPress Enter to continue...")

def show_menu_AIG(username):
    from Nmap.Nmap_tool import main_Nmap
    """ Display the Active Information Gathering menu """
    while True:
        clear()
        print(f"\n{Fore.YELLOW}{username} >> {Style.RESET_ALL} What do you want to do?\n")
        print(f"You are located in {Fore.LIGHTCYAN_EX}>>{Style.RESET_ALL} "
              f"{Fore.LIGHTYELLOW_EX}Main{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}>>{Style.RESET_ALL} "
              f"{Fore.LIGHTYELLOW_EX}Active Info. Gathering{Style.RESET_ALL}")

        options = [
            f"{Fore.GREEN}[1] Nmap Scanning commands{Style.RESET_ALL}",
            f"{Fore.GREEN}[2] Web Application Recon{Style.RESET_ALL}",
            f"{Fore.GREEN}[3] Directory & File Bruteforcing{Style.RESET_ALL}",
            f"{Fore.GREEN}[4] SMB & NetBios{Style.RESET_ALL}",
            f"{Fore.GREEN}[5] Wifi & Bluetooth Recon{Style.RESET_ALL}",
            f"{Fore.YELLOW}[6] Back to Main Menu{Style.RESET_ALL}",
            f"{Fore.RED}[7] Exit{Style.RESET_ALL}"
        ]
        for option in options:
            print(option)

        choice = input("\nEnter your choice: ").strip()

        match choice:
            case '1':
                banner_nmap("SCAN", "PORTS", "TOOL", username=username)
                main_Nmap(username)
            case '2':
                print("\nWeb Application Recon - Feature not implemented yet.")
            case '3':
                print("\nDirectory & File Bruteforcing - Feature not implemented yet.")
            case '4':
                print("\nSMB & NetBios - Feature not implemented yet.")
            case '5':
                print("\nWifi & Bluetooth Recon - Feature not implemented yet.")
            case '6':
                return
            case '7':
                print("\nExiting...")
                sys.exit(0)
            case _:
                print(f"{Fore.RED}Invalid choice, please try again.{Style.RESET_ALL}")
        input("\nPress Enter to continue...")

def show_menu_EVS(username):
    while True:
        clear()
        print(f"\n{Fore.YELLOW}{username} >> {Style.RESET_ALL} What do you want to do?\n")
        print(f"You are located in {Fore.LIGHTCYAN_EX}>>{Style.RESET_ALL} "
              f"{Fore.LIGHTYELLOW_EX}Main{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}>>{Style.RESET_ALL} "
              f"{Fore.LIGHTYELLOW_EX}Explotation & Vuln. Scanns{Style.RESET_ALL}")

        options = [
            f"{Fore.GREEN}[1] Vulnerability Scanns{Style.RESET_ALL}",
            f"{Fore.GREEN}[2] Exploit Verification{Style.RESET_ALL}",
            f"{Fore.GREEN}[3] Password Attacks{Style.RESET_ALL}",
            f"{Fore.GREEN}[4] Hash Decryption{Style.RESET_ALL}",
            f"{Fore.GREEN}[5] MITM{Style.RESET_ALL}",
            f"{Fore.YELLOW}[6] Back to Main Menu{Style.RESET_ALL}",
            f"{Fore.RED}[7] Exit{Style.RESET_ALL}"
        ]
        for option in options:
            print(option)

        choice = input("\nEnter your choice: ").strip()

        match choice:
            case '1':
                print("\nNmap Scanning - Feature not implemented yet.")
            case '2':
                print("\nMetasploit - Feature not implemented yet.")
            case '3':
                print("\nPassword Attacks - Feature not implemented yet.")
            case '4':
                print("\nHash Decryption - Feature not implemented yet.")
            case '5':
                print("\nMan In the Middle - Feature not implemented yet.")
            case '6':
                return
            case '7':
                print("\nExiting...")
                sys.exit(0)
            case _:
                print(f"{Fore.RED}Invalid choice, please try again.{Style.RESET_ALL}")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    username = get_username()
    show_menu_principal(username)