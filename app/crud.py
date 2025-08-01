from sqlalchemy import select
from datetime import datetime
from typing import Optional, List

from app.pg_db import products, users, categories, database
from app.schemas import ProductCreate, ProductUpdate, UserCreate, UserUpdate, CategoryCreate, CategoryUpdate


async def get_all_products():
    try:
        query = select(products)
        result = await database.fetch_all(query)
        return [dict(row) for row in result]
    except Exception as e:
        print(f"Error getting all products: {e}")
        return []


async def get_product_by_id(product_id: int):

    try:
        query = select(products).where(products.c.id == product_id)
        result = await database.fetch_one(query)
        return dict(result) if result else None
    except Exception as e:
        print(f"Error getting product {product_id}: {e}")
        return None


async def create_product(data: ProductCreate):

    try:
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


        return {
            "id": last_record_id,
            "name": data.name,
            "description": data.description,
            "price": data.price,
            "image_url": data.image_url,
            "quantity": data.quantity,
            "is_active": data.is_active,
            "category_id": data.category_id,
            "created_at": now,
            "updated_at": now,
            "created_by": data.created_by,
            "updated_by": data.updated_by
        }
    except Exception as e:
        print(f"Error creating product: {e}")
        raise


async def update_product(product_id: int, data: ProductUpdate) -> Optional[dict]:

    try:
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
    except Exception as e:
        print(f"Error updating product {product_id}: {e}")
        return None


async def delete_product(product_id: int) -> bool:

    try:
        query = products.delete().where(products.c.id == product_id)
        result = await database.execute(query)
        return result > 0
    except Exception as e:
        print(f"Error deleting product {product_id}: {e}")
        return False

async def get_all_users() -> List[dict]:
    try:
        query = select(users)
        result = await database.fetch_all(query)
        return [dict(row) for row in result]
    except Exception as e:
        print(f"Error getting all users: {e}")
        return []


async def get_user_by_id(user_id: int) -> Optional[dict]:
    try:
        query = select(users).where(users.c.id == user_id)
        result = await database.fetch_one(query)
        return dict(result) if result else None
    except Exception as e:
        print(f"Error getting user {user_id}: {e}")
        return None


async def create_user(data: UserCreate) -> dict:
    try:
        now = datetime.utcnow()
        query = users.insert().values(
            username=data.username,
            password=data.password,
            role_id=data.role_id,
            created_at=now,
            updated_at=now,
            created_by=data.created_by,
            updated_by=data.updated_by
        )
        last_record_id = await database.execute(query)


        return {
            "id": last_record_id,
            "username": data.username,
            "password": data.password,
            "role_id": data.role_id,
            "created_at": now,
            "updated_at": now,
            "created_by": data.created_by,
            "updated_by": data.updated_by
        }
    except Exception as e:
        print(f"Error creating user: {e}")
        raise


async def update_user(user_id: int, data: UserUpdate) -> Optional[dict]:

    try:
        now = datetime.utcnow()


        update_values = {"updated_at": now}

        if data.username is not None:
            update_values["username"] = data.username
        if data.password is not None:
            update_values["password"] = data.password
        if data.role_id is not None:
            update_values["role_id"] = data.role_id
        if data.updated_by is not None:
            update_values["updated_by"] = data.updated_by

        query = users.update().where(users.c.id == user_id).values(**update_values)
        await database.execute(query)
        return await get_user_by_id(user_id)
    except Exception as e:
        print(f"Error updating user {user_id}: {e}")
        return None


async def delete_user(user_id: int) -> bool:
    try:
        query = users.delete().where(users.c.id == user_id)
        result = await database.execute(query)
        return result > 0
    except Exception as e:
        print(f"Error deleting user {user_id}: {e}")
        return False



async def get_all_categories() -> List[dict]:
    try:
        query = select(categories)
        result = await database.fetch_all(query)
        return [dict(row) for row in result]
    except Exception as e:
        print(f"Error getting all categories: {e}")
        return []


async def get_category_by_id(category_id: int) -> Optional[dict]:
    try:
        query = select(categories).where(categories.c.id == category_id)
        result = await database.fetch_one(query)
        return dict(result) if result else None
    except Exception as e:
        print(f"Error getting category {category_id}: {e}")
        return None


async def create_category(data: CategoryCreate) -> dict:
    try:
        now = datetime.utcnow()
        query = categories.insert().values(
            name=data.name,
            description=data.description,
            created_at=now,
            updated_at=now
        )
        last_record_id = await database.execute(query)

        return {
            "id": last_record_id,
            "name": data.name,
            "description": data.description,
            "created_at": now,
            "updated_at": now
        }
    except Exception as e:
        print(f"Error creating category: {e}")
        raise


async def update_category(category_id: int, data: CategoryUpdate) -> Optional[dict]:
    try:
        now = datetime.utcnow()

        update_values = {"updated_at": now}

        if data.name is not None:
            update_values["name"] = data.name
        if data.description is not None:
            update_values["description"] = data.description

        query = categories.update().where(categories.c.id == category_id).values(**update_values)
        await database.execute(query)

        return await get_category_by_id(category_id)
    except Exception as e:
        print(f"Error updating category {category_id}: {e}")
        return None


async def delete_category(category_id: int) -> bool:
    try:
        query = categories.delete().where(categories.c.id == category_id)
        result = await database.execute(query)
        return result > 0  # Returns True if a row was deleted
    except Exception as e:
        print(f"Error deleting category {category_id}: {e}")
        return False



