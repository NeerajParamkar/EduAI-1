from fastapi import APIRouter, HTTPException, Depends
from app.db.database import users_collection
from app.models.user_model import SignupUser, LoginUser
from app.core.security import create_access_token
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ------------------- SIGNUP -------------------

@router.post("/signup")
def signup(user: SignupUser):
    # Check if user already exists
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User already exists")

    # ✅ Add this line here
    if len(user.password.encode('utf-8')) > 72:
        raise HTTPException(status_code=400, detail="Password too long (max 72 characters allowed)")

    # ✅ Check confirm password
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Hash the password
    hashed_password = pwd_context.hash(user.password)

    # Insert into MongoDB
    users_collection.insert_one({
        "email": user.email,
        "password": hashed_password
    })

    return {"message": "User created successfully"}
# ------------------- LOGIN -------------------
@router.post("/login")
def login(user: LoginUser):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user or not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user["email"]})
    return {"access_token": token, "token_type": "bearer"}

# ------------------- TEST ROUTE -------------------
@router.get("/")
def getdata():
    return "Auth service ready 🚀"
