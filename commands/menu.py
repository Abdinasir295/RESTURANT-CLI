import click
from sqlalchemy.orm import Session
from database import get_db
from models import MenuItem, Restaurant

def add_menu_item():
    """Add a new menu item"""
    name = click.prompt('Menu item name')
    description = click.prompt('Description')
    price = click.prompt('Price', type=float)
    
    restaurant_id = click.prompt('Restaurant ID', type=int)
    db = next(get_db())
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        click.echo(f"Restaurant with ID {restaurant_id} not found.")
        return

    menu_item = MenuItem(name=name, description=description, price=price, restaurant_id=restaurant_id)
    db.add(menu_item)
    db.commit()
    click.echo(f"Menu item '{name}' added successfully.")

def list_menu_items():
    """List all menu items"""
    restaurant_id = click.prompt('Restaurant ID (optional)', type=int, default=None, show_default=False)
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

def update_menu_item():
    """Update a menu item"""
    id = click.prompt('Menu item ID', type=int)
    db = next(get_db())
    menu_item = db.query(MenuItem).filter(MenuItem.id == id).first()
    if not menu_item:
        click.echo(f"Menu item with ID {id} not found.")
        return

    name = click.prompt('New name (leave empty to keep current)', default='', show_default=False)
    description = click.prompt('New description (leave empty to keep current)', default='', show_default=False)
    price = click.prompt('New price (leave empty to keep current)', type=float, default=None, show_default=False)

    if name:
        menu_item.name = name
    if description:
        menu_item.description = description
    if price is not None:
        menu_item.price = price

    db.commit()
    click.echo(f"Menu item with ID {id} updated successfully.")

def delete_menu_item():
    """Delete a menu item"""
    id = click.prompt('Menu item ID', type=int)
    db = next(get_db())
    menu_item = db.query(MenuItem).filter(MenuItem.id == id).first()
    if not menu_item:
        click.echo(f"Menu item with ID {id} not found.")
        return

    db.delete(menu_item)
    db.commit()
    click.echo(f"Menu item with ID {id} deleted successfully.")
