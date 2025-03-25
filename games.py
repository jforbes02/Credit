import random

def RPS(choice, amount):
    """
    ~~~    Need to turn this into a web-compatible rock paper scissors ~~~


    Creates Rock Paper Scissors Game against cpu that utilizes dictionaries
    :param choice: Choice of rock, paper, scissors, whichever button on webpage is pressed
    :param amount: Amount of credit user will lose or get back based on if they lose or not
    :return: amount of credit user will lose or get back based on if they lose or not
    """
    rules = {"rock":"scissors", "paper":"rock", "scissors":"paper"} #this is the rules of rps
    #cpu
    cpu_choice = random.choice(list(rules.keys()))
    print(f"Computer chose {cpu_choice}")

    result={}
    result["cpu_choice"] = cpu_choice  #cpus choice is now in the result dictionary

    if choice == cpu_choice:
        result["status"] = "tie"
        result["message"] = "TIED"
        result["amount"] = amount * 2
    elif rules[choice] == cpu_choice:
        result["status"] = "win"
        result["message"] = "WON"
        result["amount"] = -amount
    else:
        result["status"] = "loss"
        result["message"] = "LOST"
        result["amount"] = amount

    return result