# BrowserStack Automation Assignment

This repository contains Selenium WebDriver automation scripts to test the El País website  
across multiple desktop and mobile browsers using BrowserStack’s cloud infrastructure.

---

## Project Overview

This project demonstrates automated cross-browser and cross-device testing by running Selenium tests in parallel on BrowserStack cloud infrastructure.  
The tests cover:

- Windows 11 with latest Chrome  
- macOS Monterey with latest Safari  
- Windows 10 with latest Firefox  
- Samsung Galaxy S22 (Android Chrome)  
- iPhone 14 (iOS Safari)

The tests verify that the El País homepage loads correctly by checking the presence of page content and title.  
It also handles cookie consent popups automatically and saves screenshots for each session.  
Test results are marked as pass/fail in the BrowserStack dashboard for easy review.

---

## Prerequisites

- Python 3.x installed (recommend Python 3.7 or higher)  
- `selenium` Python package  
- BrowserStack account with valid username and access key

---

## Installation and Setup

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/BrowserStack-Assignment.git
cd BrowserStack-Assignment

## Features
- Scrapes top 5 opinion articles from El País (Spanish).
- Downloads cover images.
- Translates titles to English using Google Translate API.
- Identifies repeated words in translated titles.
- Ready for cross-browser automation on BrowserStack.

## Installation
```bash
pip install -r requirements.txt
```

## Run
```bash
python main.py
```
```bash
python tests/browserstack_test.py
```

##Configure BrowserStack credentials
BROWSERSTACK_USERNAME = "prachisingh_WrTAvo"
BROWSERSTACK_ACCESS_KEY = "C46LBQpENkdPsTSqTiKA"
