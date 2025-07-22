import os
import time
import subprocess
import serial

def start_rtl_power(csv_filename):
    command = f"rtl_power -f 446.300M:446.600M:1k -i 5s {csv_filename}"
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

def parse_max_power_from_line(line):
    try:
        parts = line.strip().split(',')
        dbm_values = [float(val.strip().replace(' dbm', '')) for val in parts[6:] if val.strip()]
        if dbm_values:
            return max(dbm_values)
    except Exception as e:
        print(f"Veri ayrıştırma hatası: {e}")
    return None

# LoRa seri bağlantı (örnek)
lora = serial.Serial('/dev/ttyUSB0', 9600)

def send_to_lora(data):
    lora.write(f"{data:.2f} dBm\n".encode())
    print(f"LoRa'ya gönderildi: {data:.2f} dBm")

def rtl_output(csv_filename):
    max_power = None
    while True:
        last_line = read_last_line(csv_filename)
        if last_line:
            powerdb = parse_max_power_from_line(last_line)
            if powerdb is not None and (max_power is None or powerdb > max_power):
                max_power = powerdb
                send_to_lora(max_power)
        time.sleep(1)

if __name__ == "__main__":
    csv_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "output.csv")
    rtl_power_process = start_rtl_power(csv_filename)
    try:
        rtl_output(csv_filename)
    except KeyboardInterrupt:
        rtl_power_process.terminate()
        print("\nrtl_power durduruldu.")
