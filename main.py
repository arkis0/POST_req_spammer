import requests
import threading
import time
import urllib.parse
import random

requests_sent = 0

def post_generate_random_data():
    data = {name: value for name, value in fixed_params.items()}
    data.update({name: str(random.randint(1, 1000)) for name in random_params})
    return data

def get_generate_random_data():
    query_params = urllib.parse.parse_qs(parsed_url.query)
    query_params.update({name: [str(random.randint(1, 1000))] for name in random_params})
    query_params.update({name: [value] for name, value in fixed_params.items()})
    new_query_string = urllib.parse.urlencode(query_params, doseq=True)
    new_url = urllib.parse.urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query_string, parsed_url.fragment))
    return new_url

def do_post_request():
    data = post_generate_random_data()
    try:
        response = requests.post(url, data=data)
        if 200 <= response.status_code < 300:
            print(f"[{requests_sent}] Response code: {response.status_code}\n")
        else:
            print(f"Error: {response.status_code}\n")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}. \n Timed out by website. Sleeping for 10 seconds and then retrying...")
        time.sleep(10)
        
def do_get_request():
    new_url = get_generate_random_data()
    try:
        response = requests.get(new_url)
        if 200 <= response.status_code < 300:
            print(f"[{requests_sent}] Response code: {response.status_code}\n")
        else:
            print(f"Error: {response.status_code}\n")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}. \n Timed out by website. Sleeping for 10 seconds and then retrying...\n")
        time.sleep(10)

def run_post_method():
    global requests_sent
    while True:
        threads = []
        for i in range(num_threads):
            t = threading.Thread(target=do_post_request)
            t.daemon = True
            threads.append(t)
        for i in range(num_threads):
            threads[i].start()
        for i in range(num_threads):
            threads[i].join()
        requests_sent += num_threads
        
def run_get_method():
    global requests_sent
    while True:
        threads = []
        for i in range(num_threads):
            t = threading.Thread(target=do_get_request)
            t.daemon = True
            threads.append(t)
        for i in range(num_threads):
            threads[i].start()
        for i in range(num_threads):
            threads[i].join()
        requests_sent += num_threads

chosen_method = input("Enter the method to use (GET or POST): ")
num_threads = int(input("Enter the number of threads to use (suggested 50): "))

fixed_params = {}
while True:
    param_name = input("Enter fixed parameter name (press enter to stop): ")
    if not param_name:
        break
    param_value = input("Enter fixed parameter value: ")
    fixed_params[param_name] = param_value

random_params = input("Enter the random parameter names, separate them by commas: ").split(",")

if chosen_method.lower() == "post":
    url = input("Enter the URL to send POST requests to: ")
    run_post_method()
elif chosen_method.lower() == "get":
    url = input("Enter the URL to send GET requests to: ")
    parsed_url = urllib.parse.urlparse(url)
    run_get_method()
else:
    input("Invalid method. Press any button to exit.")