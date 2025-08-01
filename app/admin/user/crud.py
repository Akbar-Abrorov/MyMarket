from app.pg_db import database, users

async def get_users():
    query = users.select()
    return await database.fetch_all(query)

async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {"detail": "User deleted"}