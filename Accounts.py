import math
import calendar
from datetime import datetime
from database import User, db, Transaction

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
        if type == "purchase" or type == "loss":
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
            if user.current_balance - amount < 0:
                amount = user.current_balance #makes sure balance is 0
                if amount == 0:
                    return "No payment needed"

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
    def weekly_debt(target_day = calendar.FRIDAY):
        """

        :param target_day:
        :return:
        """
        today = datetime.today().weekday() #4

        if today != target_day: #works only on Fridays
            return 0

        true_users = User.query.filter(User.current_balance > 0).all #all users that use their accounts
        debt_users = 0 #users that the debt
        date = datetime.today().date()


        for user in true_users:
            hit = Transaction.query.filter(
                Transaction.user_id == user.id,
                Transaction.type == "purchase",
                Transaction.description == "Weekly Interest",
                db.func.date(Transaction.created_at) == date).first()

            if hit:
                continue
            ratio = user.current_balance / user.credit_limit

            interest_rate = .22 + (ratio * .1) #interest rate of 22% (high but fun)
            total_interest = int(user.current_balance * interest_rate)
            total_interest = max(total_interest, 20) #no less than 20 dollars
            interest_description = "Weekly Interest"
            Account.transaction(user=user,
                                type="purchase",
                                amount=total_interest,
                                description=interest_description)
            debt_users += 1

        db.session.commit()

        return debt_users

    @staticmethod
    def get_credit_scores(user):
        """

        :param user: User
        :return: Credit score based on custom calculations (not real life credit calcs)
        """
        transactions = Transaction.query.filter(Transaction.user_id == user.id).all()
        if not transactions:
            return 670 #base credit score for new users

        #How much credit is used
        utilized_credit = user.current_balance / user.credit_limit
        utilized_credit_score = ((1-min(utilized_credit, 1)) * (1000 * .45))

        total_transactions = len(transactions) #how often transactoins are made
        activity_score = min(math.log(total_transactions + 1) * 40, (1000 * .35))

        #age of the account and oldest transaction
        oldest = transactions[0]
        for t in transactions: #goes through transactions to find the oldest one if an older transaction found
            if t.created_at < oldest.created_at:
                oldest = t
        account_age = (datetime.utcnow() - oldest.created_at).days
        age = min(account_age / 365, 1)
        age_score = age * (1000 * .20)

        final = utilized_credit_score + age_score + activity_score
        return max(300, min(1000, round(final)))
    @staticmethod
    def get_credit_rating(score):
        if score < 500:
            return "Poor"
        elif score < 669:
            return "Fair"
        elif score < 800:
            return "Good"
        elif score < 900:
            return "Great"
        else:
            return "WOW SO GOOD"