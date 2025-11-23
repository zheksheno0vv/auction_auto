from .database import  Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Enum, DateTime, ForeignKey, Text, DECIMAL
from typing import Optional,List
from datetime import datetime, date
from passlib.hash import bcrypt
from enum import Enum as PyEnum


class STATUS_Bye(str, PyEnum):
   salesman = 'продавец'
   buyer = 'покупатель'


class Status_Type(str, PyEnum):
   benzine = 'benzine'
   electro = 'electro'
   gaz = 'gaz'


class Status_Auto(str, PyEnum):
   manual = 'manual'
   auto = 'auto'



class Auction_Choices(str, PyEnum):
   active = 'active'
   completed = 'completed'
   complete = 'complete'


class UserProfile(Base):
   __tablename__ = 'users'

   id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
   username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
   email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
   password: Mapped[str] = mapped_column(String, nullable=False, unique=True)
   role: Mapped[STATUS_Bye] = mapped_column(Enum(STATUS_Bye), default=STATUS_Bye.buyer)
   phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
   car_user: Mapped[List['Car']] = relationship('Car', back_populates='seller',
                                                cascade='all, delete-orphan')
   feedback_seller: Mapped[List['Feedback']] = relationship('Feedback', back_populates='seller',
                                                            foreign_keys='Feedback.sellers_id',
                                                            cascade='all, delete-orphan')
   feedback_buyer: Mapped[List['Feedback']] = relationship('Feedback', back_populates='buyer',
                                                           foreign_keys='Feedback.buyers_id',
                                                           cascade='all, delete-orphan')
   tokens: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user',
                                                       cascade='all, delete-orphan')
   bid_buyer: Mapped[List['Bid']] = relationship('Bid', back_populates='buyer',
                                                 cascade='all, delete-orphan')


   def set_passwords(self, password: str):
      self.hashed_password = bcrypt.hash(password)


   def check_password(self, password: str):
      return bcrypt.verify(password, self.hashed_password)


class RefreshToken(Base):
   __tablename__ = 'refresh_token'

   id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
   token: Mapped[str] = mapped_column(String, unique=True, nullable=False)
   created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
   user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
   user: Mapped['UserProfile'] = relationship('UserProfile', back_populates="tokens")



class Car(Base):
   __tablename__ = 'cars'


   id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
   brand: Mapped[str] = mapped_column(String(32))
   model: Mapped[str] = mapped_column(String(32))
   year: Mapped[date]
   fuel_type: Mapped[Status_Type] = mapped_column(Enum(Status_Type), default=Status_Type.benzine)
   transmission: Mapped[Status_Auto] = mapped_column(Enum(Status_Auto), default=Status_Auto.auto)
   mileage: Mapped[int] = mapped_column(Integer)
   price: Mapped[float] = mapped_column(DECIMAL(10, 2))
   description: Mapped[str] = mapped_column(Text)
   images: Mapped[str] = mapped_column(String)
   seller_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
   seller: Mapped['UserProfile'] = relationship('UserProfile', back_populates='car_user')
   auction: Mapped[List['Auction']] = relationship('Auction', back_populates='car',
                                                   cascade='all, delete-orphan')


class Auction(Base):
   __tablename__ = 'auctions'


   id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
   car_id: Mapped[int] = mapped_column(ForeignKey('cars.id'))
   car: Mapped['Car'] = relationship('Car', back_populates='auction')
   start_price: Mapped[int] = mapped_column(Integer, default=0)
   min_price: Mapped[int] = mapped_column(Integer)
   start_time: Mapped[datetime] = mapped_column(DateTime)
   end_time: Mapped[datetime] = mapped_column(DateTime)
   status: Mapped[Auction_Choices] = mapped_column(Enum(Auction_Choices), default=Auction_Choices.active)
   bid_auction: Mapped[List["Bid"]] = relationship('Bid', back_populates='auction',
                                                   cascade='all,delete-orphan')


class Bid(Base):
   __tablename__ = 'bids'


   id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
   auction_id: Mapped[int] = mapped_column(ForeignKey('auctions.id'))
   auction: Mapped['Auction'] = relationship('Auction', back_populates='bid_auction')
   buyer_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
   buyer: Mapped['UserProfile'] = relationship('UserProfile', back_populates='bid_buyer')
   amount: Mapped[int] = mapped_column(Integer)
   created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())


class Feedback(Base):
   __tablename__ = 'feedback'

   id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
   sellers_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
   seller: Mapped['UserProfile'] = relationship('UserProfile', back_populates='feedback_seller',
                                                foreign_keys=[sellers_id])
   buyers_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
   buyer: Mapped['UserProfile'] = relationship('UserProfile', back_populates='feedback_buyer',
                                               foreign_keys=[buyers_id])
   rating: Mapped[int] = mapped_column(Integer)
   comment: Mapped[str] = mapped_column(Text)

