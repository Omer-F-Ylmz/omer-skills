import time

T0 = time.monotonic()  # hook bütçesi süreç başından sayılır (import dahil)

from .cli import calistir  # noqa: E402

calistir(T0)
