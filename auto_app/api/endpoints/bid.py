from auto_app.db.models import Bid
from auto_app.db.schema import BidCreateSchema, BidOutSchema
from auto_app.db.database import SessionLocale
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from typing import Optional,List


bids_router = APIRouter(prefix='/bid', tags=['Bid'])


async def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()


@bids_router.post('/', response_model=dict)
async def bid_create(bid: BidCreateSchema, db: Session = Depends(get_db)):
    bids_db = Bid(**bid.dict())
    db.add(bids_db)
    db.commit()
    db.refresh(bids_db)
    return  {'massage':  'Saved'}


@bids_router.get('/', response_model=List[BidOutSchema])
async def bid_list(db: Session = Depends(get_db)):
    return db.query(Bid).all()


@bids_router.get('/{bid_id}', response_model=BidOutSchema)
async def bid_detail(bid_id: int, db: Session = Depends(get_db)):
    bid = db.query(Bid).filter(Bid.id == bid_id).first()


    if bid is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')
    return bid


@bids_router.put('/{bid_id}', response_model=dict)
async def bid_update(bid_id: int, bids_data: BidCreateSchema, db: Session = Depends(get_db)):
    bid_db = db.query(Bid).filter(Bid.id == bid_id).first()

    if bid_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')

    for bid_key, bid_values in bids_data.dict().items():
        setattr(bid_db, bid_key, bid_values)

    db.add(bid_db)
    db.commit()
    db.refresh(bid_db)
    return bid_db


@bids_router.delete('/{bid_id}', response_model=dict)
async def bid_delete(bid_id: int, db: Session = Depends(get_db)):
    bid_db = db.query(Bid).filter(Bid.id == bid_id).first()

    if bid_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')

    db.delete(bid_db)
    db.commit()
    return {"message": "This Tasks is deleted"}
