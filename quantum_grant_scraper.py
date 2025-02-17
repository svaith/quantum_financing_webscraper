import requests
from bs4 import BeautifulSoup
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

QUANTUM_KEYWORDS = ["quantum", "qubit", "quantum computing", "quantum information", "entanglement", "superposition"]

def bing_search(query, num_results=5):
    """Fetch search results from Bing"""
    search_url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
    response = requests.get(search_url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Failed to retrieve Bing search results. Status Code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = []

    for link in soup.find_all('a', href=True):
        url = link['href']
        if "http" in url and "bing.com" not in url:
            search_results.append(url)
        if len(search_results) >= num_results:
            break

    return search_results

def scrape_funding_page(url):
    """Scrapes a page to check if it contains quantum research grants"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return None

        text = response.text.lower()
        if any(keyword in text for keyword in QUANTUM_KEYWORDS):
            return {"title": url, "url": url}
    
    except requests.exceptions.RequestException:
        return None

def find_quantum_grants():
    """Finds quantum research grants using Bing search"""
    search_queries = [
        "quantum computing research grants 2025",
        "quantum technology funding opportunities",
        "apply for quantum research grants",
        "government grants for quantum computing"
    ]

    all_grants = []

    for query in search_queries:
        print(f"Searching Bing for: {query}")
        results = bing_search(query)

        for url in results:
            grant_info = scrape_funding_page(url)
            if grant_info:
                all_grants.append(grant_info)

        time.sleep(2)

    return all_grants

if __name__ == "__main__":
    grants = find_quantum_grants()

    if grants:
        print("\nQuantum Grants Found:")
        for grant in grants:
            print(f"Title: {grant['title']}, URL: {grant['url']}")
    else:
        print("No quantum-related grants found.")
