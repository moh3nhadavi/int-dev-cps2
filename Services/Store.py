import os
import time
import sched, json
from sys import platform
import Services.IoTDevice as IoT


def store_at_desktop(text):
    if platform == "win32":
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    else:
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')

    csv_file_path = os.path.join(desktop, 'cps2.csv')

    if not os.path.isfile(csv_file_path):
        with open(csv_file_path, 'w') as csv_file:
            csv_file.write('{}\n'.format(text))

    else:
        with open(csv_file_path, 'a') as csv_file:
            csv_file.write('{}\n'.format(text))


def schedule(scheduler, time_step, url):
    # schedule the next call first
    scheduler.enter(time_step * 10, 1, schedule, (scheduler, time_step, url,))
    # then do your stuff
    json_data = IoT.get_temperature(url)
    if json_data is not None:
        json_data = json.loads(json_data)
        # print(json_data)
        store_at_desktop("{},{}".format(json_data["date"], json_data["temp"]))


def store_data(time_step, url):
    my_scheduler = sched.scheduler(time.time, time.sleep)
    my_scheduler.enter(time_step * 10, 1, schedule, (my_scheduler, time_step, url))
    my_scheduler.run()
