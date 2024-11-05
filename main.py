import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api import endpoints

# Initialize FastAPI
app = FastAPI(
    title="FastAPI with OpenAI Integration",
    description="An FastAPI application that interacts with OpenAI API.",
    version="1.0.0",
)


# Define the rate limit exceeded handler
async def _rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."},
    )


# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    # Add other trusted origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Limiter and add to FastAPI
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include API router
app.include_router(endpoints.router, prefix="/api/v1")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")


@app.on_event("startup")
async def startup_event():
    logger.info("Application startup: FastAPI with OpenAI is running.")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown: FastAPI with OpenAI is stopping.")
