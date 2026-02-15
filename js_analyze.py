#!/usr/bin/env python3
import argparse
import requests
import os
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def get_config_path():
    if os.name == "nt":
        base = os.path.join(os.environ["USERPROFILE"], ".js_analyze")
    else:
        base = os.path.join(os.path.expanduser("~"), ".config", "js_analyze")

    os.makedirs(base, exist_ok=True)
    return os.path.join(base, "config.json")

CONFIG_PATH = get_config_path()

def save_model(model):
    data = {"model": model}
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f)
    print(f"[+] Default model saved: {model}")

def load_model():
    if not os.path.exists(CONFIG_PATH):
        print("[!] Model not configured. Run:\npython js_analyze.py --set-model llama3")
        exit(1)

    with open(CONFIG_PATH) as f:
        return json.load(f)["model"]

def fetch_js(url):
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"[!] Failed fetching {url}: {e}")
        return None

def read_file(path):
    try:
        with open(path, "r", errors="ignore") as f:
            return f.read()
    except Exception as e:
        print(f"[!] Failed reading {path}: {e}")
        return None

def analyze(model, content, src):
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

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    r = requests.post(OLLAMA_URL, json=payload)
    result = r.json()["response"]

    print("\n========== ANALYSIS ==========\n")
    print(result)
    print("\n==============================\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--set-model", help="Set default Ollama model once")

    parser.add_argument("-u", "--url")
    parser.add_argument("-f", "--file")
    parser.add_argument("-o", "--list")

    args = parser.parse_args()

    if args.set_model:
        save_model(args.set_model)
        return

    model = load_model()

    if args.url:
        js = fetch_js(args.url)
        if js:
            analyze(model, js, args.url)

    elif args.file:
        js = read_file(args.file)
        if js:
            analyze(model, js, args.file)

    elif args.list:
        with open(args.list) as f:
            for u in f:
                u = u.strip()
                if not u:
                    continue
                print(f"\n[+] Processing {u}")
                js = fetch_js(u)
                if js:
                    analyze(model, js, u)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
