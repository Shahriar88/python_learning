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
