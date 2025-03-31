import json
import os

class ScoreManager:
    def __init__(self, filename="scores.json"):
        self.filename = filename
        self.scores = {
            "Facile": [],
            "Moyen": [],
            "Difficile": []
        }
        self.load_scores()
    
    def load_scores(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    # Compatibilité avec l'ancien format
                    if isinstance(data, list):
                        self.scores = {
                            "Facile": data,
                            "Moyen": [],
                            "Difficile": []
                        }
                    else:
                        self.scores = data
            except (json.JSONDecodeError, FileNotFoundError):
                # Initialisation par défaut
                self.scores = {
                    "Facile": [],
                    "Moyen": [],
                    "Difficile": []
                }
        else:
            # Initialisation par défaut
            self.scores = {
                "Facile": [],
                "Moyen": [],
                "Difficile": []
            }
            self.save_scores()
    
    def save_scores(self):

        with open(self.filename, 'w') as file:
            json.dump(self.scores, file)
    
    def add_score(self, name, time, difficulty="Facile"):
        self.scores[difficulty].append({
            "name": name,
            "time": time
        })
        
        self.scores[difficulty] = sorted(self.scores[difficulty], key=lambda x: x["time"])
        
        if len(self.scores[difficulty]) > 5:
            self.scores[difficulty] = self.scores[difficulty][:5]
        
        self.save_scores()

    def get_top_scores(self, difficulty="Facile", limit=5):
        return self.scores[difficulty][:limit]

    def is_high_score(self, time, difficulty="Facile"):
        if len(self.scores[difficulty]) < 5:
            return True
        return time < self.scores[difficulty][-1]["time"]