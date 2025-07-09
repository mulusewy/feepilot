from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, validator
import sqlite3
import os
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from database import create_db_and_tables, DATABASE_URL

# --- Rate Limiting ---
from collections import defaultdict
import time

REQUEST_COUNTS = defaultdict(lambda: {'count': 0, 'last_reset': time.time()})
RATE_LIMIT_INTERVAL = 60 # seconds
RATE_LIMIT_MAX_REQUESTS = 5 # requests per interval

def get_client_ip(request: Request):
    return request.client.host

async def rate_limit_dependency(request: Request):
    client_ip = get_client_ip(request)
    current_time = time.time()

    if current_time - REQUEST_COUNTS[client_ip]['last_reset'] > RATE_LIMIT_INTERVAL:
        REQUEST_COUNTS[client_ip]['count'] = 0
        REQUEST_COUNTS[client_ip]['last_reset'] = current_time

    if REQUEST_COUNTS[client_ip]['count'] >= RATE_LIMIT_MAX_REQUESTS:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many requests")

    REQUEST_COUNTS[client_ip]['count'] += 1

# --- Security Configuration ---
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key") # TODO: Change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# For MVP, a simple hardcoded admin user
ADMIN_USER = {
    "username": "admin",
    "hashed_password": pwd_context.hash("adminpass") # TODO: Change this in production
}

# --- FastAPI App Setup ---


app = FastAPI()

origins = [
    "http://localhost:5173",  # Frontend development server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- JWT Functions ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")


async def authenticate_user(username: str, password: str):
    if username == ADMIN_USER["username"] and pwd_context.verify(password, ADMIN_USER["hashed_password"]):
        return ADMIN_USER
    return None


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username


# --- Endpoints ---

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str

    @validator('phone')
    def validate_phone(cls, v):
        # Remove non-digit characters
        cleaned_phone = ''.join(filter(str.isdigit, v))

        # Validate length
        if len(cleaned_phone) != 10:
            raise ValueError('Phone number must be 10 digits')

        # Format to (xxx)-xxx-xxxx
        formatted_phone = f"({cleaned_phone[0:3]})-" \
                          f"{cleaned_phone[3:6]}-" \
                          f"{cleaned_phone[6:10]}"
        return formatted_phone



class UserInDB(UserCreate):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str


@app.post("/admin/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# --- Fee Structures (Simplified for example) ---
# In a real application, these would likely be fetched from a database
PSP_FEES = {
    "Stripe": {"fixed": 0.30, "variable": 0.029, "cross_border_surcharge": 0.01, "weekend_surcharge": 0.005},
    "PayPal": {"fixed": 0.49, "variable": 0.0349, "cross_border_surcharge": 0.015, "weekend_surcharge": 0.007},
    "Square": {"fixed": 0.10, "variable": 0.026, "cross_border_surcharge": 0.012, "weekend_surcharge": 0.006},
    "Wise": {"fixed": 0.0, "variable": 0.0041, "cross_border_surcharge": 0.0, "weekend_surcharge": 0.0} # Wise has different fee structure
}

WISE_API_KEY = os.getenv("WISE_API_KEY")
WISE_API_URL = "https://api.wise.com/v3/comparisons"

async def get_wise_fx_rate(source_currency: str, target_currency: str, source_amount: float):
    if not WISE_API_KEY:
        print("WISE_API_KEY not set. FX rates will not be accurate for Wise.")
        return 1.0 # Default to 1.0 if API key is not set

    headers = {"Authorization": f"Bearer {WISE_API_KEY}"}
    params = {
        "sourceCurrency": source_currency,
        "targetCurrency": target_currency,
        "sourceAmount": source_amount,
        "senders": ["PERSONAL"],
        "receivers": ["PERSONAL"],
        "paymentMethods": ["BALANCE"],
        "deliveryMethods": ["BALANCE"],
    }
    try:
        response = requests.get(WISE_API_URL, headers=headers, params=params)
        response.raise_for_status() # Raise an exception for HTTP errors
        data = response.json()
        # The Wise API response structure can be complex, this is a simplified extraction
        # You might need to inspect the actual response to get the correct rate
        if data and data[0] and data[0].get("rate"):
            return data[0]["rate"]
        return 1.0
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Wise FX rate: {e}")
        return 1.0 # Default to 1.0 on error


@app.get("/admin/simulations")
async def get_simulations(current_user: str = Depends(get_current_user)):
    try:
        with sqlite3.connect(DATABASE_URL.replace("sqlite:///./", "")) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, first_name, last_name, email, phone FROM users")
            users = cursor.fetchall()
            return [UserInDB(id=user[0], first_name=user[1], last_name=user[2], email=user[3], phone=user[4]) for user in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


class TrackingScript(BaseModel):
    script_name: str
    script_code: str


@app.post("/admin/tracking")
async def post_tracking_script(script: TrackingScript, current_user: str = Depends(get_current_user)):
    try:
        with sqlite3.connect(DATABASE_URL.replace("sqlite:///./", "")) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO tracking_scripts (script_name, script_code) VALUES (?, ?)",
                (script.script_name, script.script_code)
            )
            conn.commit()
            return {"message": "Tracking script saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@app.get("/")
async def root():
    return {"message": "FeePilot Backend is running!"}

@app.post("/submit-user", response_model=UserInDB, dependencies=[Depends(rate_limit_dependency)])
async def submit_user(user: UserCreate):
    try:
        with sqlite3.connect(DATABASE_URL.replace("sqlite:///./", "")) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (first_name, last_name, email, phone) VALUES (?, ?, ?, ?)",
                (user.first_name, user.last_name, user.email, user.phone)
            )
            conn.commit()
            user_id = cursor.lastrowid
            return UserInDB(id=user_id, **user.dict())
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


class TransactionDetails(BaseModel):
    amount: float
    currency: str
    merchant_country: str
    customer_country: str
    payment_method: str
    day_of_week: str  # "weekday" or "weekend"
    optional_markup: float = 0.0
    psps_to_compare: list[str]


class PSPFeeBreakdown(BaseModel):
    psp_name: str
    effective_rate: float
    fixed_fee: float
    variable_fee: float
    fx_cost: float
    weekend_surcharge: float
    cross_border_surcharge: float
    net_revenue: float


class SimulationResult(BaseModel):
    results: list[PSPFeeBreakdown]


@app.post("/simulate", response_model=SimulationResult, dependencies=[Depends(rate_limit_dependency)])
async def simulate_fees(details: TransactionDetails):
    results = []
    for psp_name in details.psps_to_compare:
        fees = PSP_FEES.get(psp_name)
        if not fees:
            continue

        # Base calculation
        fixed_fee = fees["fixed"]
        variable_fee = details.amount * fees["variable"]

        # FX Cost (simplified - assuming Wise is the only one with direct FX)
        fx_cost = 0.0
        if psp_name == "Wise" and details.currency != "USD": # Assuming USD as base for simplicity
            # In a real scenario, you'd need to determine the target currency for Wise
            # and potentially other PSPs if they handle FX differently.
            # For this MVP, we'll assume Wise handles FX for non-USD transactions.
            fx_rate = await get_wise_fx_rate(details.currency, "USD", details.amount)
            fx_cost = details.amount * (1 - fx_rate) # Simplified FX cost

        # Surcharges
        weekend_surcharge = 0.0
        if details.day_of_week == "weekend":
            weekend_surcharge = details.amount * fees["weekend_surcharge"]

        cross_border_surcharge = 0.0
        if details.merchant_country != details.customer_country:
            cross_border_surcharge = details.amount * fees["cross_border_surcharge"]

        # Total fees
        total_fees = fixed_fee + variable_fee + fx_cost + weekend_surcharge + cross_border_surcharge

        # Apply optional markup
        total_fees += details.amount * (details.optional_markup / 100)

        net_revenue = details.amount - total_fees

        results.append(PSPFeeBreakdown(
            psp_name=psp_name,
            effective_rate=(total_fees / details.amount) * 100 if details.amount > 0 else 0.0,
            fixed_fee=fixed_fee,
            variable_fee=variable_fee,
            fx_cost=fx_cost,
            weekend_surcharge=weekend_surcharge,
            cross_border_surcharge=cross_border_surcharge,
            net_revenue=net_revenue
        ))

    return SimulationResult(results=results)
