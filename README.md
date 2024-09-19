# Restaurant Management CLI

This is a command-line interface (CLI) application for managing a restaurant's operations, including menu items, orders, and customers.

## Installation

1. Clone this repository
2. Install the required dependencies using pip:
   ```
   pip install -r requirements.txt
   ```

## Usage

To start the CLI, run:

```
python main.py
```

## Features

1. User Authentication
   - Login
   - Register

2. Restaurant Management
   - Create a new restaurant (for new users)

3. Menu Management
   - Add menu item
   - List menu items
   - Update menu item
   - Delete menu item

4. Order Management
   - Create order
   - List orders
   - Delete order

5. Customer Management
   - Add customer
   - List customers
   - Update customer
   - Delete customer

## Workflow

1. Upon starting the CLI, you will be prompted to login or register.
2. After authentication, if you're a new user, you'll be asked to create a restaurant.
3. You'll then have access to the main menu, where you can choose to manage menu items, orders, or customers.
4. Each management section (menu, orders, customers) has its own sub-menu with specific operations.
5. You can navigate back to the main menu or exit the application at any time.

## Functions

### User Authentication
- `login_or_register()`: Handles user login and registration process.

### Menu Management
- `add_menu_item()`: Adds a new item to the restaurant's menu.
- `list_menu_items()`: Displays all items in the menu.
- `update_menu_item()`: Modifies an existing menu item.
- `delete_menu_item()`: Removes a menu item.

### Order Management
- `create_order()`: Creates a new order for a customer.
- `list_orders()`: Displays all orders, optionally filtered by customer.
- `delete_order()`: Removes an order from the system.

### Customer Management
- `add_customer()`: Adds a new customer to the system.
- `list_customers()`: Displays all customers associated with the restaurant.
- `update_customer()`: Modifies customer information.
- `delete_customer()`: Removes a customer from the system.

## Database

This application uses SQLite as its database. The database file `restaurant.db` is created in the `instance` folder when you first run the application.

## Error Handling

The application includes basic error handling for database operations and user inputs. If you encounter any issues, you may be prompted to log in again or restart the application.
