import matplotlib.pyplot as plt
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
import pandas as pd
from datetime import datetime
import numpy as np
import plotly.express as px

def chart(request):
    times = [
        "16:56:04", "16:55:56", "16:45:35", "16:34:36", "16:24:42", "16:24:42", "16:13:49", "15:41:54", 
        "15:41:42", "15:18:55", "14:44:39", "14:43:37", "14:43:21", "14:30:24", "14:26:03", "14:24:37", 
        "14:18:59", "14:17:02", "14:14:31", "14:09:01", "14:08:48", "14:06:46", "14:00:28", "14:00:11", 
        "14:00:03", "13:59:05", "13:58:41", "13:58:24", "13:57:22", "13:57:19", "13:42:14", "12:45:47", 
        "11:27:44", "11:27:44", "11:27:33", "11:27:21", "11:27:03", "11:26:44", "11:16:09", "11:15:56", 
        "11:14:35", "11:14:24", "11:14:20", "11:14:19", "9:22:33", "9:22:23", "9:20:31", "8:53:54", 
        "8:53:54", "16:10:05", "16:10:05", "16:10:04", "16:10:04", "16:10:04", "16:09:55", "15:39:58", 
        "15:29:25", "15:21:51", "15:21:43", "13:41:21", "12:18:10", "8:56:53", "17:12:12", "13:48:08", 
        "13:48:08", "13:48:08", "10:25:22", "9:02:03", "9:02:03", "9:02:02", "9:02:02", "9:02:02", 
        "9:02:00", "9:01:34", "8:59:40", "8:45:39", "8:41:51", "7:57:49", "19:28:26", "19:27:26", 
        "18:45:17", "18:45:17", "18:45:16", "18:45:16", "18:45:16", "18:45:16", "18:44:16", "17:27:38", 
        "16:49:13", "16:12:51", "15:57:20", "13:56:56", "13:56:56", "13:56:56", "13:56:56", "13:56:11", 
        "13:33:03", "12:57:18", "12:34:30", "12:26:06", "9:52:47", "9:26:05", "9:19:07", "9:19:06", 
        "9:16:42", "8:11:22", "17:32:18", "17:21:00", "13:44:13", "13:40:43", "13:40:41", "13:40:14", 
        "12:15:21", "12:08:24", "11:29:14", "11:18:17", "9:49:12", "9:08:51", "9:05:10", "8:56:43", 
        "8:56:43", "8:56:42", "8:56:42", "8:56:20", "8:56:19", "8:52:53", "9:50:39", "9:50:38", 
        "16:51:33", "16:38:34", "16:14:49", "15:39:03", "15:02:16", "14:53:06", "14:09:08", "10:46:21", 
        "10:45:30", "9:04:56", "9:04:56", "9:04:56", "9:04:56", "9:04:56", "9:04:56", "9:04:54", 
        "9:04:25", "9:04:25", "20:51:12", "20:19:38", "17:57:22", "17:57:22", "17:57:22", "17:57:22", 
        "17:57:22", "17:57:22", "17:56:26", "17:43:52", "16:58:48", "16:38:52", "14:39:52", "14:39:28", 
        "14:38:49", "14:36:35", "13:38:01", "13:38:01", "13:37:59", "13:37:59", "13:34:47", "13:28:19", 
        "11:40:30", "11:25:16", "10:12:52", "9:09:35", "9:09:35", "9:07:42", "9:00:36", "22:21:01", 
        "22:21:01", "22:20:36", "22:20:36", "17:16:25", "16:56:30", "15:37:30", "15:31:26", "14:58:07", 
        "14:49:50", "14:41:43", "14:38:56", "14:36:34", "14:34:06", "13:28:30", "12:28:18", "12:26:52", 
        "12:26:45", "12:00:43", "11:34:35", "11:24:59", "11:24:59", "10:23:25", "10:23:25", "10:23:25", 
        "10:23:25", "10:20:28", "10:09:19", "10:08:28", "9:16:12", "9:08:58", "23:47:55", "23:44:25", 
        "22:06:45", "22:06:44", "17:18:35", "16:53:33", "16:26:22", "14:56:32", "12:49:37", "11:42:26", 
        "11:31:52", "10:10:35", "10:02:54", "10:02:54", "10:02:53", "10:02:53", "10:02:53", "10:02:53", 
        "10:02:53", "10:02:53", "10:02:53", "10:02:53", "10:02:53", "10:02:53", "10:02:53", "10:02:53", 
        "10:02:53", "10:02:53", "10:02:53", "10:02:53", "10:02:53", "10:02:53", "10:02:53", "10:02:53", 
        "10:02:53", "10:02:53", "10:02:53", "10:02:53", "10:02:53", "10:02:53", "10:02:53", "10:02:53", 
        "10:02:53", "10:02:53", "9:48:41", "9:35:51", "9:06:21", "23:42:16", "23:42:16", "23:41:03", 
        "23:35:47", "23:35:47"
    ]

    # Convert times into datetime format and extract hours
    hours = [datetime.strptime(time, "%H:%M:%S").hour for time in times]

    # Define hourly bins with AM/PM format
    def format_hour(hour):
        start_hour = hour if hour <= 12 else hour - 12
        end_hour = hour + 1 if (hour + 1) <= 12 else (hour + 1) - 12
        suffix = "AM" if hour < 12 else "PM"
        return f"{start_hour}-{end_hour} {suffix}"

    hour_bins = {h: format_hour(h) for h in range(7, 24)}  # Creating labels for the bins

    # Count occurrences per hour
    hour_counts = pd.Series(hours).value_counts().sort_index()

    # Convert counts into dictionary with zero values for missing hours
    hourly_data = {h: 0 for h in range(7, 24)}
    hourly_data.update(hour_counts.to_dict())

    # Convert keys to bin labels
    x_labels = [hour_bins[h] for h in hourly_data.keys()]
    y_values = list(hourly_data.values())

    # Plot the line graph
    plt.figure(figsize=(12, 6))
    plt.plot(x_labels, y_values, marker='o', linestyle='-', color='skyblue', linewidth=2, markerfacecolor='black')

    # Add text labels for each point
    for x, y in zip(x_labels, y_values):
        plt.text(x, y, str(y), fontsize=10, ha='center', va='bottom', fontweight='bold')

    # Format the graph
    plt.xlabel("Hour of the Day", fontsize=12)
    plt.ylabel("Incident Count", fontsize=12)
    plt.title("Downtime Incidents Per Hour", fontsize=14, fontweight="bold")
    plt.xticks(rotation=45, fontsize=10)  # Rotate x-axis labels for better visibility
    plt.grid(axis='y', linestyle='--', linewidth=0.7, color='gray')

    # Show the graph
    plt.show()

    print(f"Total input times: {len(times)}")
    print(f"Total counted occurrences: {sum(y_values)}")  # Sum of all occurrences


def time_dilation(request):
    # Given dates and times
    dates = [
        '2025-02-25', '2025-02-25', '2025-02-25', '2025-02-25', '2025-02-25', '2025-02-25', '2025-02-25', '2025-02-25', '2025-02-25', '2025-02-25', 
        '2025-02-25', '2025-02-25', '2025-02-25', '2025-02-25', '2025-02-25', '2025-02-25', '2025-02-25', '2025-02-25', '2025-02-25', '2025-02-25', 
        '2025-02-25', '2025-02-25', '2025-02-25', '2025-02-25', '2025-02-25', '2025-02-25', '2025-02-25', '2025-02-25', '2025-02-25', '2025-02-24', 
        '2025-02-24', '2025-02-24', '2025-02-24', '2025-02-24', '2025-02-24', '2025-02-24', '2025-02-24', '2025-02-24', '2025-02-24', '2025-02-24', 
        '2025-02-24', '2025-02-24', '2025-02-24', '2025-02-24', '2025-02-24', '2025-02-24', '2025-02-24', '2025-02-24', '2025-02-24', '2025-02-23', 
        '2025-02-23', '2025-02-22', '2025-02-22', '2025-02-22', '2025-02-22', '2025-02-22', '2025-02-22', '2025-02-22', '2025-02-22', '2025-02-22', 
        '2025-02-22', '2025-02-22', '2025-02-22', '2025-02-22', '2025-02-22', '2025-02-22', '2025-02-22', '2025-02-22', '2025-02-22', '2025-02-22', 
        '2025-02-21', '2025-02-21', '2025-02-21', '2025-02-21', '2025-02-21', '2025-02-21', '2025-02-21', '2025-02-21', '2025-02-21', '2025-02-21', 
        '2025-02-21', '2025-02-21', '2025-02-21', '2025-02-21', '2025-02-21', '2025-02-21', '2025-02-21', '2025-02-21', '2025-02-21', '2025-02-21'
    ]

    times = [
        '19:28:25', '19:27:26', '18:45:17', '18:45:17', '18:45:16', '18:45:15', '18:45:15', '18:45:15', '18:44:16', '17:27:38', '16:49:13', 
        '16:12:51', '15:57:19', '13:56:55', '13:56:55', '13:56:55', '13:56:55', '13:56:10', '13:33:02', '12:57:18', '12:34:29', '12:26:06', 
        '09:52:46', '09:26:04', '09:19:06', '09:19:06', '09:16:41', '08:11:21', '17:32:17', '17:21:00', '13:44:12', '13:40:43', '13:40:40', 
        '13:40:14', '12:15:21', '12:08:24', '11:29:13', '11:18:16', '09:49:11', '09:08:51', '09:05:10', '08:56:42', '08:56:42', '08:56:42', 
        '08:56:42', '08:56:19', '08:56:19', '08:52:53', '09:50:39', '09:50:38', '16:51:33', '16:38:34', '16:14:48', '15:39:03', '15:02:16', 
        '14:53:06', '14:09:07', '10:46:21', '10:45:30', '09:04:56', '09:04:56', '09:04:56', '09:04:56', '09:04:56', '09:04:56', '09:04:54', 
        '09:04:24', '09:04:24', '20:51:12', '20:19:38', '17:57:22', '17:57:22', '17:57:22', '17:57:22', '17:57:22', '17:57:22', '17:56:25', 
        '17:43:52', '16:58:47', '16:38:52', '14:39:51', '14:39:27', '14:38:48', '14:36:35', '13:38:01'
    ]

   # Convert dates and times into a datetime format
    datetime_data = pd.to_datetime([f'{d} {t}' for d, t in zip(dates, times)])

    # Create a DataFrame
    df = pd.DataFrame({'Date and Time': datetime_data, 'Event Index': range(len(datetime_data))})

    # Create an interactive bar chart with darker elements
    fig = px.bar(df, x='Date and Time', y='Event Index', title="Downtime Incidents",
                labels={'Date and Time': 'Date and Time', 'Event Index': 'Incident Index'})

    # Improve layout visibility with darker elements
    fig.update_traces(marker=dict(line=dict(color='black', width=2)))  # Darker bar borders

    fig.update_layout(
        xaxis=dict(
            tickangle=-45, 
            tickmode='auto', 
            gridcolor='black',  # Darker gridlines
            griddash='dot'
        ),
        yaxis=dict(
            gridcolor='black',  # Darker gridlines
            griddash='dot'
        ),
        yaxis_title="Incident Count",
        xaxis_title="Date and Time",
        margin=dict(l=50, r=50, t=50, b=150),
        bargap=0.2,
        height=600,
        width=1200,
        font=dict(family="Arial, sans-serif", size=14, color="black"),  # Darker & bolder font
    )

    # Show the figure   
    fig.show()

def accurate(request):
    times = [
        '16:56:04', '16:55:56', '16:45:35', '16:34:36', '16:24:41', '16:24:41', '16:13:49', '15:41:54', '15:41:41', '15:18:55', 
        '14:44:38', '14:43:36', '14:43:21', '14:30:24', '14:26:02', '14:24:37', '14:18:58', '14:17:02', '14:14:30', '14:09:01', 
        '14:08:48', '14:06:46', '14:00:28', '14:00:10', '14:00:02', '13:59:04', '13:58:40', '13:58:24', '13:57:22', '13:57:19', 
        '13:42:14', '12:45:46', '11:27:43', '11:27:43', '11:27:33', '11:27:21', '11:27:02', '11:26:43', '11:16:08', '11:15:56', 
        '11:14:35', '11:14:23', '11:14:19', '11:14:18', '09:22:33', '09:22:23', '09:20:30', '08:53:54', '08:53:53', '16:10:04', 
        '16:10:04', '16:10:04', '16:10:04', '16:10:03', '16:09:55', '15:39:57', '15:29:25', '15:21:51', '15:21:42', '13:41:20', 
        '12:18:09', '08:56:53', '17:12:11', '13:48:07', '13:48:07', '13:48:07', '10:25:22', '09:02:02', '09:02:02', '09:02:02', 
        '09:02:02', '09:02:02', '09:02:00', '09:01:34', '08:59:40', '08:45:39', '08:41:50', '07:57:48', '19:28:25', '19:27:26', 
        '18:45:17', '18:45:17', '18:45:16', '18:45:15', '18:45:15', '18:45:15', '18:44:16', '17:27:38', '16:49:13', '16:12:51', 
        '15:57:19', '13:56:55', '13:56:55', '13:56:55', '13:56:55', '13:56:10', '13:33:02', '12:57:18', '12:34:29', '12:26:06', 
        '09:52:46', '09:26:04', '09:19:06', '09:19:06', '09:16:41', '08:11:21', '17:32:17', '17:21:00', '13:44:12', '13:40:43', 
        '13:40:40', '13:40:14', '12:15:21', '12:08:24', '11:29:13', '11:18:16', '09:49:11', '09:08:51', '09:05:10', '08:56:42', 
        '08:56:42', '08:56:42', '08:56:42', '08:56:19', '08:56:19', '08:52:53', '09:50:39', '09:50:38', '16:51:33', '16:38:34', 
        '16:14:48', '15:39:03', '15:02:16', '14:53:06', '14:09:07', '10:46:21', '10:45:30', '09:04:56', '09:04:56', '09:04:56', 
        '09:04:56', '09:04:56', '09:04:56', '09:04:54', '09:04:24', '09:04:24', '20:51:12', '20:19:38', '17:57:22', '17:57:22', 
        '17:57:22', '17:57:22', '17:57:22', '17:57:22', '17:56:25', '17:43:52', '16:58:47', '16:38:52', '14:39:51', '14:39:27'
    ]

    # Convert times into full datetime format (assuming same day)
    time_series = [datetime.strptime(t, "%H:%M:%S") for t in times]

    # Sort times chronologically
    time_series.sort()

    # Count occurrences of each exact time
    time_counts = pd.Series(time_series).value_counts().sort_index()

    # Plot the line graph
    plt.figure(figsize=(12, 6))
    plt.plot(time_counts.index, time_counts.values, marker='o', linestyle='-', color='skyblue', linewidth=2, markerfacecolor='black')

    # Format x-axis to show time properly
    plt.xticks(rotation=45, ha='right')  # Rotate for better visibility
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%H:%M"))  # Format as HH:MM

    # Format the graph
    plt.xlabel("Time of the Day", fontsize=12)
    plt.ylabel("Incident Count", fontsize=12)
    plt.title("Downtime Incidents Over Time", fontsize=14, fontweight="bold")
    plt.grid(axis='y', linestyle='--', linewidth=0.7, color='gray')

    # Show the graph
    plt.show()

def latest(request):
    times = [
        "13:50:21", "13:50:21", "9:17:19", "9:17:19", "13:50:57", "9:03:16", "13:48:46", "10:42:13", 
        "21:26:15", "17:27:14", "17:27:14", "17:27:14", "17:27:14", "14:01:20", "12:40:13", "12:25:43", 
        "12:25:43", "8:49:00", "8:49:00", "13:53:11", "13:53:11", "13:53:11", "13:53:11", "13:53:11", 
        "11:46:27", "9:11:58", "9:11:58", "14:13:41", "14:13:41", "10:52:14", "10:24:57", "7:33:47", 
        "15:49:21", "15:49:21", "9:19:08", "9:19:08", "15:37:48", "9:41:43", "8:45:43", "14:25:12", 
        "14:25:12", "13:50:40", "11:35:48", "11:27:49", "9:28:42"
    ]

    # Convert times into datetime format and extract hours
    hours = [datetime.strptime(time, "%H:%M:%S").hour for time in times]

    # Define hourly bins with AM/PM format
    def format_hour(hour):
        start_hour = hour if hour <= 12 else hour - 12
        end_hour = hour + 1 if (hour + 1) <= 12 else (hour + 1) - 12
        suffix = "AM" if hour < 12 else "PM"
        return f"{start_hour}-{end_hour} {suffix}"

    hour_bins = {h: format_hour(h) for h in range(7, 24)}  # Creating labels for the bins

    # Count occurrences per hour
    hour_counts = pd.Series(hours).value_counts().sort_index()

    # Convert counts into dictionary with zero values for missing hours
    hourly_data = {h: 0 for h in range(7, 24)}
    hourly_data.update(hour_counts.to_dict())

    # Convert keys to bin labels
    x_labels = [hour_bins[h] for h in hourly_data.keys()]
    y_values = list(hourly_data.values())

    # Plot the line graph
    plt.figure(figsize=(12, 6))
    plt.plot(x_labels, y_values, marker='o', linestyle='-', color='skyblue', linewidth=2, markerfacecolor='black')

    # Add text labels for each point
    for x, y in zip(x_labels, y_values):
        plt.text(x, y, str(y), fontsize=10, ha='center', va='bottom', fontweight='bold')

    # Format the graph
    plt.xlabel("Hour of the Day", fontsize=12)
    plt.ylabel("Incident Count", fontsize=12)
    plt.title("Downtime Incidents Per Hour", fontsize=14, fontweight="bold")
    plt.xticks(rotation=45, fontsize=10)  # Rotate x-axis labels for better visibility
    plt.grid(axis='y', linestyle='--', linewidth=0.7, color='gray')

    # Show the graph
    plt.show()


