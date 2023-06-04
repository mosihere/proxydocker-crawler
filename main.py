import time
import requests
import threading
from dal import DataBaseManager
from api import API_URL, cookies, header, data


class ProxyExtractor:

    def __init__(self) -> None:
        self.list_of_data = list()


    def __send_request(self, url: str) -> dict:
        """
        Send a POST request to specified URL
        and return Dictionary Object.

        Args:
            url: str
        
        Returns:
            Dictionary object contains api Response.

        ReturnType:
            Dictionary
        """

        response = requests.post(url, headers=header, data=data, cookies=cookies)
        dictionary_info = response.json()
        return dictionary_info
    
    def proxy_extractor(self, page_numbers: int) -> list:
        """
        Iterate over Pages of Website
        and Get important data and save them
        in a Dictionary Object and finally append them
        in a list.

        Args:
            page_numbers: int

        Returns:
            list_of_data

        ReturnType:
            List
        """

        proxy_info = self.__send_request(API_URL)

        for page in range(1, page_numbers + 1):
            data['page'] = str(page + 1)
            time.sleep(4)

            for proxy in proxy_info['proxies']:
                proxy_data = {
                    'country': proxy.get('country'),
                    'ip': proxy.get('ip'),
                    'port': proxy.get('port'),
                    'timeout': proxy.get('timeout'),
                    'code': proxy.get('code'),
                    'city': proxy.get('city'),
                    'lastcheck': proxy.get('lastcheck')
                }
                self.list_of_data.append(proxy_data)

        return self.list_of_data



if __name__ == "__main__":
    my_extractor = ProxyExtractor()
    db_manager = DataBaseManager()

    pages_to_crawl = int(input('++Each page contains 20 proxies++\nHow many pages you wanna crawl: '))
    
    t1 = threading.Thread(target=my_extractor.proxy_extractor, args=(pages_to_crawl, ))

    t1.start()
    t1.join()

    data = my_extractor.proxy_extractor(pages_to_crawl)

    t2 = threading.Thread(target=db_manager.commit, args=(data, ))
    t2.start()
    
    t2.join()

    print()
    print('Done')