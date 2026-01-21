import random

# Move a card from deck to hand
def draw_card(hand, deck):
    hand.append(deck.pop())

# Calculate the total score of a hand
def calculate_score(hand):
    total = 0
    aces = 0

    for card in hand:
        if card in ["J", "Q", "K"]:
            total += 10
        elif card == "A":
            total += 11
            aces += 1
        else:
            total += int(card)

    # Adjust for aces if bust
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total

# Print current game status
def print_status(player_hand, dealer_hand, hide_dealer=False):
    print("\nPlayer hand:", player_hand, "Score:", calculate_score(player_hand))

    if hide_dealer:
        print("Dealer hand:", [dealer_hand[0], "?"])
    else:
        print("Dealer hand:", dealer_hand, "Score:", calculate_score(dealer_hand))

def main():
    deck = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    player_hand = []
    dealer_hand = []

    random.shuffle(deck)

    # Initial deal
    draw_card(dealer_hand, deck)
    draw_card(player_hand, deck)
    draw_card(player_hand, deck)

    # Player turn
    while True:
        print_status(player_hand, dealer_hand, hide_dealer=True)

        if calculate_score(player_hand) > 21:
            print("You bust! Dealer wins.")
            return

        choice = input("Hit or stay? (h/s): ").lower()

        if choice == "h":
            draw_card(player_hand, deck)
        elif choice == "s":
            break
        else:
            print("Invalid choice. Enter h or s.")

    # Dealer turn
    while calculate_score(dealer_hand) < 17:
        draw_card(dealer_hand, deck)

    print_status(player_hand, dealer_hand)

    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    # Determine winner
    if dealer_score > 21:
        print("Dealer busts! You win!")
    elif dealer_score > player_score:
        print("Dealer wins!")
    elif player_score > dealer_score:
        print("You win!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    again = "y"
    while again == "y":
        main()
        again = input("Play again? (y/n): ").lower()
