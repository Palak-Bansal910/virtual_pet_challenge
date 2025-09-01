import random
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime

class Pet:
    def update_stats(self):
        if self.hunger > 5:
            self.health -= 5 * self.difficulty
            self.happiness -= 2 * self.difficulty

    def demand_attention(self):
        response = input("Respond? (y/n): ")    # placeholder
        if response.lower() == 'y':
            self.feed()     # or play, etc, 
        else:
            self.update_stats()

    def train_ml_model(self):
        if len(self.interaction_history) < 5:  # if les than 5 interaction, return, as almost no data is available
            return
        
        # prep data: x = sequence of past days/hours, y = interaction count per hour
        hours = np.array(range(24)).reshape(-1, 1)  
        interaction_counts = np.array([self.interaction_history.count(h) for h in range(24)])
        model = LinearRegression()
        model.fit(hours, interaction_counts)

        # predict activity: low scores = unavailable times
        predicted_activity = model.predict(hours)
        unavailable_hours = [h for h, activity in zip(range(24), predicted_activity) if activity < np.mean(predicted_activity)]
        return unavailable_hours


    def schedule_demand(self):
        unavailable = self.train_ml_model() or [1, 9]
        demand_hour = random.choice(unavailable)
        current_hour = datetime.now().hour
        if current_hour == demand_hour or self.difficulty > 5:
            self.demand_attention()
    def update_difficulty(self):
        if self.day <= 8:
            self.difficulty = 1 + 0.1 * self.day  # linear increase
        else:
            self.difficulty = 1 * (2 ** (self.day - 8))  # doubles daily

        print(f"Day {self.day}: Difficulty now {self.difficulty:.2f}")
