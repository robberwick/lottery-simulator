import collections
import multiprocessing
import random

from helpers import generate_lottery_numbers

class Lottery:
    def __init__(self, draw_number=None, number_of_players=None, ticket_cost=2):
        # ticket cost
        self.ticket_cost = 2
        # The numbers available to draw from
        self.available_numbers = range(1, 60)
        # how many numbers to draw
        self.numbers_to_draw = 6
        # number of the draw
        self.draw_number = draw_number
        # number of players in this draw
        self.number_of_players = number_of_players
        # winning numbers
        self.winning_numbers = generate_lottery_numbers()
        # draw results
        self.draw_results = dict()

    def check_ticket(self, entry):
        # todo - check entry is valid length, within bounds etc
        matching_numbers=set(self.winning_numbers).intersection(entry)
        return dict(matches=matching_numbers)
    
    def entries_generated_callback(self, entries):
        self.entries = entries

    def generate_and_score_entry(self, entry):
        numbers = generate_lottery_numbers()
        matches = self.check_ticket(numbers)['matches']
        return len(matches)

    def generate_results(self):
        num_processes = max(1, multiprocessing.cpu_count()-1)
        pool = multiprocessing.Pool(processes = num_processes)
        # generate an entry for each player
        # returns a list containing number of matches for each entry
        entries = pool.map(
            self.generate_and_score_entry,
            range(self.number_of_players),
            chunksize=1000,
            )
        results = collections.defaultdict(int)
        for entry in entries:
            results[entry] += 1
        return results
    
    @property
    def prize_pool(self):
        return (self.number_of_players * self.ticket_cost / 100) * 17.82

    def calculate_prize(self, number_of_matches):
        # uses figures from https://en.wikipedia.org/wiki/National_Lottery_(United_Kingdom)#Lotto
        # note we need other players to make this realistic or else 4 numbers 
        # wins more than 5 :-)
        if number_of_matches > 3 and not self.draw_results:
            self.draw_results = self.generate_results()
            
        prize = 0

    
        if number_of_matches == 2:
            prize = 2
        elif number_of_matches == 3:
            prize = 25
        elif number_of_matches == 4:
            num_other_winners = self.draw_results.get(4, 0)
            prize = (self.prize_pool / 100 * 12.9) / (num_other_winners + 1)
        elif number_of_matches == 5:
            num_other_winners = self.draw_results.get(5, 0)
            prize = (self.prize_pool / 100 * 2) / (num_other_winners + 1)
        elif number_of_matches == 6:
            num_other_winners = self.draw_results.get(6, 0)
            prize = (self.prize_pool / 100 * 83.2) / (num_other_winners + 1)
        
        return prize

