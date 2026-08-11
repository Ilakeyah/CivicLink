import csv
import random

categories = {
    "Clothing": [
        "I have winter jackets to donate",
        "Donating clothes for poor families",
        "Providing blankets for homeless people"
    ],
    "Education": [
        "Offering free tutoring for students",
        "Donating books to schools",
        "Providing career guidance sessions"
    ],
    "Healthcare": [
        "Offering free health checkups",
        "Donating medicines to clinics",
        "Providing physiotherapy support"
    ],
    "Disaster Relief": [
        "Donating food and clothes for flood victims",
        "Volunteering in disaster relief camps",
        "Providing emergency supplies during disasters"
    ],
    "Food": [
        "Donating surplus food from events",
        "Providing meals for homeless people",
        "Supplying groceries to needy families"
    ]
}

rows = []

for _ in range(2000):
    cat = random.choice(list(categories.keys()))
    desc = random.choice(categories[cat])
    rows.append([desc])

with open("valid_contributions.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["description"])
    writer.writerows(rows)

print("valid_contributions.csv generated with 2000 rows")
