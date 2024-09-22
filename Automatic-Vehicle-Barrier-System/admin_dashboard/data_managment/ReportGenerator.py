import traceback

import pandas as pd

from shared.AccessEventType import AccessEventType
from shared.SingletonDatabase import SingletonDatabase
from admin_dashboard.Settings import Settings
from admin_dashboard.data_managment.ReportType import ReportType

ACCESS_GRANTED_CSV = Settings.ACCESS_GRANTED_CSV
ACCESS_DENIED_CSV = Settings.ACCESS_DENIED_CSV
USERS_CSV = Settings.USERS_CSV
WHITELISTED_CSV = Settings.WHITELISTED_CSV


class ReportsGenerator:
    ERROR_MESSAGE = "Unknown report type - {}"

    def __init__(self):
        pass

    def generate_report(self, filters, report_type):
        """Generate reports based on filters. Can handle 'access' or 'user' report types."""
        try:
            if report_type == ReportType.ACCESS:
                access_status = filters.get('access_status')
                if access_status == AccessEventType.GRANTED:
                    data = SingletonDatabase().getInstance().get_repo(ACCESS_GRANTED_CSV).get_data(filters)
                elif access_status == AccessEventType.DENIED:
                    data = SingletonDatabase().getInstance().get_repo(ACCESS_DENIED_CSV).get_data(filters)
                else:
                    access_granted_data = SingletonDatabase().getInstance().get_repo(ACCESS_GRANTED_CSV).get_data(
                        filters)
                    access_denied_data = SingletonDatabase().getInstance().get_repo(ACCESS_DENIED_CSV).get_data(filters)
                    data = pd.concat([access_granted_data, access_denied_data])
            elif report_type == ReportType.USER:
                # New logic to generate user report based on filters
                data = SingletonDatabase().getInstance().get_repo(USERS_CSV).get_data(filters)
            elif report_type == ReportType.WHITELISTED:
                # New logic to generate whitelisted report based on filters
                data = SingletonDatabase().getInstance().get_repo(WHITELISTED_CSV).get_data(filters)
            else:
                raise ValueError(self.ERROR_MESSAGE.format(report_type))

            return data

        except Exception as e:
            traceback.print_exc()
            raise e  # Re-raise exception for the caller to handle
