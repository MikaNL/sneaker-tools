import random

class UserAgent:
    def __init__():
        pass

    def get():
        with open('user_agents.txt', 'r') as f:
            user_agents = f.read().split('\n')
        return random.choice(user_agents)