import click
from sqlalchemy.orm import Session
from database import get_db
from models import Customer

@click.group(name='customer')
def customer_commands():
    """Manage customers"""
    pass

@customer_commands.command(name='add')
@click.option('--name', prompt='Customer name', help='Name of the customer')
@click.option('--email', prompt='Email', help='Email of the customer')
@click.option('--phone', prompt='Phone', help='Phone number of the customer')
def add_customer(name, email, phone):
    """Add a new customer"""
    db = next(get_db())
    customer = Customer(name=name, email=email, phone=phone)
    db.add(customer)
    db.commit()
    click.echo(f"Customer '{name}' added successfully.")

@customer_commands.command(name='list')
def list_customers():
    """List all customers"""
    db = next(get_db())
    customers = db.query(Customer).all()
    if not customers:
        click.echo("No customers found.")
        return

    for customer in customers:
        click.echo(f"ID: {customer.id}, Name: {customer.name}, Email: {customer.email}, Phone: {customer.phone}")

@customer_commands.command(name='update')
@click.option('--id', prompt='Customer ID', type=int, help='ID of the customer to update')
@click.option('--name', help='New name of the customer')
@click.option('--email', help='New email of the customer')
@click.option('--phone', help='New phone number of the customer')
def update_customer(id, name, email, phone):
    """Update a customer"""
    db = next(get_db())
    customer = db.query(Customer).filter(Customer.id == id).first()
    if not customer:
        click.echo(f"Customer with ID {id} not found.")
        return

    if name:
        customer.name = name
    if email:
        customer.email = email
    if phone:
        customer.phone = phone

    db.commit()
    click.echo(f"Customer with ID {id} updated successfully.")

@customer_commands.command(name='delete')
@click.option('--id', prompt='Customer ID', type=int, help='ID of the customer to delete')
def delete_customer(id):
    """Delete a customer"""
    db = next(get_db())
    customer = db.query(Customer).filter(Customer.id == id).first()
    if not customer:
        click.echo(f"Customer with ID {id} not found.")
        return

    db.delete(customer)
    db.commit()
    click.echo(f"Customer with ID {id} deleted successfully.")

