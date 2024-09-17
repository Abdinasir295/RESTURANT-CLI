import click
from sqlalchemy.orm import Session
from models import Restaurant
from database import get_db

def get_or_create_restaurant(db: Session, name: str, address: str) -> Restaurant:
    """Get an existing restaurant or create a new one if it doesn't exist"""
    restaurant = db.query(Restaurant).filter(Restaurant.name == name).first()
    if restaurant:
        return restaurant
    
    new_restaurant = Restaurant(name=name, address=address)
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return new_restaurant

def validate_price(ctx, param, value):
    """Validate that the price is a positive number"""
    if value < 0:
        raise click.BadParameter('Price must be a positive number.')
    return value

def format_currency(amount: float) -> str:
    """Format a float as currency"""
    return f"${amount:.2f}"

