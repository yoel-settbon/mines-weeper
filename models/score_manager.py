import json
import os

class ScoreManager:
    def __init__(self, filename="scores.json"):
        self.filename = filename
        self.scores = []
        self.load_scores()
    
    def load_scores(self):
        """Charge les scores depuis le fichier JSON"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    self.scores = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                # Si le fichier est corrompu ou n'existe pas, on initialise avec une liste vide
                self.scores = []
        else:
            # Créer un fichier vide si le fichier n'existe pas
            self.scores = []
            self.save_scores()
    
    def save_scores(self):
        """Sauvegarde les scores dans le fichier JSON"""
        with open(self.filename, 'w') as file:
            json.dump(self.scores, file)
    
    def add_score(self, name, time):
        """Ajoute un score à la liste et trie les scores"""
        self.scores.append({
            "name": name,
            "time": time
        })
        
        # Trier les scores par temps (du plus petit au plus grand)
        self.scores = sorted(self.scores, key=lambda x: x["time"])
        
        # Limiter à 5 scores maximum
        if len(self.scores) > 5:
            self.scores = self.scores[:5]
        
        self.save_scores()
    
    def get_top_scores(self, limit=5):
        """Récupère les meilleurs scores"""
        return self.scores[:limit]
    
    def is_high_score(self, time):
        """Vérifie si le temps est un record"""
        # Si moins de 5 scores, c'est automatiquement un record
        if len(self.scores) < 5:
            return True
        
        # Sinon, comparer avec le score le plus lent
        return time < self.scores[-1]["time"]