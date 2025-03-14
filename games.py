import random

def RPS():
    """
    Creates Rock Paper Scissors Game against cpu that utilizes dictionaries
    """
    rules = {"rock":"scissors", "paper":"rock", "scissor":"paper"} #this is the rules of rps
    while True:
        try:
            #cpu
            cpu_choice = random.choice(list(rules.keys()))
            #human
            choice = input("Enter rock, paper or scissor: ")
            print(f"Computer chose {cpu_choice}")
            if choice not in rules:
                print("Invalid choice")
                continue


            if choice == cpu_choice:
                print("Tie")
            elif rules[choice] == cpu_choice:
                print("You Win!!")
            else:
                print("You lose!")

        except Exception as e:
            print(f"ERROR: {e}")

        print("thanks for playing")
        exit()

RPS()