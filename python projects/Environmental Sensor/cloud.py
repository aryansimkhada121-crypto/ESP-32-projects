import json
import urequests

class Cloud():
    def __init__(self, username, aio_key):
        self.username = username
        self.headers = {'X-AIO-Key': aio_key, 'Content-Type': 'application/json'}

    def send_values(self, feed_name, value ):
        url = f"http://io.adafruit.com/api/v2/{self.username}/feeds/{feed_name}/data"
        payload = {"value": value}
        try:
            response = urequests.post(url, json=payload, headers=self.headers)
            response.close()
            return True
        except Exception as e:
            print(f"Failed to send to {feed_name}: {e}")
            return False

    def send_all(self, moisture, temp, humidity, light):
        self.send_values("plant-moisture", moisture)
        self.send_values("plant-temp", temp)
        self.send_values("plant-humidity", humidity)
        self.send_values("plant-light", light)
        print("All sensor metrics pushed to Adafruit IO successfully!")