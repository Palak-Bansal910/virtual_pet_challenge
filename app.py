from Background_work import update_pet_status
from flask import Flask, render_template, request, jsonify
from game_logic import VirtualPetML
import database
from behaviour import Pet
from datetime import datetime
import random

app = Flask(__name__)

# -------------------------
# Initialize DB + Pet
# -------------------------
database.init_db()
pet_id = database.add_pet("Buddy")   # stored in DB
if pet_id is None:   # fallback if pet couldn't be added
    pet_id = 1

pet = VirtualPetML(name="Buddy")     # game logic + ML mood
behaviour_pet = Pet()                # behaviour system

# Add required attributes for behaviour.py
behaviour_pet.day = 1
behaviour_pet.difficulty = 1
behaviour_pet.interaction_history = []

# -------------------------
# Routes
# -------------------------
@app.route("/")
def home():
    status = pet.get_status()
    updated_pet = update_pet_status(pet, pet_id)   # pass pet_id
    return render_template("index.html", pet=updated_pet)

@app.route("/interact", methods=["POST"])
def interact():
    action = request.json.get("action")

    if action == "feed":
        message = pet.feed_pet()
    elif action == "play":
        message = pet.play_pet()
    elif action == "sleep":
        message = pet.sleep_pet()
    else:
        message = "Unknown action."

    behaviour_pet.interaction_history.append(datetime.now().hour)
    behaviour_pet.update_difficulty()
    behaviour_pet.day += 1

    state = pet.get_status()
    database.update_pet(pet_id, state)
    database.save_pet_action(pet_id, action, message)

    return jsonify({
        "message": message,
        "state": state,
        "difficulty": behaviour_pet.difficulty
    })

@app.route("/attention", methods=["GET"])
def attention():
    demand_hour = random.choice(range(24))
    current_hour = datetime.now().hour
    if current_hour == demand_hour or behaviour_pet.difficulty > 5:
        response = "Pet is demanding attention now! 🐾"
    else:
        response = "Pet is calm."
    return jsonify({"attention": response})

@app.route("/train", methods=["GET"])
def train_model():
    unavailable = behaviour_pet.train_ml_model()
    if unavailable:
        return jsonify({"unavailable_hours": unavailable})
    return jsonify({"message": "Not enough interaction history to train model."})

if __name__ == "__main__":
    app.run(debug=True)
