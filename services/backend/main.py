from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.config import settings
from config.logger import configure_logging
from apps import register_apps, register_managers

# Initialize the FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="This is the API documentation for the application.",
    version="1.0.0",
    contact={
        "name": "Sunny Kumar Sinha",
        "email": "thesunnysinha@gmail.com",
    }
)

configure_logging()

# Register apps
register_apps(app)

# Register model managers
register_managers()


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change to specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Health check endpoint
@app.get("/", tags=["Health"])
def health_check():
    """
    Health check endpoint to verify the API is up and running.
    """
    return {"status": "healthy"}
