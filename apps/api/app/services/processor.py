from __future__ import annotations

# Import stravavis - should be installed via pip install -e ../../src
try:
    from stravavis import (
        plot_calendar,
        plot_dumbbell,
        plot_elevations,
        plot_facets,
        plot_landscape,
        plot_map,
    )
    from stravavis.process_activities import process_activities
    from stravavis.process_data import process_data
except ImportError:
    # Fallback: try to import from source
    import sys
    from pathlib import Path
    
    src_path = Path(__file__).parent.parent.parent.parent.parent / "src"
    if src_path.exists():
        sys.path.insert(0, str(src_path))
        from stravavis import (
            plot_calendar,
            plot_dumbbell,
            plot_elevations,
            plot_facets,
            plot_landscape,
            plot_map,
        )
        from stravavis.process_activities import process_activities
        from stravavis.process_data import process_data
    else:
        raise ImportError(
            "stravavis not found. Please install it with: pip install -e ../../src"
        )


class VisualizationProcessor:
    """Process Strava data and generate visualizations."""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def process(
        self,
        file_paths: list[str],
        activities_csv: str | None = None,
        visualizations: list[str] | None = None,
        bbox: dict[str, float] | None = None,
        year_min: int | None = None,
        year_max: int | None = None,
    ) -> dict[str, str]:
        """Process files and generate visualizations.
        
        Returns dict mapping visualization type to output file path.
        """
        if visualizations is None:
            visualizations = ["all"]
        
        if "all" in visualizations:
            visualizations = ["facets", "map", "elevations", "landscape", "calendar", "dumbbell"]
        
        outputs = {}
        
        # Process track data (GPX/FIT/TCX)
        track_visualizations = ["facets", "map", "elevations", "landscape"]
        if any(viz in visualizations for viz in track_visualizations):
            df = process_data(file_paths)
            
            if not df.empty:
                # Extract bbox if provided
                lon_min = bbox.get("lon_min") if bbox else None
                lon_max = bbox.get("lon_max") if bbox else None
                lat_min = bbox.get("lat_min") if bbox else None
                lat_max = bbox.get("lat_max") if bbox else None
                
                if "facets" in visualizations:
                    output_file = self.output_dir / "facets.png"
                    plot_facets(df, output_file=str(output_file))
                    outputs["facets"] = str(output_file)
                
                if "map" in visualizations:
                    output_file = self.output_dir / "map.png"
                    plot_map(
                        df,
                        lon_min=lon_min,
                        lon_max=lon_max,
                        lat_min=lat_min,
                        lat_max=lat_max,
                        output_file=str(output_file),
                    )
                    outputs["map"] = str(output_file)
                
                if "elevations" in visualizations:
                    output_file = self.output_dir / "elevations.png"
                    plot_elevations(df, output_file=str(output_file))
                    outputs["elevations"] = str(output_file)
                
                if "landscape" in visualizations:
                    output_file = self.output_dir / "landscape.png"
                    plot_landscape(df, output_file=str(output_file))
                    outputs["landscape"] = str(output_file)
        
        # Process activities CSV for calendar and dumbbell
        if activities_csv and Path(activities_csv).exists():
            activities = process_activities(activities_csv)
            
            if "calendar" in visualizations:
                output_file = self.output_dir / "calendar.png"
                plot_calendar(
                    activities,
                    year_min=year_min,
                    year_max=year_max,
                    output_file=str(output_file),
                )
                outputs["calendar"] = str(output_file)
            
            if "dumbbell" in visualizations:
                output_file = self.output_dir / "dumbbell.png"
                plot_dumbbell(
                    activities,
                    year_min=year_min,
                    year_max=year_max,
                    output_file=str(output_file),
                )
                outputs["dumbbell"] = str(output_file)
        
        return outputs

