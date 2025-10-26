from rtlsdr import RtlSdr
import numpy as np
import serial
import time
import random

NODE_ID = 2        
SLOT_LENGTH = 0.5   
CYCLE_LENGTH = 4 * SLOT_LENGTH 
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

def init_lora():
    return serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)

def init_sdr():
    sdr = RtlSdr()
    sdr.sample_rate = 2.4e6
    sdr.center_freq = 446.450e6
    sdr.gain = 5
    return sdr

try:
    lora = init_lora()
    sdr = init_sdr()
    print(f"drone{NODE_ID} baslatıldı.")

    seq_id = 0
    start_time = time.time()

    while True:
        current_time = time.time()
        elapsed = (current_time - start_time) % CYCLE_LENGTH

        slot_start = (NODE_ID - 1) * SLOT_LENGTH
        slot_end = slot_start + SLOT_LENGTH

        if slot_start <= elapsed < slot_end:
            samples = sdr.read_samples(256*1024)
            Psig = np.mean(np.abs(samples)**2)
            db = 10 * np.log10(Psig / 1.0)

            msg = f"{seq_id},drone{NODE_ID}:{db:.2f}\n"
            lora.write(msg.encode())
            print(f"[drone{NODE_ID}] gönderildi: {msg.strip()}")

            seq_id += 1
            time.sleep(SLOT_LENGTH) 

        else:
        
            time.sleep(0.05)

except KeyboardInterrupt:
    print("drone durduruldu.")
except Exception as e:
    print(f"hata: {e}")
    raise 
finally:
    try:
        sdr.close()
    except:
        pass
    print("sdr kapatıldı.")
