import json

import requests
from bs4 import BeautifulSoup
import aiohttp
from writing_to_xml.writing_xml import writing

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}

# БЕРЁМ ВСЕ ССЫЛКИ ИЗ SITEMAPS
async def parser_xml(url):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await response.text(), features="lxml")

        job_url_list = [elem.text.strip() for elem in soup.find_all('loc')[:]]

    for job_url in job_url_list:
        parser_url(job_url)




def parser_url(url):
    with open("notgood.txt", encoding="utf-8") as f:
        urls_sitemaps = f.read()

    try:
        if str(url) in urls_sitemaps:
            print("УЖЕ ЕСТЬ")

        else:
            response = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(response.text, features="html.parser")

            # ЕСЛИ SITEMAP ВЕДЁТ НА ДРУГОЙ SITEMAP
            if "sitemap" in url:
                job_url_list = [elem.text.strip() for elem in soup.find_all('loc')[:]]

                for job_url in job_url_list:
                    parser_url(job_url)


            else:
                # ЕСЛИ ИМЕЕТ НУЖНУЮ РАЗМЕТКУ ПАРСИМ ЕЁ
                if '<script type="application/ld+json">' in str(soup):
                    all_info = "".join(soup.find("script", {"type": "application/ld+json"}).contents)
                    all_info = all_info.replace('	', ' ')
                    all_info = all_info.replace('\n', '')
                    all_info = all_info.replace(b'\xef\xbf\xbf'.decode('utf-8'), '')
                    all_info = all_info.replace(b'\xc2\xa0'.decode('utf-8'), '')
                    all_info = all_info.replace(b'\xe2\x80\x99'.decode('utf-8'), '')
                    all_info = all_info.replace(b'\xc3\xa2\xc2\x80\xc2\x99s'.decode('utf-8'), '')
                    all_info = json.loads(all_info)

                    writing(all_info, url)

                # ЕСЛИ НЕ ИМЕЕТ НУЖНОЙ РАЗМЕТКИ ЗАПИСЫВАЕМ САЙТ В ФАЙЛ
                else:
                    print(url, "НА САЙТЕ НЕТ ТАКОЙ РАЗМЕЕТКИ")

        with open("notgood.txt", "a", encoding="utf-8") as f:
            f.write(f"{url}\n")


    except Exception:
        with open("notgood.txt", "a", encoding="utf-8") as f:
            f.write(f"{url}\n")
        print("ТУУТ", url)