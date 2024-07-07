from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True)
    email = Column(String(64), unique=True, index=True)
    password = Column(Text)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    order = relationship('Orders', back_populates='users')

    def __repr__(self):
        return f"<Id = {self.id} - username = {self.username} - email = {self.email}>"


class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(32), unique=True, index=True)
    description = Column(Text)
    price = Column(Float)
    order = relationship('Orders', back_populates='products')


    def __repr__(self):
        return f"<Id = {self.id} - name = {self.name}>"


class Orders(Base):
    ORDER_STATUS = (
        ('PENDING', 'pending'),
        ('IN_TRANSIT', 'in_transit'),
        ('DELIVERED', 'delivered')
    )

    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    status = Column(ChoiceType(ORDER_STATUS), default='PENDING')
    quantity = Column(Integer)
    user = relationship('Users', back_populates='orders')
    product = relationship('Products', back_populates='orders')

    def __repr__(self):
        return f"<Id = {self.id} - user = {self.product_id} - product = {self.product} - status = {self.status}>"




