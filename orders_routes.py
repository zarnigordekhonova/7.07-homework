from fastapi import APIRouter
from fastapi import FastAPI

app = FastAPI()


orders_router = APIRouter(
    prefix='/orders'
)


@orders_router.get('/orders_list')
async def get_orders():
    return {
        'message': 'This page shows your orders'
    }


@orders_router.get('/orders_number')
async def orders_number():
    return {
        'message': 'Number of your order is shown here.'
    }

