import requests
import threading
import random
import psutil
import time
import keyboard

url = input("Enter the URL to send requests to: ")

field_names = input("Enter the field names separated by commas: ").split(",")

def generate_random_data():
    return {
        field_name.strip(): str(random.randint(1, 1000))
        for field_name in field_names
    }

num_requests = 0

def do_request():
    data = generate_random_data()
    try:
        response = requests.post(url, data=data).text
        if len(response) <= 100:
            print(response + "\n")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}. \n Time-outed by website. Sleeping for 10 seconds and then retrying...")
        time.sleep(10)

threads = []
    
while True:
    cpu_percent = psutil.cpu_percent()
    if cpu_percent < 50:
        num_threads = 50
    elif cpu_percent < 75:
        num_threads = 25
    else:
        num_threads = 10

    while len(threads) < num_threads:
        t = threading.Thread(target=do_request)
        t.daemon = True
        threads.append(t)
        t.start()

    while len(threads) > num_threads:
        threads.pop().join()