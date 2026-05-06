# %%
import pandas as pd
import kaggle_benchmarks as kbench

# %%
# Dataset to evaluate.
df = pd.DataFrame(
    [
        {
            "question": "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?",
            "answer": "72",
        },
        {
            "question": "Weng earns $12 an hour for babysitting. Yesterday, she just did 50 minutes of babysitting. How much did she earn?",
            "answer": "10",
        },
        {
            "question": "Betty is saving money for a new wallet which costs $100. Betty has only half of the money she needs. Her parents decided to give her $15 for that purpose, and her grandparents twice as much as her parents. How much more money does Betty need to buy the wallet?",
            "answer": "5",
        },
        {
            "question": "Julie is reading a 120-page book. Yesterday, she was able to read 12 pages and today, she read twice as many pages as yesterday. If she wants to read half of the remaining pages tomorrow, how many pages should she read?",
            "answer": "42",
        },
        {
            "question": "James writes a 3-page letter to 2 different friends twice a week.  How many pages does he write a year?",
            "answer": "624",
        }
    ]
)

# %%
# First define the task for a single row of the dataset.
@kbench.task(store_task=False)
def single_qa_task(llm, question, answer) -> dict:
    prompt = f"{question}\n\nPlease think step by step and put your final numerical answer inside <answer> tags. For example: <answer>42</answer>"
    response = llm.prompt(prompt)
    
    # Extract answer using regex from <answer> tag
    import re
    match = re.search(r'<answer>\s*(.*?)\s*</answer>', response, re.IGNORECASE | re.DOTALL)
    predicted = match.group(1).replace(',', '').strip() if match else None
    
    # Fallback to finding a number if there's extra text in the tag
    if predicted:
        nums = re.findall(r'-?\d+(?:\.\d+)?', predicted)
        predicted = nums[-1] if nums else predicted
        
    is_correct = (str(predicted) == str(answer))
    
    kbench.assertions.assert_true(
        is_correct, 
        expectation=f"Expected {answer}, got {predicted}"
    )
    
    return {
        "question": question,
        "gold_target": answer,
        "predicted_answer": predicted,
        "is_correct": is_correct,
        "raw_response": response
    }

# %%
# Define the task for the entire dataset.
@kbench.task()
def multi_qa_task(llm, df) -> tuple[float, float]:
    with kbench.client.enable_cache():
        runs = single_qa_task.evaluate(
            stop_condition=lambda runs: len(runs) == df.shape[0],
            max_attempts=1,
            llm=[llm],
            evaluation_data=df,
            n_jobs=2,
            timeout=120,
            remove_run_files=True,  # Optionally remove sub runs files.
        )
    eval_df = runs.as_dataframe()

    # Use float() to convert from np.float.
    accuracy = float(eval_df.result.str.get("is_correct").mean())
    std = float(eval_df.result.str.get("is_correct").std())
    return accuracy, std

if __name__ == "__main__":
    run = multi_qa_task.run(kbench.llm, df)
    
    print("\n" + "="*60)
    print("BENCHMARK RESULTS")
    print("="*60)
    
    if run.subruns and run.subruns.runs:
        for idx, subrun in enumerate(run.subruns.runs):
            # The result dictionary returned by single_qa_task
            res = subrun.result
            
            q = res.get('question', '')
            target = res.get('gold_target', '')
            pred = res.get('predicted_answer', '')
            correct = res.get('is_correct', False)
            
            status = "✅ PASS" if correct else "❌ FAIL"
            
            print(f"\n[Question {idx+1}]")
            print(f"Q: {q}")
            print(f"Expected:  {target}")
            print(f"Predicted: {pred}  {status}")
            print("-" * 60)
            
    print(f"\nFinal Accuracy: {run.result[0]*100:.1f}%\n")