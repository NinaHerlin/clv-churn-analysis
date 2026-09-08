# Customer Churn & CLV Analytics Dashboard

An interactive Streamlit dashboard for analyzing customer churn risk, predicted customer lifetime value (CLV), revenue at risk, regional segments, favorite products, and predicted purchases over a 180-day period.

## Features

- Filter customers by churn risk, predicted CLV, and country or area.
- Monitor filtered customers, average churn probability, total predicted CLV, and high-risk revenue at risk.
- Explore the relationship between churn probability and predicted CLV.
- Compare revenue at risk by country and products among high-risk customers.
- Review and download target customers as a CSV file.
- Explore predicted purchase frequency with an interactive chart.
- Use a light custom theme configured with CSS and Streamlit TOML settings.

## Project Structure

```text
clv-churn-analysis/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── churn_clv_predictions.csv
├── model/
│   └── notebook_exploratory.ipynb
└── .streamlit/
	 └── config.toml
```

## Requirements

- Python 3.12 or 3.13 recommended for cloud deployment
- Python 3.14 also works in the current local environment
- Streamlit
- Pandas
- Plotly

## Run Locally

1. Clone the repository and open its directory:

	```bash
	git clone https://github.com/NinaHerlin/clv-churn-analysis.git
	cd clv-churn-analysis
	```

2. Create and activate a virtual environment.

	Windows PowerShell:

	```powershell
	python -m venv .venv
	.\.venv\Scripts\Activate.ps1
	```

	macOS or Linux:

	```bash
	python3 -m venv .venv
	source .venv/bin/activate
	```

3. Install dependencies:

	```bash
	pip install -r requirements.txt
	```

4. Start the dashboard:

	```bash
	streamlit run app.py
	```

5. Open the local URL shown in the terminal, usually `http://localhost:8501`.

## Deploy with Streamlit Community Cloud

1. Push the project to GitHub.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Select **New app**.
4. Choose the repository `NinaHerlin/clv-churn-analysis`.
5. Select the `main` branch.
6. Set the main file path to:

	```text
	app.py
	```

7. Click **Deploy**.

The `data/churn_clv_predictions.csv` file must be included in the repository because the application loads it using a relative path. The `.streamlit/config.toml` file is optional for functionality but provides the dashboard theme and Streamlit settings.

## Data Columns

The dashboard expects the prediction dataset to include these columns:

```text
Customer ID
Churn_Risk
Churn_Probability
CLTV_180_days
predicted_purchases
```

The columns `Country` and `Top_Product` are supported by the dashboard. If they are missing, the application creates fallback values so the dashboard can still load.

## Notes

- The dashboard uses relative paths, so run Streamlit from the project root.
- Keep the CSV file under `data/churn_clv_predictions.csv`.
- Do not commit private customer data or credentials to a public repository.
