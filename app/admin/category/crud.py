from sqlalchemy import select
from datetime import datetime
from typing import Optional

from app.pg_db import categories, database
from app.schemas import CategoryCreate, CategoryUpdate

async def get_all_categories():
    query = select(categories)
    result = await database.fetch_all(query)
    return [dict(row) for row in result]

async def get_category_by_id(category_id: int) -> Optional[dict]:
    query = select(categories).where(categories.c.id == category_id)
    result = await database.fetch_one(query)
    return dict(result) if result else None

async def create_category(data: CategoryCreate) -> dict:
    now = datetime.utcnow()
    query = categories.insert().values(
        name=data.name,
        description=data.description,
        parent_id=data.parent_id,
        created_at=now,
        updated_at=now
    )
    last_record_id = await database.execute(query)
    return await get_category_by_id(last_record_id)

async def update_category(category_id: int, data: CategoryUpdate) -> Optional[dict]:
    now = datetime.utcnow()
    update_values = {"updated_at": now}

    if data.name is not None:
        update_values["name"] = data.name
    if data.description is not None:
        update_values["description"] = data.description
    if data.parent_id is not None:
        update_values["parent_id"] = data.parent_id

    query = categories.update().where(categories.c.id == category_id).values(**update_values)
    await database.execute(query)
    return await get_category_by_id(category_id)

async def delete_category(category_id: int) -> bool:
    query = categories.delete().where(categories.c.id == category_id)
    result = await database.execute(query)
    return result > 0
