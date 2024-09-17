import click
from sqlalchemy.orm import Session
from database import get_db
from models import MenuItem, Restaurant

@click.group(name='menu')
def menu_commands():
    """Manage menu items"""
    pass

@menu_commands.command(name='add')
@click.option('--name', prompt='Menu item name', help='Name of the menu item')
@click.option('--description', prompt='Description', help='Description of the menu item')
@click.option('--price', prompt='Price', type=float, help='Price of the menu item')
@click.option('--restaurant-id', prompt='Restaurant ID', type=int, help='ID of the restaurant')
def add_menu_item(name, description, price, restaurant_id):
    """Add a new menu item"""
    db = next(get_db())
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        click.echo(f"Restaurant with ID {restaurant_id} not found.")
        return

    menu_item = MenuItem(name=name, description=description, price=price, restaurant_id=restaurant_id)
    db.add(menu_item)
    db.commit()
    click.echo(f"Menu item '{name}' added successfully.")

@menu_commands.command(name='list')
@click.option('--restaurant-id', type=int, help='ID of the restaurant to list menu items for')
def list_menu_items(restaurant_id):
    """List all menu items"""
    db = next(get_db())
    query = db.query(MenuItem)
    if restaurant_id:
        query = query.filter(MenuItem.restaurant_id == restaurant_id)
    
    menu_items = query.all()
    if not menu_items:
        click.echo("No menu items found.")
        return

    for item in menu_items:
        click.echo(f"ID: {item.id}, Name: {item.name}, Price: ${item.price:.2f}, Restaurant ID: {item.restaurant_id}")

@menu_commands.command(name='update')
@click.option('--id', prompt='Menu item ID', type=int, help='ID of the menu item to update')
@click.option('--name', help='New name of the menu item')
@click.option('--description', help='New description of the menu item')
@click.option('--price', type=float, help='New price of the menu item')
def update_menu_item(id, name, description, price):
    """Update a menu item"""
    db = next(get_db())
    menu_item = db.query(MenuItem).filter(MenuItem.id == id).first()
    if not menu_item:
        click.echo(f"Menu item with ID {id} not found.")
        return

    if name:
        menu_item.name = name
    if description:
        menu_item.description = description
    if price:
        menu_item.price = price

    db.commit()
    click.echo(f"Menu item with ID {id} updated successfully.")

@menu_commands.command(name='delete')
@click.option('--id', prompt='Menu item ID', type=int, help='ID of the menu item to delete')
def delete_menu_item(id):
    """Delete a menu item"""
    db = next(get_db())
    menu_item = db.query(MenuItem).filter(MenuItem.id == id).first()
    if not menu_item:
        click.echo(f"Menu item with ID {id} not found.")
        return

    db.delete(menu_item)
    db.commit()
    click.echo(f"Menu item with ID {id} deleted successfully.")

