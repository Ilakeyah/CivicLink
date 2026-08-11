from flask import Flask, request, jsonify
from flask_cors import CORS

import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- APP SETUP ----------------
app = Flask(__name__)
CORS(app)

# ---------------- LOAD DATASETS ----------------
ngos_df = pd.read_csv("ngos.csv")

# Ensure required columns exist (safe for prototype)
if "current_load" not in ngos_df.columns:
    ngos_df["current_load"] = 0
if "capacity" not in ngos_df.columns:
    ngos_df["capacity"] = 5

ngos_df["specializations"] = ngos_df["specializations"].fillna("")
ngos_df["location"] = ngos_df["location"].fillna("").str.lower()

valid_df = pd.read_csv("valid_contributions.csv")
valid_df["description"] = valid_df["description"].fillna("")

# ---------------- NEARBY LOCATION MAP ----------------
NEARBY_LOCATIONS = {
    "coimbatore": ["tiruppur", "erode", "nilgiris"],
    "chennai": ["kanchipuram", "chengalpattu", "tiruvallur"],
    "madurai": ["dindigul", "theni", "virudhunagar"]
}

# ---------------- DONATION CATEGORY KEYWORDS ----------------
CATEGORY_KEYWORDS = {
    "education": [
        "education", "school", "college", "university",
        "teacher", "teaching", "tutor",
        "students", "mathematics", "maths", "science",
        "uniform", "pen", "pencil", "notebook", "stationery"
    ],
    "food": ["food", "meals", "nutrition", "groceries", "hunger"],
    "clothing": ["clothes", "clothing", "jackets", "blankets", "shirts"],
    "healthcare": ["health", "medical", "medicine", "hospital", "patients"],
    "disaster relief": ["disaster", "flood", "earthquake", "relief", "emergency"],
    "community development": ["community", "development", "welfare", "support"],
    "counselling": ["counselling", "therapy", "mental", "guidance"],
    "skill training": ["training", "skills", "workshop", "employment"]
}

# ---------------- SERVICE CATEGORY KEYWORDS ----------------
SERVICE_CATEGORY_KEYWORDS = {
    "education": [
        "teach", "teaching", "teacher", "tutor", "mentoring",
        "students", "student", "school", "college", "university",
        "education", "learning", "classes", "classroom",
        "mathematics", "maths", "science", "english",
        "computer", "coding", "programming",
        "exam", "coaching", "tuition", "guidance"
    ],
    "healthcare": [
        "health", "medical", "medicine", "doctor", "nurse",
        "hospital", "clinic", "patient", "treatment",
        "first aid", "emergency", "therapy", "rehabilitation",
        "checkup", "vaccination", "physiotherapy"
    ],
    "counselling": [
        "counselling", "therapy", "mental", "emotional",
        "stress", "anxiety", "depression", "guidance",
        "psychology", "support", "wellbeing"
    ],
    "skill training": [
        "training", "skills", "workshop", "technical",
        "vocational", "employment", "job",
        "computer", "electrician", "plumber",
        "carpenter", "mechanic", "tailoring"
    ]
}

# ---------------- TF-IDF MODELS ----------------
ngo_vectorizer = TfidfVectorizer(stop_words="english")
ngo_vectorizer.fit(ngos_df["specializations"])

verify_vectorizer = TfidfVectorizer(stop_words="english")
valid_tfidf = verify_vectorizer.fit_transform(valid_df["description"])

# =====================================================
# =============== VERIFY CONTRIBUTION =================
# =====================================================
@app.route("/verify", methods=["POST"])
def verify_contribution():
    data = request.json or {}

    contribution_type = data.get("type", "").upper()
    category_raw = data.get("category", "").lower().strip()
    description = data.get("description", "").lower().strip()

    if len(description) < 10:
        return jsonify({"verified": False, "reason": "Description is too short."})

    if not re.search(r"[a-zA-Z]{3,}", description):
        return jsonify({"verified": False, "reason": "Description lacks meaningful text."})

    category = category_raw if not category_raw.startswith("other") else "other"

    if contribution_type == "SERVICE":
        service_keywords = SERVICE_CATEGORY_KEYWORDS.get(category, [])
        if not any(k in description for k in service_keywords):
            return jsonify({
                "verified": False,
                "reason": "Service description does not match the selected category."
            })

        desc_vec = verify_vectorizer.transform([description])
        sim = cosine_similarity(desc_vec, valid_tfidf).flatten().max()

        if sim >= 0.08:
            return jsonify({"verified": True, "confidence": round(float(max(sim, 0.75)), 2)})

        return jsonify({"verified": False, "reason": "Service description is unclear."})

    if contribution_type == "DONATION":
        keywords = CATEGORY_KEYWORDS.get(category, [])
        if category != "other" and not any(k in description for k in keywords):
            return jsonify({
                "verified": False,
                "reason": "Donation items do not match the selected category."
            })

        desc_vec = verify_vectorizer.transform([description])
        sim = cosine_similarity(desc_vec, valid_tfidf).flatten().max()

        if sim < 0.10:
            return jsonify({
                "verified": False,
                "reason": "Donation description is not clear or meaningful."
            })

        return jsonify({"verified": True, "confidence": round(float(sim), 2)})

    return jsonify({"verified": False, "reason": "Invalid contribution type."})


# =====================================================
# =============== NGO RECOMMENDATION ==================
# =====================================================
@app.route("/recommend", methods=["POST"])
def recommend_ngos():
    data = request.json or {}

    category = data.get("category", "").lower()
    description = data.get("description", "").lower()
    location = data.get("location", "").lower()

    if not category and not description:
        return jsonify([])

    # -------- LOCATION FILTER --------
    filtered_ngos = ngos_df.copy()

    if location:
        filtered_ngos = filtered_ngos[
            filtered_ngos["location"] == location
        ]

    # -------- NEARBY FALLBACK --------
    fallback_used = False
    if filtered_ngos.empty and location in NEARBY_LOCATIONS:
        nearby = NEARBY_LOCATIONS[location]
        filtered_ngos = ngos_df[
            ngos_df["location"].isin(nearby)
        ]
        fallback_used = True

    if filtered_ngos.empty:
        filtered_ngos = ngos_df.copy()
        fallback_used = True

    # -------- WORKLOAD FILTER --------
    filtered_ngos = filtered_ngos[
        filtered_ngos["current_load"] < filtered_ngos["capacity"]
    ]

    # -------- SIMILARITY --------
    query = f"{category} {description}"
    query_vec = ngo_vectorizer.transform([query])
    ngo_vecs = ngo_vectorizer.transform(filtered_ngos["specializations"])

    scores = cosine_similarity(query_vec, ngo_vecs).flatten()
    filtered_ngos["match_score"] = (scores * 100).clip(max=100)

    # -------- EXPLAINABILITY --------
    results = []
    for idx, ngo in filtered_ngos.sort_values(
        by="match_score", ascending=False
    ).head(5).iterrows():

        reasons = []

        if category in ngo["specializations"].lower():
            reasons.append(f"Matches {category} services")

        if location and ngo["location"] == location:
            reasons.append(f"Located in {ngo['location'].title()}")

        if scores[list(filtered_ngos.index).index(idx)] > 0.6:
            reasons.append("High relevance to request description")

        if fallback_used:
            reasons.append("Nearby NGO shown due to limited availability")

        results.append({
            "ngo_id": int(ngo["ngo_id"]),
            "ngo_name": ngo["ngo_name"],
            "email": ngo["email"],
            "location": ngo["location"].title(),
            "specializations": ngo["specializations"],
            "match_score": round(float(ngo["match_score"]), 2),
            "reasons": reasons
        })

    return jsonify(results)


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)
