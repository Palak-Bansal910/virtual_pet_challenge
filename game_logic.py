import datetime
import numpy as np
import joblib

class VirtualPetML:
    def __init__(self, name: str, model_path="pet_mood_model.pkl"):
        self.name = name
        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        self.last_update = datetime.datetime.now()

        # Load pre-trained ML model
        try:
            self.model = joblib.load(model_path)
        except:
            self.model = None
            print("⚠️ Warning: ML model not found. Mood prediction will be random.")

    # ---------------- Actions ----------------
    def feed_pet(self):
        self.hunger = max(0, self.hunger - 20)
        self.happiness = min(100, self.happiness + 5)
        return f"{self.name} enjoyed the food 🍎"

    def play_pet(self):
        if self.energy > 10:
            self.happiness = min(100, self.happiness + 15)
            self.energy = max(0, self.energy - 10)
            self.hunger = min(100, self.hunger + 5)
            return f"{self.name} had fun playing 🎾"
        else:
            return f"{self.name} is too tired 😴"

    def sleep_pet(self):
        self.energy = min(100, self.energy + 25)
        self.hunger = min(100, self.hunger + 10)
        return f"{self.name} took a nap 💤"

    # ---------------- Decay ----------------
    def decay_stats(self):
        now = datetime.datetime.now()
        minutes_passed = (now - self.last_update).seconds // 60
        if minutes_passed >= 1:
            self.hunger = min(100, self.hunger + minutes_passed * 2)
            self.happiness = max(0, self.happiness - minutes_passed * 1)
            self.energy = max(0, self.energy - minutes_passed * 1)
            self.last_update = now

    # ---------------- Status ----------------
    def get_status(self):
        self.decay_stats()
        mood = self.predict_mood()
        return {
            "name": self.name,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "energy": self.energy,
            "mood": mood,
            "last_updated": self.last_update.isoformat()  # <-- Added this
        }


    # ---------------- ML Mood Prediction ----------------
    def predict_mood(self):
        if self.model:
            features = np.array([[self.hunger, self.happiness, self.energy]])
            return self.model.predict(features)[0]
        else:
            # fallback random mood
            return np.random.choice(["Happy 😃", "Sad 😢", "Hungry 😩", "Tired 😴"]) 
