import time
import sched
import Services.IoTDevice as IoT
import Services.Store as Store
import Services.Heater as Heater


def store_schedule(scheduler, time_step, url):
    # schedule the next call first
    scheduler.enter(time_step * 60, 1, store_schedule, (scheduler, time_step, url,))
    # then do your stuff
    json_data = IoT.get_temperature(url)
    if json_data is not None:
        Store.store_at_desktop("{},{}".format(json_data["date"], json_data["temp"]))


def store_data(time_step, url):
    my_scheduler = sched.scheduler(time.time, time.sleep)
    my_scheduler.enter(time_step * 60, 1, store_schedule, (my_scheduler, time_step, url))
    my_scheduler.run()


def do_action(action, action_device_ip):
    if "heater" in action.name.lower():
        response = Heater.switch("http://" + action_device_ip + action.endpoint)
        if response is not None:
            return True
    return False


def compare_schedule(scheduler, condition, condition_device_ip, condition_value, condition_type_value,
                     action, action_device_ip):
    if condition.name == "Temperature":
        json_data = IoT.get_temperature("http://" + condition_device_ip + condition.endpoint)
        if json_data is not None:
            can_do_action = False
            temperature = float(json_data["temp"].split(" ")[0])
            if condition_type_value == "LT":
                if temperature < float(condition_value):
                    can_do_action = True
            elif condition_type_value == "LE":
                if temperature <= float(condition_value):
                    can_do_action = True
            elif condition_type_value == "GR":
                if temperature > float(condition_value):
                    can_do_action = True
            elif condition_type_value == "GE":
                if temperature >= float(condition_value):
                    can_do_action = True
            elif condition_type_value == "EQ":
                if temperature == float(condition_value):
                    can_do_action = True

            if can_do_action:
                do_action(action, action_device_ip)

    scheduler.enter(30, 1, compare_schedule,
                    (scheduler, condition, condition_device_ip, condition_value, condition_type_value,
                     action, action_device_ip))


def compare_data(condition, condition_device_ip, condition_value, condition_type_value,
                 action, action_device_ip):
    my_scheduler = sched.scheduler(time.time, time.sleep)
    my_scheduler.enter(30, 1, compare_schedule,
                       (my_scheduler, condition, condition_device_ip, condition_value, condition_type_value,
                        action, action_device_ip))
    my_scheduler.run()


def presence_schedule(scheduler, condition, condition_device_ip, condition_value,
                      action, action_device_ip):
    if condition.name == "Presence Detection":
        response = IoT.presence_detection("http://" + condition_device_ip + condition.endpoint)
        if response is not None:
            if response == condition_value:
                do_action(action, action_device_ip)


    scheduler.enter(30, 1, presence_schedule,
                    (scheduler, condition, condition_device_ip, condition_value,
                     action, action_device_ip))


def presence_detection(condition, condition_device_ip, condition_value,
                       action, action_device_ip):
    my_scheduler = sched.scheduler(time.time, time.sleep)
    my_scheduler.enter(30, 1, presence_schedule,
                       (my_scheduler, condition, condition_device_ip, condition_value,
                        action, action_device_ip))
    my_scheduler.run()
