from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import requests

# 🔑 ВСТАВЬ СВОЙ ТОКЕН
TELEGRAM_TOKEN = "8619557470:AAG8jcWkvTB-mfEa8XEnpO9UpEG5h-n3-ew"
CHAT_ID = "148234032"

URL = "https://b353848.alteg.io/company/337850/personal/select-time?o=m991638"

TARGET_DATES = ["15", "16", "17", "18", "19", "20"]


def send_telegram(text):
    try:
        requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": text},
            timeout=10
        )
    except Exception as e:
        print("Ошибка Telegram:", e)


def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"

    service = Service("/usr/bin/chromedriver")

    return webdriver.Chrome(service=service, options=options)


driver = create_driver()
driver.get(URL)
time.sleep(10)


def check():
    try:
        buttons = driver.find_elements(By.TAG_NAME, "button")

        for btn in buttons:
            text = btn.text.strip()

            if text in TARGET_DATES:
                try:
                    btn.click()
                    time.sleep(2)

                    times = driver.find_elements(By.TAG_NAME, "button")

                    for t in times:
                        if ":" in t.text:
                            return f"{text} апреля: {t.text}"

                except Exception as e:
                    print("Ошибка клика:", e)

    except Exception as e:
        print("Ошибка поиска:", e)

    return None


while True:
    print("Проверяю...")

    try:
        result = check()

        if result:
            print("НАЙДЕНО:", result)
            send_telegram(f"🔥 Есть слот: {result}")
            break

        print("Пока нет...")

    except Exception as e:
        print("Ошибка цикла:", e)

        # перезапуск браузера если упал
        try:
            driver.quit()
        except:
            pass

        driver = create_driver()
        driver.get(URL)
        time.sleep(10)

    time.sleep(300)
    driver.refresh()
