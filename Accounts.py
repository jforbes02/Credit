import random
from database import User, Transaction, db


class Account:
    """ Handles credit limits and transactions """
    @staticmethod
    def initial_credit(age):
        """
        :param age:
        :return: returns initial credit amount given to user based on age, or 500 so it's never too low
        """
        return max(age * 125.00, 500.00)
    @staticmethod
    def transaction(user, type, amount, description):
        """

        :param user: User that is being affected
        :param type: type of transaction(increase, decrease, credit limit etc.)
        :param amount: cost of the transaction
        :param description: each transaction has a description
        :return: Transaction object
        """
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

    @staticmethod
    def weekly_debt():
        return (User.current_balance / User.credit_limit) * random.random(1, 10)