# Forex Factory Economic Scraper

An automated data extraction pipeline that scrapes the Forex Factory economic calendar, bypasses Cloudflare bot protection using headless browsers, and structures the messy HTML into a clean, machine-readable Pandas DataFrame.

---

## Overview

**What this is:** A robust web scraping and data cleaning microservice.

**Business Value:**
- **Bypasses Bot Protection:** Uses Playwright to render JavaScript and wait for network idleness, successfully bypassing Cloudflare protections that block standard Python `requests`.
- **Handles Dynamic Data:** Automatically simulates user scrolling to force the rendering of lazy-loaded DOM elements for the entire week.
- **Advanced Data Cleaning:** Uses Pandas to resolve nested HTML structures and forward-fill missing/cascading time data on merged table cells.
- **Algorithmic Trading Ready:** Automatically filters the noise and outputs a clean CSV of "High Impact" USD events, designed to be fed directly into algorithmic trading bots as macroeconomic volatility triggers.

---

## Tech Stack

| Component | Technology |
|---|---|
| **Networking & JS Rendering** | `Playwright` (Headless Chromium) |
| **HTML Parsing** | `BeautifulSoup4` |
| **Data Cleaning & Structuring** | `Pandas` |

---

## Project Structure

```
WebScrapper/
├── scraper.py           # Playwright engine: headless navigation and JS rendering
├── parser.py            # BeautifulSoup & Pandas: HTML parsing and data structuring
├── .gitignore           # Excludes venv, pycache, and local CSV results
└── README.md
```

> Output files are saved to a local `csv result/` directory which is excluded from version control.

---

## Setup & Installation

**1. Clone the repository and create a virtual environment:**

```bash
git clone https://github.com/kennycornellius-collab/Forex-News-Scraper.git
cd Forex-News-Scraper
python -m venv venv
venv\Scripts\activate  # On Windows
```

**2. Install dependencies:**

```bash
pip install playwright beautifulsoup4 pandas
```

**3. Install the Playwright Chromium binary:**

```bash
playwright install chromium
```

---

## Usage

Run the main scraper script:

```bash
python scraper.py
```

### Pipeline Execution

1. **Fetch:** Launches a headless Chromium viewport (1920x5000) to capture lazy-loaded events for the entire current ISO week.
2. **Parse:** Extracts targeted data from the DOM using robust CSS attribute selectors to prevent breakage from minor site updates.
3. **Clean:** Normalizes empty strings to `pd.NA` and uses Pandas `.ffill()` to cascade event times down through grouped rows.
4. **Export:** Generates two output files:
   - `forex_calendar.csv` — The complete, cleaned dataset for the week.
   - `usd_high_impact_calendar.csv` — A filtered dataset containing only severe USD volatility events.

---

## Sample Output (Filtered)

```
Time    Currency  Impact                  Event                        Actual  Forecast
7:30pm  USD       High Impact Expected    Core CPI m/m                 0.2%    0.3%
7:30pm  USD       High Impact Expected    CPI m/m                      0.3%    0.2%
7:30pm  USD       High Impact Expected    CPI y/y                      2.5%    2.4%
7:30pm  USD       High Impact Expected    Unemployment Claims          216K    213K
7:30pm  USD       High Impact Expected    Core PCE Price Index m/m     0.4%    0.3%
7:30pm  USD       High Impact Expected    Prelim GDP q/q               1.4%    1.3%
9:00pm  USD       High Impact Expected    JOLTS Job Openings           6.84M   6.80M
```
