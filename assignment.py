import requests
from bs4 import BeautifulSoup
import csv

def extract_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a', href=True)]
    return links

def extract_articles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    for article in soup.find_all('article'):
        title = article.find('h2')
        description = article.find('p')
        if title and description:
            articles.append({
                'title': title.text.strip(),
                'description': description.text.strip()
            })
    return articles

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'Description'])
        for article in data:
            writer.writerow([article['title'], article['description']])

# URLs for both BBC and Dawn
bbc_url = 'https://www.bbc.com/'
dawn_url = 'https://www.dawn.com/'

# Extract links from both BBC and Dawn
bbc_links = extract_links(bbc_url)
dawn_links = extract_links(dawn_url)

# Count total links
total_links = len(bbc_links) + len(dawn_links)
print("Total links:", total_links)

# Initialize a list to store articles data
articles_data = []

# Extract articles data from BBC
print("Extracting articles from BBC...")
for index, link in enumerate(bbc_links, start=1):
    if link.startswith('https://www.bbc.com'):
        articles_data.extend(extract_articles(link))
        print(f"{index}/{total_links} links done from BBC.")

# Extract articles data from Dawn
print("Extracting articles from Dawn...")
for index, link in enumerate(dawn_links, start=index):
    if link.startswith('https://www.dawn.com'):
        articles_data.extend(extract_articles(link))
        print(f"{index}/{total_links} links done from Dawn.")

# Save the extracted data to a CSV file
save_to_csv(articles_data, 'data.csv')

print("Data saved to data.csv")
