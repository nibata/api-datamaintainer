from .settings import SENTRY_DNS
import sentry_sdk


sentry_sdk.init(
    dsn=SENTRY_DNS,
    traces_sample_rate=1.0
)