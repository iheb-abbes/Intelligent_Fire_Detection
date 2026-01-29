import requests

class CommunicationModule:
    def __init__(self, pi_ip):
        self.url = f"http://{pi_ip}:5000/buzzer"

    def send_alert(self, status):
        """
        Sends HTTP requests to the remote Raspberry Pi.
        status: "on" or "off"
        
        """
        try:
            response = requests.post(self.url, json={"action": status}, timeout=2)
            return response.status_code == 200
        except Exception as e:
            print(f"Communication Error: {e}")
            return False