# %%
import kaggle_benchmarks as kbench

# %%
@kbench.task(name="car-wash-task")
def car_wash_task(llm):
    prompt = "A car wash cleans 10 cars per hour. How many cars does it clean in an 8 hour day? Think step by step and put your final numerical answer in <answer> tags."
    response = llm.prompt(prompt)
    
    import re
    match = re.search(r'<answer>\s*(.*?)\s*</answer>', response, re.IGNORECASE | re.DOTALL)
    predicted = match.group(1).strip() if match else ""
    
    kbench.assertions.assert_true(
        "80" in predicted,
        expectation=f"Expected 80, got {predicted}"
    )

# %%
if __name__ == "__main__":
    car_wash_task.run(kbench.llm)
