# Kaggle Benchmarks Demos

This repository contains two demo tasks built with the `kaggle-benchmarks` library, illustrating how you can scale from a simple single test case to evaluating an entire dataset concurrently across multiple models.

1. **Car Wash Demo (`car_wash_demo.py`)**: A very simple single-test evaluation task demonstrating basic SDK usage and assertion helpers.
2. **GSM8K Demo (`gsm8k_demo.py`)**: A dataset evaluation task that maps a single test case over a Pandas DataFrame.

## Setup

First, make sure your virtual environment is activated:

```bash
source .venv/bin/activate
```

## Executing the Demos

You can easily manage both tasks via the included `Makefile`. The make commands are configured to act upon both tasks.

### Local Development
Run the task code locally against Kaggle's Proxy:
```bash
make local
```

### Kaggle Execution Lifecycle

Commands are suffixed with either `-qa` (for the GSM8K dataset) or `-simple` (for the car wash task).

1. **Push your tasks** to Kaggle's infrastructure:
   ```bash
   make push-qa
   # or
   make push-simple
   ```

2. **Run your benchmarks** against multiple target models concurrently:
   ```bash
   make run-qa
   # or
   make run-simple
   ```

3. **Check the status** of the running models in the terminal:
   ```bash
   make status-qa
   # or 
   make status-simple
   ```

4. **Download the results** locally into a `./results` folder once the runs complete:
   ```bash
   make download-qa
   # or
   make download-simple
   ```

### Quick End-to-End Execution
To Push, Run, and Download results for a benchmark in a single sequence:
```bash
make all-qa
# or
make all-simple
```
If you just want to push, run, and download the results for both benchmarks in a single command, run:
```bash
make all
```

---

_For information on the Slidev presentation included here, navigate to the `./slides` folder and run `bun dev`._
