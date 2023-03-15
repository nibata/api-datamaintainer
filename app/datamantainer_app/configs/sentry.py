import sentry_sdk
from .settings import SENTRY_DNS


sentry_sdk.init(
    dsn=SENTRY_DNS,
    traces_sample_rate=1.0
)