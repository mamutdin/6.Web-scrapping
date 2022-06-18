import requests
import bs4
import re

KEYWORDS = ['дизайн', 'фото', 'web', 'Python']


base_url = "https://habr.com"


def full_article(url, headers):
    res = requests.get(url, headers=headers)
    text2 = res.text
    soup2 = bs4.BeautifulSoup(text2, features="html.parser")
    body = soup2.find(id="post-content-body")
    body = body.find_all('p')

    full_text = []

    for i in body:
        full_text.append(i.text)
    body = ' '.join(full_text)
    body = re.findall(r'\w+[\w-]*', body)
    return body

def main(base_url, keywords):
    pattern = r'[^\w\s-]'
    pattern2 = r'\w+[\w-]*'
    url = base_url + "/ru/all/"
    listing = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/75.0.3770.142 Safari/537.36'
               }
    response = requests.get(url, headers=headers)
    text = response.text
    soup = bs4.BeautifulSoup(text, features="html.parser")
    articles = soup.find_all("article")
    for article in articles:
        article_info_snippet = article.find(class_="tm-article-snippet__title-link")
        article_name = article_info_snippet.text
        new_article_name = re.findall(pattern2, article_name)

        article_body = article.find(
            class_='article-formatted-body article-formatted-body article-formatted-body_version-2')
        body = article_body.text
        new_body = re.findall(pattern2, body)

        article_hubs = article.find_all(class_="tm-article-snippet__hubs-item-link")
        hubs = [hub.text.strip() for hub in article_hubs]
        hubs = ' '.join(hubs)
        new_hubs = re.findall(pattern2, hubs)

        article_date = article.find(class_="tm-article-snippet__datetime-published")
        href = article_info_snippet.attrs["href"]
        date = article_date.find("time").attrs["title"]

        full_url = base_url + href
        body = full_article(full_url, headers)

        for word in keywords:
            if word in new_body or word in new_hubs or word in new_article_name or word in body:
                text = f"{date} - {article_name} - {full_url}"
                if text not in listing:
                    listing.append(text)
                    print(text)

main(base_url, KEYWORDS)
