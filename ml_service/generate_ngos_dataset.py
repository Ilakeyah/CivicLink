import pandas as pd
import random

# ---------------- CONFIG ----------------
NUM_NGOS = 2500   # You can increase to 3000+ if needed

TAMIL_NADU_DISTRICTS = [
    "Ariyalur",
    "Chengalpattu",
    "Chennai",
    "Coimbatore",
    "Cuddalore",
    "Dharmapuri",
    "Dindigul",
    "Erode",
    "Kallakurichi",
    "Kanchipuram",
    "Kanniyakumari",
    "Karur",
    "Krishnagiri",
    "Madurai",
    "Mayiladuthurai",
    "Nagapattinam",
    "Namakkal",
    "Nilgiris",
    "Perambalur",
    "Pudukkottai",
    "Ramanathapuram",
    "Ranipet",
    "Salem",
    "Sivaganga",
    "Tenkasi",
    "Thanjavur",
    "Theni",
    "Thoothukudi",
    "Tiruchirappalli",
    "Tirunelveli",
    "Tirupathur",
    "Tiruppur",
    "Tiruvallur",
    "Tiruvannamalai",
    "Tiruvarur",
    "Vellore",
    "Viluppuram",
    "Virudhunagar"
]

SPECIALIZATIONS = [
    "Education",
    "Food & Nutrition",
    "Clothing",
    "Healthcare",
    "Disaster Relief",
    "Community Development",
    "Counselling",
    "Skill Training"
]

NGO_PREFIXES = [
    "Helping Hands",
    "Bright Future",
    "Hope Foundation",
    "Care & Share",
    "Serve Humanity",
    "Life Line",
    "Uplift Trust",
    "Samaritan Group",
    "People First",
    "Social Care"
]

# ---------------- GENERATE DATA ----------------
rows = []

for i in range(1, NUM_NGOS + 1):
    ngo_name = f"{random.choice(NGO_PREFIXES)} NGO {i}"
    email = f"ngo{i}@civiclink.org"
    location = random.choice(TAMIL_NADU_DISTRICTS)

    specialization_count = random.randint(1, 3)
    specializations = ", ".join(
        random.sample(SPECIALIZATIONS, specialization_count)
    )

    rows.append({
        "ngo_id": i,
        "ngo_name": ngo_name,
        "email": email,
        "location": location,
        "specializations": specializations
    })

df = pd.DataFrame(rows)

df.to_csv("ngos.csv", index=False)

print("✅ NGO dataset regenerated successfully")
print("Total NGOs:", len(df))
print("Total Districts Covered:", df['location'].nunique())
print("Districts:", sorted(df['location'].unique()))
