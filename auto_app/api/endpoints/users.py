from auto_app.db.models import UserProfile
from auto_app.db.schema import UserCreateSchema, UserOutSchema, UserUpdateSchema
from auto_app.db.database import SessionLocale
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from typing import Optional,List


user_router = APIRouter(prefix='/user', tags=['User'])


async def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()


# @user_router.post('/', response_model=dict)
# async def user_create(user: UserCreateSchema, db: Session = Depends(get_db)):
#     user_db = UserProfile(**user.dict())
#     db.add(user_db)
#     db.commit()
#     db.refresh(user_db)
#     return {'massage':  'Saved'}


@user_router.get('/', response_model=List[UserOutSchema])
async def user_list(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()


@user_router.get('/{user_id}', response_model=UserOutSchema)
async def user_detail(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()


    if user is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')
    return user


@user_router.put('/{user_id}', response_model=dict)
async def user_update(user_id: int, user_data: UserUpdateSchema,  db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()

    if user_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')

    for user_key, user_values in user_data.dict().items():
        setattr(user_db, user_key, user_values)




    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return {'massage': 'Updated'}


@user_router.delete('/{user_id}', response_model=dict)
async def user_delete(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()

    if user_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')

    db.delete(user_db)
    db.commit()
    return {"message": "This Users is deleted"}


