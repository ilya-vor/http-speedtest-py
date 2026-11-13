#!/usr/bin/env python3
"""10 sequential HTTP(S) downloads; prints avg time, volume and speed. Stdlib, Python 3.10+."""

import http.client
import sys
import time
from urllib.parse import urlsplit

REQUESTS, TIMEOUT, CHUNK = 10, 30.0, 65536


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("usage: speedtest.py URL", file=sys.stderr)
        return 1
    try:
        p = urlsplit(args[0])
        port = p.port
    except ValueError:
        print(f"error: invalid URL: {args[0]!r}", file=sys.stderr)
        return 1
    if p.scheme not in ("http", "https") or not p.hostname:
        print(f"error: not an http(s) URL: {args[0]!r}", file=sys.stderr)
        return 1

    host, path = p.hostname, p.path or "/"
    if p.query:
        path += "?" + p.query

    cls = http.client.HTTPSConnection if p.scheme == "https" else http.client.HTTPConnection
    c = cls(host, port, timeout=TIMEOUT)
    code = 0
    try:
        c.connect()  # handshake kept out of the measured requests
        times, total = [], 0
        for _ in range(REQUESTS):
            t0 = time.perf_counter()
            c.request("GET", path, headers={"Accept-Encoding": "identity"})
            r = c.getresponse()
            while data := r.read(CHUNK):
                total += len(data)
            times.append(time.perf_counter() - t0)
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        code = 130
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        code = 1
    finally:
        c.close()
    if code:
        return code

    t = sum(times)
    speed, mb = total * 8 / t / 1e6, total / t / 1e6
    print(f"Requests          : {REQUESTS}")
    print(f"Avg request time  : {t / len(times) * 1000:.0f} ms")
    print(f"Total downloaded  : {total / 1e6:.1f} MB ({total:,} bytes)")
    print(f"Download speed    : {speed:.1f} Mbit/s ({mb:.2f} MB/s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
