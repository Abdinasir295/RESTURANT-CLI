import click
from sqlalchemy.orm import Session
from database import get_db
from models import Order, MenuItem, Customer, Restaurant

@click.group(name='order')
def order_commands():
    """Manage orders"""
    pass

@order_commands.command(name='create')
@click.option('--customer-id', prompt='Customer ID', type=int, help='ID of the customer placing the order')
@click.option('--restaurant-id', prompt='Restaurant ID', type=int, help='ID of the restaurant')
@click.option('--items', prompt='Menu item IDs (comma-separated)', help='IDs of menu items in the order')
def create_order(customer_id, restaurant_id, items):
    """Create a new order"""
    db = next(get_db())
    
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        click.echo(f"Customer with ID {customer_id} not found.")
        return

    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        click.echo(f"Restaurant with ID {restaurant_id} not found.")
        return

    item_ids = [int(item.strip()) for item in items.split(',')]
    menu_items = db.query(MenuItem).filter(MenuItem.id.in_(item_ids)).all()
    
    if len(menu_items) != len(item_ids):
        click.echo("One or more menu items not found.")
        return

    total_price = sum(item.price for item in menu_items)
    
    order = Order(customer_id=customer_id, restaurant_id=restaurant_id, total_price=total_price)
    order.items.extend(menu_items)
    
    db.add(order)
    db.commit()
    
    click.echo(f"Order created successfully. Order ID: {order.id}, Total Price: ${total_price:.2f}")

@order_commands.command(name='list')
@click.option('--customer-id', type=int, help='ID of the customer to list orders for')
def list_orders(customer_id):
    """List all orders"""
    db = next(get_db())
    query = db.query(Order)
    if customer_id:
        query = query.filter(Order.customer_id == customer_id)
    
    orders = query.all()
    if not orders:
        click.echo("No orders found.")
        return

    for order in orders:
        click.echo(f"Order ID: {order.id}, Customer ID: {order.customer_id}, Restaurant ID: {order.restaurant_id}, Total Price: ${order.total_price:.2f}")
        for item in order.items:
            click.echo(f"  - {item.name}: ${item.price:.2f}")

@order_commands.command(name='delete')
@click.option('--id', prompt='Order ID', type=int, help='ID of the order to delete')
def delete_order(id):
    """Delete an order"""
    db = next(get_db())
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        click.echo(f"Order with ID {id} not found.")
        return

    db.delete(order)
    db.commit()
    click.echo(f"Order with ID {id} deleted successfully.")

