import time
import asyncio
import aiohttp
from dal import commit
from typing import Dict, List
from api import API_URL, cookies, header, data


async def send_request(session: aiohttp.ClientSession, url: str, page: int) -> List[Dict]:
    """
    Send a POST request to specified URL
    and return List of proxy dictionaries.

    Args:
        session: aiohttp.ClientSession
        url: str
        page: int

    Returns:
        List[Dict]
    """
    data['page'] = str(page)
    async with session.post(url, headers=header, data=data, cookies=cookies) as response:
        proxy_info = await response.json()
        return proxy_info['proxies']


async def get_proxy_info(url: str, pages: int) -> List[Dict]:
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, url, page) for page in range(1, pages + 1)]
        return await asyncio.gather(*tasks)


def proxy_normalizer(proxy_info: List[Dict]) -> List[Dict]:
    """
    Normalize proxy information.

    Args:
        proxy_info: List[Dict]

    Returns:
        List[Dict]
    """
    normalized_data = []
    for _ in proxy_info:
        for proxy in _:
            proxy_data = {
                'country': proxy.get('country'),
                'ip': proxy.get('ip'),
                'port': proxy.get('port'),
                'timeout': proxy.get('timeout'),
                'code': proxy.get('code'),
                'city': proxy.get('city'),
                'lastcheck': proxy.get('lastcheck')
            }
            normalized_data.append(proxy_data)
    return normalized_data


async def main():
    pages = int(input('How many pages you wanna crawl? Each page contains 20 proxies: '))
    start = time.time()
    proxy_info = await get_proxy_info(API_URL, pages)
    normalized_info = proxy_normalizer(proxy_info)
    commit(normalized_info)
    end = time.time()
    consumed_time = end - start
    print(f'Consumed time for {pages} pages: {consumed_time} seconds\n{pages * 20} proxies crawled successfully.')


if __name__ == "__main__":
    asyncio.run(main())