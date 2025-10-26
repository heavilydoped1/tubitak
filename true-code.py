from rtlsdr import RtlSdr
import numpy as np
import serial
import time

NODE_ID = 2
SLOT_LENGTH = 0.5
CYCLE_LENGTH = 4 * SLOT_LENGTH
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

def init_lora():
    while True:
        try:
            lora = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
            print("LoRa başlatıldı.")
            return lora
        except Exception as e:
            print(f"LoRa başlatılamadı: {e}. 3 sn sonra tekrar denenecek...")
            time.sleep(3)

def init_sdr():
    while True:
        try:
            sdr = RtlSdr()
            sdr.sample_rate = 2.4e6
            sdr.center_freq = 446.450e6
            sdr.gain = 5
            print("SDR başlatıldı.")
            return sdr
        except Exception as e:
            print(f"SDR başlatılamadı: {e}. 3 sn sonra tekrar denenecek...")
            time.sleep(3)

def read_sdr_db(sdr):
    samples = sdr.read_samples(256*1024)
    Psig = np.mean(np.abs(samples)**2)
    return 10 * np.log10(Psig / 1.0)

def send_message(lora, seq_id, db):
    msg = f"mesaj:{seq_id},drone{NODE_ID}:{db:.2f}\n"
    lora.write(msg.encode())
    print(f"[drone{NODE_ID}] gönderildi: {msg.strip()}")

seq_id = 0

print(f"drone{NODE_ID} sistem başlatılıyor...")

while True:
    try:
        # SDR ve LoRa başlat
        lora = init_lora()
        sdr = init_sdr()
        start_time = time.time()
        print(f"drone{NODE_ID} aktif.")

        while True:
            try:
                current_time = time.time()
                elapsed = (current_time - start_time) % CYCLE_LENGTH
                slot_start = (NODE_ID - 1) * SLOT_LENGTH
                slot_end = slot_start + SLOT_LENGTH

                if slot_start <= elapsed < slot_end:
                    db = read_sdr_db(sdr)
                    send_message(lora, seq_id, db)
                    seq_id += 1
                    time.sleep(SLOT_LENGTH)
                else:
                    time.sleep(0.05)

            except Exception as e_inner:
                print(f"SDR veya LoRa hatası: {e_inner}. 3 sn sonra tekrar başlatılacak...")
                try:
                    sdr.close()
                except:
                    pass
                time.sleep(3)
                break  # iç döngüden çık ve SDR/LoRa’yı yeniden başlat

    except KeyboardInterrupt:
        print("Drone durduruldu.")
        try:
            sdr.close()
        except:
            pass
        break
