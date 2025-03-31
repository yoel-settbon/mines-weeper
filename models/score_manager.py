import json
import os

class ScoreManager:
    def __init__(self, filename="scores.json"):
        self.filename = filename
        self.scores = {
            "Easy": [],
            "Medium": [],
            "Hard": []
        }
        self.load_scores()
    
    def load_scores(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    # Compatibility with old format
                    if isinstance(data, list):
                        self.scores = {
                            "Easy": data,
                            "Medium": [],
                            "Hard": []
                        }
                    else:
                        self.scores = data
            except (json.JSONDecodeError, FileNotFoundError):
                # Default initialization
                self.scores = {
                    "Easy": [],
                    "Medium": [],
                    "Hard": []
                }
        else:
            # Default initialization
            self.scores = {
                "Easy": [],
                "Medium": [],
                "Hard": []
            }
            self.save_scores()
    
    def save_scores(self):
        with open(self.filename, 'w') as file:
            json.dump(self.scores, file)
    
    def add_score(self, name, time, difficulty="Easy"):
        self.scores[difficulty].append({
            "name": name,
            "time": time
        })
        
        self.scores[difficulty] = sorted(self.scores[difficulty], key=lambda x: x["time"])
        
        if len(self.scores[difficulty]) > 5:
            self.scores[difficulty] = self.scores[difficulty][:5]
        
        self.save_scores()

    def get_top_scores(self, difficulty="Easy", limit=5):
        return self.scores[difficulty][:limit]

    def is_high_score(self, time, difficulty="Easy"):
        if len(self.scores[difficulty]) < 5:
            return True
        return time < self.scores[difficulty][-1]["time"]
