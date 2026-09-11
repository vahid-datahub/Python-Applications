from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel

router = APIRouter(prefix="/auth")

SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(data: LoginRequest):
    if data.username != "admin" or data.password != "1234":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"sub": data.username}, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except (JWTError, KeyError):
        raise HTTPException(status_code=401, detail="Invalid token")