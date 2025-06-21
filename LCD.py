"""
how to run 

---
sudo crontab -e
add "@reboot python3 /home/pi/boot_LCD/LCD.py &" at last line 
---

tbf - show no ssid, - crontab no permission 
htf - create new file and add sudo LCD file on it and make it executable 

"""
import time
import smbus2
import signal
import socket
import subprocess

LCD_ADDR = 0x27  
bus = smbus2.SMBus(1)

LCD_CHR = 1  # Data mode
LCD_CMD = 0  # Command mode
LCD_BACKLIGHT = 0x08  # Backlight ON
ENABLE = 0b00000100  # Enable bit

def lcd_byte(bits, mode):
    high_bits = mode | (bits & 0xF0) | LCD_BACKLIGHT
    low_bits = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT
    bus.write_byte(LCD_ADDR, high_bits)
    bus.write_byte(LCD_ADDR, high_bits | ENABLE)
    time.sleep(0.0005)
    bus.write_byte(LCD_ADDR, high_bits & ~ENABLE)
    bus.write_byte(LCD_ADDR, low_bits)
    bus.write_byte(LCD_ADDR, low_bits | ENABLE)
    time.sleep(0.0005)
    bus.write_byte(LCD_ADDR, low_bits & ~ENABLE)
    
def lcd_init():
    lcd_byte(0x33, LCD_CMD)  # Initialize
    lcd_byte(0x32, LCD_CMD)  # Set to 4-bit mode
    lcd_byte(0x06, LCD_CMD)  # Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # Display ON, Cursor OFF
    lcd_byte(0x28, LCD_CMD)  # 2-line mode, 5x8 font
    lcd_byte(0x01, LCD_CMD)  # Clear display
    time.sleep(0.2)
    
def lcd_display(text, line=1):
    if line == 1:
        lcd_byte(0x80, LCD_CMD)  # First line
    elif line == 2:
        lcd_byte(0xC0, LCD_CMD)  # Second line
    for char in text:
        lcd_byte(ord(char), LCD_CHR)
def lcd_clear():
    lcd_byte(0x01, LCD_CMD)  # Clear display
    time.sleep(0.2)
    
def signal_handler(sig, frame):
    print("\nClearing LCD and exiting...")
    lcd_clear()
    exit(0)

def display_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception:
        ip = "No IP"

    ssid = get_wifi_ssid()

    lcd_clear()
    lcd_display(f"{ssid[:16]}", line=1) # LCDs usually have 16 chars per line
    lcd_display(f"IP:{ip[:13]}", line=2)

def wait_for_network(timeout=30):
    """Wait until the Pi has a network connection or timeout"""
    for _ in range(timeout):
        try:
            # Try to connect to an external server
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            s.close()
            return True
        except:
            time.sleep(1)
    return False

def get_wifi_ssid():
    try:
        result = subprocess.check_output(
            ["iwconfig", "wlan0"],
            stderr=subprocess.DEVNULL
        ).decode()

        for line in result.splitlines():
            if "ESSID" in line:
                ssid = line.split("ESSID:")[1].strip().strip('"')
                return ssid if ssid else "No SSID"
        return "No SSID"
    except Exception:
        return "No SSID"

        
signal.signal(signal.SIGINT, signal_handler)

def run_lcd_demo():
    """Run a simple LCD demo: display 'Autobotic' and keep running."""
    lcd_init()
    lcd_display("Autobotic")

    try:
        while True:
            time.sleep(1)  # Keep script running
    except KeyboardInterrupt:
        pass

# run code
if __name__ == "__main__":
    lcd_init()
    lcd_clear()
    lcd_display("Waiting for WiFi", line=1)

    if wait_for_network(timeout=30):
        display_ip_address()
    else:
        lcd_clear()
        lcd_display("No network found", line=1)
