from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
import sessions

BASE = declarative_base()

class Product(BASE):
    __tablename__ = "Product"
    _id_ = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(32), nullable=False)
    product_manufacturer = Column(String(32), nullable=False)
    pruduct_measurement_type = Column(String(32), nullable=False)

class Customer(BASE):
    __tablename__ = "Customer"
    _id_ = Column(Integer, primary_key=True, autoincrement=True)
    customer_fullname = Column(String(60), nullable=False)
    customer_address = Column(String(100), nullable=False)
    customer_phone = Column(String(30), nullable = False)
    customer_contact_person = Column(String(40))

class Order(BASE):
    __tablename__ = "Order"
    _id_ = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey(Product._id_), nullable=False)
    customer_id = Column(Integer, ForeignKey(Customer._id_), nullable=False)
    order_count = Column(Integer, nullable=False)
    order_date = Column(DateTime)
    order_price = Column(Float) # на единицу измерения
