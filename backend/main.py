"""
SvelteKit + FastAPI Starter — Backend
Free edition by Quartalis (https://quartalis.co.uk)
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from jose import JWTError, jwt
from passlib.context import CryptContext

from config import settings

app = FastAPI(
    title="SvelteKit + FastAPI Starter",
    description="Free starter by Quartalis — upgrade at quartalis.co.uk/store",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Password hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# --- In-memory user store (swap for a real DB in production) ---
fake_users_db: dict[str, dict] = {}


# --- Models ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserOut(BaseModel):
    email: str
    name: str
    created_at: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- Helpers ---
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(hours=settings.JWT_EXPIRY_HOURS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None or email not in fake_users_db:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return fake_users_db[email]


# --- Routes ---
@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "1.0.0", "edition": "free"}


@app.post("/api/auth/register", response_model=UserOut)
async def register(user: UserCreate):
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    now = datetime.now(timezone.utc).isoformat()
    fake_users_db[user.email] = {
        "email": user.email,
        "name": user.name,
        "hashed_password": hash_password(user.password),
        "created_at": now,
    }
    return UserOut(email=user.email, name=user.name, created_at=now)


@app.post("/api/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user["email"]})
    return Token(access_token=token)


@app.get("/api/me", response_model=UserOut)
async def me(current_user: dict = Depends(get_current_user)):
    return UserOut(
        email=current_user["email"],
        name=current_user["name"],
        created_at=current_user["created_at"],
    )
