from auto_app.db.models import Feedback
from auto_app.db.schema import FeedbackSchema, CarOutSchema, CarUpdateSchema
from auto_app.db.database import SessionLocale
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from typing import Optional,List


feed_router = APIRouter(prefix='/feed', tags=['Feedback'])


async def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()


@feed_router.post('/', response_model=dict)
async def feed_create(feed: FeedbackSchema, db: Session = Depends(get_db)):
    feeds_db = Feedback(**feed.dict())
    db.add(feeds_db)
    db.commit()
    db.refresh(feeds_db)
    return  {'massage':  'Saved'}


@feed_router.get('/', response_model=List[CarOutSchema])
async def feed_list(db: Session = Depends(get_db)):
    return db.query(Feedback).all()


@feed_router.get('/{feeds_id}', response_model=FeedbackSchema)
async def feed_detail(feeds_id: int, db: Session = Depends(get_db)):
    feeds = db.query(Feedback).filter(Feedback.id == feeds_id).first()


    if feeds is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')
    return feeds


@feed_router.put('/{feed_id}', response_model=FeedbackSchema)
async def feed_update(feed_id: int, feeds_data: FeedbackSchema, db: Session = Depends(get_db)):
    feed_db = db.query(Feedback).filter(Feedback.id == feed_id).first()

    if feed_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')

    for feeds_key, feeds_values in feeds_data.dict().items():
        setattr(feed_db, feeds_key, feeds_values)

    db.add(feed_db)
    db.commit()
    db.refresh(feed_db)
    return feed_db


@feed_router.delete('/{feed_id}', response_model=dict)
async def feed_delete(feed_id: int, db: Session = Depends(get_db)):
    feed_db = db.query(Feedback).filter(Feedback.id == feed_id).first()

    if feed_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')

    db.delete(feed_db)
    db.commit()
    return {"message": "This Tasks is deleted"}
