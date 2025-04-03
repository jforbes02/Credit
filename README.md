# Credit Game

Credit Game is an interactive web application that simulates a simplified credit system where users can learn about credit management in a fun, gamified environment. The application allows users to manage virtual credit, play games to pay down debt, make purchases with credit, and experience how credit scores are calculated.

## Features

### 1. User Authentication
- **Registration**: New users can sign up by providing username, email, password, and age.
- **Login/Logout**: Users can securely log in to access their account and log out when finished.
- **Account Management**: Users can delete their accounts if needed.

### 2. Credit System
- **Age-Based Credit Limits**: New users are assigned an initial credit limit based on their age (age × $125, with a minimum of $500).
- **Current Balance**: The system tracks a user's current credit balance based on purchases and payments.
- **Available Credit**: Users can see how much credit they have available to use (credit limit - current balance).

### 3. Transaction Management
- **Transaction Types**: The system supports various transaction types:
  - **Purchases**: Increases the user's balance when they buy items
  - **Payments**: Reduces the user's balance when they win games
  - **Credit Increases**: Adjusts the user's credit limit upward
  - **Credit Decreases**: Adjusts the user's credit limit downward
- **Transaction History**: Users can view their recent transaction history on their dashboard.

### 4. Weekly Interest Simulation
- **Automatic Interest Charges**: Every Friday, interest is charged on outstanding balances.
- **Variable Interest Rate**: Interest rates vary based on credit utilization:
  - Base rate of 22%
  - Additional 0-10% based on credit utilization ratio
  - Minimum $20 interest charge

### 5. Credit Score System
- **Dynamic Credit Score Calculation**: Credit scores (ranging from 300-1000) are calculated based on:
  - Credit utilization (45% weight)
  - Account activity (35% weight)
  - Account age (20% weight)
- **Credit Rating**: Users receive a rating based on their score:
  - Poor: < 500
  - Fair: 500-669
  - Good: 670-799
  - Great: 800-899
  - "WOW SO GOOD": 900+

### 6. Games for Payment
- **Rock-Paper-Scissors Game**: Users can play RPS to pay down their debt:
  - Winning reduces the user's balance by the wagered amount
  - Losing increases the user's balance by the wagered amount
  - Ties result in a "double or nothing" scenario where the wager doubles
- **Wager System**: Users set their own wager amount for each game.

### 7. Virtual Store
- **Item Purchases**: Users can buy virtual items (cats with different prices) using their credit.
- **Inventory Management**: Purchased items appear in the user's dashboard.
- **Purchase Confirmation**: Modal dialog confirms purchases before they're processed.

### 8. User Dashboard
- **Credit Summary**: Shows credit limit, current balance, and available credit.
- **Interest Information**: Displays current interest rate based on utilization.
- **Credit Score Display**: Shows the user's current credit score and rating.
- **Item Display**: Shows all purchased items with their quantities and values.
- **Transaction History**: Lists recent transactions with dates, amounts, types, and descriptions.

## Technical Implementation

### Backend
- **Flask Framework**: Powers the web application.
- **SQLAlchemy ORM**: Manages database interactions.
- **Flask-Login**: Handles user authentication.
- **Werkzeug Security**: Provides password hashing functionality.

### Frontend
- **HTML/CSS**: Responsive design with custom styling.
- **JavaScript**: Handles interactive elements:
  - Game mechanics for Rock-Paper-Scissors
  - Purchase modal functionality
  - Dynamic updates to user interface
- **Jinja2 Templates**: Renders dynamic content from the Flask backend.

### Database Structure
- **Users**: Stores user information, credit limits, and balances.
- **Transactions**: Records all financial activities.
- **Items**: Catalogs products available in the store.
- **User-Items Relationship**: Tracks which users own which items.

## Educational Benefits

The Credit Game offers a simplified but educational introduction to several financial concepts:
- Understanding credit utilization and limits
- Impact of regular payments on credit health
- How interest accumulates on carried balances
- Factors that influence credit scores
- Consequences of overspending

## Getting Started

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install flask flask-sqlalchemy flask-login
   ```
3. Run the application:
   ```
   python app.py
   ```
4. Access the application at http://localhost:5001

## Note

This is a simplified simulation for educational purposes and does not reflect actual credit scoring systems or interest calculations used by financial institutions.
