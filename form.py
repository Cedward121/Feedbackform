from fastapi import FastAPI, Form, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from typing import Optional

# Define your app and template folder 
app = FastAPI(title="Form App")
templates = Jinja2Templates(directory="Folder")

#OAuth2 token based auth
oauth2_scheme =  OAuth2PasswordBearer(tokenUrl="token")

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Simulated user Database
fake_users_db = {
    "alice": {
        "username": "Alice",
        "password": pwd_context.hash("secretpassword"),
        "role": "admin" #user_role: admin, user,etc
    },
    "bob": {
        "username": "Bob",
        "password": pwd_context.hash("mypassword"),
        "role": "user"
    }
}

# Secret Key for JWT
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#Functions for password verification and JWT creation

def verify_password (plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_from_db(username: str):
    return fake_users_db.get(username)

# get current user from jwt token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token is invalid")
        return get_user_from_db(username)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token is invalid")
    

#User Login, Main Page Route
@app.get("/main")
def main_page(request:Request):
    return templates.TemplateResponse("hisindex.html", {"request":request})

#Route for form submission, post
@app.post("/subform")
def submit_form(username: str = Form(...), password: str = Form(...)):
    user = get_user_from_db(username)
    if user is None or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail = "Invalid username or password")
    return {"Welcome": username}

#Route to log in and receive a JWT token
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_from_db(form_data.username)
    if user is None or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub":form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

#Example of protected route with Authorization
@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    # check if user has the role of admin
    if current_user["role"] != "admin":
        raise HTTPException(status_code=401, detail="You do not have permission to access this resource.")
    return {"message": f"Welcome, {current_user['username']}! This is a protected route"}