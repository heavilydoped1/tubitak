from rtlsdr import RtlSdr
import numpy as np
import serial
import time
import random

NODE_ID = 2          # her drone için 1, 2, 3, 4
SLOT_LENGTH = 0.5    # her drone’un gönderim süresi (saniye)
ACK_TIMEOUT = 0.2
MAX_RETRIES = 3
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

def send_with_ack(lora, msg, seq_id):
    for attempt in range(MAX_RETRIES):
        lora.write(msg.encode())
        print(f"({seq_id}) Drone{NODE_ID} gönderim {attempt+1}: {msg.strip()}")

        # ACK bekle
        start = time.time()
        while time.time() - start < ACK_TIMEOUT:
            if lora.in_waiting:
                incoming = lora.readline().decode(errors='ignore').strip()
                if incoming == f"ACK,{seq_id}":
                    print(f"[Drone{NODE_ID}] ACK alındı ✅")
                    return True

        # ACK yok → random backoff
        backoff = random.uniform(0.1, 0.3)
        print(f"[Drone{NODE_ID}] ACK yok, {backoff:.2f}s bekleniyor...")
        time.sleep(backoff)

    print(f"[Drone{NODE_ID}] ({seq_id}) gönderim başarısız ❌")
    return False

try:
    lora = init_lora()
    sdr = init_sdr()
    print(f"Drone{NODE_ID} başlatıldı.")

    seq_id = 0
    beacon_detected = False
    cycle_start = 0

    while True:
        # Beacon dinleme
        if not beacon_detected:
            if lora.in_waiting:
                line = lora.readline().decode(errors='ignore').strip()
                if line == "BEACON_START":
                    beacon_detected = True
                    cycle_start = time.time()
                    print(f"[Drone{NODE_ID}] Beacon alındı, cycle başladı!")

        # Beacon alındıysa, kendi slot zamanını hesapla
        if beacon_detected:
            current_time = time.time()
            elapsed = current_time - cycle_start
            slot_start = (NODE_ID - 1) * SLOT_LENGTH
            slot_end = slot_start + SLOT_LENGTH

            # Slot zamanı geldiğinde gönderim yap
            if slot_start <= elapsed < slot_end:
                samples = sdr.read_samples(256*1024)
                Psig = np.mean(np.abs(samples)**2)
                db = 10 * np.log10(Psig / 1.0)
                msg = f"{seq_id},Drone{NODE_ID}:{db:.2f}\n"
                send_with_ack(lora, msg, seq_id)
                seq_id += 1
                time.sleep(SLOT_LENGTH)  # slot bitene kadar bekle

            # Cycle bitince beacon’ı tekrar bekle
            if elapsed > 4 * SLOT_LENGTH:
                beacon_detected = False

except KeyboardInterrupt:
    print("Drone durduruldu.")
except Exception as e:
    print("Hata:", e)
finally:
    try:
        sdr.close()
    except:
        pass
    print("SDR kapatıldı.")
