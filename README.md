# JS Analyze AI – JavaScript Security Analyzer

AI-powered JavaScript analysis tool that helps bug hunters automatically extract:

* Application logic
* API endpoints
* URLs & subdomains
* Paths
* Hardcoded secrets
* Authentication flows
* Vulnerabilities & attack surface

The tool uses **Google Gemini models** to perform deep security analysis on JavaScript files.

---

## Features

* Analyze **remote JS files**
* Analyze **local JS files**
* Analyze **multiple JS URLs**
* Store API key once (no need to enter again)
* Works on **Windows and Linux**
* Designed for **bug bounty recon workflows**

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/js-analyze-ai.git
cd js-analyze-ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Setup API Key (one-time)

```bash
python js_analyze.py --set-key YOUR_GEMINI_API_KEY
```

---

## Usage

### Analyze a single JS URL

```bash
python js_analyze.py -u https://target.com/app.js
```

### Analyze a local JS file

```bash
python js_analyze.py -f app.js
```

### Analyze multiple JS URLs

Create `urls.txt`:

```
https://target.com/app.js
https://target.com/main.js
```

Run:

```bash
python js_analyze.py -o urls.txt
```

---

## Example Output

The tool automatically extracts:

* Endpoints
* Secrets
* URLs
* Subdomains
* Authentication logic
* Vulnerability hints
* Recon attack surface

---

## requirements.txt

```
google-genai
requests
```

---

## Use Cases

* Bug bounty recon automation
* JavaScript endpoint discovery
* API hunting
* Secret exposure detection
* Hidden attack surface discovery

---

## Disclaimer

This tool is intended for **authorized security testing, bug bounty programs, and educational purposes only**.
Do not use against systems without permission.

