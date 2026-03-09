# Forex Factory Economic Scraper

An automated data extraction pipeline that scrapes the Forex Factory economic calendar, bypasses Cloudflare bot protection using headless browsers, and structures the messy HTML into a clean, machine-readable Pandas DataFrame.

---

## Overview

A robust web scraping and data cleaning microservice that extracts, structures, and delivers a filtered economic calendar every week — fully automated via GitHub Actions with zero infrastructure cost.

The scraper handles two non-trivial problems that block standard approaches: Cloudflare bot protection that rejects plain HTTP requests, and lazy-loaded DOM elements that only render after user interaction. Playwright resolves both by running a real headless Chromium session and simulating scroll behavior before extraction begins.

On the data side, Forex Factory's HTML uses merged table cells for grouped event times — meaning most rows have no time value at all. A Pandas forward-fill pass reconstructs the correct time for every row before export.

The pipeline runs automatically every Monday on GitHub's cloud servers, commits the freshly scraped CSV directly back to the repository, and requires no local setup or manual intervention to keep the data current.

---

## Tech Stack

| Component | Technology |
|---|---|
| **Networking & JS Rendering** | `Playwright` (Headless Chromium) |
| **HTML Parsing** | `BeautifulSoup4` |
| **Data Cleaning & Structuring** | `Pandas` |
| **Automation** | GitHub Actions |

---

## Project Structure

```
WebScrapper/
├── .github/
│   └── workflows/
│       └── scraper.yml      # GitHub Actions workflow — runs every Monday at 00:00 UTC
├── scraper.py               # Playwright engine: headless navigation and JS rendering
├── parser.py                # BeautifulSoup & Pandas: HTML parsing and data structuring
├── csv result/              # Auto-committed output directory (updated weekly by CI)
├── .gitignore               # Excludes venv and pycache
└── README.md
```

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

Run the scraper manually:

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

## Automation — GitHub Actions

The repository includes a workflow that runs the full scraper pipeline automatically every Monday at 00:00 UTC using GitHub's free cloud runners — no local machine or paid infrastructure required.

After each run, the workflow commits the updated CSV files directly back to the repository under `csv result/`, keeping the data current without any manual intervention.

The workflow can also be triggered manually at any time via the **Actions** tab using the `workflow_dispatch` event.

```yaml
name: Forex Factory Weekly Scraper

on:
  schedule:
    - cron: '0 0 * * 1'
  workflow_dispatch:

jobs:
  scrape-and-update:
    runs-on: ubuntu-latest

    permissions:
      contents: write

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install playwright beautifulsoup4 pandas
          playwright install chromium

      - name: Run the Scraper
        run: python scraper.py

      - name: Commit and Push the New Data
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add .
          git commit -m "data: auto-update weekly forex calendar" || exit 0
          git push
```

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