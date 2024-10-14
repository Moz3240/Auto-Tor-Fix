# GitHub: Moz3240

import time
import os
import subprocess
import sys
import requests
import re
from pathlib import Path

def run_command(command, capture_output=False, check=True):
    try:
        if capture_output:
            result = subprocess.run(command, shell=True, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return result.stdout.strip()
        else:
            subprocess.run(command, shell=True, check=check)
    except subprocess.CalledProcessError as e:
        print(f"[!] Error executing the command: {command}\nerror: {e}")
        raise e

def check_root():
    if os.geteuid() != 0:
        print("[!] Please run the script with root access (sudo).")
        sys.exit(1)

def ensure_pip3():
    try:
        check_pip3 = run_command('dpkg -s python3-pip', capture_output=True)
        if 'install ok installed' not in check_pip3:
            raise subprocess.CalledProcessError
    except subprocess.CalledProcessError:
        print('[+] pip3 Not installed. Installing pip3...')
        run_command('apt update')
        run_command('apt install python3-pip -y')
        print('[!] pip3 Successfully installed.')

def ensure_dependencies():
    try:
        import requests
    except ImportError:
        print('[+] The requests library is not installed. Installing...')
        run_command('pip3 install requests')
        run_command('pip3 install requests[socks]')
        print('[!] The requests library has been successfully installed.')

def find_torrc():
    possible_paths = [
        '/etc/tor/torrc',
        '/usr/local/etc/tor/torrc',
        '/etc/torrc'
    ]
    for path in possible_paths:
        if Path(path).is_file():
            return path
    print("[!] Torrc file not found. Please specify its path.")
    custom_path = input("[+] Please enter the torrc path: ")
    if Path(custom_path).is_file():
        return custom_path
    else:
        print("[!] The path entered is invalid.")
        sys.exit(1)

def ensure_tor():
    try:
        run_command('which tor', capture_output=True)
    except subprocess.CalledProcessError:
        print('[+] Tor is not installed. Installing Tor...')
        run_command('apt update')
        run_command('apt install tor -y')
        print('[!] Tor has been successfully installed.')

def clear_screen():
    os.system("clear")

def get_current_ip():
    url = 'https://www.myexternalip.com/raw'
    try:
        response = requests.get(url, proxies={
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }, timeout=10)
        return response.text.strip()
    except requests.RequestException:
        return "Error in receiving IP"

def change_ip():
    try:
        run_command('systemctl reload tor || service tor reload')
        print('[+] Your IP is changing...')
        time.sleep(5) 
        new_ip = get_current_ip()
        print('[+] Your IP has changed to: ' + new_ip)
    except Exception as e:
        print(f'[!] IP change was not successful: {e}')

def stop_tor():
    try:
        run_command('systemctl stop tor || service tor stop')
        print('[!] Tor service stopped.')
    except subprocess.CalledProcessError:
        print('[!] Failed to stop Tor service.')

def add_manual_ip(torrc_path):
    ips = []
    while True:
        ip = input("\n[+] Enter your desired IP (enter [N] to finish) >> ")
        if ip.lower() == 'n':
            break
        if validate_ip(ip):
            ips.append(ip)
        else:
            print("[!] The IP entered is invalid. Please enter a valid IP.")
    
    if ips:
        exit_nodes = ','.join(ips)
        try:
            with open(torrc_path, 'r') as f:
                lines = f.readlines()
            with open(torrc_path, 'w') as f:
                for line in lines:
                    if not (line.startswith("ExitNodes") or line.startswith("StrictNodes")):
                        f.write(line)
            with open(torrc_path, 'a') as f:
                f.write(f"\nExitNodes {exit_nodes}\n")
                f.write("StrictNodes 1\n")
            print('\n[■] Manual Tor running...\n')
            run_command('systemctl reload tor || service tor reload')
        except PermissionError:
            print('[!] You do not have sufficient access to edit the torrc file.')
        except Exception as e:
            print(f'[!] Error adding ip {e}')
    else:
        print('[!] No IP was added.')

def remove_manual_ips(torrc_path):
    try:
        with open(torrc_path, 'r') as f:
            lines = f.readlines()
        
        with open(torrc_path, 'w') as f:
            for line in lines:
                if not (line.startswith("ExitNodes") or line.startswith("StrictNodes")):
                    f.write(line)
        print('\n[■] The IP list has been successfully deleted.')
        run_command('systemctl reload tor || service tor reload')
    except FileNotFoundError:
        print('[!] Torrc file not found.')
    except PermissionError:
        print('[!] You do not have sufficient access to edit the torrc file.')
    except Exception as e:
        print(f'[!] Error deleting IP list {e}')

def validate_ip(ip):
    pattern = re.compile(
        r'^(\d{1,3}\.){3}\d{1,3}$'
    )
    if pattern.match(ip):
        parts = ip.split('.')
        for part in parts:
            if int(part) < 0 or int(part) > 255:
                return False
        return True
    return False

# main
def main_menu(torrc_path):
    while True:
        clear_screen()
        print('''\033[1;32;40m \n
┌────────────────────────────────────────────────────────┐
│    _         _          _____            _____ _       │
│   / \  _   _| |_ ___   |_   _|__  _ __  |  ___(_)_  __ │
│  / _ \| | | | __/ _ \    | |/ _ \| '__| | |_  | \ \/ / │
│ / ___ \ |_| | || (_) |   | | (_) | |    |  _| | |>  <  │
│/_/   \_\__,_|\__\___/    |_|\___/|_|    |_|   |_/_/\_\ │
└────────────────────────────────────────────────────────┘
        ''')
        print("\033[1;40;31m GitHub: M O Z 3 2 4 0 | Tor is online : 127.0.0.1:9050\n")
        print(" 1. Auto")
        print(" 2. Manual Mode")
        print(" 3. Exit")
        choice = input("\n[+] Enter your choice (1-3): >> ")

        if choice == '1':
            automatic_mode(torrc_path)
        elif choice == '2':
            manual_mode(torrc_path)
        elif choice == '3':
            print("Exiting")
            stop_tor()
            sys.exit()
        else:
            print("[!] Invalid selection. Try again.")
            time.sleep(2)

# Auto
def automatic_mode(torrc_path):
    clear_screen()
    print("\033[1;92;40m A U T O | T O R\n")
    time.sleep(1)
    
    x = input("[+] time to change IP in Sec [type=60] >> ")
    lin = input("[+] how many times do you want to change your IP [type=1000] for infinite IP change type [0] >> ")

    if not x.isdigit() or not lin.isdigit():
        print("[!] Invalid input. Enter whole numbers.")
        time.sleep(2)
        return
    
    try:
        interval = int(x)
        count = int(lin)
    except ValueError:
        print("[!] Invalid input. Enter whole numbers.")
        time.sleep(2)
        return

    try:
        with open(torrc_path, 'r') as f:
            lines = f.readlines()
        with open(torrc_path, 'w') as f:
            for line in lines:
                if not (line.startswith("ExitNodes") or line.startswith("StrictNodes")):
                    f.write(line)
        run_command('systemctl reload tor || service tor reload')
        print("\n[■] Auto mode is activated ~\n")
    except FileNotFoundError:
        print('[!] Torrc file not found.')
    except PermissionError:
        print('[!] You do not have sufficient access to edit the torrc file.')
    except Exception as e:
        print(f'[!] Error in setting automatic mode: {e}')

    try:
        if count == 0:
            print("[+] Start Auto changing IP indefinitely. Press [ Ctrl+C ] to stop.")
            while True:
                time.sleep(interval)
                change_ip()
        else:
            print(f"[+] Starting Auto IP change for {count} times")
            for i in range(count):
                time.sleep(interval)
                change_ip()
            print('[■] IP change finished.')
    except KeyboardInterrupt:
        print('\n[!] Auto IP change stopped by user.')
    except Exception as e:
        print(f'[!] Error: {e}')

    input("[!] Press [ Enter ] to return to the main menu.")

# manual_mode
def manual_mode(torrc_path):
    while True:
        clear_screen()
        print("\033[1;92;40m M A N U A L | M O D E\n")
        time.sleep(1)
        
        print(" 1. Add IP")
        print(" 2. Delete ip list")
        print(" 3. Main Menu")
        choice = input("[+] Enter your choice (1-3): >> ")

        if choice == '1':
            add_manual_ip(torrc_path)
        elif choice == '2':
            remove_manual_ips(torrc_path)
        elif choice == '3':
            break
        else:
            print("[!] Invalid selection. Try again.")
            time.sleep(2)
            continue

        input("Press [ Enter ] to continue...")

def main():
    check_root()
    ensure_pip3()
    ensure_dependencies()
    ensure_tor()
    
    torrc_path = find_torrc()
    
    clear_screen()
    print("Starting Tor...")
    try:
        run_command('systemctl start tor || service tor start')
    except subprocess.CalledProcessError:
        print("[!] Failed to start Tor service.")
        sys.exit(1)
    
    time.sleep(3)
    current_ip = get_current_ip()
    if current_ip != "Error in receiving IP":
        print(f"\033[1;92;40m Tor Actived (127.0.0.1:9050)\n[+] IP : {current_ip}\n")
    else:
        print("\033[1;93;40m Tor Actived 127.0.0.1 : 9050\n")
    
    main_menu(torrc_path)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n[!] User = Stopped')
        stop_tor()
        sys.exit()
    except Exception as e:
        print(f'[!] Error: {e}')
        stop_tor()
        sys.exit()
