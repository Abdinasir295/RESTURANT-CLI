import click
from sqlalchemy.orm import Session
from commands import (
    add_menu_item, list_menu_items, update_menu_item, delete_menu_item,
    create_order, list_orders, delete_order,
    add_customer, list_customers, update_customer, delete_customer
)
from database import init_db, get_db
from models import Customer, Restaurant, MenuItem, Order
from werkzeug.security import check_password_hash, generate_password_hash
import sqlalchemy.orm.exc
from utils import get_or_create_restaurant

@click.group()
def cli():
    pass

def login_or_register():
    while True:
        click.echo("\nAuthentication:")
        choice = click.prompt("Choose an option", type=click.Choice(['1', '2', '3']))
        if choice == '1':
            name = click.prompt("Enter your name")
            password = click.prompt("Enter your password", hide_input=True)
            db = next(get_db())
            user = db.query(Customer).filter(Customer.name == name).first()
            if user and check_password_hash(user.password, password):
                db.refresh(user)
                return user
            else:
                click.echo("Invalid credentials. Please try again.")
        elif choice == '2':
            name = click.prompt("Enter your name")
            password = click.prompt("Enter your password", hide_input=True, confirmation_prompt=True)
            db = next(get_db())
            existing_user = db.query(Customer).filter(Customer.name == name).first()
            if existing_user:
                click.echo("User already exists. Please choose a different name.")
            else:
                new_user = Customer(name=name, password=generate_password_hash(password))
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                return new_user
        elif choice == '3':
            return None

def interactive_cli():
    click.echo("Welcome to the Restaurant Management CLI!")
    
    user = None
    while user is None:
        click.echo("\nPlease choose an option:")
        click.echo("1. Login")
        click.echo("2. Register")
        click.echo("3. Exit")
        user = login_or_register()
        if user is None:
            click.echo("Thank you for using the Restaurant Management CLI. Goodbye!")
            return

    click.echo(f"Welcome, {user.name}!")
    
    db = next(get_db())
    if not user.restaurant_id:
        click.echo("You don't have a restaurant yet. Let's create one!")
        restaurant_name = click.prompt("Enter a name for your restaurant")
        restaurant_address = click.prompt("Enter the address of your restaurant")
        restaurant = get_or_create_restaurant(db, restaurant_name, restaurant_address)
        user.restaurant_id = restaurant.id
        db.commit()
        click.echo(f"Restaurant '{restaurant.name}' created successfully!")
    else:
        restaurant = db.query(Restaurant).filter(Restaurant.id == user.restaurant_id).first()
        click.echo(f"Welcome back to your restaurant: {restaurant.name}")

    try:
        while True:
            click.echo("\nMain Menu:")
            choice = click.prompt(
                "1. Manage Menu\n2. Manage Orders\n3. Manage Customers\n4. Exit",
                type=click.Choice(['1', '2', '3', '4'])
            )
            
            if choice == '1':
                manage_menu()
            elif choice == '2':
                manage_orders()
            elif choice == '3':
                manage_customers()
            elif choice == '4':
                click.echo("Thank you for using the Restaurant Management CLI. Goodbye!")
                break
    except sqlalchemy.orm.exc.DetachedInstanceError:
        click.echo("An error occurred. Please try logging in again.")

def manage_menu():
    while True:
        click.echo("\nMenu Management:")
        choice = click.prompt(
            "1. Add Menu Item\n2. List Menu Items\n3. Update Menu Item\n4. Delete Menu Item\n5. Back to Main Menu",
            type=click.Choice(['1', '2', '3', '4', '5'])
        )
        
        if choice == '1':
            add_menu_item()
        elif choice == '2':
            list_menu_items()
        elif choice == '3':
            update_menu_item()
        elif choice == '4':
            delete_menu_item()
        elif choice == '5':
            break

def manage_orders():
    while True:
        click.echo("\nOrder Management:")
        choice = click.prompt(
            "1. Create Order\n2. List Orders\n3. Delete Order\n4. Back to Main Menu",
            type=click.Choice(['1', '2', '3', '4'])
        )
        
        if choice == '1':
            create_order()
        elif choice == '2':
            list_orders()
        elif choice == '3':
            delete_order()
        elif choice == '4':
            break

def manage_customers():
    while True:
        click.echo("\nCustomer Management:")
        choice = click.prompt(
            "1. Add Customer\n2. List Customers\n3. Update Customer\n4. Delete Customer\n5. Back to Main Menu",
            type=click.Choice(['1', '2', '3', '4', '5'])
        )
        
        if choice == '1':
            add_customer()
        elif choice == '2':
            list_customers()
        elif choice == '3':
            update_customer()
        elif choice == '4':
            delete_customer()
        elif choice == '5':
            break

def guided_tour():
    click.echo("Welcome to the Restaurant Management CLI Guided Tour!")
    click.echo("This tour will walk you through the main features of our system.")
    
    db = next(get_db())
    restaurant = get_or_create_restaurant(db, "Tour Restaurant", "123 Tour Street")
    
    click.echo("\n1. Adding a menu item")
    click.echo("Let's add a sample menu item to our restaurant.")
    new_item = MenuItem(name="Tour Burger", description="A delicious burger for our tour", price=9.99, restaurant_id=restaurant.id)
    db.add(new_item)
    db.commit()
    click.echo(f"Added '{new_item.name}' to the menu.")
    
    click.echo("\n2. Listing menu items")
    click.echo("Now, let's see the list of menu items:")
    menu_items = db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant.id).all()
    for item in menu_items:
        click.echo(f"- {item.name}: ${item.price:.2f}")
    
    click.echo("\n3. Adding a customer")
    click.echo("Let's add a sample customer to our system.")
    new_customer = Customer(name="Tour Customer", password=generate_password_hash("tourpass"), restaurant_id=restaurant.id)
    db.add(new_customer)
    db.commit()
    click.echo(f"Added customer: {new_customer.name}")
    
    click.echo("\n4. Creating an order")
    click.echo("Now, let's create a sample order for our customer.")
    new_order = Order(customer_id=new_customer.id, restaurant_id=restaurant.id, total_price=new_item.price)
    new_order.items.append(new_item)
    db.add(new_order)
    db.commit()
    click.echo(f"Created order for {new_customer.name} with total price: ${new_order.total_price:.2f}")
    
    click.echo("\n5. Listing orders")
    click.echo("Let's see the list of orders:")
    orders = db.query(Order).filter(Order.restaurant_id == restaurant.id).all()
    for order in orders:
        click.echo(f"- Order ID: {order.id}, Customer: {order.customer.name}, Total: ${order.total_price:.2f}")
    
    click.echo("\nThis concludes our guided tour of the Restaurant Management CLI.")
    click.echo("Feel free to explore more features in the interactive CLI!")

@cli.command()
def interactive_tour():
    init_db()
    guided_tour()

if __name__ == '__main__':
    init_db()
    interactive_cli()