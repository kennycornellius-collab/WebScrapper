from bs4 import BeautifulSoup
import pandas as pd
import os
def parse_calendar_html(html_content: str) -> pd.DataFrame:
    print("Parsing HTML with BeautifulSoup")
    soup = BeautifulSoup(html_content, 'html.parser')
    
    table = soup.find("table", class_="calendar__table")
    if not table:
        print("Could not find the calendar table. Structure may have changed.")
        return pd.DataFrame()
        
    events = []
    for row in table.find_all("tr", class_=lambda c: c and "calendar__row" in c):
        
        time_tag = row.select_one('td[class*="time"]')
        currency_tag = row.select_one('td[class*="currency"]')
        impact_tag = row.select_one('td[class*="impact"]')
        event_tag = row.select_one('td[class*="event"]')
        actual_tag = row.select_one('td[class*="actual"]')
        forecast_tag = row.select_one('td[class*="forecast"]')

        time_str = time_tag.get_text(strip=True) if time_tag else ""
        currency = currency_tag.get_text(strip=True) if currency_tag else ""
        event = event_tag.get_text(strip=True) if event_tag else ""
        actual = actual_tag.get_text(strip=True) if actual_tag else ""
        forecast = forecast_tag.get_text(strip=True) if forecast_tag else ""
        impact = ""
        if impact_tag:
            span = impact_tag.find("span", title=True)
            if span:
                impact = span["title"]
            else:
                span_icon = impact_tag.find("span", class_=lambda c: c and "impact" in c)
                if span_icon:
                    impact_class = " ".join(span_icon.get("class", []))
                    if "red" in impact_class: impact = "High"
                    elif "ora" in impact_class: impact = "Medium"
                    elif "yel" in impact_class: impact = "Low"
                    elif "gre" in impact_class: impact = "Non-Economic"
        if event:
            events.append({
                "Time": time_str,
                "Currency": currency,
                "Impact": impact,
                "Event": event,
                "Actual": actual,
                "Forecast": forecast
            })
            
    df = pd.DataFrame(events)

    if not df.empty:
        df['Time'] = df['Time'].str.strip()
        df['Time'] = df['Time'].replace(r'^\s*$', pd.NA, regex=True)
        df['Time'] = df['Time'].ffill()
        df['Time'] = df['Time'].fillna('All Day')
    if not df.empty:
        usd_high_impact = df[(df['Currency'] == 'USD') & (df['Impact'].str.contains('High', na=False, case=False))]
        print("\n--- High Impact USD Events (Gold Triggers) ---")
        print(usd_high_impact.to_string())
        os.makedirs("data", exist_ok=True)
        usd_high_impact.to_csv("data/usd_high_impact_calendar.csv", index=False)
        print("\nFiltered high-impact data saved to usd_high_impact_calendar.csv")
    return df