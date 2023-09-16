import requests
import time
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)


test_url = 'https://www.example.com'

# Functie om proxies te testen
def test_proxies(proxy_list, test_url):
    working_proxies = []
    bad_proxies = []

    ascii_art = f"""{Fore.CYAN}

██████╗░██████╗░░█████╗░██╗░░██╗██╗░░░██╗  ░█████╗░██╗░░██╗███████╗░█████╗░██╗░░██╗███████╗██████╗░
██╔══██╗██╔══██╗██╔══██╗╚██╗██╔╝╚██╗░██╔╝  ██╔══██╗██║░░██║██╔════╝██╔══██╗██║░██╔╝██╔════╝██╔══██╗
██████╔╝██████╔╝██║░░██║░╚███╔╝░░╚████╔╝░  ██║░░╚═╝███████║█████╗░░██║░░╚═╝█████═╝░█████╗░░██████╔╝
██╔═══╝░██╔══██╗██║░░██║░██╔██╗░░░╚██╔╝░░  ██║░░██╗██╔══██║██╔══╝░░██║░░██╗██╔═██╗░██╔══╝░░██╔══██╗
██║░░░░░██║░░██║╚█████╔╝██╔╝╚██╗░░░██║░░░  ╚█████╔╝██║░░██║███████╗╚█████╔╝██║░╚██╗███████╗██║░░██║
╚═╝░░░░░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░  ░╚════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
{Style.RESET_ALL}"""

    print(Fore.WHITE + f"Proxy testing for {len(proxy_list)} proxies:")
    print(Fore.WHITE + "=============================================")
    print(ascii_art)

    for proxy in proxy_list:
        proxy_url = f"http://{proxy.strip()}"
        proxies = {
            'http': proxy_url,
            'https': proxy_url,
        }

        response_time = -1  
        try:
            start_time = time.time()
            response = requests.get(test_url, proxies=proxies, timeout=3)
            end_time = time.time()
            response_time = end_time - start_time

            if response.status_code == 200:
                result = f"{Fore.GREEN}{{+}}{Style.RESET_ALL} Proxy {proxy.strip()}: Tested in {response_time:.2f} seconds"
                working_proxies.append(proxy)
            else:
                result = f"{Fore.RED}{{-}}{Style.RESET_ALL} Proxy {proxy.strip()}: Error ({response.status_code})"
                bad_proxies.append(proxy)
        except requests.exceptions.RequestException as e:
            result = f"{Fore.RED}{{-}}{Style.RESET_ALL} Proxy {proxy.strip()}: Connection error ({e})"
            bad_proxies.append(proxy)

        print(result)
        if response_time != -1:
            print(f"  Connection time: {response_time:.2f} seconds")
        else:
            print("  Connection time: N/A")

    print("\n" + Fore.WHITE + "Summary:")
    print(Fore.WHITE + "=========")
    print(f"{Fore.GREEN}{{+}}{Style.RESET_ALL} Working proxies: {len(working_proxies)}")
    print(f"{Fore.RED}{{-}}{Style.RESET_ALL} Bad proxies: {len(bad_proxies)}")

   
    user_input = custom_input(f"Do you want to remove bad proxies and keep the good ones in proxies.txt? ({Fore.GREEN}Y{Style.RESET_ALL}/{Fore.RED}n{Style.RESET_ALL}): ").strip().lower()

    if user_input == 'y':
        with open('proxies.txt', 'w') as file:
            file.writelines(working_proxies)
        print(Fore.GREEN + "Good proxies have been saved to proxies.txt." + Style.RESET_ALL)
    else:
        print(Fore.RED + "No changes have been made to proxies.txt." + Style.RESET_ALL)

# Aangepaste input functie om kleuren correct weer te geven
def custom_input(prompt):
    try:
        # Kleur tijdelijk uitschakelen
        Fore._style_stack = []
        return input(prompt)
    finally:
        # Kleur herstellen
        init(autoreset=True)


def display_working_proxies(working_proxies):
    print(Fore.GREEN + "Working Proxies:" + Style.RESET_ALL)
    for proxy in working_proxies:
        print(f"{Fore.GREEN}{{+}} {proxy.strip()}{Style.RESET_ALL}")


def display_bad_proxies(bad_proxies):
    print(Fore.RED + "Bad Proxies:" + Style.RESET_ALL)
    for proxy in bad_proxies:
        print(f"{Fore.RED}{{-}} {proxy.strip()}{Style.RESET_ALL}")


def add_proxy(proxy_list):
    new_proxy = input("Enter a new proxy to add (e.g., 147.0.0.4:8480): ").strip()
    proxy_list.append(new_proxy)
    with open('proxies.txt', 'a') as file:
        file.write(f"{new_proxy}\n")
    print(Fore.GREEN + "Proxy added successfully." + Style.RESET_ALL)


def remove_proxy(proxy_list):
    proxy_to_remove = input("Enter the proxy to remove (e.g., 147.0.0.4:8480): ").strip()
    if proxy_to_remove in proxy_list:
        proxy_list.remove(proxy_to_remove)
        with open('proxies.txt', 'w') as file:
            file.writelines(proxy_list)
        print(Fore.GREEN + "Proxy removed successfully." + Style.RESET_ALL)
    else:
        print(Fore.RED + "Proxy not found in the list." + Style.RESET_ALL)

# Optie om de proxylijst te schonen
def clean_proxy_list(proxy_list):
    proxy_list = [proxy.strip() for proxy in proxy_list if proxy.strip()]
    with open('proxies.txt', 'w') as file:
        file.writelines(proxy_list)
    print(Fore.GREEN + "Proxy list cleaned successfully." + Style.RESET_ALL)

# Optie om de proxylijst te resetten
def reset_proxy_list():
    confirmation = input("Are you sure you want to reset the proxy list? This will remove all proxies. (y/n): ").strip().lower()
    if confirmation == 'y':
        with open('proxies.txt', 'w') as file:
            file.write('')
        print(Fore.GREEN + "Proxy list reset successfully." + Style.RESET_ALL)
    else:
        print(Fore.RED + "Proxy list reset cancelled." + Style.RESET_ALL)

# Functie om het gekleurde menu af te drukken
def print_colored_menu():
    print(Fore.CYAN + r"""

██████╗░██████╗░░█████╗░██╗░░██╗██╗░░░██╗  ░█████╗░██╗░░██╗███████╗░█████╗░██╗░░██╗███████╗██████╗░
██╔══██╗██╔══██╗██╔══██╗╚██╗██╔╝╚██╗░██╔╝  ██╔══██╗██║░░██║██╔════╝██╔══██╗██║░██╔╝██╔════╝██╔══██╗
██████╔╝██████╔╝██║░░██║░╚███╔╝░░╚████╔╝░  ██║░░╚═╝███████║█████╗░░██║░░╚═╝█████═╝░█████╗░░██████╔╝
██╔═══╝░██╔══██╗██║░░██║░██╔██╗░░░╚██╔╝░░  ██║░░██╗██╔══██║██╔══╝░░██║░░██╗██╔═██╗░██╔══╝░░██╔══██╗
██║░░░░░██║░░██║╚█████╔╝██╔╝╚██╗░░░██║░░░  ╚█████╔╝██║░░██║███████╗╚█████╔╝██║░╚██╗███████╗██║░░██║
╚═╝░░░░░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░  ░╚════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
""" + Style.RESET_ALL)
    print("Menu:")
    print("[1] " + Fore.WHITE + "Check proxies" + Style.RESET_ALL)
    print("[2] " + Fore.WHITE + "Display Working Proxies" + Style.RESET_ALL)
    print("[3] " + Fore.WHITE + "Display Bad Proxies" + Style.RESET_ALL)
    print("[4] " + Fore.WHITE + "Add Proxy" + Style.RESET_ALL)
    print("[5] " + Fore.WHITE + "Remove Proxy" + Style.RESET_ALL)
    print("[6] " + Fore.WHITE + "Clean Proxy List" + Style.RESET_ALL)
    print("[7] " + Fore.WHITE + "Reset Proxy List" + Style.RESET_ALL)
    print("[8] " + Fore.WHITE + "Exit" + Style.RESET_ALL)
if __name__ == "__main__":
    while True:
        print_colored_menu()

        choice = custom_input("Select an option: ").strip()

        if choice == '1':
            with open('proxies.txt', 'r') as file:
                proxy_list = file.readlines()
            test_proxies(proxy_list, test_url)
        elif choice == '2':
            with open('proxies.txt', 'r') as file:
                working_proxies = [proxy.strip() for proxy in file.readlines()]
            display_working_proxies(working_proxies)
        elif choice == '3':
            with open('proxies.txt', 'r') as file:
                bad_proxies = [proxy.strip() for proxy in file.readlines()]
            display_bad_proxies(bad_proxies)
        elif choice == '4':
            with open('proxies.txt', 'r') as file:
                proxy_list = [proxy.strip() for proxy in file.readlines()]
            add_proxy(proxy_list)
        elif choice == '5':
            with open('proxies.txt', 'r') as file:
                proxy_list = [proxy.strip() for proxy in file.readlines()]
            remove_proxy(proxy_list)
        elif choice == '6':
            with open('proxies.txt', 'r') as file:
                proxy_list = file.readlines()
            clean_proxy_list(proxy_list)
        elif choice == '7':
            reset_proxy_list()
        elif choice == '8':
            break
        else:
            print(Fore.RED + "Invalid choice. Please select a valid option." + Style.RESET_ALL)
#ELECTICHYDRA DISCORD AKA ANOEM_074