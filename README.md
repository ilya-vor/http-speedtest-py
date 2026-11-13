# speedtest.py — sequential HTTP download speed test

Single-file, stdlib-only tool that makes **10 sequential HTTP(S) requests** to a
URL, waits for each response body to be fully read, and prints the **average
request time**, **total downloaded volume** and **download speed**.

## Requirements

- **Python 3.10+**, no third-party packages.

## Usage

```bash
git clone https://github.com/ilya-vor/http-speedtest-py.git
cd http-speedtest-py
python speedtest.py URL          # URL = http(s) address, e.g. a large image/file
```

> ⚠️ Downloads *real* data (10 × file size). Check the file size on metered links.

### Example

```bash
python speedtest.py "https://speed.cloudflare.com/__down?bytes=25000000"
```

```
Requests          : 10
Avg request time  : 2031 ms
Total downloaded  : 250.0 MB (250,000,000 bytes)
Download speed    : 98.5 Mbit/s (12.31 MB/s)
```

## Units

Decimal (SI) units, same convention providers advertise:

- **Mbit/s** = 10⁶ bits/s; **MB/s** = 10⁶ bytes/s; **kB/MB/GB** = 10³/10⁶/10⁹ bytes.
- Binary prefixes (KiB/MiB) are **never** used.

```
speed_Mbit_s = total_body_bytes × 8 / total_request_time / 1e6
```

## How it works

One keep-alive connection is reused across all 10 requests; each body is read to
the end in 64 KB chunks; `Accept-Encoding: identity` is sent so counted bytes
equal the real file size. Use files **≥ 10 MB** for a meaningful number (small
files are latency-bound).

## Exit codes

| Code | Meaning |
|---|---|
| `0` | success |
| `1` | usage/URL/connection error |
| `130` | interrupted (Ctrl+C) |

## License

MIT.
