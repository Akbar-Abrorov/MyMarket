from sqlalchemy import select
from datetime import datetime
from typing import Optional

from app.pg_db import products, database
from app.schemas import ProductCreate, ProductUpdate

async def get_all_products():
    query = select(products)
    result = await database.fetch_all(query)
    return [dict(row) for row in result]

async def get_product_by_id(product_id: int) -> Optional[dict]:
    query = select(products).where(products.c.id == product_id)
    result = await database.fetch_one(query)
    return dict(result) if result else None

async def create_product(data: ProductCreate) -> dict:
    now = datetime.utcnow()
    query = products.insert().values(
        name=data.name,
        description=data.description,
        price=data.price,
        image_url=data.image_url,
        quantity=data.quantity,
        is_active=data.is_active,
        category_id=data.category_id,
        created_at=now,
        updated_at=now,
        created_by=data.created_by,
        updated_by=data.updated_by
    )
    last_record_id = await database.execute(query)
    return await get_product_by_id(last_record_id)

async def update_product(product_id: int, data: ProductUpdate) -> Optional[dict]:
    now = datetime.utcnow()
    update_values = {"updated_at": now}

    if data.name is not None:
        update_values["name"] = data.name
    if data.description is not None:
        update_values["description"] = data.description
    if data.price is not None:
        update_values["price"] = data.price
    if data.image_url is not None:
        update_values["image_url"] = data.image_url
    if data.quantity is not None:
        update_values["quantity"] = data.quantity
    if data.is_active is not None:
        update_values["is_active"] = data.is_active
    if data.category_id is not None:
        update_values["category_id"] = data.category_id
    if data.updated_by is not None:
        update_values["updated_by"] = data.updated_by

    query = products.update().where(products.c.id == product_id).values(**update_values)
    await database.execute(query)
    return await get_product_by_id(product_id)

async def delete_product(product_id: int) -> bool:
    query = products.delete().where(products.c.id == product_id)
    result = await database.execute(query)
    return result > 0