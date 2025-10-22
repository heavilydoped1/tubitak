# send-signal.py
from rtlsdr import RtlSdr
import numpy as np
import serial
import time

def init_lora():
    return serial.Serial('/dev/ttyUSB0', 9600)

def init_sdr():
    sdr = RtlSdr()
    sdr.sample_rate = 2.4e6
    sdr.center_freq = 446.450e6
    sdr.gain = 5
    return sdr

def send_to_lora(lora, db):
    msg = f"1. drone: {db:.2f}"
    lora.write(msg.encode())
    print(f"sended message from lora: {db:.2f}")

try:
    lora = init_lora()
    sdr = init_sdr()
    print("✅ LoRa ve SDR başarıyla başlatıldı!")

    while True:
        samples = sdr.read_samples(256*1024)
        Psig = np.mean(np.abs(samples)**2)
        Pfull = 1.0
        db = 10.0 * np.log10(Psig / Pfull)
        send_to_lora(lora, db)
        time.sleep(0.01)

except Exception as e:
    print(f"🚨 Hata oluştu: {e}")
    raise  # Bu sayede dıştaki process görebilir

except KeyboardInterrupt:
    print("🧠 Kullanıcı tarafından durduruldu.")

finally:
    try:
        sdr.close()
    except:
        pass
    print("📡 SDR kapatıldı.")
