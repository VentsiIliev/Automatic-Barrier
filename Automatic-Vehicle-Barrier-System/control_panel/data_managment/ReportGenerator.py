import traceback
from pathlib import Path
import pandas as pd
from PyQt5.QtWidgets import QMessageBox
from API.SingletonDatabase import SingletonDatabase
from control_panel.Constants import ACCESS_GRANTED_TABLE, ACCESS_DENIED_TABLE
from repositories.DataFiltering import filterData  # Assuming filtering functions are in 'filtering_module'


class ReportsGenerator:
    def __init__(self):
        pass

    def generate_report(self, filters):
        try:
            # Prepare file paths
            base_directory = Path(__file__).resolve().parent.parent  # Go up two levels
            database_directory = base_directory / 'database'

            access_granted_path = database_directory / ACCESS_GRANTED_TABLE
            access_denied_path = database_directory / ACCESS_DENIED_TABLE

            # # Check if files exist
            # if not access_granted_path.exists():
            #     raise FileNotFoundError(f"File not found: {access_granted_path}")
            # if not access_denied_path.exists():
            #     raise FileNotFoundError(f"File not found: {access_denied_path}")

            # Load data based on access status
            access_status = filters.get('access_status')
            if access_status == "GRANTED":
                data = SingletonDatabase().getInstance().get_repo("granted").get_data(filters)
            elif access_status == "DENIED":
                data = SingletonDatabase().getInstance().get_repo("denied").get_data(filters)
            else:
                access_granted_data = SingletonDatabase().getInstance().get_repo("granted").get_data(filters)
                access_denied_data = SingletonDatabase().getInstance().get_repo("denied").get_data(filters)
                data = pd.concat([access_granted_data, access_denied_data])

            return data

        except Exception as e:
            traceback.print_exc()
            raise e  # Re-raise exception for the caller to handle
