---
theme: default
navigator: false
highlighter: shiki
drawings:
  persist: false
transition: slide-left
css: unocss
fonts:
  sans: 'Inter, system-ui, sans-serif'
  mono: 'Fira Code'
layout: title
speaker: Ivan Leo
email: ileo@google.com
website: kaggle.com/benchmarks
date: May 2026
---

# Kaggle Benchmarks

Building and sharing the future of AI evaluation through open community benchmarks.

---
layout: one-col
---

# Benchmarks

- Kaggle aims to be the world's trusted and open platform for evaluating AI on tough tasks that drive progress
- Since Jan 2026, we've had over **8K** evals measuring everything from mathematical reasoning to social cognition
- We've recently launched community benchmarks where anyone can create and share their own benchmarks for free

---
layout: section
number: 1
---

# Local Benchmarks

Define and build your benchmarks directly as code

---
layout: one-col
---

# Setup & Workflow

Bring your favourite code editor (Eg. Antigravity) and run a single command to start building, testing and deploying your benchmarks on Kaggle


<br>

<div class="p-4 bg-gray-50 rounded-lg border border-gray-200 mt-8 mx-auto w-3/4 dark:bg-gray-900 dark:border-gray-800 text-sm">
  <div class="text-xs text-center text-gray-500 font-bold mb-2 tracking-wider">AGENTIC WORKFLOW</div>

```bash
npx skill add kaggle-skills/kaggle-create-benchmark
```
</div>

---
layout: two-cols
---

# Defining a Task

Start by defining evaluation logic for a single test case.

- **The Task Decorator:** Annotate a function with `@kbench.task(store_task=False)` to define an atomic evaluation block.
- **Model Proxy:** Use `llm.prompt()` to query the model under test securely.
- **Assertions:** Validate model outputs with built-in assertion helpers (`assert_true`) for precise tracking.

::right::

<div class="p-4 bg-gray-50 rounded-lg border border-gray-200 mt-8 mr-8 dark:bg-gray-900 dark:border-gray-800 text-sm max-h-94 overflow-y-auto">
  <div class="text-xs text-center text-gray-500 font-bold mb-2 tracking-wider">SINGLE TEST CASE</div>

```python
import kaggle_benchmarks as kbench

@kbench.task(store_task=False)
def single_qa_task(llm, question, answer) -> dict:
    prompt = f"{question}\n\nPut answer in <answer> tags."
    
    # Prompt the proxy
    response = llm.prompt(prompt)
    predicted = extract_answer(response)
    
    # Validate correctness
    is_correct = (str(predicted) == str(answer))
    kbench.assertions.assert_true(
        is_correct, 
        expectation=f"Expected {answer}, got {predicted}"
    )
    
    return {"is_correct": is_correct}
```
</div>

---
layout: two-cols
---

# Scaling to Datasets

Map your single test case over many potential inputs concurrently.

- **Scale Seamlessly:** Define your benchmark loop and use `.evaluate()` to map the atomic task over a Pandas DataFrame.
- **Concurrent Execution:** `llm.prompt()` automatically scales evaluation, letting you run multiple models against the benchmark simultaneously.
- **Parallel Jobs:** Use `n_jobs` to accelerate evaluation across rows.

::right::

<div class="p-4 bg-gray-50 rounded-lg border border-gray-200 mt-8 mr-8 dark:bg-gray-900 dark:border-gray-800 text-sm max-h-94 overflow-y-auto">
  <div class="text-xs text-center text-gray-500 font-bold mb-2 tracking-wider">DATASET EVALUATION</div>

```python
import pandas as pd

# 1. Simple DataFrame format
df = pd.DataFrame([
    {"question": "What is 2 + 2?", "answer": "4"},
    {"question": "What is 3 * 5?", "answer": "15"}
])

# 2. Dataset Evaluation Task
@kbench.task()
def multi_qa_task(llm, dataset) -> float:
    runs = single_qa_task.evaluate(
        evaluation_data=dataset,
        llm=[llm],
        n_jobs=4
    )
    eval_df = runs.as_dataframe()
    return float(eval_df.result.str.get("is_correct").mean())

# 3. Execution
if __name__ == "__main__":
    multi_qa_task.run(kbench.llm, df)
```
</div>

---
layout: two-cols
---

# Testing & Publishing

Execute real-time evaluations from your terminal.

- **Local Execution:** Run the task locally using Gemini Flash
- **Real-time Traces:** Show execution traces and assertion outputs directly in the terminal
- **Multi-Model Execution:** Pass multiple models to evaluate them side-by-side on Kaggle's infrastructure.
- **Publish:** Move local task to a live Kaggle Benchmark page and leaderboard

::right::

<div class="p-4 bg-gray-50 rounded-lg border border-gray-200 mt-8 mr-8 dark:bg-gray-900 dark:border-gray-800 text-sm max-h-94 overflow-y-auto">
  <div class="text-xs text-center text-gray-500 font-bold mb-2 tracking-wider">END-TO-END WORKFLOW</div>

```bash {all|2|5|8|11|all}
# 1. Initialize environment & get proxy auth
kaggle b init -y

# 2. Push local file to a Kaggle Benchmark
kaggle b t push my-task -f task.py --wait

# 3. Run concurrently against multiple models
kaggle b t run my-task -m google/gemini-3.1-flash-lite anthropic/claude-sonnet-4 --wait

# 4. Download evaluation outputs
kaggle b t download my-task -o ./results
```
</div>

---
layout: section
number: 2
---

# Early Access Program

Help us build the future of agentic evaluation.

---
layout: two-cols
---

# Join the Waitlist

We are recruiting early-access testers!

- **What you get:** Access to the `kaggle-benchmarks` library with new local development support.
- **CLI extensions:** The new CLI extensions for local task management.
- **Skill File:** The `skill.md` automation file for AI coding agents.
- **Future Roadmap:** Self-service Docker-backed tasks for complex, agentic Benchmarks.

::right::

<div class="mt-8 mr-8 flex flex-col justify-center items-center h-full gap-4">
  <div class="text-center font-bold text-lg text-gray-700 dark:text-gray-300">Scan to join the waitlist</div>
  <img src="https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=https://www.kaggle.com/discussions/product-announcements/697452" class="max-w-[200px] rounded-lg shadow-sm border border-gray-200" />
</div>

---
layout: one-col
---

# Closing Thoughts

<br/>

> "Progress in AI shouldn't be defined by a small number of large labs. It should be built, verified, and shared by the community."

<br/>

**Join us:** [kaggle.com/discussions/product-announcements/697452](https://www.kaggle.com/discussions/product-announcements/697452)
