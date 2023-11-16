import asyncio
import logging
import time
import traceback
from pprint import pprint
from typing import List
from fake_useragent import UserAgent
import aiohttp
import requests
from bs4 import BeautifulSoup
from enum import Enum

from domain.models.url import FetchStatus, AnswerDataFetched


def get_title_rage(page):  #: requests.models.Request
    soup = BeautifulSoup(page, 'html.parser')
    result = soup.find_all('title')
    if result is not None and len(result) > 0:
        return result[0].getText()
    return ''


def define_successful(title: str, code: int):
    if code != 200:
        return False
    elif title == "Bot Detection" or \
            title == "DDOS Protection" or \
            title == "CAPTCHA" or \
            title == 'Captcha' or \
            "Проверка" in title:
        return False
    return True


async def check_response(response: requests.Response, response_in_byte):
    is_json = False
    page_title = "NO_PAGE"
    if response.headers["Content-Type"] == "application/json":
        is_json = True

    if not is_json:
        page_title = get_title_rage(response_in_byte)
    is_successful = define_successful(page_title, response.status)
    if is_successful:
        logging.info(f'{response.text}')
        if is_json:
            data = await response.json()
        else:
            data = response_in_byte
        return data, page_title
    else:
        return -1, page_title


def get_cookie_from_async_response(response):
    headers = response.headers
    logging.info(f"cookie: {headers}")
    cookie_ = headers.getall('Set-Cookie')
    return cookie_


class ProxyLoader:
    def get_proxy(self):
        return {
            "https": " ",
            "http": " "
        }


def check_captcha_in_soup(soup: BeautifulSoup):
    captcha_element = soup.find(lambda tag: tag.name and 'captcha' in tag.name.lower())

    return captcha_element


async def fetch_url(proxy_manager: ProxyLoader,
                    url: str,
                    timeout: int = 5
                    ):
    """
    :param proxy_manager:
    :param url:
    :param proxies:
    :param timeout:
    :return:

    """

    custom_data = {}
    user_agent = UserAgent()
    custom_headers = {'User-Agent': user_agent.random}

    async with aiohttp.ClientSession() as session:
        try:
            timeout = aiohttp.ClientTimeout(total=timeout)
            start_time = time.monotonic()
            async with session.get(url,
                                   headers=custom_headers,
                                   data=custom_data,
                                   timeout=timeout,
                                   # proxy=proxies["https"],
                                   ssl=False
                                   ) as response:

                resp_bytes = await response.read()
                res_checking, title_checking = await check_response(response, resp_bytes.decode('utf-8', errors='replace'))
                end_time = time.monotonic()
                if res_checking == -1:
                    if response.status == 401:
                        logging.warning(
                            f"Request to {url} not succeeded in {end_time - start_time:.4f} seconds "
                            f"with status code {response.status} and title {title_checking} and "
                            f"text {await response.json()}")

                        return FetchStatus.CAPTCHA

                    elif response.status == 404:
                        logging.info(f"Request to {url} not succeeded in {end_time - start_time:.4f} "
                                     f"seconds with status code {response.status} and "
                                     f"title {title_checking} "
                                     f"and credentials: {custom_headers}")
                        return FetchStatus.NOT_FOUND
                    else:
                        logging.warning(
                            f"Request to {url} not succeeded in {end_time - start_time:.4f} seconds"
                            f" with status code {response.status} "
                            f"and title {title_checking} "
                            f"and credentials: {custom_headers.get('Cookie')}")
                        if response.status == 200:  # переписать по-нормальному потом, но по логике при 200 статусе и ответа -1 только капча может быть
                            logging.warning(
                                f"CAPTCHA! Request to {url} not succeeded in {end_time - start_time:.4f} "
                                f"seconds with status code {response.status} and "
                                f"credentials: {custom_headers.get('Cookie')}")

                            return FetchStatus.CAPTCHA

                    return
                else:
                    if check_captcha_in_soup(BeautifulSoup(res_checking, 'html.parser')):
                        logging.warning(f"CAPTCHA! Request to {url} not succeeded in {end_time - start_time:.4f} "
                                        f"seconds with status code {response.status} "
                                        f"and credentials: {custom_headers.get('Cookie')}")

                        return FetchStatus.CAPTCHA

                    else:
                        logging.info(f"Request to {url} succeeded in {end_time - start_time:.4f} seconds"
                                     f"and credentials: {custom_headers.get('Cookie')}")

                    return res_checking
        except TimeoutError as error:
            end_time = time.monotonic()
            tb = error.__traceback__
            print("TimeOut-TimeOut", error.with_traceback(tb))
            logging.error(f"Error fetching {url}: {error} during {end_time - start_time:.4f}"
                          f"and credentials: {custom_headers.get('Cookie')} because {error.with_traceback(tb)} "
                          f"or {error, error.__class__.__name__}")
            return
        except Exception as error:
            end_time = time.monotonic()
            tb = error.__traceback__
            print(error.with_traceback(tb), traceback.format_exc())
            logging.error(f"Error fetching {url}: {error} during {end_time - start_time:.4f}"
                          f"and credentials: {custom_headers.get('Cookie')} because {error.with_traceback(tb)} "
                          f"or {error, error.__class__.__name__}")
            return


async def parse_one_request(url: str,
                            proxy_manager: ProxyLoader=None,
                            timeout: int = 30,
                            ) -> AnswerDataFetched:
    retry_delay = 2
    retry_limit = 5

    for retry_count in range(retry_limit):
        result = await fetch_url(url=url,
                                 timeout=timeout,
                                 proxy_manager=proxy_manager,
                                 )
        if result == FetchStatus.CAPTCHA:
            return AnswerDataFetched(
                url=url,
                status=FetchStatus.CAPTCHA,
            )

        elif result == FetchStatus.NOT_FOUND:
            return AnswerDataFetched(
                url=url,
                status=FetchStatus.NOT_FOUND,
            )

        elif result is not None:
            return AnswerDataFetched(
                url=url,
                status=FetchStatus.SUCCESSFUL,
                content=result
            )

        await asyncio.sleep(retry_delay * retry_count)
    logging.error(f"Failed to fetch {url} after {retry_limit}")
    return AnswerDataFetched(
        url=url,
        status=FetchStatus.FAILED
    )


async def parse_all_urls(urls: List[str]) -> List[AnswerDataFetched]:
    # Ограничиваем количество одновременно выполняемых корутин
    sem = asyncio.Semaphore(10)

    async def limited_process_url(url):
        async with sem:
            return await parse_one_request(url)

    tasks = [limited_process_url(url) for url in urls]
    results: List[AnswerDataFetched] = await asyncio.gather(*tasks)
    #print(type(results))
    for result in results:
        pprint(result.status)
    return results


if __name__ == "__main__":
    list_url = [
        'https://habr.com/ru/articles/322034/',
        'https://pet-mir.ru/',
        'https://www.bgoperator.ru/',
        'https://europcar.ru/',
        'https://pozdravok.com/pozdravleniya/den-rozhdeniya/proza-2.htm',
        'https://chestvuj.ru/',
        'https://www.pozdravik.ru/',
        'https://kipmu.ru/domashnie-zhivotnye/',
        'https://foxford.ru/wiki/okruzhayuschiy-mir/domashnie-pitomcy',
        'https://adme.media/zhizn-zhivotnye/20-strannyh-malenkih-sekretov-kotorye-hranyat-nashi-pitomcy-2151865/'
    ]
    asyncio.run(parse_all_urls(urls=list_url))
