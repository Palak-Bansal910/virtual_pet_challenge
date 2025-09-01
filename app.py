from flask import Flask, render_template, request, jsonify
from game_logic import VirtualPetML
import database
from datetime import datetime

app = Flask(__name__)

# Initialize pet
pet = VirtualPetML(name="Buddy")

@app.route("/")
def home():
    status = pet.get_status()
    return render_template("index.html", pet=status)

@app.route("/interact", methods=["POST"])
def interact():
    action = request.json.get("action")

    # Perform action
    if action == "feed":
        message = pet.feed_pet()
    elif action == "play":
        message = pet.play_pet()
    elif action == "sleep":
        message = pet.sleep_pet()
    else:
        message = "Unknown action."

    # Save in database (optional, if you adjust database.py helpers)
    database.save_pet_state(pet.get_status(), action=action)

    return jsonify({
        "message": message,
        "state": pet.get_status()
    })

if __name__ == "__main__":
    app.run(debug=True)
