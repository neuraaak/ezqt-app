# Python Concurrency & Performance Standards (UIA)

Optimization, scale, and modern concurrency patterns for high-performance Python.

<rules>
- **MODEL:** Choose the correct pattern for the workload (I/O vs CPU).
- **FREE-THREADED:** Use standard `threading` for CPU-bound tasks in Python 3.14+ (without GIL).
- **ASYNCIO:** Prefer for I/O-bound operations with many concurrent tasks.
- **GENERATORS:** Use generators to process data streams instead of loading everything to memory.
- **PROFILE:** Always profile before optimizing with `cProfile` or `Tachyon`.
</rules>

## Concurrency Models

| Pattern             | Scenario                        | Key Tool                |
| :------------------ | :------------------------------ | :---------------------- |
| **Asyncio**         | High-volume I/O                 | `async/await`, `uvloop` |
| **Threading**       | CPU-bound (3.14+), I/O-bound    | `threading.Thread`      |
| **Multiprocessing** | Isolated processes (legacy CPU) | `multiprocessing.Pool`  |

## Optimization Techniques

- **`__slots__`:** Use for data-intensive classes with millions of instances.
- **`lru_cache`:** Use for expensive calculations with fixed inputs.
- **Vectorization:** Prefer NumPy for numerical computation over raw loops.

<examples>
# Async I/O Pattern
import asyncio

async def fetch_data(url: str) -> dict: # simulated I/O
await asyncio.sleep(0.1)
return {"data": url}

# Generator for Large Datasets

def stream_large_file(path: Path):
with path.open("r") as f:
for line in f:
yield line.strip()
</examples>

<success_criteria>

- Concurrency model is matched to workload.
- Generators are used for large file processing.
- No premature optimization without profiling data.

</success_criteria>
