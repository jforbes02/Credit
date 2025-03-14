import random
from database import User, Transaction, db


class Account:
    @staticmethod
    def inital_credit(age):
        """
        :param age:
        :return: returns initial credit amount given to user based on age, or 500 so its never too low
        """
        return max(age * 125.00, 500.00)
    @staticmethod
    def transaction(user, type, amount, description):
        if type == "purchase":
            if user.current_balance + amount > user.credit_limit:
                return "You dont have enough credit"

            user.current_balance += amount

            transaction = Transaction(
                amount = amount,
                type = type,
                user_id=user.id,
                description=description
            )

            db.session.add(transaction)
            db.session.commit()
            return transaction
        elif type == "payment":
            user.current_balance -= amount
            transaction = Transaction(
                amount = amount,
                type = type,
                user_id=user.id,
                description=description
            )
            db.session.add(transaction)
            db.session.commit()
            return transaction
        elif type == "credit_increase":
            user.credit_limit += amount
            transaction = Transaction(
                amount = amount,
                type = type,
                user_id=user.id,
                description=description
            )
            db.session.add(transaction)
            db.session.commit()
            return transaction
        elif type == "credit_decrease":
            user.credit_limit -= amount
            transaction = Transaction(
                amount = amount,
                type = type,
                user_id=user.id,
                description=description
            )
            db.session.add(transaction)
            db.session.commit()
            return transaction
        else:
            return "Invalid Type"
        return transaction



@staticmethod
def weekly_debt():
    return (User.current_balance / User.credit_limit) * random.random(1, 10)