# 🌐 WebTester

A simple Python automation script that tests websites by:

- Visiting all discovered links on a given page  
- Printing page titles for each visited link  
- Returning to the base URL  
- Attempting to click all `<button>` elements (best-effort)  

Built with **Selenium + Firefox WebDriver**.

---

## 🚀 Features

- Crawl all anchor (`<a>`) links from a base URL  
- Visit each link and display its title  
- Detect and attempt to click `<button>` elements  
- Supports **headless mode** (no browser window)  
- Handles page load waits and timeouts gracefully  

---

## 📦 Installation

Clone the repo:

```bash
git clone git@github.com:murugiclin/webtester.git
cd webtester
