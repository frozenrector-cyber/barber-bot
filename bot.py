import requests
import time

# 🔑 ВСТАВЬ СВОЙ ТОКЕН
TELEGRAM_TOKEN = "8619557470:AAG8jcWkvTB-mfEa8XEnpO9UpEG5h-n3-ew"

# 👇 твой chat_id (мы уже нашли)
CHAT_ID = "148234032"

# 📅 нужные даты
DATES = [
    "2026-04-15",
    "2026-04-16",
    "2026-04-17",
    "2026-04-18",
    "2026-04-19",
    "2026-04-20",
]

# 🔗 API Altegio
URL = "https://b353848.alteg.io/timeslots"


def send_telegram(text):
    requests.get(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": text
        }
    )


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
                "staff_id": 991638  # 👈 ЭТО ТВОЙ БАРБЕР
            }
        ]
    }

    response = requests.post(URL, json=payload)
    data = response.json()

    print(f"Ответ для {date}:", data)  # 👈 чтобы видеть что происходит

    found = []

    for slot in data.get("data", []):
        attrs = slot["attributes"]

        if attrs["is_bookable"]:
            found.append(attrs["time"])

    return found


# 🔁 основной цикл
while True:
    print("Проверяю даты...")

    for date in DATES:
        slots = check_date(date)

        if slots:
            message = f"🔥 Есть слоты на {date}:\n" + "\n".join(slots)
            print(message)
            send_telegram(message)
            exit()

    print("Пока нет нужных дат...\n")
    time.sleep(30)