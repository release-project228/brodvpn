#!/usr/bin/env python3
"""Check TCP reachability of hosts — a small network diagnostic.

Example: python probe.py 1.1.1.1:443 8.8.8.8:53
"""
import socket
import sys


def check(host: str, port: int, timeout: float = 5.0) -> bool:
    s = socket.socket()
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        return True
    except OSError:
        return False
    finally:
        s.close()


def main() -> int:
    targets = [a.split(":") for a in sys.argv[1:]] or [["1.1.1.1", "443"]]
    ok = True
    for pair in targets:
        try:
            host, port = pair[0], int(pair[1])
        except (IndexError, ValueError):
            print(f"bad target: {pair}", file=sys.stderr)
            continue
        reachable = check(host, port)
        ok &= reachable
        print(f"{host}:{port}  {'ok' if reachable else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
