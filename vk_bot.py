from bs4 import BeautifulSoup as bs
import requests


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 YaBrowser/20.12.3.140 Yowser/2.5 Safari/537.36'
}


class VkBot:
    def __init__(self, user_id):
        print("Создан объект бота!")
        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(self._USER_ID)
        self._SURNAME = self._get_user_surname_from_vk_id(self._USER_ID)

    def _get_user_name_from_vk_id(self, user_id):
        try:
            respond = requests.get("https://vk.com/id" + str(user_id), headers=headers)
            soup = bs(respond.text, "lxml")
            user_name = soup.find('h1', class_='page_name').text
            return user_name.split()[0]
        except:
            respond = requests.get("https://vk.com/club" + str(abs(user_id)), headers=headers)
            soup = bs(respond.text, "lxml")
            publick_name = soup.find('h1', class_='page_name').text
            return publick_name

    def _get_user_surname_from_vk_id(self, user_id):
        try:
            respond = requests.get("https://vk.com/id" + str(user_id), headers=headers)
            soup = bs(respond.text, "lxml")
            user_name = soup.find('h1', class_='page_name').text
            return user_name.split()[1]
        except:
            respond = requests.get("https://vk.com/club" + str(abs(user_id)), headers=headers)
            soup = bs(respond.text, "lxml")
            publick_name = soup.find('h1', class_='page_name').text
            return publick_name
