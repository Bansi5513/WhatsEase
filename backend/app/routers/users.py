# backend/app/routers/users.py
from fastapi import APIRouter, HTTPException
from ..database import users_col
from ..models import UserCreate
from ..auth import hash_password, create_access_token, verify_password
from fastapi import Body

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register")
async def register(user: UserCreate):
    existing = await users_col.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    user_doc = {
        "email": user.email,
        "full_name": user.full_name,
        "hashed_password": hash_password(user.password),
    }
    await users_col.insert_one(user_doc)
    return {"msg":"registered"}

@router.post("/login")
async def login(data=Body(...)):
    # data should have { "email": "...", "password": "..." }
    email = data.get("email")
    password = data.get("password")
    user = await users_col.find_one({"email": email})
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": email})
    return {"access_token": token}
