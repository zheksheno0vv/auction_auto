from auto_app.db.models import Auction
from auto_app.db.schema import AuctionCreateSchema, AuctionOutSchema, AuctionUpdateSchema
from auto_app.db.database import SessionLocale
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from typing import Optional,List


auction_router = APIRouter(prefix='/auction', tags=['Auction'])


async def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()


@auction_router.post('/', response_model=dict)
async def auction_create(task: AuctionCreateSchema, db: Session = Depends(get_db)):
    auction_db = Auction(**task.dict())
    db.add(auction_db)
    db.commit()
    db.refresh(auction_db)
    return  {'massage':  'Saved'}


@auction_router.get('/', response_model=List[AuctionOutSchema])
async def auction_list(db: Session = Depends(get_db)):
    return db.query(Auction).all()


@auction_router.get('/{auction_id}', response_model=AuctionOutSchema)
async def auction_detail(auction_id: int, db: Session = Depends(get_db)):
    auction = db.query(Auction).filter(Auction.id == auction_id).first()


    if auction is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')
    return auction


@auction_router.put('/{auction_id}', response_model=dict)
async def car_update(auction_id: int, auction_data: AuctionUpdateSchema, db: Session = Depends(get_db)):
    auction_db = db.query(Auction).filter(Auction.id == auction_id).first()

    if auction_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')

    for auctions_key, auctions_values in auction_data.dict().items():
        setattr(auction_db, auctions_key, auctions_values)

    db.add(auction_db)
    db.commit()
    db.refresh(auction_db)
    return auction_db


@auction_router.delete('/{auction_id}', response_model=dict)
async def auction_delete(auction_id: int, db: Session = Depends(get_db)):
    auction_db = db.query(Auction).filter(Auction.id == auction_id).first()

    if auction_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')

    db.delete(auction_db)
    db.commit()
    return {"message": "This Tasks is deleted"}
