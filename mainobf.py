import chromedriver_autoinstaller
import undetected_chromedriver as uc
import random
import sys
import os
import subprocess
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style, init
import customtkinter as ctk
from tkinter import simpledialog, messagebox

init(autoreset=True)

CHROME_EXECUTABLE_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
]

def get_random_proxy(proxies):
    proxy_url = random.choice(proxies)
    return {"http": proxy_url, "https": proxy_url}

def get_random_user_agent():
    return random.choice(user_agents)

def get_chrome_options():
    options = uc.ChromeOptions()
    options.binary_location = CHROME_EXECUTABLE_PATH
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')
    options.add_argument(f'--user-agent={get_random_user_agent()}')
    return options

def simulate_view(proxies, target_url):
    proxy = get_random_proxy(proxies)
    options = get_chrome_options()
    options.add_argument(f'--proxy-server={proxy["http"]}')

    driver = None
    success = False
    reason = None
    try:
        chromedriver_autoinstaller.install()

        driver = uc.Chrome(
            options=options,
            version_main=103
        )
        driver.get(target_url)

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        driver.execute_script("window.scrollTo(0, 0);")

        body = driver.find_element(By.TAG_NAME, "body")
        body_width = body.size['width']
        body_height = body.size['height']

        x_center = body_width / 2
        y_center = body_height / 2

        actions = ActionChains(driver)
        actions.move_to_element_with_offset(body, x_center, y_center).click().perform()

        message = f"{Fore.GREEN}View simulated successfully! | Proxy: {proxy['http']} | User-Agent: {get_random_user_agent()}{Style.RESET_ALL}"
        print(message)
        success = True
    except Exception as e:
        error_type = type(e).__name__
        message = f"{Fore.RED}Failed to simulate view: {error_type} - {str(e)}{Style.RESET_ALL}"
        print(message)
        reason = str(e)
    finally:
        if driver:
            driver.quit()
        kill_chrome_process()
    return success, reason

def kill_chrome_process():
    try:
        chrome_processes = subprocess.check_output('tasklist', shell=True).decode()
        if 'chrome.exe' in chrome_processes:
            subprocess.call(['taskkill', '/F', '/IM', 'chrome.exe'])
            print(f"{Fore.YELLOW}Terminated remaining Chrome processes.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Failed to terminate Chrome processes: {e}{Style.RESET_ALL}")

def check_proxies(proxies, target_url):
    working_proxies = []
    for proxy in proxies:
        try:
            response = requests.get(target_url, proxies={"http": proxy, "https": proxy}, timeout=5)
            if response.status_code == 200:
                working_proxies.append(proxy)
                print(f"{Fore.GREEN}Working proxy: {proxy}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Failed proxy: {proxy}{Style.RESET_ALL}")
        except requests.RequestException:
            print(f"{Fore.RED}Failed proxy: {proxy}{Style.RESET_ALL}")

    with open('workingproxy.txt', 'w') as file:
        for proxy in working_proxies:
            file.write(proxy + '\n')

    print(f"{Fore.GREEN}Working proxies saved to 'workingproxy.txt'.{Style.RESET_ALL}")
    return working_proxies

class ViewBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Slat.cc Destroyer By Germanized")
        self.root.geometry("450x350")
        self.root.minsize(450, 350)  # Minimum window size
        self.root.configure(bg='#2e2e2e')

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.proxies = self.load_proxies_from_file('proxy.txt')

        self.frame = ctk.CTkFrame(root, corner_radius=20)
        self.frame.pack(padx=20, pady=20, fill='both', expand=True)

        self.title_label = ctk.CTkLabel(self.frame, text="Slat.cc Destroyer", font=("Roboto", 24, 'bold'))
        self.title_label.pack(pady=(10, 5))

        self.subtitle_label = ctk.CTkLabel(self.frame, text="F*ck qwerl1_3 for ignoring me for a week in obfing it so u cant skid", font=("Roboto", 12), text_color="#FF6666")
        self.subtitle_label.pack(pady=(0, 20))

        self.url_label = ctk.CTkLabel(self.frame, text="Enter Target URL:", font=("Roboto", 14))
        self.url_label.pack(pady=(0, 5))

        self.url_entry = ctk.CTkEntry(self.frame, width=300)
        self.url_entry.pack(pady=(0, 10))

        self.start_button = ctk.CTkButton(self.frame, text="Start View Botting", command=self.start_view_botting, corner_radius=10)
        self.start_button.pack(pady=(0, 10), fill='x')

        self.check_button = ctk.CTkButton(self.frame, text="Check Proxies", command=self.check_proxies, corner_radius=10)
        self.check_button.pack(pady=(0, 10), fill='x')

        self.exit_button = ctk.CTkButton(self.frame, text="Exit", command=root.quit, corner_radius=10)
        self.exit_button.pack(pady=(0, 10), fill='x')

        self.status_label = ctk.CTkLabel(self.frame, text="Status will be shown here", font=("Roboto", 12))
        self.status_label.pack(pady=(10, 0))

    def load_proxies_from_file(self, file_path):
        proxies = []
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith("http://") or line.startswith("https://"):
                        proxies.append(line)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Proxy file not found: {file_path}")
            sys.exit()
        return proxies

    def start_view_botting(self):
        target_url = self.url_entry.get()
        if not target_url:
            messagebox.showwarning("Warning", "Please enter a valid target URL.")
            return

        num_views = simpledialog.askinteger("Input", "Enter the number of views to simulate:")
        if num_views:
            hits = 0
            misses = 0
            for _ in range(num_views):
                success, reason = simulate_view(self.proxies, target_url)
                if success:
                    hits += 1
                else:
                    misses += 1
                self.update_status(f"Hits: {hits} Misses: {misses} - Last Error: {reason}")

    def check_proxies(self):
        target_url = self.url_entry.get()
        if not target_url:
            messagebox.showwarning("Warning", "Please enter a valid target URL.")
            return

        working_proxies = check_proxies(self.proxies, target_url)
        if working_proxies:
            messagebox.showinfo("Info", "Working proxies found and saved to 'workingproxy.txt'.")
            self.proxies = working_proxies
        else:
            messagebox.showwarning("Warning", "No working proxies found.")

    def update_status(self, message):
        print(message)
        self.status_label.configure(text=message)

if __name__ == "__main__":
    root = ctk.CTk()
    app = ViewBotApp(root)
    root.mainloop()
