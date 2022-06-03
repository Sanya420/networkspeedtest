import speedtest
import time
import psutil
import logging

##logging.basicConfig(filename='netspd.log', level=logging.DEBUG, format='%(asctime)s:%(message)s')

formatter = logging.Formatter('%(asctime)s:%(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('net.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def spd_test():
    spd = speedtest.Speedtest()
    spd.get_best_server()

    print(f"Ping: {spd.results.ping} ms")
    print(f"Download speed: {round(spd.download() / 1000 / 1000, 1)} Mbit/s")
    print(f"Upload speed: {round(spd.upload() / 1000 / 1000, 1)} Mbit/s")

    logger.debug(f"Ping: {spd.results.ping} ms")
    logger.debug(f"Download speed: {round(spd.download() / 1000 / 1000, 1)} Mbit/s")
    logger.debug(f"Upload speed: {round(spd.upload() / 1000 / 1000, 1)} Mbit/s")


def bnd_width():
    last_recevied = psutil.net_io_counters().bytes_recv
    last_sent = psutil.net_io_counters().bytes_sent
    last_total = last_recevied + last_sent

    while True:
        bytes_received = psutil.net_io_counters().bytes_recv
        bytes_sent = psutil.net_io_counters().bytes_sent
        bytes_total = bytes_received + bytes_sent

        new_r = bytes_received - last_recevied
        new_s = bytes_sent - last_sent
        new_t = bytes_total - last_total

        mb_new_r = new_r / 1024 / 1024
        mb_new_s = new_s / 1024 / 1024
        mb_new_t = new_t / 1024 / 1024

        print(f"{mb_new_r:.2f} MB download, {mb_new_s:.2f} MB upload, {mb_new_t:.2f} MB total")

        last_recevied = bytes_received
        last_sent = bytes_sent
        last_total = bytes_total

        time.sleep(1)

def main():
    spd_test()
    bnd_width()


if __name__ == '__main__':
    main()
