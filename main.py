import requests
import threading
import time
import urllib.parse
import random
field_names = 'null'

def post_generate_random_data():
    return {
        field_name.strip(): str(random.randint(1, 1000))
        for field_name in field_names
    }

def do_post_request():
    data = post_generate_random_data()
    try:
        response = requests.post(url, data=data).text
        if len(response) <= 400:
            print(response + "\n")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}. \n Time-outed by website. Sleeping for 10 seconds and then retrying...")
        time.sleep(10)
        
def do_get_request():
    query_params = urllib.parse.parse_qs(parsed_url.query)
    for key in query_params:
        query_params[key] = [str(random.randint(1, 1000))]

    new_query_string = urllib.parse.urlencode(query_params, doseq=True)
    new_url = urllib.parse.urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query_string, parsed_url.fragment))

    try:
        response = requests.get(new_url).text
        if len(response) <= 400:
            print(response + "\n")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}. \n Time-outed by website. Sleeping for 10 seconds and then retrying...")
        time.sleep(10)

def run_post_method():
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
            
def run_get_method():
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


chosen_method = input("Enter the method to use (GET or POST): ")
if chosen_method == "POST" or chosen_method == "post":
    url = input("Enter the URL to send requests to: ")
    field_names = input("Enter the field names separated by commas: ").split(",")
    num_threads = int(input("Enter the number of threads to use(suggested 50): "))
    run_post_method()
elif chosen_method == "GET" or chosen_method == "get":
    url = input("Enter the URL to send requests to: ")
    parsed_url = urllib.parse.urlparse(url)
    num_threads = int(input("Enter the number of threads to use: "))
    run_get_method()
else:
    print("Invalid method. Exiting...")
    exit()