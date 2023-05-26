
import time;

def time_now():
    time_now_attribute = time.localtime(time.time());
    return str(time_now_attribute[0]) + str(time_now_attribute[1]) + str(time_now_attribute[2]) + '_' + str(time_now_attribute[3]) + str(time_now_attribute[4]) + str(time_now_attribute[5]);
