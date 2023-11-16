import asyncio
import json
import os
import re
from typing import List, Optional
from urllib.parse import urljoin, quote_plus

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from app.schema import UserInput, RelatedSource


def get_start_url(payload: str):
    text = f'related:{payload}'
    text = quote_plus(text)
    base_url = "https://yandex.ru"
    start_query = f"search/?text={text}"  # стартовый запрос, должен вводиться пользователем
    start_url = urljoin(base_url, start_query)
    return start_url


async def search_links(source_request: UserInput):
    found_target_links = set()  # ссылки на целевой ресурс (**.**)

    async with async_playwright() as p:

        browser_type = p.firefox
        browser = await browser_type.launch()

        link_to_find = source_request.url
        if source_request.text is not None:
            link_to_find += source_request.text
        start_url = get_start_url(link_to_find)
        page = await browser.new_page()
        search_link_to_crawl = start_url
        await page.goto(search_link_to_crawl)

        print(f'payload: {source_request}; requested page: {search_link_to_crawl} current page: {page.url}')

        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')

        target_links = soup.find_all(name='a',
                                     attrs={'class': 'Link Link_theme_normal OrganicTitle-Link organic__url link'})
        found_target_links.update([target_link['href'] for target_link in target_links])
        print(f"found target links: {len(target_links)}")
        # set(found_target_links)
        await page.close()
        #category['channels'] = get_previews_links(category['channels'])
        answer_data = RelatedSource(url=source_request.url,
                                    list_url=set(found_target_links))

        await browser.close()
    return answer_data


async def test():
    data = await search_links(source_request=UserInput(url='http://gymn11.ru/index.php'))
    print(data)


if __name__ == "__main__":
    asyncio.run(test())
