from lottery import Lottery
from helpers import generate_lottery_numbers
import time

money_spent = 0
winnings = 0
ticket_cost = 2
number_of_players = 32000000

if __name__ == '__main__':
    draw_number = 0
    while True:
        draw_number = draw_number + 1
        my_numbers = generate_lottery_numbers()
        money_spent = money_spent + ticket_cost
        print(f"my numbers: {my_numbers}")

        lottery = Lottery(
            draw_number=draw_number,
            number_of_players=number_of_players,
            ticket_cost=ticket_cost
        )
        print(f"Winning lottery numbers {lottery.winning_numbers}")

        print(f"number of players = {number_of_players}")

        matching_numbers = lottery.check_ticket(my_numbers)['matches']
        matching_number_count = len(matching_numbers)

        print(f"Matching numbers: {len(matching_numbers)}")
        if matching_numbers:
            print(matching_numbers)

        prize = lottery.calculate_prize(len(matching_numbers))
        
        if matching_number_count == 2:
            # it's just a free play for next time, so we consider that
            # money back to pay for next week's entry
            money_spent = money_spent + prize
        elif matching_number_count > 2:
            winnings = winnings + prize
        
        print(f"money spent: £{money_spent:.2f} winnings: £{winnings:.2f}")
        print(f"balance: £{winnings - money_spent:.2f}")
        time.sleep(0.1)