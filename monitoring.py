import os
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Установка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Укажите путь к папке, где будут сохраняться скриншоты
screenshots_folder = 'Screenshots'

# Укажите ссылки, по которым нужно перейти
links = [
    'https://eda.yandex.ru/r/rumyancev?placeSlug=rumyancev_zlaum',
    'https://eda.yandex.ru/r/vasabi?placeSlug=vasabi_3jtpk'
]

# Укажите адрес
address = '16 Линия Васильевского Острова'
latitude = 59.9363  # широта
longitude = 30.2706  # долгота

# Проверьте, существует ли файл monitor.txt
if os.path.exists('monitor.txt'):
    logging.info("Файл monitor.txt найден. Чтение ссылок из файла...")
    with open('monitor.txt', 'r') as file:
        links_from_file = file.readlines()
    links = [link.strip() for link in links_from_file]
    logging.info(f"Ссылки из файла: {links}")
else:
    logging.info("Файл monitor.txt не найден. Будут использованы ссылки из кода.")

# Создайте папку для скриншотов, если она не существует
if not os.path.exists(screenshots_folder):
    logging.info(f"Создание папки {screenshots_folder}")
    os.makedirs(screenshots_folder)
else:
    logging.info(f"Папка {screenshots_folder} уже существует. Очистка папки...")
    for file in os.listdir(screenshots_folder):
        os.remove(os.path.join(screenshots_folder, file))
    logging.info(f"Папка {screenshots_folder} очищена.")

# Создайте экземпляр браузера
try:
    logging.info("Запуск браузера")
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    logging.info("Браузер запущен")
except Exception as e:
    logging.error(f"Ошибка при запуске браузера: {e}")
    exit(1)

# Установите геолокацию
try:
    logging.info("Установка геолокации")
    driver.execute_cdp_cmd(
        "Emulation.setGeolocationOverride",
        {
            "latitude": latitude,
            "longitude": longitude,
            "accuracy": 100
        },
    )
    logging.info("Геолокация установлена")
except Exception as e:
    logging.error(f"Ошибка при установке геолокации: {e}")

# Перейдите по каждой ссылке и сделайте скриншот
screenshot_number = 1
for link in links:
    logging.info(f"Переход по ссылке {link}")
    try:
        driver.get(link)
        # Ждем 5 секунд
        time.sleep(5)
        screenshot_name = f'{screenshot_number}.png'
        logging.info(f"Сохранение скриншота {screenshot_name}")
        driver.save_screenshot(os.path.join(screenshots_folder, screenshot_name))
        # Ждем 2 секунды перед открытием следующей страницы
        time.sleep(2)
        screenshot_number += 1
    except Exception as e:
        logging.error(f"Ошибка при переходе по ссылке {link}: {e}")

# Закройте браузер
logging.info("Закрытие браузера")
driver.quit()