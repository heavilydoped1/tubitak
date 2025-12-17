
The system continuously:
	1.	Listens to a specific RF band using RTL-SDR
	2.	Calculates signal power (in dB)
	3.	Sends this telemetry data to a LoRa transmitter
	4.	Uses TDMA-based scheduling to support multiple nodes
	5.	Monitors system health using watchdog 

Hardware Requirements

RF Side
	•	RTL-SDR USB dongle
	•	Antenna tuned to target frequency

Communication
	•	LoRa module (UART-based)
	•	USB-to-TTL converter (if needed)

Host
	•	Linux-based system (Ubuntu / Raspberry Pi recommended)

Software Requirements
	•	Python 3.x
	•	Required libraries:

pip install numpy pyrtlsdr pyserial


⸻
LoRa Initialization

def init_lora():
    return serial.Serial('/dev/ttyUSB0', 9600)

	•	Opens UART connection to the LoRa module
	•	/dev/ttyUSB0 → USB-to-Serial device
	•	9600 baud → default LoRa UART speed

RTL-SDR Initialization

def init_sdr():
    sdr = RtlSdr()
    sdr.sample_rate = 2.4e6
    sdr.center_freq = 446.450e6
    sdr.gain = 5
    return sdr

	•	Samples RF data at 2.4 MS/s
	•	Tuned to 446.450 MHz for PMR radios
	•	Manual gain control for stability

RF Power Calculation

samples = sdr.read_samples(256*1024)
Psig = np.mean(np.abs(samples)**2)
Pfull = 1.0
db = 10.0 * np.log10(Psig / Pfull)

	•	Reads raw I/Q samples
	•	Computes average signal power
	•	Converts power to dB scale

LoRa Data Transmission

def send_to_lora(lora, db):
    msg = f"1. drone: {db:.2f}"
    lora.write(msg.encode())

	•	Formats telemetry message
	•	Sends power value via LoRa

Main Loop

while True:
    ...
    send_to_lora(lora, db)
    time.sleep(0.01)

	•	Continuous measurement
	•	Periodic transmission
	•	Timing can be synchronized with TDMA slots

The TDMA implementation:
	assigns time slots to different drones/nodes
	prevents LoRa packet collision

Files:
	•	tdma_code.py → basic implementation
	•	tdma-code-better.py → optimized & cleaner version

Watchdog & Reliability

	•	watchdog.py → monitors process health
	
	•	send-signal-watchdog.py → TX with fault tolerance

