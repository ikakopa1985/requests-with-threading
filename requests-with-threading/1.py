import threading
import requests
import time
import random
import json

class CustomThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(CustomThread, self).__init__(*args, **kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        super(CustomThread, self).join()
        return self._return


def requestUrl(url):
    response = requests.get(url)
    response_text = response.content.decode('utf-8')
    return json.loads(response_text)

startTime = time.perf_counter()
print('\n'*40)
url = 'https://dummyjson.com/products/'
th = []
results = []

for item in range(0,100):
    th.append(CustomThread(target=requestUrl, args=((url + str(item+1)),)))
    th[item].start()

for item in range(0,100):
    res = th[item].join()
    results.append(res)

with open('response.json', 'w') as json_file:
    json.dump(results, json_file)

with open('response.json', 'r') as json_file:
    json_data = json_file.read()
    parsed_data = json.loads(json_data)
    print(parsed_data)

print()
finish = time.perf_counter()
print(f'Done!  in  {finish - startTime}s')