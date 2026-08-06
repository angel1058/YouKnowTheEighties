import cloudscraper
from bs4 import BeautifulSoup
import json
import datetime
import time
import os

def get_chart_dates(start_year, end_year):
    # Find first Sunday of start_year
    current_date = datetime.date(start_year, 1, 1)
    while current_date.weekday() != 6: # 6 is Sunday
        current_date += datetime.timedelta(days=1)
        
    end_date = datetime.date(end_year, 12, 31)
    dates = []
    while current_date <= end_date:
        dates.append(current_date.strftime("%Y%m%d"))
        current_date += datetime.timedelta(days=7)
    return dates

def scrape_4_decades():
    # Use cloudscraper to bypass CloudFront / Cloudflare 403 Forbidden protection
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
    )

    dates = get_chart_dates(1970, 2009)
    total_weeks = len(dates)
    
    songs_map = {}  # (TITLE_UPPER, ARTIST_UPPER) -> id
    songs_list = []
    charts = {}
    next_id = 1

    print("=" * 65, flush=True)
    print(f"Starting 4-Decade UK Chart Scrape (1970-2009): {total_weeks} Weeks", flush=True)
    print("=" * 65, flush=True)

    start_time = time.time()

    for idx, date_str in enumerate(dates):
        url = f"https://www.officialcharts.com/charts/singles-chart/{date_str}/7501/"
        retry = 0
        success = False
        
        while retry < 3 and not success:
            try:
                res = scraper.get(url, timeout=12)
                if res.status_code != 200:
                    retry += 1
                    time.sleep(0.5)
                    continue

                soup = BeautifulSoup(res.text, 'html.parser')
                title_tags = soup.find_all('a', class_='chart-name')
                artist_tags = soup.find_all('a', class_='chart-artist')

                week_ids = []
                min_len = min(20, len(title_tags), len(artist_tags))

                for i in range(min_len):
                    title_spans = title_tags[i].find_all('span')
                    title_text = title_spans[-1].get_text(strip=True) if title_spans else title_tags[i].get_text(strip=True)
                    
                    artist_spans = artist_tags[i].find_all('span')
                    artist_text = artist_spans[-1].get_text(strip=True) if artist_spans else artist_tags[i].get_text(strip=True)

                    key = (title_text.upper(), artist_text.upper())
                    if key not in songs_map:
                        songs_map[key] = next_id
                        songs_list.append({"id": next_id, "t": title_text, "a": artist_text})
                        next_id += 1
                    
                    week_ids.append(songs_map[key])

                charts[date_str] = week_ids
                success = True
                
                # Single-line updating terminal progress bar
                curr_idx = idx + 1
                pct = (curr_idx / total_weeks) * 100
                bar_len = 25
                filled = int(bar_len * curr_idx // total_weeks)
                bar = '█' * filled + '░' * (bar_len - filled)
                
                elapsed = time.time() - start_time
                rate = curr_idx / elapsed if elapsed > 0 else 0
                eta_sec = (total_weeks - curr_idx) / rate if rate > 0 else 0
                eta_min = eta_sec / 60

                print(f"\r[{curr_idx:4d}/{total_weeks}] ({date_str}) [{bar}] {pct:5.1f}% | Songs: {len(songs_list):4d} | ETA: {eta_min:.1f}m", end="", flush=True)

            except Exception as e:
                retry += 1
                time.sleep(0.5)

    out_file = "charts_70s_80s_90s_00s_top20_compressed.json"
    dataset = {
        "songs": songs_list,
        "charts": charts
    }

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, separators=(',', ':'))

    file_size_kb = os.path.getsize(out_file) / 1024
    print("\n" + "=" * 65, flush=True)
    print(f"SUCCESS! Scraped {len(charts)} weeks across 4 decades.", flush=True)
    print(f"Total Unique Songs: {len(songs_list)}", flush=True)
    print(f"Saved to {out_file} ({file_size_kb:.2f} KB)", flush=True)
    print("=" * 65, flush=True)

if __name__ == "__main__":
    scrape_4_decades()