import requests
import time

TELEGRAM_TOKEN = "8619557470:AAG8jcWkvTB-mfEa8XEnpO9UpEG5h-n3-ew"
CHAT_ID = "148234032"

DATES = [
    "2026-04-15",
    "2026-04-16",
    "2026-04-17",
    "2026-04-18",
    "2026-04-19",
    "2026-04-20",
]

URL = "https://b353848.alteg.io/timeslots"


def send_telegram(text):
    try:
        requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            params={
                "chat_id": CHAT_ID,
                "text": text
            },
            timeout=10
        )
    except Exception as e:
        print("Ошибка Telegram:", e)


def check_date(date):
    payload = {
        "context": {
            "location_id": 337850
        },
        "filter": {
            "date": date
        },
        "records": [
            {
                "attendance_service_items": [
                    {
                        "id": 9494127,
                        "type": "service"
                    }
                ],
                "staff_id": 991638
            }
        ]
    }

    try:
        response = requests.post(
            URL,
            json=payload,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Origin": "https://b353848.alteg.io",
                "Referer": "https://b353848.alteg.io/",
            },
            timeout=10
        )

        if response.status_code != 200:
            print(f"{date} → ошибка ответа:", response.status_code)
            return []

        if not response.text.strip():
            print(f"{date} → пустой ответ")
            return []

        data = response.json()

    except Exception as e:
        print(f"{date} → ошибка запроса:", e)
        return []

    found = []

    for slot in data.get("data", []):
        attrs = slot["attributes"]

        if attrs.get("is_bookable"):
            found.append(attrs["time"])

    print(f"{date} → найдено:", found)

    return found


while True:
    print("Проверяю даты...\n")

    for date in DATES:
        slots = check_date(date)

        if slots:
            message = f"🔥 Есть слоты на {date}:\n" + "\n".join(slots)
            print(message)
            send_telegram(message)
            exit()

    print("Пока нет нужных дат...\n")

    time.sleep(300)
