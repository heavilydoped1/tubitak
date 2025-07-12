import os
import time
import serial
import threading
import subprocess

SERIAL_PORT = '/dev/ttyUSB0'  # LoRa'nın bağlı olduğu port
BAUD_RATE = 9600
CSV_FILENAME = 'output.csv'

def start_rtl_power(csv_filename):
    command = f"rtl_power -f 446.300M:446.600M:1k -i 5s {csv_filename}"
    return subprocess.Popen(command, shell=True)

def read_last_line(csv_filename):
    try:
        with open(csv_filename, 'r') as file:
            lines = file.readlines()
            if lines:
                return lines[-1]
    except Exception as e:
        print(f"[read_last_line HATA] {e}")
    return None

def rtl_power_reader(csv_filename, ser):
    last_sent_power = None
    while True:
        last_line = read_last_line(csv_filename)
        if last_line:
            parts = last_line.strip().split(',')
            try:
                # İlk 5 sütunu atla, geri kalanlar dBm değerleri
                dbm_values = [float(p) for p in parts[5:] if p.strip() != '']
                if not dbm_values:
                    continue

                max_power = max(dbm_values)

                # Yalnızca değişen güç değeri gönderilir
                if last_sent_power is None or max_power != last_sent_power:
                    last_sent_power = max_power
                    msg = f"{max_power:.2f}"
                    ser.write((msg + '\r\n').encode('utf-8'))
                    print(f"[GÖNDERİLDİ - LoRa] Max Güç: {msg} dBm")

            except Exception as e:
                print(f"[Veri işleme hatası] {e}")
        time.sleep(5)

def main():
    try:
        # Seri port açılıyor
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"[SERİ PORT AÇILDI] {SERIAL_PORT} @ {BAUD_RATE} baud")

        # rtl_power başlatılıyor
        rtl_proc = start_rtl_power(CSV_FILENAME)
        print("[rtl_power BAŞLATILDI]")

        # Okuma thread'i başlatılıyor
        t = threading.Thread(target=rtl_power_reader, args=(CSV_FILENAME, ser), daemon=True)
        t.start()

        print("Çıkmak için Ctrl+C bas")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[PROGRAM DURDURULUYOR]")
        try:
            rtl_proc.terminate()
            print("[rtl_power DURDURULDU]")
        except:
            pass
    except Exception as e:
        print(f"[ANA HATA] {e}")

if __name__ == '__main__':
    main()
