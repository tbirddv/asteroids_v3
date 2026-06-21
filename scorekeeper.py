from constants import SCORE_PER_SIZE, ASTEROID_MIN_RADIUS

class Scorekeeper:
    score = 0

    @classmethod
    def increment(cls, radius):
        cls.score += SCORE_PER_SIZE * radius / ASTEROID_MIN_RADIUS
    
    @classmethod
    def get_score(cls):
        return cls.score
    
    @classmethod
    def reset_score(cls):
        cls.score = 0