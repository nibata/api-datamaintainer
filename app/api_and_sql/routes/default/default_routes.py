from ...controller.default.default_controller import test_sentry
from fastapi import APIRouter


router = APIRouter()


@router.get("/", tags=["default"])
async def default_page():
    return {"app": "API AND SQL"}


@router.get("/test_sentry", tags=["default"], include_in_schema=False)
async def test_sentry_function():
    rtn = test_sentry()
    
    return rtn
