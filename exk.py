from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

import datetime
import settings
import time


def up_all(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # безоконный режим
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(
        executable_path=settings.CHROME_DRIVER_URL,
        options=chrome_options
        )
    driver.get(url)

    username = driver.find_element_by_name("username")
    password = driver.find_element_by_name("password")
    username.send_keys(settings.USERNAME)  # ввод логина и пароля
    password.send_keys(settings.PASSWORD)
    button = driver.find_element_by_class_name("butt-enter")
    button.click()  # нажимаем Войти
    time.sleep(5)  # ждем прогрузки
    try:  # на случай появления баннера
        target = driver.find_element_by_class_name("brand-div")
        target.click()  # закрываем баннер
        time.sleep(1)
    except NoSuchElementException:
        pass
    button = driver.find_element_by_xpath(
        "//a[@href='https://exkavator.ru/trade/companymanager/show_lots/rent.html']")
    button.click()  # открываем вкладку Аренда
    time.sleep(3)  # ждем прогрузки
    up_all_butt = driver.find_element_by_class_name("myob_upall_butt")
    up_all_butt.click()  # поднимаем объявления
    time.sleep(5)  # на всякий случай ждем
    driver.quit()  # закрываем браузер


if __name__ == "__main__":
    while True:
        now = datetime.datetime.now()  # на сервере должен стоять часовой пояс МСК
        if now.minute == 0:
            if now.hour == 9 or now.hour == 11 or now.hour == 13 or now.hour == 15:
                print("Пора поднимать объявления")
                url = "https://exkavator.ru/auth/"
                up_all(url)
                time.sleep(7000)  # спим почти 2 часа
            elif now.hour == 17:
                print("Пора поднимать объявления")
                url = "https://exkavator.ru/auth/"
                up_all(url)
                time.sleep(57000)  # спим до утра
        else:
            print("Сплю, но скоро проснусь")
            time.sleep(5)  # для отслеживания лога