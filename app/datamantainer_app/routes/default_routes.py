from fastapi import APIRouter, Depends, HTTPException
from ..controller.default_controller import test_sentry


router = APIRouter()


@router.get("/default/test_sentry")
async def test_sentry_function():
    rtn = test_sentry()
    
    return rtn
