import random

def RPS(amount):
    """
    Creates Rock Paper Scissors Game against cpu that utilizes dictionaries
    :param amount: Amount of credit user will lose or get back based on if they lose or not
    :return: amount of credit user will lose or get back based on if they lose or not
    """
    rules = {"rock":"scissor", "paper":"rock", "scissor":"paper"} #this is the rules of rps
    win_loss = 0
    try:
        #cpu
        cpu_choice = random.choice(list(rules.keys()))
        #human
        choice = input("Enter rock, paper or scissor: ")
        print(f"Computer chose {cpu_choice}")
        if choice not in rules:
            print("Invalid choice")
            return RPS(amount)


        if choice == cpu_choice:
            print("Tie")
            return RPS(amount * 2)
        elif rules[choice] == cpu_choice:
            print("You Win!!")
            return -amount
        else:
            print("You lose!")
            return amount

    except Exception as e:
        print(f"ERROR: {e}")
        return 0
