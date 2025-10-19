import time
import os

while True:
    try:
        os.system("python3 /home/furkan/tubitak/send-signal.py")
    except Exception as e:
        print(f"hata oluştu: {e}")
    
    print("kod çöktü 3 saniye sonra yeniden başlatılıyor...")
    time.sleep(3)
