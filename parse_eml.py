"""Pull the useful parts out of a .eml file for phishing triage.

Usage: python parse_eml.py sample.eml [more.eml ...]

Prints headers, SPF/DKIM/DMARC results, the Received chain, every link
in the body, and a SHA256 for each attachment. Attachments are hashed
in memory and never written to disk.
"""
import email
import hashlib
import re
import sys
from email import policy
from urllib.parse import urlparse

URL_RE = re.compile(r'https?://[^\s"\'<>)]+', re.I)


def get_body(msg):
    parts = []
    for part in msg.walk():
        if part.get_content_maintype() == "text" and not part.get_filename():
            try:
                parts.append(part.get_content())
            except Exception:
                raw = part.get_payload(decode=True) or b""
                parts.append(raw.decode("utf-8", "replace"))
    return "\n".join(parts)


def analyze(path):
    with open(path, "rb") as f:
        msg = email.message_from_bytes(f.read(), policy=policy.default)

    print("=" * 80)
    print(path)
    for name in ["Date", "From", "Return-Path", "Reply-To", "To", "Subject", "Message-ID"]:
        if msg.get(name):
            print(f"{name}: {msg.get(name)}")

    # SPF / DKIM / DMARC
    auth = " ".join(str(h) for h in msg.get_all("Authentication-Results", []))
    for check in ["spf", "dkim", "dmarc"]:
        print(f"{check.upper()}: {re.findall(check + r'=(\w+)', auth)}")
    dkim_domain = re.findall(r"header\.d=([^\s;]+)", auth)
    print(f"DKIM signed for: {dkim_domain}")

    # Received chain, oldest hop last
    print("Received (newest first):")
    for hop in msg.get_all("Received", []):
        print("   ", " ".join(str(hop).split())[:150])

    # Links
    urls = sorted(set(URL_RE.findall(get_body(msg))))
    print(f"Links ({len(urls)}):")
    for u in urls:
        print("   ", u[:150], "->", urlparse(u).hostname)

    # Attachments
    for part in msg.walk():
        if part.get_filename():
            data = part.get_payload(decode=True) or b""
            sha = hashlib.sha256(data).hexdigest()
            print(f"Attachment: {part.get_filename()} ({part.get_content_type()}, {len(data)} bytes) sha256={sha}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    for p in sys.argv[1:]:
        analyze(p)
