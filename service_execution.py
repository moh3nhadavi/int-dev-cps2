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


def do_action(action, action_device):
    if "heater" in action.name.lower():
        response = Heater.switch("http://" + action_device.ip + action.endpoint)
        if response is not None:
            return True
    return False


def compare_schedule(scheduler, condition, condition_device, condition_value, condition_type_value,
                     action, action_device):
    did_action = False
    if condition.name == "Temperature":
        json_data = IoT.get_temperature("http://" + condition_device.ip + condition.endpoint)
        if json_data is not None:
            can_do_action = False
            if condition_type_value == "LT":
                if json_data["temp"] < condition_value:
                    can_do_action = True
            elif condition_type_value == "LE":
                if json_data["temp"] <= condition_value:
                    can_do_action = True
            elif condition_type_value == "GR":
                if json_data["temp"] > condition_value:
                    can_do_action = True
            elif condition_type_value == "GE":
                if json_data["temp"] >= condition_value:
                    can_do_action = True
            elif condition_type_value == "EQ":
                if json_data["temp"] == condition_value:
                    can_do_action = True

            if can_do_action:
                if do_action(action, action_device):
                    did_action = True
    if not did_action:
        scheduler.enter(60, 1, compare_schedule,
                        (scheduler, condition, condition_device, condition_value, condition_type_value,
                         action, action_device))


def compare_data(condition, condition_device, condition_value, condition_type_value,
                 action, action_device):
    my_scheduler = sched.scheduler(time.time, time.sleep)
    my_scheduler.enter(60, 1, compare_schedule,
                       (my_scheduler, condition, condition_device, condition_value, condition_type_value,
                        action, action_device))
    my_scheduler.run()
