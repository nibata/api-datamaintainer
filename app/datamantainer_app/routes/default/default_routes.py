from ...controller.default.default_controller import test_sentry
from fastapi import APIRouter


router = APIRouter()


@router.get("/default/test_sentry", tags=["default"])
async def test_sentry_function():
    rtn = test_sentry()
    
    return rtn
