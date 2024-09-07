import os
import time
import json
import subprocess

def start_rtl_power(csv_filename):
    command = f"rtl_power -f 446.449M:446.451M:1k -g 20 -i 3s {csv_filename}"
    process = subprocess.Popen(command, shell=True)
    return process

def read_last_line(csv_filename):
    try:
        with open(csv_filename, 'r') as file:
            lines = file.readlines()
            if lines:
                return lines[-1]
    except FileNotFoundError:
        pass

    return None

def rtl_output(csv_filename):
    power = None
    while True:
        last_line = read_last_line(csv_filename)
        if last_line:
            parts = last_line.strip().split(',')
            try:
                powerdb = float(parts[7].replace(' db', ''))
                if power is None or powerdb > power:
                    power = powerdb
                    data = {'power': power}
            except (IndexError, ValueError):
                continue

        time.sleep(1)

if __name__=="__main__":
    script_dir = os.path.dirname(os.path.realpath(__file__))
    csv_filename = os.path.join(script_dir, "output.csv")
    rtl_power_process = start_rtl_power(csv_filename)
    try:
        rtl_output(csv_filename)
    except KeyboardInterrupt:
        rtl_power_process.terminate()
        print("\nrtl_power durduruldu.")
