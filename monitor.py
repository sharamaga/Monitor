import config
import argparse
import psutil
import telebot  # install pytelegrambotapi
import time
from time import sleep


def get_load_by_pid(pid_num):
    if psutil.pid_exists(pid_num):
        if psutil.Process(pid_num).is_running():
            try:
                process = psutil.Process(pid_num)
            except process.AccessDenied:
                print('Access denied to the process with PID ' + str(pid_num))
            else:
                return process.cpu_percent()
        else:
            print('Process with PID ' + str(pid_num) + ' is not running')
    else:
        print('Process with PID ' + str(pid_num) + ' do not exists')

    return -1


def parse_cmd():
    out_dict = {}
    cmd_parser = argparse.ArgumentParser(description='Monitoring script')
    cmd_parser.add_argument("-p", type=int, action="store", dest="pid", required=True, help="Process ID to be checked")
    cmd_parser.add_argument("-t", type=int, action="store", dest="th", default=50, help="Threshold for CPU load")
    cmd_parser.add_argument("-i", type=int, action="store", dest="interval", default=3, help="Update interval")

    args = cmd_parser.parse_args()
    out_dict['p'] = args.pid
    out_dict['t'] = args.th
    out_dict['i'] = args.interval

    return out_dict


def monitoring():
    # Create bot
    try:
        bot = telebot.TeleBot(config.token)
    except BaseException:
        print('Attempt to start Telegram bot is fail, check token')
        return

    # Attempt to send something to Telegram bot to check that chat.id is correct
    try:
        bot.send_message(config.chat_id, 'This is test message, if you see it Telegram, bot works perfect')
    except BaseException:
        print('Chat ID is incorrect, set proper chat_id')
        return

    # Get input from command line
    config_dict = parse_cmd()

    # main loop
    while True:
        # Get percent of CPU load and compare it with threshold
        load = get_load_by_pid(config_dict.get('p'))
        if load != -1:
            print('pid = ' + str(config_dict.get('p')) + '  load = ' + str(load))
            if int(load) > config_dict.get('t'):
                # Send massage to telegram bot with percentage of load and PID
                bot.send_message(config.chat_id, 'pid = ' + str(config_dict.get('p')) + '  load = ' + str(load))
        # Sleep some time
        time.sleep(config_dict.get('i'))


if __name__ == '__main__':
    monitoring()
