"""Module for processing attendance data from Jupyter notebooks."""

from pathlib import Path
import nbformat
import pandas as pd
from typing import Dict, List, Optional, Set
import re

def normalize_name(name: str) -> str:
    """Normalize member names to handle variations."""
    name = name.strip()
    name_lower = name.lower()
    
    if "dijkstra" in name_lower \
        or "tbd (dijkstra?)" in name_lower \
        or "tbd : )" in name_lower:
        return "Dijkstra (TBD :))"
    
    return name

def extract_members_from_cell(cell_text: str) -> List[str]:
    """Extract member names from the first cell of a notebook."""
    lines = cell_text.splitlines()
    members_section = False
    members = []

    for line in lines:
        if "members:" in line.lower():
            members_section = True
            continue
        if members_section:
            stripped = line.strip()
            if stripped.startswith("-") or stripped.startswith("*"):
                name = stripped[1:].strip()
                if name:
                    members.append(normalize_name(name))
            elif stripped == "" or not stripped[0].isspace():
                break  # End of members section
    return members

def read_notebook(notebook_path: Path) -> Optional[List[str]]:
    """Read a notebook file and extract member names."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
            first_cell = nb.cells[0].get("source", "")
            return extract_members_from_cell(first_cell)
    except FileNotFoundError:
        print(f"Warning: Could not find notebook {notebook_path}")
        return None

def get_officer_names() -> Set[str]:
    """Get the list of officer names from officers.py."""
    try:
        # Import the OFFICERS set from officers.py
        from officers import OFFICERS
        return set(OFFICERS)
    except ImportError:
        print("Warning: Could not import OFFICERS from officers.py")
        return set()

def process_attendance_data(base_dir: Path, report_type: str) -> Optional[pd.DataFrame]:
    """Process attendance data from notebooks and return a DataFrame."""
    if not base_dir.exists():
        print(f"Error: Directory {base_dir} does not exist")
        return None
    
    # Get officer names if needed
    officers = get_officer_names() if report_type in ["Officers Only", "Both"] else set()
    
    # Initialize data structures
    monthly_data: Dict[str, Dict[str, int]] = {}
    all_members: Set[str] = set()
    
    # Process each month folder
    month_folders = sorted([f for f in base_dir.iterdir() if f.is_dir()])
    
    for month_folder in month_folders:
        month_name = month_folder.name
        monthly_data[month_name] = {}
        
        # Process each notebook in the month folder
        for notebook_file in month_folder.glob('*.ipynb'):
            members = read_notebook(notebook_file)
            if members:
                # Filter for officers if needed
                if report_type == "Officers Only":
                    members = [m for m in members if m in officers]
                elif report_type == "Both":
                    # Keep track of all members for the "Both" report
                    all_members.update(members)
                    # Only count officers for this month's data
                    members = [m for m in members if m in officers]
                
                # Update attendance counts
                for member in members:
                    monthly_data[month_name][member] = monthly_data[month_name].get(member, 0) + 1
    
    # Create DataFrame
    df = pd.DataFrame(monthly_data).fillna(0).astype(int)
    
    # Add total column
    df['Total'] = df.sum(axis=1)
    
    # Add total row (unique members per month)
    df.loc['Total Members'] = df.apply(lambda x: (x > 0).sum())
    
    # Sort by total attendance
    df = df.sort_values('Total', ascending=False)
    
    return df

def create_notebook_report(df: pd.DataFrame) -> nbformat.NotebookNode:
    """Create a Jupyter notebook report from the attendance data."""
    nb = nbformat.v4.new_notebook()
    
    # Add title cell
    nb.cells.append(nbformat.v4.new_markdown_cell("# Attendance Report"))
    
    # Add timestamp
    nb.cells.append(nbformat.v4.new_markdown_cell(
        f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ))
    
    # Add attendance table
    nb.cells.append(nbformat.v4.new_markdown_cell("## Attendance Summary"))
    nb.cells.append(nbformat.v4.new_code_cell("df"))
    
    return nb 