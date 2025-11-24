import uvicorn
from fastapi import FastAPI
import fastapi
from auto_app.db.database import SessionLocale
import redis.asyncio as redis
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from auto_app.api.endpoints import auth, users, feedback, car, bid, auction
from auto_app.admin.setup import setup_admin
from starlette.middleware.sessions import SessionMiddleware
from auto_app.config import SECRET_KEY



async def init_redis():
    return redis.from_url('redis://localhost', encoding='utf-8', decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await init_redis()
    await  FastAPILimiter.init(redis)
    yield
    await  redis.close()


async def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title='Подержанные автомобили из США')



app.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")

setup_admin(app)


app.include_router(auth.auth_router)
app.include_router(users.user_router)
app.include_router(car.cars_router)
app.include_router(feedback.feed_router)
app.include_router(bid.bids_router)
app.include_router(auction.auction_router)



if __name__ == "__main__":
    uvicorn.run(auto_app, host="127.0.0.1", port=8000)