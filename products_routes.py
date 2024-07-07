from fastapi import APIRouter

product_router = APIRouter(
    prefix='/products'
)

@product_router.get("/")
async def products_list():
    return {
        'message': 'Page for Products-details'
    }


@product_router.get("/products-section")
async def get_products():
    return {
        'message': "Welcome to Products section"
    }

