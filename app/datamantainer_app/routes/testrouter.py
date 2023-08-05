from ..models.testmodel import ReadTestTable
from ..controller.testcontroller import TestController
from ..configs.database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from typing import List

router = APIRouter()

@router.get("/test",
            response_model=List[ReadTestTable])
async def read_users():
    async with SessionLocal() as session:
        async with session.begin():
            test_controller = TestController(session)
            db_tests = await test_controller.get_test()
            session.expunge_all()

            return db_tests

