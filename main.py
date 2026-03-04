from fastapi import FastAPI
from apps.registration.routers import router as user_route
from apps.doctors.routers import router as doctor_router
from apps.auth.routers import router as auth_router

app = FastAPI()

app.include_router(user_route)
app.include_router(doctor_router)
app.include_router(auth_router)

