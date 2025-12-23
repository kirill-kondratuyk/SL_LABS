import shelve
import os

phones = {
    "iPhone 14": {
        "США": 999,
        "Великобритания": 949,
        "Германия": 1099,
        "Франция": 1049,
        "Китай": 8999,
        "Япония": 129800,
        "Индия": 89900,
        "Россия": 89990
    },
    "Samsung S23": {
        "США": 799,
        "Великобритания": 769,
        "Германия": 849,
        "Франция": 819,
        "Китай": 5999,
        "Япония": 99800,
        "Индия": 69900,
        "Россия": 74990
    },
    "Google Pixel 7": {
        "США": 599,
        "Великобритания": 599,
        "Германия": 649,
        "Франция": 629,
        "Китай": 4999,
        "Япония": 79800,
        "Индия": 54900,
        "Россия": 59990
    },
    "Xiaomi 13": {
        "США": 699,
        "Великобритания": 669,
        "Германия": 749,
        "Франция": 719,
        "Китай": 3999,
        "Япония": 89800,
        "Индия": 44900,
        "Россия": 49990
    },
    "OnePlus 11": {
        "США": 729,
        "Великобритания": 699,
        "Германия": 799,
        "Франция": 769,
        "Китай": 4499,
        "Япония": 94800,
        "Индия": 49900,
        "Россия": 54990
    },
    "Huawei P50": {
        "США": 899,
        "Великобритания": 849,
        "Германия": 949,
        "Франция": 899,
        "Китай": 5999,
        "Япония": 109800,
        "Индия": 79900,
        "Россия": 84990
    },
    "Motorola Edge 40": {
        "США": 549,
        "Великобритания": 529,
        "Германия": 599,
        "Франция": 579,
        "Китай": 2999,
        "Япония": 69800,
        "Индия": 34900,
        "Россия": 39990
    }
}

print("Список телефонов и их средние стоимости:")
for phone, prices in phones.items():
    avg_price = sum(prices.values()) / len(prices)
    print(f"{phone}: {avg_price:.2f}")

avg_prices = {}
for phone, prices in phones.items():
    avg_prices[phone] = sum(prices.values()) / len(prices)

min_phone = min(avg_prices, key=avg_prices.get)
del phones[min_phone]
print(f"\nУдален телефон с минимальной средней стоимостью: {min_phone}")

max_avg_price = max(avg_prices.values())
threshold = 0.3 * max_avg_price

print("\nТелефоны, отличающиеся по стоимости менее чем на 30% от максимальной:")
for phone, avg in avg_prices.items():
    if phone in phones and (max_avg_price - avg) / max_avg_price <= 0.3:
        print(f"{phone}: {avg:.2f}")

print("\nТелефоны, стоимость в США > стоимости в Великобритании:")
for phone, prices in phones.items():
    if prices["США"] > prices["Великобритания"]:
        print(f"{phone}: США={prices['США']}, Великобритания={prices['Великобритания']}")

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "phones_db")

with shelve.open(db_path) as db:
    db["phones"] = phones

print(f"\nСловарь сохранен в файлы:")
for file in os.listdir(current_dir):
    if file.startswith("phones_db."):
        print(f"  - {file}")