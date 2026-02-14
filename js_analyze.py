#!/usr/bin/env python3
import argparse
import requests
import os
import json
from google import genai

MODEL = "models/gemini-2.5-pro"

# ---------- CONFIG PATH CROSS PLATFORM ----------
def get_config_path():
    if os.name == "nt":
        base = os.path.join(os.environ["USERPROFILE"], ".js_analyze")
    else:
        base = os.path.join(os.path.expanduser("~"), ".config", "js_analyze")

    os.makedirs(base, exist_ok=True)
    return os.path.join(base, "config.json")

CONFIG_PATH = get_config_path()

# ---------- SAVE API KEY ----------
def save_api_key(key):
    with open(CONFIG_PATH, "w") as f:
        json.dump({"api_key": key}, f)
    print(f"[+] API key saved to {CONFIG_PATH}")

# ---------- LOAD API KEY ----------
def load_api_key():
    if not os.path.exists(CONFIG_PATH):
        print("[!] API key not set. Run:\npython js_analyze.py --set-key YOUR_KEY")
        exit(1)

    with open(CONFIG_PATH) as f:
        return json.load(f)["api_key"]

# ---------- FETCH JS ----------
def fetch_js(url):
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"[!] Failed fetching {url}: {e}")
        return None

# ---------- READ LOCAL FILE ----------
def read_file(path):
    try:
        with open(path, "r", errors="ignore") as f:
            return f.read()
    except Exception as e:
        print(f"[!] Failed reading {path}: {e}")
        return None

# ---------- GEMINI ANALYSIS ----------
def analyze(client, content, src):
    prompt = f"""
You are a professional bug bounty hunter.

Analyze this JavaScript and extract:

- functionality summary
- all URLs
- API endpoints
- subdomains
- paths
- hardcoded secrets
- authentication logic
- vulnerabilities
- attack surface

Source: {src}

Code:
{content}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    print("\n========== ANALYSIS ==========\n")
    print(response.text)
    print("\n==============================\n")

# ---------- MAIN ----------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--set-key", help="Save API key once")

    parser.add_argument("-u", "--url")
    parser.add_argument("-f", "--file")
    parser.add_argument("-o", "--list")

    args = parser.parse_args()

    # set key mode
    if args.set_key:
        save_api_key(args.set_key)
        return

    api_key = load_api_key()
    client = genai.Client(api_key=api_key)

    if args.url:
        js = fetch_js(args.url)
        if js:
            analyze(client, js, args.url)

    elif args.file:
        js = read_file(args.file)
        if js:
            analyze(client, js, args.file)

    elif args.list:
        with open(args.list) as f:
            for u in f:
                u = u.strip()
                if not u:
                    continue
                print(f"\n[+] Processing {u}")
                js = fetch_js(u)
                if js:
                    analyze(client, js, u)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()

