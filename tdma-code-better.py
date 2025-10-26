from rtlsdr import RtlSdr
import numpy as np
import serial
import time

NODE_ID = 2
SLOT_LENGTH = 0.5
CYCLE_LENGTH = 4 * SLOT_LENGTH
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600
GUARD_TIME = 0.06 

def init_lora():
    return serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)

def init_sdr():
    sdr = RtlSdr()
    sdr.sample_rate = 2.4e6
    sdr.center_freq = 446.450e6
    sdr.gain = 5
    return sdr

def busy_sleep_until(target_t):
    
    while True:
        now = time.monotonic()
        rem = target_t - now
        if rem <= 0:
            return
        if rem > 0.02:
            time.sleep(0.01)
        else:
            
            pass

try:
    lora = init_lora()
    sdr = init_sdr()
    print(f"drone{NODE_ID} başlatıldı (improved scheduler).")

    seq_id = 0
    start = time.monotonic()

    while True:
        now = time.monotonic()
        elapsed = (now - start) % CYCLE_LENGTH

        slot_index = NODE_ID - 1
        slot_start = slot_index * SLOT_LENGTH
        slot_end = slot_start + SLOT_LENGTH
        if slot_start <= elapsed < slot_end:
            cycle_num = int((now - start) // CYCLE_LENGTH)
            absolute_slot_start = start + cycle_num * CYCLE_LENGTH + slot_start
            tx_time = absolute_slot_start + GUARD_TIME/2

            if time.monotonic() < tx_time:
                busy_sleep_until(tx_time)

            samples = sdr.read_samples(128*1024)  # 128k
            Psig = np.mean(np.abs(samples)**2)
            db = 10 * np.log10(Psig / 1.0)

            msg = f"{seq_id},Drone{NODE_ID}:{db:.2f}\n"
            lora.write(msg.encode())
            print(f"[Drone{NODE_ID}] Gönderildi: {msg.strip()}")

            seq_id += 1

            end_time = absolute_slot_start + SLOT_LENGTH - GUARD_TIME/2
            busy_sleep_until(end_time)

        else:
            time.sleep(0.02)

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
