import datetime
from firebase_initializer import initialize_google_analytics
import pandas as pd
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)


def export_events_to_csv(output_csv_path, date_range_start, date_range_end):
    try:
        google_analytics_service = initialize_google_analytics()

        response = google_analytics_service.reports().batchGet(
            body={
                "reportRequests": [
                    {
                        "dateRanges": [{"startDate": date_range_start, "endDate": date_range_end}],
                        "metrics": [{"expression": "ga:totalEvents"}],
                        "dimensions": [{"name": "ga:eventCategory"}, {"name": "ga:eventAction"}]
                    }
                ]
            }
        ).execute()

        data = []

        for report in response.get('reports', []):
            rows = report.get('data', {}).get('rows', [])
            for row in rows:
                event_name = row['dimensions'][0]
                event_count = row['metrics'][0]['values'][0]
                data.append({'Event Name': event_name,
                            'Event Count': event_count})

        df = pd.DataFrame(data)

        df.to_csv(output_csv_path, index=False)

        print('Events data exported to CSV successfully.')
    except Exception as e:
        print('Error exporting events data to CSV:', e)


def sample_run_report(property_id):
    """Runs a simple report on a Google Analytics 4 property."""
    # TODO(developer): Uncomment this variable and replace with your
    #  Google Analytics 4 property ID before running the sample.
    # property_id = "YOUR-GA4-PROPERTY-ID"

    # Using a default constructor instructs the client to use the credentials
    # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="city")],
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="2024-02-27", end_date="today")],
    )
    response = client.run_report(request)

    print("Report result:")
    for row in response.rows:
        print(row.dimension_values[0].value, row.metric_values[0].value)


if __name__ == '__main__':

    google_analytics_service = initialize_google_analytics()

    date_range_start = '2024-03-01'
    date_range_end = '2024-03-14'

    output_csv_path = '/Users/hyounjun/Desktop/Calback-Data-ML/data/raw/events/output.csv'

    export_events_to_csv(output_csv_path,
                         date_range_start, date_range_end)
