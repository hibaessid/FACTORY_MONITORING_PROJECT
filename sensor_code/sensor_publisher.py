import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

sensor_pin = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_pin, GPIO.IN)

counter = 0
t = None
broker_address = "test.mosquitto.org"
client_id = "raspberry_pi_client"

def on_message(client, userdata, message):
    pass

def on_publish(client, userdata, mid):
    print(f"Message {mid} published successfully.")

client = mqtt.Client(client_id)
client.on_message = on_message
client.on_publish = on_publish

try:
    client.connect(broker_address)
    client.loop_start()

    while True:
        if GPIO.input(sensor_pin) == GPIO.LOW:
            time.sleep(0.4)
            if counter == 0:
                t = time.time()

            counter += 1
            result = client.publish("sensor/partCount", str(counter))
            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                print("Failed to publish partCount.")
            else:
                print(counter)

            progress = (counter / 10) * 100
            result = client.publish("sensor/progress", str(progress))
            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                print("Failed to publish progress.")
            else:
                print(progress)

            total_time = time.time() - t
            result = client.publish("sensor/preparationTime", str(total_time))
            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                print("Failed to publish preparationTime.")
            else:
                print(total_time)

            if counter == 10:
                counter = 0

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()
    client.loop_stop()
    client.disconnect()