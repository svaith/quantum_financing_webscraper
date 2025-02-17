import requests
from bs4 import BeautifulSoup
import time
import csv

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
    search_results = set()

    for link in soup.find_all('a', href=True):
        url = link['href']
        if "http" in url and "bing.com" not in url:
            search_results.add(url) 
        if len(search_results) >= num_results:
            break

    return list(search_results)

def scrape_funding_page(url):
    """Scrapes a page to check if it contains quantum research grants"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return None

        text = response.text.lower()
        if any(keyword in text for keyword in QUANTUM_KEYWORDS):
            return {"url": url}
    
    except requests.exceptions.RequestException:
        return None

def find_quantum_grants():
    """Finds quantum research grants using Bing search"""
    search_queries = [
        "quantum computing grants 2025",
        "quantum research funding opportunities",
        "apply for quantum technology grants",
        "government grants for quantum research",
        "NSF quantum computing grants",
        "DOE quantum research funding",
        "DARPA quantum computing funding opportunities",
        "NIH funding for quantum technology",
        "NASA quantum computing research grants",
        "US quantum technology funding",
        "Google quantum computing research funding",
        "IBM quantum grants and fellowships",
        "Microsoft Azure Quantum research funding",
        "Amazon AWS quantum research grants",
        "Quantum funding"
    ]

    all_grants = []

    for query in search_queries:
        print(f"Searching Bing for: {query}")
        results = bing_search(query)

        for url in results:
            grant_info = scrape_funding_page(url)
            if grant_info and grant_info not in all_grants:
                all_grants.append(grant_info)

        time.sleep(2)

    return all_grants

def write_grants_to_csv(grants, filename="quantum_grants.csv"):
    """Write the grants data to a CSV file"""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["URL"]) 
        for idx, grant in enumerate(grants, start=1):
            writer.writerow([grant['url']])

def write_grants_to_text(grants, filename="quantum_grants.txt"):
    """Write the grants data to a text file"""
    with open(filename, mode='w', encoding='utf-8') as file:
        for idx, grant in enumerate(grants, start=1):
            file.write(f"URL: {grant['url']}\n\n")

def print_grants(grants, save_to_file=True, file_format="csv"):
    """Print the structured grant results"""
    if grants:
        print("\nQuantum Grants Found:")
        for idx, grant in enumerate(grants, start=1):
            print(f"URL: {grant['url']}")
        
       
        if save_to_file:
            if file_format == "csv":
                write_grants_to_csv(grants)
                print(f"\nResults written to 'quantum_grants.csv'.")
            elif file_format == "txt":
                write_grants_to_text(grants)
                print(f"\nResults written to 'quantum_grants.txt'.")
    else:
        print("No quantum-related grants found.")

if __name__ == "__main__":
    grants = find_quantum_grants()
    print_grants(grants, save_to_file=True, file_format="csv") 
