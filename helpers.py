import random

def generate_lottery_numbers(*args, **kwargs):
    return random.sample(range(1,60), 6)