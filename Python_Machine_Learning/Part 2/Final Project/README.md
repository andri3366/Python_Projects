# Machine Learning Final Project

This project trains takes different Jupyter notebooks and creates a machine learning pipeline, using the following problems:
- Real estate price prediction (regression)
- Loan eligibility prediction (classification)
- UCLA admission prediction (classification)
- Mall customer segmentation (clustering)

It also generates PDF reports for EDA, model diagnostics, and clustering analysis.

## Project Structure

- `main.py`: Runs the pipeline (clean data, engineer features, train, evaluate, create reports)
- `streamlit.py`: Streamlit UI for interactive prediction/segmentation
- `src/config/datasets.py`: Central dataset/model/report config registryDataset configuration registry
- `src/data/make_dataset.py`: Raw data loading and cleaning
- `src/features/build_features.py`: Feature engineering and Streamlit input transformation
- `src/models/train.py`: Train/test split, scaling, model training, model saving
- `src/models/predict.py`: Evaluation and cross-validation
- `src/visualization/visualize.py`: Plotting and PDF report generation
- `data/raw`: Raw CSV files
- `data/processed`: Cleaned and engineered datasets
- `models`: Saved model (`.pkl`)

## Requirements

- Python 3.14
- pip

Dependencies are listed in `requirements.txt`:
- pandas
- numpy
- matplotlib
- scikit-learn
- seaborn
- streamlit

## Setup

1. Open a terminal in the project root.
2. Create and activate a virtual environment.

Windows PowerShell:

```powershell
python -m venv venv
```
```powershell
venv\Scripts\Activate
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run the Training + Reporting Pipeline

Run:

```powershell
python main.py
```

What this does:
- Reads each dataset from `data/raw`
- Writes cleaned files to `data/processed/cleaned_*.csv` (optional)
- Writes engineered files to `data/processed/final_*.csv` (required)
- Trains configured models and saves them into `models/`
- Generates dataset reports as PDF files in the project root

## Run the Streamlit Application

After models have been trained and saved, start the UI:

```powershell
streamlit run streamlit.py
```

Then open the local URL shown in terminal (`http://localhost:8501`).

## Adding New Features

### 1. Add a New Dataset

1. Place raw file in `data/raw/`.
2. Add a dataset entry in `src/config/datasets.py` with:
   - `raw_path`, `cleaned_path`, `final_path`
   - `target`
   - `problem_type` (`regression`, `classification`, or `clustering`)
   - `scale`, optional `scaler`
   - `train_test_split` (for supervised tasks)
   - `models` list
   - `plot` list for report pages (include plot type for raw or processed data)
3. Add any dataset-specific cleaning rules to `load_and_preprocess_data()` in `src/data/make_dataset.py`.
4. Add feature engineering rules to `create_dummy_var()` in `src/features/build_features.py`.
5. Re-run `python main.py`.

### 2. Add a New Model to an Existing Dataset

1. In `src/config/datasets.py`, append a model block under the dataset's `models` list.

Example:

```python
{
    "name": "RandomForestClassifier",
    "kwargs": {
        "n_estimators": 300,
        "random_state": 123
    },
    "cv": 5
}
```

2. Ensure the model class exists in the `models` mapping in `src/models/train.py`.
3. Run `python main.py` to train and save the new model.
4. For Streamlit support, verify model selection logic in `streamlit.py` still maps to the correct saved filename.

### 3. Add New Engineered Features

1. Update transformation logic in `create_dummy_var()` (`src/features/build_features.py`).
2. Keep feature names consistent.
3. If a feature is used in the UI, update:
   - `problem_features[...]["input"]`
   - `problem_features[...]["features"]`
   in `streamlit.py`.
4. If categorical encoding changes, update `streamlit_input()` so user input is transformed to the exact training columns.
5. Retrain with `python main.py`.

### 4. Add or Update Report Visuals

1. Add plot entries to the dataset `plot` list in `src/config/datasets.py`.
2. Implement/adjust plotting helpers in `src/visualization/visualize.py`.
3. Re-run `python main.py` and inspect the generated PDF.

