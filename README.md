# Cake Shop Management System

## Overview

This Cake Shop Management System is a simple console-based application that helps manage a cake 
shop's inventory, orders, and payments. It provides functionalities for customers to browse cakes, 
add them to a cart, generate a bill, and make payments. Additionally, administrators can manage 
cake products and user accounts.
To login as a ADMIN you can use AdminID as "**admin**" and password as "**admin**"

## Features

- Display a list of available cakes.
- Search for cakes by flavor.
- Add cakes to a shopping cart.
- Edit the shopping cart (change quantities).
- Generate a bill with tax calculation.
- User registration and login.
- Admin functions (product management and user management).

## Getting Started

To run this application locally, follow these steps:

1. Clone the repository:
        git clone https://github.com/anurag5100/Cake-Shop-Management.-Mini-Project-.git
   
3. Navigate to the project directory:
        cd cake-shop-management

4. Install the requirements
```bash
python3 -m venv venv
source venv/bin/activate
pip instal -r requirements.txt
```

5. Run the application:
        python main.py

## Usage

- Upon starting the application, users can choose options from the main menu to interact with the system.
- Customers can browse cakes, add them to the cart, edit the cart, and generate bills.
- Administrators can manage cake products and user accounts.

## Technologies Used

- Python
- Console-based interface

## Tests
```bash
python -m pytest -s
```



