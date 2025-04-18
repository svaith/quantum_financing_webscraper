import time
import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

QUANTUM_KEYWORDS = [
    "quantum", "qubit", "entanglement", "superposition",
    "quantum computing", "quantum technology", "quantum research",
    "quantum funding", "quantum grant", "quantum fellowship"
]

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    return driver

def bing_search_selenium(query, num_results=10):
    driver = setup_driver()
    search_url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
    driver.get(search_url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    urls = set()

    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith("http") and "bing.com" not in href and "microsoft.com" not in href:
            urls.add(href)
        if len(urls) >= num_results:
            break

    driver.quit()
    return list(urls)

def scrape_funding_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return None
        content = response.text.lower()
        if any(keyword in content for keyword in QUANTUM_KEYWORDS):
            return {"url": url}
    except requests.exceptions.RequestException:
        return None
    return None

def find_quantum_grants():
    search_queries = [
        "quantum computing grants 2025",
        "quantum technology funding opportunities",
        "apply for quantum research grants",
        "government quantum research grants",
        "NSF quantum computing funding",
        "DOE quantum funding",
        "DARPA quantum computing programs",
        "NIH quantum technology funding",
        "NASA quantum research programs",
        "Google quantum fellowship",
        "IBM quantum research grants",
        "Microsoft Azure Quantum grants",
        "Amazon Braket quantum funding"
    ]

    all_grants = []

    for query in search_queries:
        print(f"Searching Bing for: {query}")
        urls = bing_search_selenium(query)
        print(f"Found {len(urls)} URLs")
        for url in urls:
            print(f"Checking: {url}")
            result = scrape_funding_page(url)
            if result and result not in all_grants:
                all_grants.append(result)
        time.sleep(1)

    return all_grants

def write_to_csv(grants, filename="quantum_grants.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["URL"])
        for grant in grants:
            writer.writerow([grant['url']])
    print(f"Results saved to {filename}")

def print_grants(grants):
    if not grants:
        print("No quantum-related grants found.")
        return

    print("Quantum Grants Found:")
    for idx, grant in enumerate(grants, start=1):
        print(f"{idx}. {grant['url']}")

if __name__ == "__main__":
    grants = find_quantum_grants()
    print_grants(grants)
    write_to_csv(grants)
