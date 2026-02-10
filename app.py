from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# ------------------ DEMO USER STORAGE ------------------
users = {}

@app.route("/")
def home():
    return "Market Merge AI backend is running"

# ------------------ AUTHENTICATION ------------------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username in users:
        return jsonify({"error": "User already exists"}), 400

    users[username] = password
    return jsonify({"message": "Signup successful"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if users.get(username) == password:
        return jsonify({"message": "Login successful"})
    return jsonify({"error": "Invalid credentials"}), 401


# ------------------ PRICE COMPARISON LOGIC ------------------
def fetch_platform_data(base_price):
    return [
        {
            "platform": "Amazon",
            "price": base_price + random.randint(10, 60),
            "rating": round(random.uniform(4.0, 4.6), 1),
            "delivery": "2 Days",
            "return_policy": "10 Days"
        },
        {
            "platform": "Flipkart",
            "price": base_price + random.randint(20, 80),
            "rating": round(random.uniform(3.8, 4.5), 1),
            "delivery": "3 Days",
            "return_policy": "7 Days"
        },
        {
            "platform": "Meesho",
            "price": base_price - random.randint(5, 40),
            "rating": round(random.uniform(3.7, 4.3), 1),
            "delivery": "4 Days",
            "return_policy": "5 Days"
        },
        {
            "platform": "Ajio",
            "price": base_price + random.randint(30, 90),
            "rating": round(random.uniform(4.0, 4.4), 1),
            "delivery": "3 Days",
            "return_policy": "15 Days"
        },
        {
            "platform": "Myntra",
            "price": base_price + random.randint(15, 70),
            "rating": round(random.uniform(4.1, 4.7), 1),
            "delivery": "2 Days",
            "return_policy": "14 Days"
        }
    ]

@app.route("/compare", methods=["POST"])
def compare():
    data = request.json
    link = data.get("link")
    base_price = data.get("price")

    if not link or not base_price:
        return jsonify({"error": "Product link and price required"}), 400

    platforms = fetch_platform_data(int(base_price))
    best_platform = min(platforms, key=lambda x: x["price"])

    explanation = (
        f"{best_platform['platform']} is recommended because it offers the lowest price "
        f"at ₹{best_platform['price']} with a rating of {best_platform['rating']}. "
        f"It also provides delivery in {best_platform['delivery']} and a "
        f"{best_platform['return_policy']} return policy."
    )

    return jsonify({
        "best_platform": best_platform,
        "ai_explanation": explanation,
        "comparison": platforms
    })


# ------------------ PRICE HISTORY ------------------
@app.route("/price-history", methods=["GET"])
def price_history():
    return jsonify({
        "days": ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"],
        "prices": [260, 255, 245, 235, 230]
    })

if __name__ == "__main__":
    app.run(debug=True)