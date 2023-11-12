from ...controller.default.default_controller import test_sentry
from fastapi import APIRouter


router = APIRouter()


@router.get("/", tags=["default"])
async def default_page():
    return {"app": "API AND SQL"}


@router.get("/test_sentry", tags=["default"], include_in_schema=False)
async def test_sentry_function():
    rtn = test_sentry()

    # no testeo return dado que quiero que este endpoint se caiga antes para que mande mensaje a Sentry
    # I do not test the return due that I want this to fail before so the app send the message to Sentry
    return rtn  # pragma: no cover
