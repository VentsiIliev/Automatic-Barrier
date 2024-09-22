import traceback

import pandas as pd

from API.SingletonDatabase import SingletonDatabase


class ReportsGenerator:
    def __init__(self):
        pass

    def generate_report(self, filters, report_type="access"):
        """Generate reports based on filters. Can handle 'access' or 'user' report types."""
        try:
            if report_type == "access":
                # Existing access report generation code
                access_status = filters.get('access_status')
                print("access_status ->>", access_status)
                if access_status == "GRANTED":
                    data = SingletonDatabase().getInstance().get_repo("granted").get_data(filters)
                elif access_status == "DENIED":
                    data = SingletonDatabase().getInstance().get_repo("denied").get_data(filters)
                else:
                    print("All access status")
                    access_granted_data = SingletonDatabase().getInstance().get_repo("granted").get_data(filters)
                    print("access_granted_data ->>", access_granted_data)
                    access_denied_data = SingletonDatabase().getInstance().get_repo("denied").get_data(filters)
                    print("access_denied_data ->>", access_denied_data)
                    data = pd.concat([access_granted_data, access_denied_data])
                    print("data ->>", data)
            elif report_type == "user":
                # New logic to generate user report based on filters
                data = SingletonDatabase().getInstance().get_repo("users").get_data(filters)
            elif report_type == "whitelisted":
                # New logic to generate whitelisted report based on filters
                data = SingletonDatabase().getInstance().get_repo("whitelisted").get_data(filters)
            else:
                raise ValueError("Unknown report type")

            return data

        except Exception as e:
            traceback.print_exc()
            raise e  # Re-raise exception for the caller to handle
