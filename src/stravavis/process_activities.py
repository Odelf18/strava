from __future__ import annotations

import pandas as pd


def process_activities(activities_path):
    # Import activities.csv from Strava bulk export zip
    activities = pd.read_csv(activities_path)

    # Normalize column names (handle French/English locales)
    column_mapping = {
        "ID de l'activité": "activity_id",
        "Activity ID": "activity_id",
        "Type d'activité": "activity_type",
        "Activity Type": "activity_type",
        "Date de l'activité": "activity_date",
        "Activity Date": "activity_date",
        "Nom du fichier": "filename",
        "Filename": "filename",
        "Distance": "distance",
        "Temps écoulé": "elapsed_time",
        "Elapsed Time": "elapsed_time",
    }
    
    # Rename columns if they exist
    for old_col, new_col in column_mapping.items():
        if old_col in activities.columns:
            activities = activities.rename(columns={old_col: new_col})
    
    # Ensure activity_type column exists (for filtering)
    if "activity_type" not in activities.columns:
        # Try to find similar column
        for col in activities.columns:
            if "type" in col.lower() or "activité" in col.lower():
                activities = activities.rename(columns={col: "activity_type"})
                break

    return activities
