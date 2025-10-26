# watchdog.py
import time
import subprocess

PATH = "/home/furkan/tubitak/send-signal.py"

while True:
    print("send-signal.py başlatılıyor...")
    result = subprocess.run(["python3", PATH], capture_output=True, text=True)

    print("Kod çöktü veya kapandı.")
    print("Çıktı:")
    print(result.stdout)
    print("Hata:")
    print(result.stderr)

    print("3 saniye sonra yeniden başlatılacak...\n")
    time.sleep(3)
