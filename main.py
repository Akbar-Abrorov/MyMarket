from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import products, users, categories
from app.pg_db import database, metadata, engine

from app.admin.category import views as admin_category
from app.admin.product import views as admin_product
from app.admin.user import views as admin_user
from app.auth.views import router as admin_auth_router
from app.admin.files import views as admin_product_files

app = FastAPI(
    title="MyMarket API",
    docs_url="/api/docs",
    redoc_url="/api/redocs",
    version="2.0",
    description="API for MyMarket, a sample e-commerce application",
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()

app.router.lifespan_context = lifespan

app.include_router(categories.router)
app.include_router(products.router)


app.include_router(admin_auth_router)
app.include_router(admin_product_files.router)
app.include_router(admin_category.router)
app.include_router(admin_product.router)
app.include_router(admin_user.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
