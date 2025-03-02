import socket
import os
import sys
import subprocess
import psutil
from colorama import Fore, Style, init
from utils import run_command, enable_autocomplete, open_command_in_new_terminal
from tabulate import tabulate
import re

init(autoreset=True)

# Dictionary with options
EXTRA_OPTIONS = {
    "1": ("UDP Scan", "-sU"),
    "2": ("Packet Trace", "--packet-trace"),
    "3": ("Verbose Mode", "-v"),
    "4": ("Aggressive Timing", "-T4"),
    "5": ("OS Detection", "-O"),
    "6": ("Service Version Detection", "-sV"),
    "7": ("DNS Resolution Disable", "-n"),
    "8": ("Disable Ping", "-Pn"),
    "9": ("Nmap - Personalized commands (type any nmap command)", ""),
    "10": ("Save Scan to File", "")
}

enable_autocomplete()

def get_network_interfaces():
    """Retrieve all network interfaces and their IPs."""
    interfaces = []
    net_info = psutil.net_if_addrs()  # Get network interfaces

    for interface, addresses in net_info.items():
        for addr in addresses:
            if addr.family == socket.AF_INET:  # IPv4 only
                interfaces.append((interface, addr.address))

    return interfaces

def display_network_info():
    """Prints all detected network interfaces with spacing for readability."""
    interfaces = get_network_interfaces()

    if interfaces:
        print(f"\n{Fore.CYAN}Your Network Interfaces:{Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}{'Interface':<15} {'IP Address':<20}{Style.RESET_ALL}")  # Header

        for interface, ip in interfaces:
            print(f"{Fore.GREEN}{interface:<15} {Fore.YELLOW}{ip:<20}{Style.RESET_ALL}")  # Data row
    else:
        print(f"{Fore.RED}No active network interfaces detected.{Style.RESET_ALL}")

def run_nmap_scan(base_command, extra_flags="", output_file=""):
    """Ejecuta un escaneo Nmap y muestra el resultado.
    command = f"nmap {base_command} {extra_flags}".strip()

    if output_file:
        command += f" -oN {output_file}"

    print(f"\n{Fore.YELLOW}Executing: {command}{Style.RESET_ALL}\n")
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        print(result.stdout if result.stdout else f"{Fore.RED}No output received.{Style.RESET_ALL}")
        if result.stderr:
            print(f"{Fore.RED}Error:{Style.RESET_ALL}\n{result.stderr}")
    except Exception as e:
        print(f"{Fore.RED}Failed to execute Nmap scan: {e}{Style.RESET_ALL}")"""
    """Ejecuta un escaneo Nmap y muestra el resultado de forma más visual."""
    command = f"nmap {base_command} {extra_flags}".strip()

    if output_file:
        command += f" -oN {output_file}"

    print(f"\n{Fore.YELLOW}Executing: {command}{Style.RESET_ALL}\n")
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        output = result.stdout
        if not output:
            print(f"{Fore.RED}No output received.{Style.RESET_ALL}")
            return

        # Analitzar i filtrar la sortida
        ports_info = []
        os_info = "Unknown"
        closed_ports = 0
        scan_time = "Unknown"
        raw_packets_sent = "Unknown"
        raw_packets_rcvd = "Unknown"

        for line in output.split("\n"):
            port_match = re.match(r"(\d+/\w+)\s+(open|filtered|open\|filtered|closed)\s+(\S+)\s?(.*)", line)
            if port_match:
                ports_info.append([port_match.group(1), port_match.group(2), port_match.group(3), port_match.group(4)])
            elif "OS details" in line and ":" in line:
                os_info = line.split(":", 1)[1].strip()
            elif "Not shown:" in line:
                closed_ports_match = re.search(r"(\d+) closed", line)
                closed_ports = int(closed_ports_match.group(1)) if closed_ports_match else 0
            elif "scanned in" in line:
                scan_time = line.split("scanned in")[-1].strip()
            elif "Raw packets sent:" in line:
                packet_match = re.search(r"Raw packets sent: (\d+) .*\| Rcvd: (\d+)", line)
                if packet_match:
                    raw_packets_sent = packet_match.group(1)
                    raw_packets_rcvd = packet_match.group(2)

        # Mostrar la informació de manera més visual
        print(f"\n{Fore.GREEN}Scan Results:{Style.RESET_ALL}\n")
        print(f"{Fore.BLUE}Detected OS:{Style.RESET_ALL} {os_info}\n")

        if ports_info:
            print(tabulate(ports_info, headers=["Port", "State", "Service", "Version"], tablefmt="grid"))
        else:
            print(f"{Fore.RED}No open ports found.{Style.RESET_ALL}")

        print(
            f"\n{Fore.YELLOW}Summary:{Style.RESET_ALL} {len(ports_info)} open/filtered ports, {closed_ports} closed ports")
        print(f"{Fore.YELLOW}Scan Duration:{Style.RESET_ALL} {scan_time}")
        print(
            f"{Fore.YELLOW}Raw Packets Sent:{Style.RESET_ALL} {raw_packets_sent} | {Fore.YELLOW}Received:{Style.RESET_ALL} {raw_packets_rcvd}")

    except Exception as e:
        print(f"{Fore.RED}Error executing Nmap: {e}{Style.RESET_ALL}")


def get_extra_options():
    """Displays a submenu for extra options and returns the chosen parameters."""
    output_file = ""

    while True:
        os.system("clear" if os.name == "posix" else "cls")
        print(f"\n{Fore.CYAN}=== Extra Scan Options ==={Style.RESET_ALL}")
        for key, (desc, _) in EXTRA_OPTIONS.items():
            print(f"{Fore.GREEN}[{key}] {desc}{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}[0] Done selecting options{Style.RESET_ALL}")

        choices = input("\nEnter extra options (e.g., 1+2+3) or '0' to continue: ").strip()

        if choices == "0":
            return "", output_file

        selected_flags = []
        for choice in choices.split("+"):
            if choice in EXTRA_OPTIONS:
                if choice == "9":
                    username = os.getlogin()
                    print(f"\n{Fore.CYAN}{username} >> here Nmap personalized commands{Style.RESET_ALL}\n")
                    custom_command = input(f"{username} >> ").strip()
                    run_nmap_scan(custom_command, "")
                if choice == "10":
                    output_file = input("\nEnter filename to save scan (e.g., scan_results.txt): ").strip()
                else:
                    selected_flags.append(EXTRA_OPTIONS[choice][1])
            else:
                print(f"{Fore.RED}Invalid option: {choice}{Style.RESET_ALL}")

        if selected_flags:
            return " ".join(selected_flags), output_file

def main_Nmap(username):
    #scanner = nmap.PortScanner()
    while True:
        os.system("clear" if os.name == "posix" else "cls")
        print(f"\n{Fore.CYAN}=== Nmap Scanner Interface ==={Style.RESET_ALL}\n")

        options = {
            "1": ("General Scan (Ports 1-65535)", "-p 1-65535"),
            "2": ("Quick Scan (Common Ports)", "-F"),
            "3": ("OS Detection Scan", "-O"),
            "4": ("Stealth Scan (SYN Scan)", "-sS"),
            "5": ("Aggressive Scan (Version + OS)", "-A"),
        }

        for key, (desc, _) in options.items():
            print(f"{Fore.GREEN}[{key}] {desc}{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}[6] Back to Main Menu{Style.RESET_ALL}")
        print(f"{Fore.RED}[7] Exit{Style.RESET_ALL}")

        choice = input("\nEnter your choice: ").strip()

        if choice in options:
            base_command = options[choice][1]
            user_ip = display_network_info()  # Get the user's IP address
            print(f"\n{Fore.CYAN}Your IP Address: {Fore.GREEN}{user_ip}{Style.RESET_ALL}")
            target = input("\nEnter target IP or domain: ").strip()

            extra_flag_prompt = input(f"\nWould you like to add extra filters? (Y/N): ").strip().lower()

            extra_flags, output_file = "", ""
            if extra_flag_prompt == "y":
                extra_flags, output_file = get_extra_options()

            run_nmap_scan(f"{base_command} {target}", extra_flags, output_file)

        elif choice == "6":
            return
        elif choice == "7":
            print("\nExiting...")
            sys.exit(0)
        else:
            print(f"\n{Fore.YELLOW}Opening command in new terminal: {choice}{Style.RESET_ALL}")
            open_command_in_new_terminal(choice)

        input("\nPress Enter to continue...")