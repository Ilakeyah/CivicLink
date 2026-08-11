import random
import csv

locations = ["Coimbatore", "Chennai", "Bangalore", "Madurai", "Trichy"]

categories = [
    "Education",
    "Food",
    "Clothing",
    "Healthcare",
    "Disaster Relief",
    "Community Development"
]

# ---------- NGO DATA ----------
ngos = []
for i in range(1, 501):
    specs = random.sample(categories, random.randint(1, 3))
    ngos.append({
        "ngo_id": i,
        "ngo_name": f"NGO_{i}",
        "email": f"ngo{i}@example.com",
        "location": random.choice(locations),
        "specializations": ",".join(specs),
        "capacity": random.randint(30, 80),
        "current_load": random.randint(0, 25)
    })

# ---------- CONTRIBUTIONS ----------
contributions = []
for i in range(1, 2001):
    cat = random.choice(categories)
    contributions.append({
        "contribution_id": i,
        "user_id": random.randint(1, 300),
        "type": random.choice(["DONATION", "SERVICE"]),
        "category": cat,
        "description": f"I want to offer support related to {cat.lower()} for people in need",
        "location": random.choice(locations),
        "status": random.choice(["OPEN", "CLOSED"])
    })

# ---------- INTERACTIONS ----------
interactions = []
interaction_id = 1
for _ in range(3500):
    interactions.append({
        "interaction_id": interaction_id,
        "contribution_id": random.randint(1, 2000),
        "ngo_id": random.randint(1, 500),
        "accepted": random.choice([0, 1]),
        "response_time": random.randint(1, 48),
        "success": random.choice([0, 1])
    })
    interaction_id += 1

# ---------- WRITE CSV ----------
def write_csv(filename, data):
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

write_csv("ngos.csv", ngos)
write_csv("contributions.csv", contributions)
write_csv("interactions.csv", interactions)

print("Datasets generated successfully!")
