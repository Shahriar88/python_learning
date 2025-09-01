# 📘 Python Tutorial – Part 1

## ✅ Topics Covered
- **Basic Python syntax and usage**
- **Using NumPy for numerical operations**
- **Array creation and manipulation**
- **Random number generation**
- **Writing custom functions**
- **Function decorators (for execution time measurement)**
- **Thread-based parallelism with `ThreadPoolExecutor`**
- **Splitting workloads into chunks for parallel computation**
- **Vectorization vs threading performance comparison**
- **Acceleration with Numba JIT**:
  - `@njit` → compile Python to native machine code for speed
  - `prange` → parallelize loops across multiple CPU cores
- **Saving variables efficiently** (`pickle`, `joblib`, `np.save`)

## 🛠️ Implemented Functions
- **`make_data()`** → Create random dataset with `[x, y, m, b, eqn]`
- **`compute_eqn_block()`** → Compute equations on blocks of rows
- **`fill_eqn_threaded()`** → Parallel update of equation column
- **`fill_eqn_numba()`** → Numba-accelerated, parallelized computation
- **`timeit_decorator()`** → Measure execution time of functions

## ⚡ Key Concepts Practiced
- **Difference between threads and cores in Python execution**
- **When threading can help** (CPU-bound vs IO-bound workloads)
- **Numba JIT compilation** to speed up heavy numerical loops
- **Using `prange` to exploit multiple cores automatically**
- **Verifying parallel computation correctness**
- **Profiling performance of threaded vs vectorized vs JIT-compiled code**
- **Efficient ways to persist Python variables**

## 📂 Files
- **`python_tutorial_P1_V1.ipynb`** → Jupyter Notebook export  
- **`python_tutorial_P1_V1.html`** → HTML export of tutorial session


# 📘 Python Tutorial – Part 2

## ✅ Topics Covered

* **Efficient workload chunking** for large datasets
* **Thread-based parallelism (with chunks)** using `ThreadPoolExecutor`
* **Vectorized computation in chunks** with NumPy
* **Numba JIT acceleration in chunks**:

  * Using `@njit(parallel=True)` with `prange`
  * Handling very large arrays by splitting into batches
* **CUDA acceleration with Numba**:

  * `@cuda.jit` kernels for elementwise operations
  * Choosing `threads_per_block` and `blocks_per_grid`
  * Chunk-based GPU processing for large arrays
  * Optimized CUDA kernel with tuned block sizes
* **Device information utilities**:

  * `print_cpu_info()` → CPU core/thread details
  * `print_cuda_info()` → GPU details (name, SMs, warp size, max threads/block)
* **Performance comparison across approaches**:

  * Numba (CPU, chunked)
  * CUDA (basic & optimized, chunked)
  * ThreadPoolExecutor (chunked)
  * Pure NumPy vectorization (chunked)

## 🛠️ Implemented Functions

* **`run_numba_chunked()`** → Numba JIT computation in chunks
* **`run_cuda_chunked()`** → CUDA kernel execution in chunks
* **`pick_chunk_size()`** → Automatically tune GPU chunk size
* **`fill_eqn_threaded_chunked()`** → Thread-based parallel processing with chunks
* **`fill_eqn_vectorized_chunked()`** → NumPy vectorized chunked computation
* **`print_cpu_info()` / `print_cuda_info()`** → Hardware inspection helpers

## ⚡ Key Concepts Practiced

* **Chunking strategy** to process massive arrays without exhausting memory
* **CPU vs GPU tradeoffs**: when GPU wins, when CPU (NumPy) is more efficient
* **Threads vs vectorization vs GPU kernels** performance insights
* **CUDA architecture basics**:

  * Streaming Multiprocessors (SMs)
  * Warp size
  * Threads per block tuning
* **Correctness validation** → Comparing results across all approaches with `np.allclose`

## 📂 Files

* **`python_tutorial_P2_V0.ipynb`** → Jupyter Notebook export
* **`python_tutorial_P2_V0.html`** → HTML export of tutorial session
