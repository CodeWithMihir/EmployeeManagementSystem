from fastapi import FastAPI
import models as models
from database import engine, Base
from routers import *


app=FastAPI()

Base.metadata.create_all(bind=engine)

#app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
#app.include_router(employeesroute.router, prefix="/employees", tags=["Employee Management"])

app.include_router(auth.router)
app.include_router(departmentcontroller.router)
app.include_router(employeecontroller.router)
app.include_router(salarycontroller.router)
app.include_router(promotioncontroller.router)