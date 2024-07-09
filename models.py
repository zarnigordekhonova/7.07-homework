from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True)
    email = Column(String(64), unique=True, index=True)
    password = Column(Text)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    orders = relationship('Orders', back_populates='user')

    def __repr__(self):
        return f"<User(Id={self.id}, username={self.username}, email={self.email})>"

class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(32), unique=True, index=True)
    description = Column(Text)
    price = Column(Float)
    orders = relationship('Orders', back_populates='product')

    def __repr__(self):
        return f"<Product(Id={self.id}, name={self.name})>"

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
    quantity = Column(Integer, nullable=True)
    user = relationship('Users', back_populates='orders')
    product = relationship('Products', back_populates='orders')

    def __repr__(self):
        return f"<Order(Id={self.id}, user_id={self.user_id}, product_id={self.product_id}, status={self.status})>"
