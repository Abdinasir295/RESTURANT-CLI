import click
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from database import init_db
from commands import menu_commands, order_commands, customer_commands
from config import DATABASE_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)

@click.group()
def cli():
    """Restaurant Management CLI"""
    pass

# Register command groups
cli.add_command(menu_commands)
cli.add_command(order_commands)
cli.add_command(customer_commands)

@cli.command()
def init():
    """Initialize the database"""
    with app.app_context():
        init_db()
    click.echo("Database initialized successfully.")

@cli.command()
def test_db():
    """Test database connection"""
    try:
        with app.app_context():
            db.session.execute(text("SELECT 1"))
        click.echo("Database connection successful!")
    except Exception as e:
        click.echo(f"Database connection failed: {str(e)}")

if __name__ == '__main__':
    cli()
