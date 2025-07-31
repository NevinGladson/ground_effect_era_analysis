import fastf1
import pandas as pd
import matplotlib.pyplot as plt
import os
import time

# Enable persistent cache
fastf1.Cache.enable_cache('cache')

# Track type mapping (flattened)
circuit_type_map = {
    'Bahrain': 'Permanent',
    'Saudi Arabia': 'Street',
    'Australia': 'Hybrid',
    'Emilia Romagna': 'Permanent',
    'Miami': 'Street',
    'Spain': 'Permanent',
    'Monaco': 'Street',
    'Azerbaijan': 'Street',
    'Canada': 'Hybrid',
    'United Kingdom': 'Permanent',
    'Austria': 'Permanent',
    'France': 'Permanent',
    'Hungary': 'Permanent',
    'Belgium': 'Permanent',
    'Netherlands': 'Permanent',
    'Italy': 'Permanent',
    'Singapore': 'Street',
    'Japan': 'Permanent',
    'United States': 'Permanent',
    'Mexico City': 'Permanent',
    'São Paulo': 'Permanent',
    'Abu Dhabi': 'Permanent',
    'Qatar': 'Permanent',
    'Las Vegas': 'Hybrid',
    'China': 'Permanent'
}

# Define race names per year
races_by_year = {
    2022: ["Bahrain", "Saudi Arabia", "Australia", "Emilia Romagna", "Miami", "Spain", "Monaco", "Azerbaijan", "Canada",
           "United Kingdom", "Austria", "France", "Hungary", "Belgium", "Netherlands", "Italy", "Singapore", "Japan",
           "United States", "Mexico City", "São Paulo", "Abu Dhabi"],
    2023: ["Bahrain", "Saudi Arabia", "Australia", "Azerbaijan", "Miami", "Monaco", "Spain", "Canada", "Austria",
           "United Kingdom", "Hungary", "Belgium", "Netherlands", "Italy", "Singapore", "Japan", "Qatar",
           "United States", "Mexico City", "São Paulo", "Las Vegas", "Abu Dhabi"],
    2024: ["Bahrain", "Saudi Arabia", "Australia", "Japan", "China", "Miami", "Emilia Romagna", "Monaco", "Canada",
           "Spain", "Austria", "United Kingdom", "Hungary", "Belgium", "Netherlands", "Italy", "Azerbaijan",
           "Singapore", "United States", "Mexico City", "São Paulo", "Las Vegas", "Qatar", "Abu Dhabi"]
}

# Checkpointing
checkpoint_file = "f1_2022_2024_team_driver_results_checkpoint.csv"
if os.path.exists(checkpoint_file):
    df_results = pd.read_csv(checkpoint_file)
    processed_races = set(zip(df_results['Year'], df_results['Race']))
else:
    df_results = pd.DataFrame()
    processed_races = set()

# Begin data collection
for year, races in races_by_year.items():
    for race in races:
        if (year, race) in processed_races:
            print(f"Skipping already processed: {year} - {race}")
            continue

        try:
            session = fastf1.get_session(year, race, 'R')
            session.load()
            race_type = circuit_type_map.get(race, 'Unknown')
            print(f"Processing: {year} - {race} ({race_type})")
            time.sleep(60)

            # --- Top Speeds ---
            top_speeds = {}
            try:
                laps = session.laps.pick_quicklaps()
                for drv in laps['Driver'].unique():
                    drv_laps = laps.pick_driver(drv)
                    fastest_lap = drv_laps.pick_fastest()
                    car_data = fastest_lap.get_car_data()
                    top_speeds[drv] = car_data['Speed'].max()
                    time.sleep(1)  # Telemetry call
            except Exception as e:
                print(f"Top speed error in {year} {race}: {e}")

            # --- Qualifying Positions ---
            quali_positions = {}
            try:
                quali_session = fastf1.get_session(year, race, 'Q')
                quali_session.load()
                time.sleep(40)
                for _, row in quali_session.results.iterrows():
                    drv = row['Abbreviation']
                    quali_positions[drv] = row['Position']
            except Exception as e:
                print(f"Quali data missing: {year} {race}: {e}")

            # --- Final Results Compilation ---
            new_rows = []
            for _, row in session.results.iterrows():
                driver = row['Abbreviation']
                team = row['TeamName']
                grid_pos = row['GridPosition']
                race_pos = row['Position']
                status = row['Status']

                overtakes = None
                if pd.notna(grid_pos) and pd.notna(race_pos) and status == 'Finished':
                    try:
                        overtakes = int(grid_pos) - int(race_pos)
                    except:
                        pass

                new_rows.append({
                    'Year': year,
                    'Race': race,
                    'TrackType': race_type,
                    'Driver': driver,
                    'Team': team,
                    'GridPosition': grid_pos,
                    'QualifyingPosition': quali_positions.get(driver),
                    'RacePosition': race_pos,
                    'Status': status,
                    'TopSpeed': top_speeds.get(driver),
                    'EstimatedOvertakes': overtakes
                })

            df_results = pd.concat([df_results, pd.DataFrame(new_rows)], ignore_index=True)
            df_results.to_csv(checkpoint_file, index=False)

        except Exception as e:
            print(f"Failed to process {year} - {race}: {e}")

# Optional final export
df_results.to_csv("f1_2022_2024_team_driver_results.csv", index=False)
df_results.head()
