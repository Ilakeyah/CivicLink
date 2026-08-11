import csv
import random

invalid_samples = [
    "hello",
    "ok",
    "test",
    "asdfgh",
    "12345",
    "nothing",
    "random words",
    "lorem ipsum",
    "hi",
    "donation",
    "service",
    "good",
    "nice",
    "abcd",
    ".",
    "???",
    "sample text",
    "checking",
    "blah blah",
    "xyz"
]

rows = []

for _ in range(1200):
    rows.append([random.choice(invalid_samples)])

with open("invalid_contributions.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["description"])
    writer.writerows(rows)

print("invalid_contributions.csv generated with 1200 rows")
