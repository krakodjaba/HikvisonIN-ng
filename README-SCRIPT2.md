### README.md:

```markdown
# Hikvision Camera Scanner and Exploit

This script scans a specified range of IP addresses for vulnerable Hikvision cameras using common ports (80, 554, 8080). If a vulnerable camera is found, it attempts to download a snapshot from it.

## Requirements

- `python-nmap`: For network scanning.
- `requests`: For making HTTP requests to the cameras.
- `argparse`: For command-line argument parsing.

You can install the required libraries using `pip`:

```bash
pip install python-nmap requests
```

## Usage

### Command-line arguments:

- `-r` or `--iprange`: The IP range or subnet to scan (required). You can specify a range like `192.168.1.0/24` or a list of IPs separated by commas, e.g., `192.168.1.1,192.168.1.2`.
- `-s` or `--savefile`: Flag to save snapshots from vulnerable cameras. If this flag is set, the script will attempt to download a snapshot.
- `-v` or `--verbose`: Enables verbose output, showing additional information about each scan and vulnerability check.

### Example usage:

1. **Scan a subnet and download snapshots from vulnerable cameras:**
   ```bash
   python camera_scanner.py -r 192.168.1.0/24 -v -s
   ```

2. **Scan a specific list of IPs without downloading snapshots:**
   ```bash
   python camera_scanner.py -r 192.168.1.1,192.168.1.2 -v
   ```

## How It Works

1. **Scanning with Nmap**: The script scans the provided IP range for open ports 80, 554, and 8080 (common ports for Hikvision cameras).
2. **Vulnerability Check**: For each open port, the script tries to access the snapshot URL (`/onvif-http/snapshot?auth=YWRtaW46MTEK`). If the camera is vulnerable (i.e., responds with HTTP 200), it is logged and optionally a snapshot is downloaded.
3. **Saving Snapshots**: If the `-s` flag is provided, the script attempts to download snapshots and save them locally using the camera's IP and port in the filename.

## Important Notes

- **Ethical Use**: This script is intended for use on your own devices or with permission. Scanning and exploiting cameras without authorization is illegal.
- **Error Handling**: The script will handle connection issues and will continue scanning the rest of the IP range.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```