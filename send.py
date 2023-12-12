from datetime import datetime
import requests

current_datetime = datetime.now()

formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
IP = "172.31.107.255"
user = "Mike Banabila"
machine = "MacBook Pro"
msi = 14.8e9


# Specify the target IP address and endpoint
target_ip = "127.0.0.1:5000"
endpoint = "/collect"

post_data = {
    "machine_name": machine,
    "msi_usage": msi,
    "I.P": IP,
    "user": user,
    "time" : formatted_datetime
}

url = f"http://{target_ip}{endpoint}"

response = requests.post(url, data=post_data)

if response.status_code == 200:
    print("POST request successful!")
    
    # Print specific fields from the response
    print("Response Status Code:", response.status_code)
    print("Response Headers:", response.headers)
    print("Response Content:", response.text)
else:
    print(f"POST request failed with status code {response.status_code}")
    print("Response Content:", response.text)
