import json
import os

class ScoreManager:
    def __init__(self, filename="scores.json"):
        self.filename = filename
        self.scores = []
        self.load_scores()
    
    def load_scores(self):
        
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    self.scores = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
        
                self.scores = []
        else:
        
            self.scores = []
            self.save_scores()
    
    def save_scores(self):

        with open(self.filename, 'w') as file:
            json.dump(self.scores, file)
    
    def add_score(self, name, time):
        self.scores.append({
            "name": name,
            "time": time
        })
        
        self.scores = sorted(self.scores, key=lambda x: x["time"])

        if len(self.scores) > 5:
            self.scores = self.scores[:5]
        
        self.save_scores()
    
    def get_top_scores(self, limit=5):
        return self.scores[:limit]
    
    def is_high_score(self, time):

        if len(self.scores) < 5:
            return True

        return time < self.scores[-1]["time"]