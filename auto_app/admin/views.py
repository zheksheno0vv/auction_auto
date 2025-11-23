from sqladmin import   ModelView
from auto_app.db.models import UserProfile, Car, Auction, Bid, Feedback


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username, UserProfile.role]
    name = 'User'
    name_plural = 'Users'



class CarAdmin(ModelView, model=Car):
    column_list = [Car.id, Car.model]
    name = 'Car'
    name_plural = 'Cars'



class AuctionAdmin(ModelView, model=Auction):
    column_list = [Auction.id]


class BidAdmin(ModelView, model=Bid):
    column_list = [Bid.id, Bid.amount]


class FeedbackAdmin(ModelView, model=Feedback):
    column_list = [Feedback.id, Feedback.comment]