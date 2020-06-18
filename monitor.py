import config
import argparse
import psutil
import telebot  # install pytelegrambotapi
import time
from time import sleep


def get_load_by_pid(pid_num):
    try:
        process = psutil.Process(pid_num)
    except psutil.NoSuchProcess:
        print('No process with PID ' + str(pid_num))
    except psutil.AccessDenied:
        print('Access denied to the process with PID ' + str(pid_num))
    else:
        return process.cpu_percent()


def main():
    cmd_parser = argparse.ArgumentParser(description='Monitoring script')
    cmd_parser.add_argument("-p", type=int, action="store", dest="pid", required=True, help="Process ID to be checked")
    cmd_parser.add_argument("-t", type=int, action="store", dest="th", default=50, help="Threshold for CPU load")
    cmd_parser.add_argument("-i", type=int, action="store", dest="interval", default=3, help="Update interval")

    args = cmd_parser.parse_args()
    pid = args.pid
    th = args.th
    interval = args.interval

    monitor(pid, th, interval)


def monitor(pid, th, interval):
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

    while True:
        # Get percent of CPU load and compare it with threshold
        load = get_load_by_pid(pid)
        if load != -1:
            print('pid = ' + str(pid) + '  load = ' + str(load))
            if int(load) > th:
                # Send massage to telegram bot with percentage of load and PID
                bot.send_message(config.chat_id, 'pid = ' + str(pid) + '  load = ' + str(load))
        # Sleep some time
        time.sleep(interval)


if __name__ == '__main__':
    main()
