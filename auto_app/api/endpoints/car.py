from auto_app.db.models import Car
from auto_app.db.schema import CarCreateSchema, CarOutSchema, CarUpdateSchema
from auto_app.db.database import SessionLocale
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from typing import Optional,List


cars_router = APIRouter(prefix='/car', tags=['Car'])


async def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()


@cars_router.post('/', response_model=dict)
async def cars_create(task: CarCreateSchema, db: Session = Depends(get_db)):
    cars_db = Car(**task.dict())
    db.add(cars_db)
    db.commit()
    db.refresh(cars_db)
    return  {'massage':  'Saved'}


@cars_router.get('/', response_model=List[CarOutSchema])
async def car_list(db: Session = Depends(get_db)):
    return db.query(Car).all()


@cars_router.get('/{cars_id}', response_model=CarOutSchema)
async def car_detail(cars_id: int, db: Session = Depends(get_db)):
    cars = db.query(Car).filter(Car.id == cars_id).first()


    if cars is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')
    return cars


@cars_router.put('/{car_id}', response_model=CarUpdateSchema)
async def car_update(car_id: int, cars_data: CarUpdateSchema, db: Session = Depends(get_db)):
    car_db = db.query(Car).filter(Car.id == car_id).first()

    if car_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')

    for car_key, car_values in cars_data.dict().items():
        setattr(car_db, car_key, car_values)

    db.add(car_db)
    db.commit()
    db.refresh(car_db)
    return car_db


@cars_router.delete('/{car_id}', response_model=dict)
async def car_delete(car_id: int, db: Session = Depends(get_db)):
    car_db = db.query(Car).filter(Car.id == car_id).first()

    if car_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')

    db.delete(car_db)
    db.commit()
    return {"message": "This Tasks is deleted"}
