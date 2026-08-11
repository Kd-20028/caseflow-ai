from fastapi import FastAPI
from app.routes import cases, analytics

from app.database import Base, engine
from app import models


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="CaseFlow AI API",
    description="Backend API for the CaseFlow AI case management platform",
    version="0.1.0"
)

app.include_router(cases.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"message": "CaseFlow AI API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
