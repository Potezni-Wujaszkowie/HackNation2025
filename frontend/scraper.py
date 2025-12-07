import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import os

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
OUTPUT_DIR = "uploads_text"
CRAWL_DELAY = 0

visited_urls = set()

def is_valid(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def save_content(url, content):
    parsed_url = urlparse(url)
    filename_part = parsed_url.netloc + parsed_url.path.replace('/', '_')
    if not filename_part or filename_part.endswith('_'):
        filename_part += "index"

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    filename = os.path.join(OUTPUT_DIR, f"{filename_part}.txt")

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"--- URL: {url} ---\n\n")
            f.write(content)
        print(f"Saved content for: {url}")
    except Exception as e:
        print(f"Error saving content for {url}: {e}")

def crawl_website(url, max_depth, current_depth=0):
    if current_depth > max_depth:
        print(f"Max depth reached for: {url}")
        return

    if url in visited_urls:
        print(f"Already visited: {url}")
        return

    if not is_valid(url):
        print(f"Invalid URL skipped: {url}")
        return

    visited_urls.add(url)
    print(f"\n--- Crawling Depth {current_depth}: {url} ---")

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()

    content = soup.get_text(separator=' ', strip=True)

    save_content(url, content)

    if current_depth < max_depth:
        base_url_netloc = urlparse(url).netloc

        for link in soup.find_all('a', href=True):
            href = link.get('href')

            absolute_url = urljoin(url, href)
            parsed_absolute = urlparse(absolute_url)

            if is_valid(absolute_url) and \
               parsed_absolute.netloc == base_url_netloc and \
               not parsed_absolute.fragment:

                time.sleep(CRAWL_DELAY)
                crawl_website(absolute_url, max_depth, current_depth + 1)


if __name__ == "__main__":
    START_URL = "https://www.nato.int/en/news-and-events/articles"

    src_gov = [
        # POLSKA - oficjalne źródła rządowe
        "https://www.gov.pl/web/diplomacy/news",
        "https://www.gov.pl/web/mswia-en/news",
        "https://www.pap.pl/en",
        "https://www.gov.pl/web/aktualnosci"
        # NIEMCY - oficjalne źródła rządowe'
        ,
        "https://www.bundesregierung.de/breg-en/news",
        "https://www.bundeskanzler.de/bk-en/news",
        "https://www.auswaertiges-amt.de/en/news"
        # WIELKA BRYTANIA - oficjalne źródła rządowe'
        ,
        "https://www.gov.uk/search/news-and-communications",
        "https://www.gov.uk/government/news",
        "https://www.parliament.uk/business/news/"
        # USA - oficjalne źródła rządowe
        ,
        "https://www.whitehouse.gov/news/",
        "https://www.whitehouse.gov/briefing-room/",
        "https://www.state.gov/press-releases/",
        "https://www.usa.gov/news"
        # Dodatkowe RSS-y (jeśli chcesz scrapować automatycznie)
        ,
        "https://www.gov.pl/web/diplomacy/news.rss",
        "https://www.bundesregierung.de/breg-en/news.rss",
        "https://www.gov.uk/government/announcements.atom",
        "https://www.whitehouse.gov/news/feed/",
        "https://www.state.gov/rss-feed/press-releases/feed/",
    ]

    MAX_CRAWL_DEPTH = 0

    legit_urls = [
        "https://www.nato.int/en/news-and-events/articles/news/2025/12/04/the-director-general-of-the-international-military-staff-discusses-nato-ukraine-cooperation-with-visiting-ukraine-military-personnel?selectedLocale="
        , "https://www.nato.int/en/news-and-events/articles/news/2025/11/26/nato-and-ukraine-announce-new-joint-initiative-to-accelerate-defence-innovation-unite-brave-nato?selectedLocale="
        , "https://www.nato.int/en/news-and-events/articles/news/2025/11/23/nato-deputy-secretary-general-visits-logistical-hub-in-poland-of-the-nato-security-assistance-and-training-for-ukraine?selectedLocale="
        , "https://www.nato.int/en/news-and-events/articles/news/2025/11/17/nato-allies-wrap-up-major-air-exercise-falcon-strike-2025-in-italy?selectedLocale="
        , "https://www.gov.pl/web/obrona-narodowa/bojowe-wozy-piechoty-borsuk-wchodza-na-wyposazenie-wojska-polskiego"
        , "https://www.gov.pl/web/obrona-narodowa/wspolpraca-na-rzecz-bezpieczenstwa-infrastruktury-krytycznej"
        , "https://www.gov.pl/web/premier/wspolna-deklaracja-podsumowujaca-polsko---niemieckie-konsultacje-miedzyrzadowe"
    ]

    visited_urls = set()

    for url in legit_urls:
        print(f"Starting crawl for: {url} with Max Depth: {MAX_CRAWL_DEPTH}")
        print("-" * 50)

        crawl_website(url, MAX_CRAWL_DEPTH)

        print("-" * 50)
        print(f"Crawl finished. Total pages visited: {len(visited_urls)}")
        print(f"Content saved to the '{OUTPUT_DIR}' directory.")
    