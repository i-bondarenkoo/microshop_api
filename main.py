from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from database import engine, Base
import models
from routers.customer import router as customer_router
from routers.product import router as product_router
from routers.order import router as order_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(customer_router)
app.include_router(product_router)
app.include_router(order_router)


@app.get("/")
def hello():
    return {"message": "Привет это мой первый FastAPI сервер!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
