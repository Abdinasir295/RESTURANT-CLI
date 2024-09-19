import click
from sqlalchemy.orm import Session
from database import get_db
from models import Customer
from werkzeug.security import generate_password_hash, check_password_hash

def add_customer():
    name = click.prompt('Customer name')
    password = click.prompt('Password', hide_input=True, confirmation_prompt=True)
    restaurant_id = click.prompt('Restaurant ID', type=int)
    
    db = next(get_db())
    existing_customer = db.query(Customer).filter(Customer.name == name).first()
    if existing_customer:
        click.echo(f"Customer with name '{name}' already exists.")
        return
    
    new_customer = Customer(name=name, password=generate_password_hash(password), restaurant_id=restaurant_id)
    db.add(new_customer)
    db.commit()
    click.echo(f"Customer '{name}' added successfully.")

def list_customers():
    restaurant_id = click.prompt('Restaurant ID', type=int)
    db = next(get_db())
    customers = db.query(Customer).filter(Customer.restaurant_id == restaurant_id).all()
    if not customers:
        click.echo("No customers found for this restaurant.")
        return
    
    for customer in customers:
        click.echo(f"ID: {customer.id}, Name: {customer.name}")

def update_customer():
    customer_id = click.prompt('Customer ID', type=int)
    db = next(get_db())
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        click.echo(f"Customer with ID {customer_id} not found.")
        return
    
    name = click.prompt('New name (leave empty to keep current)', default='', show_default=False)
    password = click.prompt('New password (leave empty to keep current)', hide_input=True, default='', show_default=False)
    
    if name:
        customer.name = name
    if password:
        customer.password = generate_password_hash(password)
    
    db.commit()
    click.echo(f"Customer with ID {customer_id} updated successfully.")

def delete_customer():
    customer_id = click.prompt('Customer ID', type=int)
    db = next(get_db())
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        click.echo(f"Customer with ID {customer_id} not found.")
        return
    
    db.delete(customer)
    db.commit()
    click.echo(f"Customer with ID {customer_id} deleted successfully.")
