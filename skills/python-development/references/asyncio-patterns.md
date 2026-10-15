# Asyncio Patterns & Best Practices

Asynchronous Python allows high-concurrency I/O operations on a single thread. Misunderstandings around the event loop, blocking calls, and unhandled task exceptions are frequent sources of production bugs.

## 1. Structured Concurrency: `asyncio.TaskGroup` (Python 3.11+)

Avoid legacy `asyncio.gather(*tasks)` when possible. Use `TaskGroup`, which guarantees that if one task fails, all other concurrent tasks in the group are promptly cancelled and errors are bundled into an `ExceptionGroup`:

```python
import asyncio

async def fetch_user(user_id: int) -> dict: ...
async def fetch_orders(user_id: int) -> list: ...

async def load_dashboard(user_id: int):
    async with asyncio.TaskGroup() as tg:
        user_task = tg.create_task(fetch_user(user_id))
        orders_task = tg.create_task(fetch_orders(user_id))

    # At this point, both tasks have completed successfully
    user = user_task.result()
    orders = orders_task.result()
    return {"user": user, "orders": orders}
```

---

## 2. Never Block the Event Loop

Any synchronous CPU-heavy work or synchronous I/O (such as `time.sleep`, `requests.get`, or standard file I/O) freezes the event loop, stalling all other concurrent tasks.

### Delegating to Worker Threads
Use `asyncio.to_thread` to run blocking calls without freezing the event loop:

```python
import asyncio
import time

def sync_slow_hash(data: bytes) -> str:
    # CPU-bound or blocking call
    time.sleep(1)
    return "computed_hash"

async def handle_request(payload: bytes) -> str:
    # Safely offload to a background thread
    result = await asyncio.to_thread(sync_slow_hash, payload)
    return result
```

---

## 3. Timeouts and Graceful Cancellation

Always guard network I/O with timeouts:

```python
import asyncio

async def query_service(url: str) -> str:
    try:
        async with asyncio.timeout(5.0): # Python 3.11+ context manager
            async with httpx.AsyncClient() as client:
                res = await client.get(url)
                return res.text
    except TimeoutError:
        raise ServiceUnavailableError(f"Endpoint {url} did not reply in 5s")
```

When handling `asyncio.CancelledError`, always re-raise it or perform fast cleanup and exit:
```python
async def background_worker():
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        # Perform mandatory cleanup
        await flush_queue()
        raise  # MUST re-raise CancelledError to allow proper shutdown
```
