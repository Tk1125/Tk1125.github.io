from bs4 import BeautifulSoup
import requests
from datetime import datetime

response = requests.get("https://www.wired.com/")
soup = BeautifulSoup(response.text, 'html.parser')

newsLinks = soup.find_all('a', href=True)

news = []

for linkTag in newsLinks:
    h2Tag = linkTag.find('h2')
    if not h2Tag:
        continue

    title = h2Tag.get_text(strip=True)
    link = linkTag.get('href')

    if not link:
        continue

    fullLink = "https://www.wired.com/" + link
    
    newsResponse = requests.get(fullLink)
    newsSoup = BeautifulSoup(newsResponse.text, 'html.parser')

    dateTag = newsSoup.find('time')
    if dateTag and 'datetime' in dateTag.attrs:
        pubDate_str = dateTag['datetime']
        pubDate = datetime.fromisoformat(pubDate_str.replace('Z', '+00:00')).date()
        if pubDate >= datetime(2022, 1, 1).date():
            pubDate = pubDate.strftime("%Y-%m-%d")
            news.append((title, fullLink, pubDate))

    else:
        pubDate = 'Not available'

news.sort(key=lambda x: datetime.strptime(x[2], "%Y-%m-%d"), reverse=True)

htmlContent = "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>Article Aggregator</title>\n</head>\n<body>\n <ul>\n"

for title, link, pub_date in news:
    htmlContent += f'        <p><a href="{link}" target="_blank">{title}</a> - Published on: {pub_date}</p>\n'

htmlContent += "    </ul>\n</body>\n</html>"

with open('articles.html', 'w') as file:
    file.write(htmlContent)