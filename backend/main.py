from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import create_tables
from routes import tasks, auth


# Create FastAPI app instance
app = FastAPI(title="Todo API", version="0.1.0")


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(tasks.router, prefix="/api/{user_id}", tags=["tasks"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])


@app.on_event("startup")
def on_startup():
    """Create database tables on startup"""
    create_tables()


@app.get("/")
def read_root():
    return {"message": "Todo API is running!"}