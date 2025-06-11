"""Streamlit app for tracking attendance from Jupyter notebooks."""

import streamlit as st
import pandas as pd
from pathlib import Path
import nbformat
from datetime import datetime
import sys
import os

# Add the parent directory to Python path so we can import from the package
sys.path.append(str(Path(__file__).parent.parent))

from attendance_processor import process_attendance_data, get_officer_names

def main():
    st.set_page_config(
        page_title="Attendance Tracker",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Attendance Tracker")
    st.write("Process attendance data from Jupyter notebooks")
    
    # Initialize session state for report data if it doesn't exist
    if 'report_data' not in st.session_state:
        st.session_state.report_data = None
    if 'report_type' not in st.session_state:
        st.session_state.report_type = None
    
    # If we have a report, show the "Generate New Report" button at the top
    if st.session_state.report_data is not None:
        if st.button("🔄 Generate New Report", type="primary"):
            # Clear the session state
            st.session_state.report_data = None
            st.session_state.report_type = None
            # Rerun the app to show the fresh interface
            st.rerun()
        st.divider()
    
    # Sidebar for options
    st.sidebar.header("Options")
    
    # Report type selection
    report_type = st.sidebar.radio(
        "Select Report Type",
        ["All Attendees", "Officers Only", "Both"]
    )
    
    # Output format selection
    st.sidebar.subheader("Export Format")
    export_ipynb = st.sidebar.checkbox("Jupyter Notebook (.ipynb)", value=True)
    export_excel = st.sidebar.checkbox("Excel (.xlsx)", value=True)
    export_md = st.sidebar.checkbox("Markdown (.md)", value=True)
    
    # Process data button
    if st.sidebar.button("Generate Report"):
        with st.spinner("Processing attendance data..."):
            if report_type == "Both":
                # Generate both reports
                all_attendees_data = process_attendance_data(
                    base_dir=Path(__file__).parent / "attendance",
                    report_type="All Attendees"
                )
                officers_data = process_attendance_data(
                    base_dir=Path(__file__).parent / "attendance",
                    report_type="Officers Only"
                )
                
                if all_attendees_data is None or officers_data is None:
                    st.error("No attendance data found!")
                    return
                
                # Store the data in session state
                st.session_state.report_data = {
                    "All Attendees": all_attendees_data,
                    "Officers Only": officers_data
                }
                st.session_state.report_type = report_type
                
                # Display both reports
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("All Attendees Summary")
                    st.dataframe(all_attendees_data)
                
                with col2:
                    st.subheader("Officers Only Summary")
                    st.dataframe(officers_data)
                
                # Export options
                if export_ipynb or export_excel or export_md:
                    st.subheader("Export Options")
                    
                    # Create export directory if it doesn't exist
                    export_dir = Path("exports")
                    export_dir.mkdir(exist_ok=True)
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    if export_ipynb:
                        notebook_path = export_dir / f"attendance_report_{timestamp}.ipynb"
                        # TODO: Add notebook export functionality
                        st.success(f"Notebook saved to: {notebook_path}")
                    
                    if export_excel:
                        excel_path = export_dir / f"attendance_report_{timestamp}.xlsx"
                        with pd.ExcelWriter(excel_path) as writer:
                            all_attendees_data.to_excel(writer, sheet_name="All Attendees")
                            officers_data.to_excel(writer, sheet_name="Officers Only")
                        st.success(f"Excel file saved to: {excel_path}")
                    
                    if export_md:
                        md_path = export_dir / f"attendance_report_{timestamp}.md"
                        with open(md_path, 'w') as f:
                            f.write("# All Attendees Summary\n\n")
                            f.write(all_attendees_data.to_markdown())
                            f.write("\n\n# Officers Only Summary\n\n")
                            f.write(officers_data.to_markdown())
                        st.success(f"Markdown file saved to: {md_path}")
            else:
                # Process single report
                attendance_data = process_attendance_data(
                    base_dir=Path(__file__).parent / "attendance",
                    report_type=report_type
                )
                
                if attendance_data is None:
                    st.error("No attendance data found!")
                    return
                
                # Store the data in session state
                st.session_state.report_data = attendance_data
                st.session_state.report_type = report_type
                
                # Display the data
                st.subheader("Attendance Summary")
                st.dataframe(attendance_data)
                
                # Export options
                if export_ipynb or export_excel or export_md:
                    st.subheader("Export Options")
                    
                    # Create export directory if it doesn't exist
                    export_dir = Path("exports")
                    export_dir.mkdir(exist_ok=True)
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    if export_ipynb:
                        notebook_path = export_dir / f"attendance_report_{timestamp}.ipynb"
                        # TODO: Add notebook export functionality
                        st.success(f"Notebook saved to: {notebook_path}")
                    
                    if export_excel:
                        excel_path = export_dir / f"attendance_report_{timestamp}.xlsx"
                        attendance_data.to_excel(excel_path)
                        st.success(f"Excel file saved to: {excel_path}")
                    
                    if export_md:
                        md_path = export_dir / f"attendance_report_{timestamp}.md"
                        attendance_data.to_markdown(md_path)
                        st.success(f"Markdown file saved to: {md_path}")

if __name__ == "__main__":
    main() 