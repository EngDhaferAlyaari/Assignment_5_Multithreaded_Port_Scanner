"""Assignment 5: Multithreaded TCP port scanner (IPv4)."""

import argparse
import ipaddress
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


MAX_WORKERS = 50
MAX_PORTS_PER_SCAN = 1024


def check_port(target_ip, port, timeout):
    """Return True when a TCP connection to this port succeeds."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.settimeout(timeout)
            return client.connect_ex((target_ip, port)) == 0
    except OSError:
        return False


def scan_ports(target_ip, start_port, end_port, timeout=0.5,
               workers=MAX_WORKERS, show_all=False):
    """Scan ports concurrently and print results as they finish."""
    started = time.perf_counter()
    open_ports = []
    total = end_port - start_port + 1

    print("Target IP:", target_ip)
    print("Ports:", f"{start_port}-{end_port}")
    print("Threads:", workers)
    print("-" * 44)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(check_port, target_ip, port, timeout): port
            for port in range(start_port, end_port + 1)
        }
        for future in as_completed(futures):
            port = futures[future]
            if future.result():
                open_ports.append(port)
                print(f"[OPEN] Port {port}", flush=True)
            elif show_all:
                print(f"[NOT OPEN] Port {port}", flush=True)

    elapsed = time.perf_counter() - started
    open_ports.sort()
    print("-" * 44)
    print("Open ports:", len(open_ports))
    print("Not open / unreachable:", total - len(open_ports))
    print(f"Elapsed time: {elapsed:.2f} seconds")
    return open_ports


def build_parser():
    parser = argparse.ArgumentParser(
        description="Scan TCP ports on an IPv4 address you own or have permission to test."
    )
    parser.add_argument("target", nargs="?", help="Target IPv4 address, e.g. 127.0.0.1")
    parser.add_argument("--start", type=int, default=1, help="First port (default: 1)")
    parser.add_argument("--end", type=int, default=1024, help="Last port (default: 1024)")
    parser.add_argument("--timeout", type=float, default=0.5, help="Seconds per connection (default: 0.5)")
    parser.add_argument("--workers", type=int, default=50, help="Parallel threads, 1-50 (default: 50)")
    parser.add_argument("--show-all", action="store_true", help="Also show ports that did not accept connections")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.target is None and sys.stdin.isatty():
        try:
            args.target = input("Enter target IPv4 address [127.0.0.1]: ").strip() or "127.0.0.1"
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")
            return 1
    if not args.target:
        parser.error("enter a target IPv4 address (example: 127.0.0.1)")

    try:
        address = ipaddress.ip_address(args.target)
    except ValueError:
        parser.error("invalid IP address")
    if address.version != 4:
        parser.error("this version supports IPv4 addresses only")
    if not (1 <= args.start <= args.end <= 65535):
        parser.error("port range must satisfy 1 <= start <= end <= 65535")
    if args.end - args.start + 1 > MAX_PORTS_PER_SCAN:
        parser.error("select at most 1024 ports per scan")
    if not (1 <= args.workers <= MAX_WORKERS):
        parser.error("workers must be between 1 and 50")
    if not (0.05 <= args.timeout <= 10.0):
        parser.error("timeout must be from 0.05 to 10 seconds")

    try:
        scan_ports(str(address), args.start, args.end,
                   timeout=args.timeout, workers=args.workers,
                   show_all=args.show_all)
    except KeyboardInterrupt:
        print("\nScan interrupted.")
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
