import pandas as pd
import json

# Load data with error handling
data = []
with open('processed_user_login_data.json') as f:
    for line in f:
        try:
            data.append(json.loads(line))
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON on line: {line}")
            print(e)

# Check if data is loaded
if not data:
    print("No valid data found. Please check the input file.")
else:
    df = pd.DataFrame(data)

    # Basic Analysis
    print("Data Summary:")
    print(df.describe())

    # Example Insights
    # 1. Count logins by device type
    device_type_counts = df['device_type'].value_counts()
    print("Logins by Device Type:")
    print(device_type_counts)

    # 2. Count logins by locale
    locale_counts = df['locale'].value_counts()
    print("Logins by Locale:")
    print(locale_counts)

    # 3. Logins over time
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    logins_over_time = df.resample('D', on='timestamp').size()
    print("Logins Over Time:")
    print(logins_over_time)

    # Visualization with Plotly
    import plotly.express as px

    # Logins by Device Type
    fig_device_type = px.bar(device_type_counts, x=device_type_counts.index, y=device_type_counts.values,
                             title='Logins by Device Type', labels={'index': 'Device Type', 'y': 'Count'})
    fig_device_type.show()

    # Logins by Locale
    fig_locale = px.bar(locale_counts, x=locale_counts.index, y=locale_counts.values,
                        title='Logins by Locale', labels={'index': 'Locale', 'y': 'Count'})
    fig_locale.show()
