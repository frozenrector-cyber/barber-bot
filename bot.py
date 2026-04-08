from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests

TELEGRAM_TOKEN = "8619557470:AAG8jcWkvTB-mfEa8XEnpO9UpEG5h-n3-ew"
CHAT_ID = "148234032"

URL = "https://b353848.alteg.io/company/337850/personal/select-time?o=m991638"

TARGET_DATES = ["15", "16", "17", "18", "19", "20"]


def send_telegram(text):
    requests.get(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": text}
    )


options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

driver.get(URL)
time.sleep(10)


def check():
    buttons = driver.find_elements(By.TAG_NAME, "button")

    for btn in buttons:
        text = btn.text.strip()

        # ищем даты
        if text in TARGET_DATES:
            try:
                btn.click()
                time.sleep(2)

                times = driver.find_elements(By.TAG_NAME, "button")

                for t in times:
                    if ":" in t.text:
                        return f"{text} апреля: {t.text}"

            except:
                pass

    return None


while True:
    print("Проверяю...")

    result = check()

    if result:
        send_telegram(f"🔥 Есть слот: {result}")
        break

    time.sleep(300)
    driver.refresh()
