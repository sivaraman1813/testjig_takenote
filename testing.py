import tkinter as tk
from tkinter import messagebox
import time
import numpy as np
import serial.tools.list_ports

# ===== GLOBAL VARIABLES =====
board = None
TARGET_NAME = "TakeNote V_3.2"

# ===== ARDUINO CONNECTION =====
def find_arduino_port():
    """Detect Arduino or USB-serial device."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        desc = port.description.lower()
        if ("arduino" in desc or 
            "ch340" in desc or 
            "usb" in desc or 
            "ttyacm" in port.device.lower() or 
            "ttyusb" in port.device.lower()):
            return port.device
    return None

def connect_arduino():
    """Automatically connect to Arduino on startup."""
    global board
    try:
        import pyfirmata
    except ImportError:
        print("⚠️ pyfirmata not installed")
        messagebox.showerror("Library Missing", "Please install pyfirmata library.")
        return None

    arduino_port = find_arduino_port()
    if not arduino_port:
        print("⚠️ No Arduino detected")
        messagebox.showwarning("Arduino Not Found", "No Arduino detected.")
        return None

    try:
        board = pyfirmata.Arduino(arduino_port)
        print(f"✅ Connected to Arduino on {arduino_port}")
        return board
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        messagebox.showerror("Connection Failed", f"Failed to connect Arduino: {e}")
        return None

# ===== BRAILLE CONVERSION =====

def alplow_brl(rec):
    """Convert lowercase character to braille pattern"""
    alp_lower_brl = {
        "a": np.array([0,0,1,0,0,0,0,0,0], dtype=bool),
        "b": np.array([0,1,1,0,0,0,0,0,0], dtype=bool),
        "c": np.array([0,0,1,1,0,0,0,0,0], dtype=bool),
        "d": np.array([0,0,1,1,1,0,0,0,0], dtype=bool),
        "e": np.array([0,0,1,0,1,0,0,0,0], dtype=bool),
        "f": np.array([0,1,1,1,0,0,0,0,0], dtype=bool),
        "g": np.array([0,1,1,1,1,0,0,0,0], dtype=bool),
        "h": np.array([0,1,1,0,1,0,0,0,0], dtype=bool),
        "i": np.array([0,1,0,1,0,0,0,0,0], dtype=bool),
        "j": np.array([0,1,0,1,1,0,0,0,0], dtype=bool),
        "k": np.array([1,0,1,0,0,0,0,0,0], dtype=bool),
        "l": np.array([1,1,1,0,0,0,0,0,0], dtype=bool),
        "m": np.array([1,0,1,1,0,0,0,0,0], dtype=bool),
        "n": np.array([1,0,1,1,1,0,0,0,0], dtype=bool),
        "o": np.array([1,0,1,0,1,0,0,0,0], dtype=bool),
        "p": np.array([1,1,1,1,0,0,0,0,0], dtype=bool),
        "q": np.array([1,1,1,1,1,0,0,0,0], dtype=bool),
        "r": np.array([1,1,1,0,1,0,0,0,0], dtype=bool),
        "s": np.array([1,1,0,1,0,0,0,0,0], dtype=bool),
        "t": np.array([1,1,0,1,1,0,0,0,0], dtype=bool),
        "u": np.array([1,0,1,0,0,1,0,0,0], dtype=bool),
        "v": np.array([1,1,1,0,0,1,0,0,0], dtype=bool),
        "w": np.array([0,1,0,1,1,1,0,0,0], dtype=bool),
        "x": np.array([1,0,1,1,0,1,0,0,0], dtype=bool),
        "y": np.array([1,0,1,1,1,1,0,0,0], dtype=bool),
        "z": np.array([1,0,1,0,1,1,0,0,0], dtype=bool),
        "*": np.array([1,0,0,0,1,0,0,0,0], dtype=bool),
        "@": np.array([1,0,0,1,1,0,0,0,0], dtype=bool),
        ":": np.array([0,1,0,0,1,0,0,0,0], dtype=bool),
        ",": np.array([0,1,0,0,0,0,0,0,0], dtype=bool),
        "!": np.array([1,1,0,0,1,0,0,0,0], dtype=bool),
        ".": np.array([0,1,0,0,1,1,0,0,0], dtype=bool),
        "?": np.array([1,1,0,0,0,1,0,0,0], dtype=bool),
        ";": np.array([1,1,0,0,0,0,0,0,0], dtype=bool),
        "/": np.array([1,0,0,1,0,0,0,0,0], dtype=bool),
        "non": np.array([0,0,0,0,0,0,0,0,0], dtype=bool),
        " ": np.array([0,0,0,0,0,0,0,1,0], dtype=bool),
        "\n": np.array([0,0,0,0,0,0,0,0,1], dtype=bool),
        '"': np.array([1,0,0,0,1,1,0,0,0], dtype=bool),
        "'": np.array([1,0,0,0,0,0,0,0,0], dtype=bool),
        "(": np.array([1,1,1,0,1,1,0,0,0], dtype=bool),
        ")": np.array([1,1,0,1,1,1,0,0,0], dtype=bool),
        "&": np.array([1,1,1,1,0,1,0,0,0], dtype=bool),
        "%": np.array([0,0,1,1,0,1,0,0,0], dtype=bool),
        "+": np.array([1,0,0,1,0,1,0,0,0], dtype=bool),
        "-": np.array([1,0,0,0,0,1,0,0,0], dtype=bool),
    }
    return alp_lower_brl.get(rec, alp_lower_brl["non"])

def alpup_brl(rec):
    """Convert uppercase character to braille pattern"""
    alp_upper_brl = {
        "A": np.array([0,0,1,0,0,0,0,0,0], dtype=bool),
        "B": np.array([0,1,1,0,0,0,0,0,0], dtype=bool),
        "C": np.array([0,0,1,1,0,0,0,0,0], dtype=bool),
        "D": np.array([0,0,1,1,1,0,0,0,0], dtype=bool),
        "E": np.array([0,0,1,0,1,0,0,0,0], dtype=bool),
        "F": np.array([0,1,1,1,0,0,0,0,0], dtype=bool),
        "G": np.array([0,1,1,1,1,0,0,0,0], dtype=bool),
        "H": np.array([0,1,1,0,1,0,0,0,0], dtype=bool),
        "I": np.array([0,1,0,1,0,0,0,0,0], dtype=bool),
        "J": np.array([0,1,0,1,1,0,0,0,0], dtype=bool),
        "K": np.array([1,0,1,0,0,0,0,0,0], dtype=bool),
        "L": np.array([1,1,1,0,0,0,0,0,0], dtype=bool),
        "M": np.array([1,0,1,1,0,0,0,0,0], dtype=bool),
        "N": np.array([1,0,1,1,1,0,0,0,0], dtype=bool),
        "O": np.array([1,0,1,0,1,0,0,0,0], dtype=bool),
        "P": np.array([1,1,1,1,0,0,0,0,0], dtype=bool),
        "Q": np.array([1,1,1,1,1,0,0,0,0], dtype=bool),
        "R": np.array([1,1,1,0,1,0,0,0,0], dtype=bool),
        "S": np.array([1,1,0,1,0,0,0,0,0], dtype=bool),
        "T": np.array([1,1,0,1,1,0,0,0,0], dtype=bool),
        "U": np.array([1,0,1,0,0,1,0,0,0], dtype=bool),
        "V": np.array([1,1,1,0,0,1,0,0,0], dtype=bool),
        "W": np.array([0,1,0,1,1,1,0,0,0], dtype=bool),
        "X": np.array([1,0,1,1,0,1,0,0,0], dtype=bool),
        "Y": np.array([1,0,1,1,1,1,0,0,0], dtype=bool),
        "Z": np.array([1,0,1,0,1,1,0,0,0], dtype=bool),
    }
    return alp_upper_brl.get(rec, np.array([0,0,0,0,0,0,0,0,0], dtype=bool))

def num_brl(rec):
    """Convert number to braille pattern"""
    number_brl = {
        "1": np.array([0,0,1,0,0,0,0,0,0], dtype=bool),
        "2": np.array([0,1,1,0,0,0,0,0,0], dtype=bool),
        "3": np.array([0,0,1,1,0,0,0,0,0], dtype=bool),
        "4": np.array([0,0,1,1,1,0,0,0,0], dtype=bool),
        "5": np.array([0,0,1,0,1,0,0,0,0], dtype=bool),
        "6": np.array([0,1,1,1,0,0,0,0,0], dtype=bool),
        "7": np.array([0,1,1,1,1,0,0,0,0], dtype=bool),
        "8": np.array([0,1,1,0,1,0,0,0,0], dtype=bool),
        "9": np.array([0,1,0,1,0,0,0,0,0], dtype=bool),
        "0": np.array([0,1,0,1,1,0,0,0,0], dtype=bool),
    }
    return number_brl.get(rec, np.array([0,0,0,0,0,0,0,0,0], dtype=bool))

# Arduino control functions
def file_open():
    """Send file open command to Arduino"""
    if not board:
        return
    board.digital[5].write(0)
    board.digital[6].write(0)
    board.digital[7].write(0)
    board.digital[8].write(0)
    board.digital[9].write(0)
    board.digital[10].write(0)
    board.digital[2].write(1)
    board.digital[3].write(0)
    board.digital[4].write(1)
    time.sleep(0.5)
    board.digital[2].write(0)
    board.digital[4].write(0)
    time.sleep(0.5)

def file_close():
    """Send file close command to Arduino"""
    if not board:
        return
    board.digital[5].write(0)
    board.digital[6].write(0)
    board.digital[7].write(0)
    board.digital[8].write(0)
    board.digital[9].write(0)
    board.digital[10].write(0)
    board.digital[2].write(1)
    board.digital[3].write(1)
    board.digital[4].write(0)
    time.sleep(0.5)
    board.digital[2].write(0)
    board.digital[3].write(0)
    time.sleep(0.5)

def dot_led(outled):
    """Send braille pattern to Arduino LEDs"""
    if not board:
        return
    board.digital[5].write(outled[0])
    board.digital[6].write(outled[1])
    board.digital[7].write(outled[2])
    board.digital[8].write(outled[3])
    board.digital[9].write(outled[4])
    board.digital[10].write(outled[5])
    board.digital[2].write(outled[6])
    board.digital[3].write(outled[7])
    board.digital[4].write(outled[8])
    time.sleep(0.5)
    board.digital[5].write(0)
    board.digital[6].write(0)
    board.digital[7].write(0)
    board.digital[8].write(0)
    board.digital[9].write(0)
    board.digital[10].write(0)
    board.digital[2].write(0)
    board.digital[3].write(0)
    board.digital[4].write(0)
    time.sleep(0.5)

def al_num():
    """Send alphabet to number mode switch"""
    if not board:
        return
    board.digital[5].write(1)
    board.digital[6].write(0)
    board.digital[7].write(0)
    board.digital[8].write(1)
    board.digital[9].write(1)
    board.digital[10].write(1)
    time.sleep(0.5)
    board.digital[5].write(0)
    board.digital[6].write(0)
    board.digital[7].write(0)
    board.digital[8].write(0)
    board.digital[9].write(0)
    board.digital[10].write(0)
    time.sleep(0.5)

def num_al():
    """Send number to alphabet mode switch"""
    if not board:
        return
    board.digital[5].write(0)
    board.digital[6].write(0)
    board.digital[7].write(0)
    board.digital[8].write(0)
    board.digital[9].write(1)
    board.digital[10].write(1)
    time.sleep(0.5)
    board.digital[5].write(0)
    board.digital[6].write(0)
    board.digital[7].write(0)
    board.digital[8].write(0)
    board.digital[9].write(0)
    board.digital[10].write(0)
    time.sleep(0.5)

def capital():
    """Send capital letter indicator"""
    if not board:
        return
    board.digital[5].write(0)
    board.digital[6].write(0)
    board.digital[7].write(0)
    board.digital[8].write(0)
    board.digital[9].write(0)
    board.digital[10].write(1)
    time.sleep(0.5)
    board.digital[5].write(0)
    board.digital[6].write(0)
    board.digital[7].write(0)
    board.digital[8].write(0)
    board.digital[9].write(0)
    board.digital[10].write(0)
    time.sleep(0.5)
# ===== ARDUINO CONTROL =====


# ===== TEST FUNCTION =====
def test_individual(txt_widget, status_label):
    """Test individual text from a Tkinter Text widget."""
    global board
    if board is None:
        messagebox.showwarning("Board Error", "Arduino not connected. Connect first.")
        return
    
    text_content = txt_widget.get("1.0", tk.END)
    count = 0
    num_flog = 0
    
    file_open()
    time.sleep(1)
    
    for char in text_content[:-1]:
        if char.islower():
            if num_flog == 1: num_al()
            num_flog = 0
            outled = alplow_brl(char)
        elif char.isupper():
            if num_flog == 1: num_al()
            num_flog = 0
            capital()
            outled = alpup_brl(char)
        elif char.isdigit():
            if num_flog == 0: al_num()
            num_flog = 1
            outled = num_brl(char)
        else:
            outled = alplow_brl(char)
        
        dot_led(outled)
        count += 1
        if count % 10 == 0:
            txt_widget.update()
    
    file_close()
    status_label.config(text=f"Hardware testing complete: {count} characters")
    print(f"✅ Hardware testing completed: {count} characters")

# ===== GUI =====
root = tk.Tk()
root.title("TakeNote Braille Test Jig")
root.geometry("450x350")

tk.Label(root, text="Enter Text:").pack(pady=5)
txt_input = tk.Text(root, height=5)
txt_input.pack(pady=5, padx=10, fill="x")

test_btn = tk.Button(root, text="Run Test", 
                     command=lambda: test_individual(txt_input, status_label))
test_btn.pack(pady=5)

status_label = tk.Label(root, text="Status: Connecting to Arduino...")
status_label.pack(pady=10)

# Automatically connect Arduino on startup
connect_arduino()
if board:
    status_label.config(text="Status: Arduino Connected")
else:
    status_label.config(text="Status: Arduino Not Connected")

root.mainloop()
