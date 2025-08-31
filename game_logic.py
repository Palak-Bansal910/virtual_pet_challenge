def update_difficulty(self):
        if self.day <= 8:
            self.difficulty = 1 + 0.1 * self.day  # linear increase
        else:
            self.difficulty = 1 * (2 ** (self.day - 8))  # doubles daily

        print(f"Day {self.day}: Difficulty now {self.difficulty:.2f}")