# Factory Monitoring Project

## Overview

The **Factory Monitoring Project** is a real-time monitoring system designed to track the progress and efficiency of part processing in a factory environment. This system uses proximity sensors to detect parts, calculates preparation time, and displays progress. The data is visualized on a dashboard, providing valuable insights for operators.

## Features

- **Real-time Part Detection**: Uses proximity sensors to detect each part on the factory line.
- **Preparation Time Calculation**: Measures and displays the preparation time for each part.
- **Progress Tracking**: Shows progress as a percentage on a dashboard.
- **Threshold Alerts**: Displays an emoji and alert message when a specified threshold is reached.

## Technologies Used

- **Hardware**:
  - Raspberry Pi: Acts as an MQTT broker.
  - Proximity Sensor: Detects parts and provides input data.
- **Software**:
  - **Flask**: Backend framework to create APIs for data handling and processing.
  - **MQTT**: Protocol used for efficient real-time data transfer.
  - **JavaScript (Frontend)**: Handles real-time data fetching and dynamically displays information.
  - **HTML/CSS**: Frontend structure and styling for the dashboard.

## Project Structure

```plaintext
factory_monitoring_project/
│
├── backend/
│   └── app.py                # Flask backend application
│
├── sensor_code/
│   └── sensor_publisher.py    # Sensor data publisher running on Raspberry Pi
│
├── static/
│   ├── script.js              # JavaScript file for frontend logic
│   └── styles.css             # CSS file for styling the dashboard
│
├── templates/
│   └── index.html             # HTML file for the dashboard
│
└── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
