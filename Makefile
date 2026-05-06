.PHONY: local-qa local-simple push-qa push-simple run-qa run-simple status-qa status-simple download-qa download-simple all-qa all-simple models

# Default target
help:
	@echo "Available commands:"
	@echo "  make local-qa      - Run the QA benchmark locally"
	@echo "  make local-simple  - Run the simple benchmark locally"
	@echo "  make push-qa       - Push the QA task to Kaggle"
	@echo "  make push-simple   - Push the simple task to Kaggle"
	@echo "  make run-qa        - Run the QA task against multiple models"
	@echo "  make run-simple    - Run the simple task against multiple models"
	@echo "  make status-qa     - Check status of the QA runs"
	@echo "  make status-simple - Check status of the simple runs"
	@echo "  make download-qa   - Download the QA results"
	@echo "  make download-simple - Download the simple results"
	@echo "  make all-qa        - Push, run, and download QA in sequence"
	@echo "  make all-simple    - Push, run, and download simple in sequence"

# --- Local Run ---
local-qa:
	python gsm8k_demo.py

local-simple:
	python car_wash_demo.py

# --- Push ---
push-qa:
	kaggle b t push multi-qa-task -f gsm8k_demo.py --wait

push-simple:
	kaggle b t push car-wash-task -f car_wash_demo.py --wait

# --- Run ---
run-qa:
	kaggle b t run multi-qa-task -m gemini-3.1-flash-lite-preview claude-haiku-4-5-20251001 --wait

run-simple:
	kaggle b t run car-wash-task -m gemini-3.1-flash-lite-preview claude-haiku-4-5-20251001 --wait

# --- Status ---
status-qa:
	kaggle b t status multi-qa-task

status-simple:
	kaggle b t status car-wash-task

# --- Download ---
download-qa:
	kaggle b t download multi-qa-task -o ./results

download-simple:
	kaggle b t download car-wash-task -o ./results

# --- Combined Commands ---
all-qa: push-qa run-qa download-qa
all-simple: push-simple run-simple download-simple

# List all available models to run on
models:
	kaggle b t models

# Full end-to-end pipeline
all: push run download
