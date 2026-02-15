# JS Analyze AI – Local JavaScript Security Analyzer (Ollama Edition)

JS Analyze AI is a **local AI-powered JavaScript security analysis tool** designed for bug hunters, security researchers, and recon automation workflows.

This version runs **fully offline using local Ollama models**, so **no API key is required**.

---

## Features

* Analyze **remote JavaScript URLs**
* Analyze **local JavaScript files**
* Analyze **multiple JS files from a list**
* Uses **local Ollama AI models**
* One-time model configuration
* Works on **Linux, Windows, and macOS**
* Designed for **bug bounty recon automation**

---

## Installation

### 1. Install Ollama

Download and install:

https://ollama.com

Then pull a model (example):

```bash
ollama pull llama3
```

---

### 2. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/js-analyze-ai.git
cd js-analyze-ai
```

---

### 3. Install Python requirements

```bash
pip install -r requirements.txt
```

---

## One-Time Model Setup

Set the default Ollama model (only once):

```bash
python js_analyze.py --set-model llama3
```

The model name will be saved automatically and used for all future runs.

---

## Usage

### Analyze a remote JavaScript file

```bash
python js_analyze.py -u https://target.com/app.js
```

### Analyze a local JavaScript file

```bash
python js_analyze.py -f app.js
```

### Analyze multiple JavaScript URLs

Create a file `urls.txt`:

```
https://target.com/app.js
https://target.com/main.js
```

Run:

```bash
python js_analyze.py -o urls.txt
```

---

## Output

The tool automatically extracts:

* Application logic summary
* API endpoints
* URLs & subdomains
* Paths
* Hardcoded secrets
* Authentication logic
* Vulnerability hints
* Attack surface

---

## requirements.txt

```
requests
```

---

## Disclaimer

This tool is intended for **authorized security testing, bug bounty programs, and educational purposes only**.
Do not use against systems without permission.

---
