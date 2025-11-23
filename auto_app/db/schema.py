from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from auto_app.db.models import STATUS_Bye, Status_Type, Status_Auto, Auction_Choices




class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone_number: str
    role: STATUS_Bye


    class Config:
        from_attributes = True


class UserUpdateSchema(BaseModel):
    username: str
    email: EmailStr
    role:STATUS_Bye


    class Config:
        from_attributes = True


class UserOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True



class CarCreateSchema(BaseModel):
    brand: str
    model: str
    year: date
    fuel_type: Status_Type
    transmission: Status_Auto
    mileage: int
    price: float
    description: str
    images: str
    seller_id: int

    class Config:
        from_attributes = True


class CarUpdateSchema(BaseModel):
    transmission: Status_Auto
    price: float
    description: str
    images: str
    seller_id: int

    class Config:
        from_attributes = True


class CarOutSchema(BaseModel):
    id: int
    brand: str
    model: str
    year: date
    fuel_type: Status_Type
    transmission: Status_Auto
    mileage: int
    price: float
    description: str
    images: str
    seller_id: int


    class Config:
        from_attributes = True


class AuctionCreateSchema(BaseModel):
    car_id: int
    start_price: int
    min_price: int
    start_time: datetime
    end_time: datetime
    status: Auction_Choices



    class Config:
        from_attributes = True


class AuctionUpdateSchema(BaseModel):
    start_price: int
    min_price: int
    start_time: datetime
    end_time: datetime
    status: Auction_Choices


    class Config:
        from_attributes = True


class AuctionOutSchema(BaseModel):
    id:int
    car_id: int
    start_price: int
    min_price: int
    start_time: datetime
    end_time: datetime
    status: Auction_Choices

    class Config:
        from_attributes = True


class BidCreateSchema(BaseModel):
    auction_id: int
    buyer_id: int
    amount: int


    class Config:
        from_attributes = True


class BidOutSchema(BaseModel):
    id: int
    auction_id: int
    buyer_id: int
    amount: int
    created_at: datetime


    class Config:
        from_attributes = True


class FeedbackSchema(BaseModel):
    id: int
    sellers_id: int
    buyers_id: int
    rating: int
    comment: str


    class Config:
        from_attributes = True