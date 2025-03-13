from fastapi import FastAPI
from .database import SessionLocal, User
from .models import UserBase

app = FastAPI()

@app.post("/users/")
def create_user(user: UserBase):
    db = SessionLocal()
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}")
def read_user(user_id: int):
    db = SessionLocal()
    db_user = db.query(User).get(user_id)
    if db_user is None:
        return {"error": "User not found"}
    return db_user

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserBase):
    db = SessionLocal()
    db_user = db.query(User).get(user_id)
    if db_user is None:
        return {"error": "User not found"}
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()
    db_user = db.query(User).get(user_id)
    if db_user is None:
        return {"error": "User not found"}
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}