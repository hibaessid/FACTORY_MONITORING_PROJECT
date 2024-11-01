from flask import Flask, jsonify, render_template
import paho.mqtt.client as mqtt
import threading
import logging

app = Flask(__name__)

# MQTT Broker Configuration
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883

# MQTT Topics
TOPIC_PART_COUNT = "sensor/partCount"
TOPIC_PREP_TIME = "sensor/preparationTime"
TOPIC_PROGRESS = "sensor/progress"

# Shared data storage with a lock for thread safety
sensor_data = {
    "partCount": 0,
    "preparationTime": 0,
    "progress": 0
}
data_lock = threading.Lock()

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Callback functions to update each value when new data is received
def on_part_count(client, userdata, message):
    with data_lock:
        sensor_data["partCount"] = int(message.payload.decode())
    logging.info(f"Updated partCount: {sensor_data['partCount']}")

def on_preparation_time(client, userdata, message):
    with data_lock:
        sensor_data["preparationTime"] = float(message.payload.decode())
    logging.info(f"Updated preparationTime: {sensor_data['preparationTime']}")

def on_progress(client, userdata, message):
    with data_lock:
        sensor_data["progress"] = float(message.payload.decode())
    logging.info(f"Updated progress: {sensor_data['progress']}")

# Setup MQTT Client
def mqtt_thread():
    client = mqtt.Client()
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT)
        logging.info("Connected to MQTT broker at test.mosquitto.org")
    except Exception as e:
        logging.error(f"Failed to connect to MQTT broker: {e}")
        return

    # Subscribe to each topic and assign a specific callback
    client.message_callback_add(TOPIC_PART_COUNT, on_part_count)
    client.message_callback_add(TOPIC_PREP_TIME, on_preparation_time)
    client.message_callback_add(TOPIC_PROGRESS, on_progress)
    
    client.subscribe(TOPIC_PART_COUNT)
    client.subscribe(TOPIC_PREP_TIME)
    client.subscribe(TOPIC_PROGRESS)
    
    logging.info("MQTT client connected and subscribed to topics.")
    client.loop_forever()

# Start the MQTT client in a separate thread
threading.Thread(target=mqtt_thread).start()

# Flask endpoint to retrieve sensor data in HTML format
@app.route('/')
def index():
    with data_lock:
        data_copy = sensor_data.copy()
    return render_template('index.html', sensor_data=data_copy)

# New Flask endpoint to retrieve sensor data in JSON format
@app.route('/api/sensor-data', methods=['GET'])
def get_sensor_data():
    with data_lock:
        data_copy = sensor_data.copy()
    return jsonify(data_copy)

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
