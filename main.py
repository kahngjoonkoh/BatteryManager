from psutil import sensors_battery
from time import time, sleep, ctime
import sched
import ctypes

s = sched.scheduler(time, sleep)


def main():
    if not hlt():
        battery_check()
    else:
        pass


def hlt():
    with open("log.txt", 'r') as f:
        if f.read(3) == 'hlt':
            f.close()
            return True
        else:
            f.close()
            return False


def battery_check():
    battery = sensors_battery()
    percent = int(battery.percent)
    plugged = battery.power_plugged

    if percent >= 80 and plugged:
        ctypes.windll.user32.MessageBoxW(0, f"Battery is {percent}%. Unplug charger for best battery life",
                                         "Battery Manager", 0)
    battery_log(percent, plugged)
    s.enter(300, 1, main)


def battery_log(percent, plugged):
    with open("log.txt", 'a') as f:
        f.write("\n| {0:^24} |{1:^4}% | {2:^12} |".format(str(ctime(time())), percent,
                                                          "Charging" if plugged else "Not Charging"))
        f.close()


s.enter(0, 1, main)
s.run()
