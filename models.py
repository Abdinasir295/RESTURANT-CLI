from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Association table for many-to-many relationship between Order and MenuItem
order_items = Table('order_items', Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('menu_item_id', Integer, ForeignKey('menu_items.id'))
)

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)

    menu_items = relationship("MenuItem", back_populates="restaurant")
    orders = relationship("Order", back_populates="restaurant")
    customers = relationship("Customer", back_populates="restaurant")

class MenuItem(Base):
    __tablename__ = 'menu_items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))

    restaurant = relationship("Restaurant", back_populates="menu_items")
    orders = relationship("Order", secondary=order_items, back_populates="items")

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    total_price = Column(Float, nullable=False)

    restaurant = relationship("Restaurant", back_populates="orders")
    customer = relationship("Customer", back_populates="orders")
    items = relationship("MenuItem", secondary=order_items, back_populates="orders")

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))

    orders = relationship("Order", back_populates="customer")
    restaurant = relationship("Restaurant", back_populates="customers")
