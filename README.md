# 🏎️ F1 Performance Analysis (2022–2024)

This project analyzes Formula 1 race data from 2022 to 2024 using the [FastF1](https://theoehrly.github.io/Fast-F1/) Python library. It extracts and visualizes insights about team and driver performance across different track types, races, and seasons.

---

## 📌 Overview

- ✅ Data collected from official F1 sessions via the FastF1 API
- 📊 Exploratory analysis by team, driver, race, and track type
- 🧮 Custom performance scoring system combining qualifying, race finish, overtakes, and telemetry (top speed)
- 📈 Visualization of trends across time and race conditions
- 🔥 Key performance metrics: `QualifyingPosition`, `RacePosition`, `RaceDelta`, `TopSpeed`, `EstimatedOvertakes`

---

## 📁 Project Structure
```
├── scripts/
│ └── data_collection.py # Code to fetch & save data using FastF1
│
├── notebooks/
|└── f1_data_analysis.ipynb # Visualizations, scoring, and insights
│
├── data/
│ └── f1_2022_2024_team_driver_results.csv

```
## Future Improvements
- Add regression model to predict Race Position based on qualifying, track type, and car data
- Deploy a lightweight dashboard (e.g., Streamlit)
