from lottery import Lottery
from helpers import generate_lottery_numbers
import time

class LottoSim():

    def __init__(self):
        self.money_spent = 0
        self.winnings = 0
        self.ticket_cost = 2
        self.number_of_players = 32000000
        self.draw_number = 0
        
    
    def run(self):
        while True:
            self.draw_number = self.draw_number + 1
            my_numbers = generate_lottery_numbers()
            self.money_spent = self.money_spent + self.ticket_cost

            lottery = Lottery(
                draw_number=self.draw_number,
                number_of_players=self.number_of_players,
                ticket_cost=self.ticket_cost
            )


            matching_numbers = lottery.check_ticket(my_numbers)['matches']
            matching_number_count = len(matching_numbers)


            prize = lottery.calculate_prize(len(matching_numbers))
            
            if matching_number_count == 2:
                # it's just a free play for next time, so we consider that
                # money back to pay for next week's entry
                self.money_spent = self.money_spent + prize
            elif matching_number_count > 2:
                self.winnings = self.winnings + prize


            self.draw(my_numbers, lottery.winning_numbers, matching_numbers)
            
    
    def draw(self, entry_numbers, winning_numbers, matching_numbers):
        # child sublclasses should implement a drawing routine
        raise NotImplementedError()


class ConsoleLottoSim(LottoSim):

    def draw(self, entry_numbers, winning_numbers, matching_numbers):
        print(f"my numbers: {entry_numbers}")
        print(f"Winning lottery numbers {winning_numbers}")
        print(f"number of players = {self.number_of_players}")
        print(f"Matching numbers: {len(matching_numbers)}")
        if matching_numbers:
            print(matching_numbers)
        print(f"money spent: £{self.money_spent:.2f} self.winnings: £{self.winnings:.2f}")
        print(f"balance: £{self.winnings - self.money_spent:.2f}")

        # a small sleep so we can see what's happening
        time.sleep(0.1)


if __name__ == '__main__':
    lottsim = ConsoleLottoSim()
    lottsim.run()