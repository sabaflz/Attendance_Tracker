# Attendance Tracker

A Streamlit web application for tracking attendance from Jupyter notebooks.

## Features

- Process attendance data from Jupyter notebooks
- Generate reports for all attendees or officers only
- Export reports in multiple formats:
  - Jupyter Notebook
  - Excel
  - Markdown
- Interactive web interface
- Real-time data processing

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Update the officer names in `officers.py` if needed.

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Select the report type:
   - All Attendees: Shows attendance for all members
   - Officers Only: Shows attendance for officers only
   - Both: Shows both reports

2. Choose the export format(s):
   - Jupyter Notebook
   - Excel
   - Markdown

3. Click "Generate Report" to process the data and view the results.

4. Use the export buttons to save the report in your chosen format(s).

## File Structure

- `app.py`: Main Streamlit application
- `attendance_processor.py`: Core attendance processing logic
- `officers.py`: List of officer names
- `requirements.txt`: Python dependencies
- `exports/`: Directory for exported reports

## Notes

- The app expects Jupyter notebooks to be organized in monthly folders
- Each notebook should have a "members:" section in the first cell
- Member names should be listed with "-" or "*" bullets
- The app normalizes member names to handle variations 