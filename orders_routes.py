from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi import FastAPI
from database import session, engine
from schemas_auth import OrdersModel, OrdersUpdateModel
from models import Orders, Users
from fastapi_jwt_auth import AuthJWT

app = FastAPI()
import logging

orders_router = APIRouter(
    prefix='/orders'
)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

session = session(bind=engine)


@orders_router.get('/')
async def get_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
    return {'message': "This page shows your orders"}


@orders_router.post("/create", response_model=OrdersModel)
async def product_order(order: OrdersModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        logger.error(f"Authorization error: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    current_user = Authorize.get_jwt_subject()
    user = session.query(Users).filter(Users.username == current_user).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    new_order = Orders(
        quantity=order.quantity,
        product_id=order.product_id,
        user_id=order.user_id
    )

    new_order.user_id = user.id
    session.add(new_order)
    session.commit()

    response_data = {
        'id': new_order.id,
        "product_id": new_order.product_id,
        "user_id": new_order.user_id,
        "quantity": new_order.quantity,
        "status": new_order.status
    }

    return jsonable_encoder(response_data)


@orders_router.get('/orders_list')
async def get_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid token"
        )

    user_id = Authorize.get_jwt_subject()
    user = session.query(Users).filter(Users.username == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.is_staff:
        orders = session.query(Orders).all()
    else:
        orders = session.query(Orders).filter(Orders.user_id == user.id).all()
        return orders
    return orders


@orders_router.get('/{id}')
async def get_order_id(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    current_user = Authorize.get_jwt_subject()
    user = session.query(Users).filter(Users.username == current_user).first()
    order = session.query(Orders).filter(Orders.id == id).first()

    if not user.id == order.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@orders_router.patch("/orders_update/{id}")
async def orders_update(id: int, orders_update: OrdersUpdateModel, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    current_user = Authorize.get_jwt_subject()
    user = session.query(Users).filter(Users.username == current_user).first()
    order = session.query(Orders).filter(Orders.id == id).first()

    if not user.id == order.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    if orders_update.product_id is not None:
        order.product_id = orders_update.product_id

    if orders_update.quantity is not None:
        order.quantity = orders_update.quantity

    if orders_update.status is not None:
        order.status = orders_update.status

    session.commit()
    session.refresh(order)

    return {
        "message": "Order updated successfully",
        "order": order
    }


@orders_router.delete('/delete/{id}')
async def delete_order(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    current_user = Authorize.get_jwt_subject()
    user = session.query(Users).filter(Users.username == current_user).first()
    order = session.query(Orders).filter(Orders.id == id).first()

    if not user.id == order.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    session.delete(order)
    session.commit()

    return {"order": "Order deleted successfully!"}
