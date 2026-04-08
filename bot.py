from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import requests
import sys

# 🔑 ВСТАВЬ СВОЙ ТОКЕН
TELEGRAM_TOKEN = "8619557470:AAG8jcWkvTB-mfEa8XEnpO9UpEG5h-n3-ew"
CHAT_ID = "148234032"

URL = "https://b353848.alteg.io/company/337850/personal/select-time?o=m991638"

# 📅 нужные даты (дни месяца)
TARGET_DATES = ["15", "16", "17", "18", "19", "20"]

# ⏱ интервал проверки (сек)
CHECK_INTERVAL = 300  # 5 минут


# ---------- УТИЛИТЫ ----------

def log(text):
    print(text)
    sys.stdout.flush()


def send_telegram(text):
    try:
        requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": text},
            timeout=10
        )
    except Exception as e:
        log(f"Ошибка Telegram: {e}")


# ---------- SELENIUM ----------

def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"

    service = Service("/usr/bin/chromedriver")

    return webdriver.Chrome(service=service, options=options)


def open_page(driver):
    driver.get(URL)
    time.sleep(8)


# ---------- ЛОГИКА ----------

def check_slots(driver):
    try:
        buttons = driver.find_elements(By.TAG_NAME, "button")

        for btn in buttons:
            text = btn.text.strip()

            # ищем нужные даты
            if text in TARGET_DATES:
                try:
                    btn.click()
                    time.sleep(2)

                    times = driver.find_elements(By.TAG_NAME, "button")

                    for t in times:
                        if ":" in t.text:
                            return f"{text} апреля: {t.text}"

                except Exception as e:
                    log(f"Ошибка клика: {e}")

    except Exception as e:
        log(f"Ошибка поиска: {e}")

    return None


# ---------- ЗАПУСК ----------

driver = create_driver()
open_page(driver)

log("Бот запущен ✅")
send_telegram("🤖 Бот запущен и работает")

last_found = None  # чтобы не спамить


# ---------- ОСНОВНОЙ ЦИКЛ ----------

while True:
    log(f"ЖИВ: {time.strftime('%H:%M:%S')}")
    log("Проверяю...")

    try:
        result = check_slots(driver)

        if result:
            if result != last_found:
                last_found = result
                log(f"🔥 НАЙДЕНО: {result}")
                send_telegram(f"🔥 Есть слот: {result}")
            else:
                log("Слот уже отправляли")

        else:
            log("Пока нет...")

    except Exception as e:
        log(f"Ошибка цикла: {e}")

        try:
            driver.quit()
        except:
            pass

        log("Перезапускаю браузер...")
        driver = create_driver()
        open_page(driver)

    # обновляем страницу
    try:
        driver.refresh()
    except:
        pass

    log("Обновил страницу\n")

    time.sleep(CHECK_INTERVAL)
