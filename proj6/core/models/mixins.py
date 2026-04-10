from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DATETIME, func
from datetime import datetime, timezone


def now_utc():
    dt = datetime.now(tz=timezone.utc)
    return dt.replace(microsecond=0, tzinfo=None)


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        default=now_utc,
        server_default=func.now(),
    )
