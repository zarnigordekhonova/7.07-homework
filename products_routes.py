from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from database import session, engine
from models import Products, Users
from fastapi_jwt_auth import AuthJWT
from schemas_auth import ProductsModel, ProductUpdateModel

session = session(bind=engine)
product_router = APIRouter(
    prefix='/products'
)

@product_router.get("/")
async def products_list():
    return {
        'message': 'Page for Products-details'
    }


@product_router.post("/add")
async def get_products(product: ProductsModel, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')

    new_product = Products(
        name=product.name, #models ga product name unique true yozilgan!
        price=product.price
    )
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    session.close()

    return new_product


@product_router.get("/list_products")
async def get_list(Authorize: AuthJWT=Depends()):
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
    else:
        product = session.query(Products).all()
        return product


@product_router.patch("/update/{id}")
async def update_product(id: int, update_product: ProductUpdateModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid token"
        )
    user_id = Authorize.get_jwt_subject()
    user = session.query(Users).filter(Users.username == user_id).first()
    product = session.query(Products).filter(Products.id == id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    if update_product.name is not None:
        product.name = update_product.name

    if update_product.price is not None:
        product.price = update_product.price

    if update_product.description is not None:
        product.description = update_product.description


    session.commit()
    session.refresh(product)

    return {
        "message": "Product updated successfully",
        "product": product
    }


@product_router.get("/{id}")
async def get_id_product(id: int, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid token"
        )

    user_id = Authorize.get_jwt_subject()
    user = session.query(Users).filter(Users.username == user_id).first()
    product = session.query(Products).filter(Products.id == id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@product_router.delete("/delete/{id}")
async def delete_product(id: int, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid token"
        )

    user_id = Authorize.get_jwt_subject()
    user = session.query(Users).filter(Users.username == user_id).first()
    product = session.query(Products).filter(Products.id == id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    session.delete(product)
    session.commit()

    return {"message": "Product deleted successfully!"}