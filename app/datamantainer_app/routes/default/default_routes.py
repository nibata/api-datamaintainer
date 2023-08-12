from ...controller.default.default_controller import test_sentry
from fastapi import APIRouter


router = APIRouter()


@router.get("/default/test_sentry")
async def test_sentry_function():
    rtn = test_sentry()
    
    return rtn
