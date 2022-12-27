from parser_xml.parser import parser_xml
import asyncio


def read_sitemaps():
    # ЧИТАЕМ ВЕСЬ ФАЙЛ С SITEMAPами
    with open("sitemaps.txt", encoding="utf-8") as f:
        urls_sitemaps = f.readlines()

    # ПРОХОДИМСЯ ПО ВСЕМ SITEMAPам
    for url_sitemap in urls_sitemaps:
        try:
            asyncio.run(parser_xml(url_sitemap.rstrip()))

        except Exception as ex:
            print(f"ERROR: {url_sitemap} == {ex}")


def main():
    read_sitemaps()


if __name__ == '__main__':
    main()
