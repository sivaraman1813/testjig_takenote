import platform
import os
import sys
import time
import subprocess
import re
import csv
import difflib
import datetime
import glob
import numpy as np
import socket

# Tkinter imports with error handling
try:
    import tkinter as tk
    from tkinter import *
    from tkinter.filedialog import askopenfilename
    from tkinter import ttk
    from tkinter import messagebox
    import tkinter.font as tkFont
    print("✅ Tkinter loaded successfully")
except ImportError as e:
    print(f"❌ Tkinter import failed: {e}")
    sys.exit(1)

# Optional imports with graceful fallback
try:
    import pyfirmata
    PYFIRMATA_AVAILABLE = True
    print("✅ PyFirmata available")
except ImportError:
    print("⚠️  pyfirmata not available - hardware features disabled")
    PYFIRMATA_AVAILABLE = False

try:
    import bluetooth
    from bluetooth import *
    BLUETOOTH_AVAILABLE = True
    print("✅ Bluetooth available")
except ImportError:
    print("⚠️  pybluez not available - Bluetooth features disabled")
    BLUETOOTH_AVAILABLE = False

try:
    import Hex2TxtTakenote_ENG1_aug_2021
    CONVERTER_AVAILABLE = True
    print("✅ Hex converter available")
except ImportError:
    print("⚠️  Hex2TxtTakenote_ENG1_aug_2021 not available")
    CONVERTER_AVAILABLE = False

# Global variables
time_hour = 0
time_minute = 0
time_second = 0
version_number = ""
a = 0
TARGET_NAME = "TakeNote V_3.2"
PORT = 1
board = None

# Arduino board initialization with auto-detection
import serial.tools.list_ports

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
    """Try to connect using pyfirmata."""
    try:
        import pyfirmata
    except ImportError:
        print("⚠️ pyfirmata not installed")
        return None

    arduino_port = find_arduino_port()

    if not arduino_port:
        print("⚠️ No Arduino detected")
        return None

    print(f"🔍 Trying to connect on: {arduino_port}")

    try:
        board = pyfirmata.Arduino(arduino_port)
        print(f"✅ Connected to Arduino on {arduino_port}")
        return board
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return None


# -------- Run Test --------
if __name__ == "__main__":
    connect_arduino()


#---------------------------Bluetooth Transfer Functions------------------
def find_device(target_name, timeout=8):
    """Find the target Bluetooth device"""
    if not BLUETOOTH_AVAILABLE:
        return None
    
    print(f"🔍 Scanning for {target_name}...")
    try:
        devices = bluetooth.discover_devices(lookup_names=True, duration=timeout)
        for addr, name in devices:
            print(f"  • {name} ({addr})")
            if name and target_name in name:
                return addr
        return None
    except Exception as e:
        print(f"Error during device discovery: {e}")
        return None

def parse_and_save(data_stream):
    """Split incoming stream into separate files based on firmware markers."""
    if not data_stream:
        print("⚠️  No data received.")
        return []
    
    data_str = data_stream.decode(errors='ignore')
    print(f"📄 Received data length: {len(data_str)} characters")
    
    files = re.findall(r'(/NOTE\d+\.txt)(.*?)(?:Continue 01111110 \$)', data_str)
    saved_files = []
    
    if not files:
        print("⚠️  No files found in stream.")
        if data_str.strip():
            filename = f"received_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(data_str.strip())
            saved_files.append(filename)
            print(f"✅ Saved raw data as: {filename}")
        return saved_files
    
    for filename, content in files:
        clean_name = filename.strip('/')
        try:
            with open(clean_name, 'w') as f:
                f.write(content.strip())
            abs_path = os.path.abspath(clean_name)
            saved_files.append(clean_name)
            print(f"✅ Saved file: {abs_path}")
        except Exception as e:
            print(f"❌ Error saving {clean_name}: {e}")
    
    if "File Transfer Done 01111110 $" in data_str:
        print("✅ All files transferred successfully.")
    else:
        print("⚠️  File transfer may be incomplete (missing final marker).")
    
    return saved_files

def receive_all(sock):
    """Read until the transfer is complete, return the complete byte stream."""
    sock.settimeout(10.0)
    buffer = bytearray()
    
    try:
        while True:
            chunk = sock.recv(1024)
            if not chunk:
                break
            print(f"⬇️  Received {len(chunk)} bytes")
            buffer.extend(chunk)
            
            if b"File Transfer Done 01111110 $" in buffer:
                print("✅ Transfer complete marker received.")
                break
    except socket.timeout:
        print("⏱️  Socket timed out (no more data).")
    except Exception as e:
        print(f"⚠️  Receive error: {e}")
    finally:
        sock.close()
    
    return buffer

#---------------------------Hardware Testing Functions------------------
def test_individual():
    
    """Test individual characters from the text using hardware"""
    if not board or not PYFIRMATA_AVAILABLE:
        messagebox.showwarning(
            "Hardware Not Available",
            "Arduino hardware is not connected. Hardware testing is disabled."
        )
        return
    
    text_content = txt1.get("1.0", tk.END)
    count = 0
    num_flog = 0
    
    print("Testing individual characters with hardware:")
    status_label.config(text="Hardware testing in progress...")
    
    # Open file on hardware
    file_open()
    time.sleep(2)
    
    for char in text_content[:-1]:
        print(f"Character {count}: '{char}' (ASCII: {ord(char)})")
        
        if char >= 'a' and char <= 'z':
            if num_flog == 1:
                num_al()
            num_flog = 0
            outled = alplow_brl(char)
        elif char >= 'A' and char <= 'Z':
            if num_flog == 1:
                num_al()
            num_flog = 0
            capital()
            outled = alpup_brl(char)
        elif char >= '0' and char <= '9':
            if num_flog == 0:
                al_num()
            num_flog = 1
            outled = num_brl(char)
        else:
            outled = alplow_brl(char)
        
        dot_led(outled)
        count += 1
        
        # Update progress
        if count % 10 == 0:
            window.update()
    
    file_close()
    print(f"✅ Hardware testing completed: {count} characters")
    status_label.config(text=f"Hardware testing complete: {count} characters")

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

#---------------------------Analysis Functions-------------------------------
def result():
    """Run automated test jig analysis"""
    try:
        # Get TakeNote number from entry field
      
        
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "=== AUTOMATED TEST JIG RESULTS ===\n\n")
    
        
        current_time = datetime.datetime.now()
        result_text.insert(tk.END, f"Date: {current_time.day}/{current_time.month}/{current_time.year}\n")
        result_text.insert(tk.END, f"Time: {current_time.hour}:{current_time.minute}:{current_time.second}\n")
        result_text.insert(tk.END, f"Time Taken: {time_hour}h:{time_minute}m:{time_second}s\n\n")
        
        # Check for input and output directories
        input_dir = "C:\\Testjig\\Input_files"
        output_dir = "C:\\Testjig\\output_from_takenote"
        
        if not os.path.exists(input_dir):
            result_text.insert(tk.END, f"⚠️  Input directory not found: {input_dir}\n")
            return
        
        if not os.path.exists(output_dir):
            result_text.insert(tk.END, f"⚠️  Output directory not found: {output_dir}\n")
            return
        
        # Count files
        count_input = len([f for f in os.listdir(input_dir) if f.endswith('.txt')])
        count_output = len([f for f in os.listdir(output_dir) if f.endswith('_op.txt')])
        
        result_text.insert(tk.END, f"Files given to TestJig: {count_input}\n")
        result_text.insert(tk.END, f"Files from TakeNote: {count_output}\n\n")
        
        # Compare files
        results = []
        for i in range(1, min(count_input, count_output) + 1):
            input_file = os.path.join(input_dir, f"file{i}.txt")
            output_file = os.path.join(output_dir, f"para{i}_op.txt")
            
            if os.path.exists(input_file) and os.path.exists(output_file):
                with open(input_file, 'r') as f1, open(output_file, 'r') as f2:
                    data1 = f1.read()
                    data2 = f2.read()
                    
                    len1, len2 = len(data1), len(data2)
                    error = len1 - len2
                    score = (len2 / len1 * 100) if len1 > 0 else 0
                    
                    result_text.insert(tk.END, f"File {i}:\n")
                    result_text.insert(tk.END, f"  Input chars: {len1}\n")
                    result_text.insert(tk.END, f"  Output chars: {len2}\n")
                    result_text.insert(tk.END, f"  Missing: {error}\n")
                    result_text.insert(tk.END, f"  Score: {score:.2f}%\n")
                    result_text.insert(tk.END, f"  Result: {'PASS ✓' if error == 0 else 'FAIL ✗'}\n\n")
        
        status_label.config(text="Automated test analysis complete")
        
    except Exception as e:
        result_text.insert(tk.END, f"\n❌ Error: {str(e)}\n")
        print(f"Error in result(): {e}")

def display_csv(file_path, text_widget):
    """Display CSV file in formatted table"""
    try:
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            rows = list(reader)
            
            if not rows:
                text_widget.insert(tk.END, "\nThe CSV file is empty.\n")
                return
            
            column_widths = [max(len(str(item)) for item in col) for col in zip(*rows)]
            border_row = "+" + "+".join(["-" * (width + 2) for width in column_widths]) + "+"
            
            text_widget.tag_configure("header", foreground="blue", font=("Courier", 12, "bold"))
            text_widget.insert(tk.END, "\n" + border_row + "\n")
            
            header = rows[0]
            formatted_header = "| " + " | ".join(f"{str(item).ljust(width)}" for item, width in zip(header, column_widths)) + " |"
            text_widget.insert(tk.END, formatted_header + "\n", "header")
            text_widget.insert(tk.END, border_row + "\n")
            
            for row in rows[1:]:
                formatted_row = "| " + " | ".join(f"{str(item).ljust(width)}" for item, width in zip(row, column_widths)) + " |"
                text_widget.insert(tk.END, formatted_row + "\n")
            
            text_widget.insert(tk.END, border_row + "\n")
    
    except FileNotFoundError:
        text_widget.insert(tk.END, f"\nError: {file_path} not found.\n")
    except Exception as e:
        text_widget.insert(tk.END, f"\nError reading {file_path}: {e}\n")

def get():
    """Load a text file and convert hex to text if needed"""
    try:
        initial_dir = os.getcwd()
        
        filepath = askopenfilename(
            initialdir=initial_dir,
            title="Select a text file",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        
        if not filepath:
            return
        
        print(f"Selected file path: {filepath}")
        txt1.delete("1.0", tk.END)
        
        with open(filepath, "r", encoding='utf-8') as input_file:
            text = input_file.read()
        
        print(f"Original content length: {len(text)} characters")
        converted_text = convert_hex_content_to_english(text)
        txt1.insert(tk.END, converted_text)
        typed1.delete("1.0", tk.END)
        
        status_label.config(text=f"Loaded: {os.path.basename(filepath)} - Hex converted to English")
        print(f"✅ File loaded successfully")
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {str(e)}")
        status_label.config(text="Error loading file")
        print(f"❌ Error: {e}")

def convert_hex_content_to_english(content):
    """Convert hex format content to English text"""
    if CONVERTER_AVAILABLE:
        try:
            converted = Hex2TxtTakenote_ENG1_aug_2021.convert_hex_to_text(content)
            if converted and converted != content:
                print("✅ Converted using Hex2TxtTakenote_ENG1_aug_2021")
                return converted
        except Exception as e:
            print(f"⚠️  External converter failed: {e}")
    
    try:
        cleaned = content.replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')
        hex_chars = sum(c in '0123456789ABCDEFabcdef' for c in cleaned)
        hex_percentage = (hex_chars / len(cleaned) * 100) if len(cleaned) > 0 else 0
        
        if hex_percentage > 80 and len(cleaned) >= 10:
            print(f"📊 Detected hex content ({hex_percentage:.1f}% hex characters)")
            converted_text = ""
            i = 0
            
            while i < len(cleaned) - 1:
                try:
                    hex_pair = cleaned[i:i+2]
                    decimal_value = int(hex_pair, 16)
                    
                    if 32 <= decimal_value <= 126:
                        converted_text += chr(decimal_value)
                    elif decimal_value == 10:
                        converted_text += '\n'
                    elif decimal_value == 13:
                        converted_text += '\r'
                    elif decimal_value == 9:  # Tab
                        converted_text += '\t'
                    else:
                        # Non-printable, show as [HEX]
                        converted_text += f"[{hex_pair}]"
                    
                    i += 2
                    
                except ValueError:
                    # Not a valid hex pair, skip
                    converted_text += cleaned[i]
                    i += 1
            
            if converted_text.strip():
                print(f"✅ Converted hex to text: {len(converted_text)} characters")
                return converted_text
            else:
                print("⚠️  Hex conversion resulted in empty text")
        else:
            print(f"ℹ️  Content doesn't appear to be hex format ({hex_percentage:.1f}% hex)")
    
    except Exception as e:
        print(f"⚠️  Built-in hex conversion error: {e}")
    
    # If conversion failed or not hex, return original content
    print("ℹ️  Returning original content")
    return content


def transfer_files():
    """Transfer files via Bluetooth and automatically evaluate"""
    global version_number
    
    # Always simulate on macOS if Bluetooth is not available
    if not BLUETOOTH_AVAILABLE or platform.system() == "Darwin":
        messagebox.showwarning(
            "Bluetooth Not Available",
            "Bluetooth is not supported on macOS or required modules are missing. Simulating file transfer."
        )
        simulate_transfer()
        return

    try:
        print(f"🔍 Starting Bluetooth transfer for {TARGET_NAME}...")
        status_label.config(text="Searching for TakeNote device...")
        
        # Find the device
        addr = find_device(TARGET_NAME)
        if not addr:
            messagebox.showerror("Device Not Found", f"Could not find '{TARGET_NAME}' device!")
            status_label.config(text="Device not found")
            return
        
        version_number = TARGET_NAME
        label1.config(text=version_number)
        
        print(f"🔗 Connecting to {TARGET_NAME} at {addr}:{PORT}")
        status_label.config(text="Connecting to device...")
        
        # Create Bluetooth socket
        sock = socket.socket(
            socket.AF_BLUETOOTH,
            socket.SOCK_STREAM,
            socket.BTPROTO_RFCOMM,
        )
        
        # Connect to device
        sock.connect((addr, PORT))
        print("✅ Connected!")
        status_label.config(text="Connected! Requesting files...")
        
        # Send command to request all files
        cmd = b'0'  # Request all new files
        sock.send(cmd)
        print(f"📡 Sent {cmd!r} → requesting all new files")
        
        # Receive all data
        status_label.config(text="Receiving files...")
        data = receive_all(sock)
        
        if not data:
            messagebox.showwarning("No Data", "No data received from device.")
            status_label.config(text="No data received")
            return
        
        # Parse and save files
        status_label.config(text="Parsing and saving files...")
        saved_files = parse_and_save(data)
        
        if not saved_files:
            messagebox.showwarning("No Files", "No files were saved from the transfer.")
            status_label.config(text="No files saved")
            return
        
        # Process the received files
        status_label.config(text="Processing received files...")
        process_transferred_files(saved_files)
        
        # Show completion message
        messagebox.showinfo("Transfer Complete", f"Successfully transferred and processed {len(saved_files)} files.")
        status_label.config(text=f"Transfer completed: {len(saved_files)} files")
        
    except Exception as e:
        print(f"❌ Bluetooth transfer error: {e}")
        messagebox.showerror("Transfer Error", f"Bluetooth transfer failed: {e}")
        status_label.config(text="Transfer failed")

def simulate_transfer():
    """Simulate file transfer for testing when Bluetooth is not available"""
    print("Simulating file transfer...")
    status_label.config(text="Simulating file transfer...")
    
    # Look for existing NOTE files in current directory for simulation
    note_files = [f for f in os.listdir('.') if f.startswith('NOTE') and f.endswith('.txt')]
    
    if note_files:
        print(f"Found {len(note_files)} NOTE files for simulation")
        status_label.config(text=f"Found {len(note_files)} files for simulation")
        process_transferred_files(note_files)
    else:
        # Create a sample file for demonstration
        sample_content = "This is a simulated transfer file for testing purposes."
        sample_file = "NOTE1_simulated.txt"
        with open(sample_file, 'w') as f:
            f.write(sample_content)
        print(f"Created sample file: {sample_file}")
        process_transferred_files([sample_file])
    
    # Simulate delay
    window.after(2000, lambda: status_label.config(text="Transfer simulation completed"))

def process_transferred_files(file_list):
    """Process the transferred files and load them for evaluation"""
    if not file_list:
        return
    
    # Use the most recent file (or first one) as the typed input
    latest_file = file_list[0]  # You might want to sort by date/time
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if content appears to be hex data and convert if possible
        if content.strip().replace(' ', '').replace('\n', '').replace('\r', '').isalnum() and len(content) > 50:
            # Might be hex data, try to convert
            converted_content = convert_hex_content_to_english(content)
            if converted_content != content:
                print(f"✅ Converted hex data to text")
                content = converted_content
        
        # Load the content into the typing area
        typed1.delete("1.0", tk.END)
        typed1.insert(tk.END, content)
        
        print(f"✅ Loaded transferred file content: {latest_file}")
        
        # If we have reference text loaded, automatically start comparison
        if txt1.get("1.0", tk.END).strip():
            window.after(1000, compare_user_input)  # Small delay then auto-compare
        else:
            # Show message to load reference text
            txt1.delete("1.0", tk.END)
            txt1.insert(tk.END, f"✅ Transferred file loaded: {latest_file}\n\n")
            txt1.insert(tk.END, "Please use 'GET FILE' to load a reference text for comparison.\n\n")
            txt1.insert(tk.END, f"Transferred content preview:\n{content[:200]}{'...' if len(content) > 200 else ''}")
        
    except Exception as e:
        print(f"❌ Error processing transferred file {latest_file}: {e}")
        messagebox.showerror("File Processing Error", f"Error processing transferred file: {e}")


def compare_user_input():
    """Compare the typed text with the reference text"""
    reference_text = txt1.get("1.0", tk.END).strip()
    typed_text = typed1.get("1.0", tk.END).strip()
    
    if not reference_text:
        messagebox.showwarning("No Reference", "Please load a reference text file first using 'GET FILE'")
        return
    
    if not typed_text:
        messagebox.showwarning("No Input", "Please enter some text in the typing area")
        return
    
    # Clear results area
    result_text.delete("1.0", tk.END)

    # Comprehensive Braille number-key mapping
    braille_keys = {
        # Lowercase letters
        "a": "1",    "b": "12",   "c": "14",   "d": "145",  "e": "15",
        "f": "124",  "g": "1245", "h": "125",  "i": "24",   "j": "245",
        "k": "13",   "l": "123",  "m": "134",  "n": "1345", "o": "135",
        "p": "1234", "q": "12345","r": "1235", "s": "234",  "t": "2345",
        "u": "136",  "v": "1236", "w": "2456", "x": "1346", "y": "13456",
        "z": "1356",
        
        # Uppercase letters (Capital sign + letter)
        "A": "6-1",    "B": "6-12",   "C": "6-14",   "D": "6-145",  "E": "6-15",
        "F": "6-124",  "G": "6-1245", "H": "6-125",  "I": "6-24",   "J": "6-245",
        "K": "6-13",   "L": "6-123",  "M": "6-134",  "N": "6-1345", "O": "6-135",
        "P": "6-1234", "Q": "6-12345","R": "6-1235", "S": "6-234",  "T": "6-2345",
        "U": "6-136",  "V": "6-1236", "W": "6-2456", "X": "6-1346", "Y": "6-13456",
        "Z": "6-1356",
        
        # Numbers (Number sign + letter)
        "0": "3456-245", "1": "3456-1",   "2": "3456-12",  "3": "3456-14",  
        "4": "3456-145", "5": "3456-15",  "6": "3456-124", "7": "3456-1245",
        "8": "3456-125", "9": "3456-24",
        
        # Punctuation marks
        ",": "2",           # Comma
        ";": "23",          # Semicolon
        ":": "25",          # Colon
        ".": "256",         # Period
        "!": "235",         # Exclamation mark
        "?": "236",         # Question mark
        "'": "3",           # Apostrophe
        '"': "5",           # Quotation mark
        "-": "36",          # Hyphen
        "(": "2356",        # Opening parenthesis
        ")": "2356",        # Closing parenthesis
        "/": "34",          # Slash
        "@": "4-1",         # At sign
        "#": "3456",        # Number sign
        "$": "4-234",       # Dollar sign
        "%": "4-356",       # Percent sign
        "&": "4-12346",     # Ampersand
        "*": "5-35",        # Asterisk
        "+": "5-235",       # Plus sign
        "=": "5-2356",      # Equals sign
        " ": "0",           # Space
    }

    # Helper function to format braille keys with commas
    def format_braille_key(key):
        """Format braille key to show dots separated by commas (e.g., '1,2,3')"""
        if key == "?":
            return "?"
        # Replace hyphens with commas and add commas between individual digits
        # Handle cases like "6-1" -> "6,1" and "234" -> "2,3,4"
        formatted = key.replace("-", ",")
        # Add commas between consecutive digits if not already present
        result = []
        for char in formatted:
            if char.isdigit():
                result.append(char)
            elif char == ",":
                result.append(char)
        return ",".join([c for c in result if c != ","])

    # Helper function to get the word at a given character position
    def get_word_at_position(text, pos):
        """Return the whole word that contains character index 'pos'."""
        if pos >= len(text):
            return ""
        words = text.split()
        index = 0
        for w in words:
            start = index
            end = index + len(w)
            if start <= pos < end:
                return w
            index = end + 1   # +1 for space
        return ""
    
    # Helper function to get character type
    def get_char_type(char):
        """Identify character type"""
        if char.isalpha():
            return "Letter"
        elif char.isdigit():
            return "Number"
        elif char in ".,;:!?'\"":
            return "Punctuation"
        elif char in "@#$%&*+-=/()[]{}":
            return "Symbol"
        elif char == " ":
            return "Space"
        else:
            return "Character"

    matcher = difflib.SequenceMatcher(None, reference_text, typed_text)
    accuracy_percentage = matcher.ratio() * 100
    
    corrections = []
    total_errors = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():

        # REPLACEMENT
        if tag == "replace":
            typed_word = get_word_at_position(typed_text, j1)
            correct_word = get_word_at_position(reference_text, i1)

            wrong_char = correct_char = "?"
            char_type = "Character"
            for k in range(min(len(correct_word), len(typed_word))):
                if typed_word[k] != correct_word[k]:
                    wrong_char = typed_word[k]
                    correct_char = correct_word[k]
                    char_type = get_char_type(correct_char)
                    break

            wrong_braille = format_braille_key(braille_keys.get(wrong_char, "?"))
            correct_braille = format_braille_key(braille_keys.get(correct_char, "?"))

            corrections.append(
                f"Position {i1}:\n"
                f"  Typed word: '{typed_word}'\n"
                f"  Correct word: '{correct_word}'\n"
                f"  Wrong {char_type}: '{wrong_char}' → Correct {char_type}: '{correct_char}'\n"
                f"  Wrong braille key: {wrong_braille} → Correct braille key: {correct_braille}\n"
            )
            total_errors += 1

        # DELETE (Missing content - should have been typed)
        elif tag == "delete":
            missing_content = reference_text[i1:i2]
            missing_chars = [char for char in missing_content]
            char_types = [get_char_type(char) for char in missing_chars]

            correct_word = get_word_at_position(reference_text, i1)
            typed_word = get_word_at_position(typed_text, j1) if j1 < len(typed_text) else ""

            # Build missing characters info (character and type only)
            missing_chars_info = ', '.join(f"'{char}' ({char_type})" for char, char_type in zip(missing_chars, char_types))
            
            # Build braille keys separately on a new line
            missing_braille_keys = ', '.join(f"'{char}': {format_braille_key(braille_keys.get(char, '?'))}" for char in missing_chars)

            if missing_content.strip() and ' ' in missing_content:
                corrections.append(
                    f"Position {i1}:\n"
                    f"  Missing content (not typed): '{missing_content}'\n"
                    f"  Missing characters: {missing_chars_info}\n"
                    f"  Correct braille keys: {missing_braille_keys}\n"
                )
            else:
                corrections.append(
                    f"Position {i1}:\n"
                    f"  Typed word: '{typed_word}' (missing characters)\n"
                    f"  Correct word: '{correct_word}'\n"
                    f"  Missing characters: {missing_chars_info}\n"
                    f"  Correct braille keys: {missing_braille_keys}\n"
                )
            total_errors += 1

       # INSERT (Extra content - should NOT have been typed)
        elif tag == "insert":
            extra_content = typed_text[j1:j2]
            
            # Split the extra content by spaces to identify separate insertions
            parts = []
            current_part = ""
            part_start = j1
            
            for idx, char in enumerate(extra_content):
                if char == ' ':
                    if current_part:
                        parts.append((part_start, current_part, 'chars'))
                        part_start = j1 + idx + 1
                        current_part = ""
                else:
                    current_part += char
            
            if current_part:
                parts.append((part_start, current_part, 'chars'))
            
            # Process each part separately
            for part_pos, part_content, part_type in parts:
                extra_chars = [char for char in part_content]
                char_types = [get_char_type(char) for char in extra_chars]
                extra_chars_info = ', '.join(f"'{char}' ({char_type})" for char, char_type in zip(extra_chars, char_types))
                
                # Check if this part is a complete word or extra characters in a word
                is_surrounded_by_spaces = (
                    (part_pos > 0 and typed_text[part_pos - 1] == ' ') and 
                    (part_pos + len(part_content) < len(typed_text) and typed_text[part_pos + len(part_content)] == ' ')
                )
                
                if is_surrounded_by_spaces or len(parts) > 1:
                    # This is an extra word
                    corrections.append(
                        f"Position {i1}:\n"
                        f"  Extra word typed (should not be typed): '{part_content}'\n"
                        f"  Extra characters: {extra_chars_info}\n"
                    )
                else:
                    # Extra characters within a word
                    typed_word = get_word_at_position(typed_text, part_pos)
                    correct_word = ""
                    if i1 > 0:
                        correct_word = get_word_at_position(reference_text, i1 - 1)
                    if not correct_word and i1 < len(reference_text):
                        correct_word = get_word_at_position(reference_text, i1)
                    
                    corrections.append(
                        f"Position {i1}:\n"
                        f"  Typed word: '{typed_word}' (has extra characters)\n"
                        f"  Correct word: '{correct_word}'\n"
                        f"  Extra characters: {extra_chars_info}\n"
                    )
                
                total_errors += 1


    # Display results
    result_text.insert(tk.END, "=== TYPING ANALYSIS RESULTS ===\n\n")
    result_text.insert(tk.END, f"Accuracy: {accuracy_percentage:.2f}%\n")
    result_text.insert(tk.END, f"Total Errors: {total_errors}\n\n")

    if corrections:
        result_text.insert(tk.END, "=== DETAILED CORRECTIONS ===\n\n")
        for c in corrections[:30]:  # show first 30 corrections
            result_text.insert(tk.END, c + "\n")
        if len(corrections) > 30:
            result_text.insert(tk.END, f"...and {len(corrections)-30} more errors\n")
    else:
        result_text.insert(tk.END, "🎉 Perfect match! No corrections needed.\n")

    status_label.config(text=f"Analysis complete: {accuracy_percentage:.1f}% accuracy")
    print(f"Comparison completed: {accuracy_percentage:.2f}% accuracy")

def clear_all():
    """Clear all text areas"""
    txt1.delete("1.0", tk.END)
    typed1.delete("1.0", tk.END)
    result_text.delete("1.0", tk.END)
    status_label.config(text="All areas cleared")

def save_results():
    """Save the analysis results to a file"""
    results = result_text.get("1.0", tk.END).strip()
    if not results:
        messagebox.showwarning("No Results", "No analysis results to save")
        return
    
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"typing_analysis_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(results)
        
        messagebox.showinfo("Saved", f"Results saved to {filename}")
        status_label.config(text=f"Results saved: {filename}")
        
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save results: {e}")

#---------------------------GUI Setup-------------------------------
print("🚀 Initializing TakeNote GUI...")

# Create main window
window = tk.Tk()
window.title("TakeNote - Braille Text Analysis Tool")
window.geometry("1200x800")
window.configure(bg='#f0f0f0')

# Configure grid weights for responsive design
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

# Header frame
header_frame = tk.Frame(window, bg='#2c3e50', height=60)
header_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
header_frame.grid_propagate(False)

# Title and version label
title_font = tkFont.Font(family="Arial", size=16, weight="bold")
title_label = tk.Label(header_frame, text="TakeNote Analysis Tool", 
                      font=title_font, fg='white', bg='#2c3e50')
title_label.pack(side=tk.LEFT, padx=20, pady=15)

label1 = tk.Label(header_frame, text="Ready", font=("Arial", 12), 
                  fg='#ecf0f1', bg='#2c3e50')
label1.pack(side=tk.RIGHT, padx=20, pady=15)

# Main content frame
main_frame = tk.Frame(window, bg='#f0f0f0')
main_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

# Left panel - Reference text
left_frame = tk.LabelFrame(main_frame, text="Reference Text", 
                          font=("Arial", 11, "bold"), bg='#f0f0f0')
left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
left_frame.grid_rowconfigure(1, weight=1)
left_frame.grid_columnconfigure(0, weight=1)

# Reference text buttons
ref_buttons_frame = tk.Frame(left_frame, bg='#f0f0f0')
ref_buttons_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

btn_get = tk.Button(ref_buttons_frame, text="GET FILE", command=get,
                   bg='#3498db', fg='white', font=("Arial", 10, "bold"),
                   relief=tk.RAISED, bd=2)
btn_get.pack(side=tk.LEFT, padx=5)

btn_test_all = tk.Button(ref_buttons_frame, text="TEST TAKE NOTE", 
                        bg='#e74c3c', fg='white', font=("Arial", 10, "bold"),
                        relief=tk.RAISED, bd=2)
btn_test_all.pack(side=tk.RIGHT, padx=5)  # Changed LEFT to RIGHT

btn_clear = tk.Button(ref_buttons_frame, text="CLEAR ALL", command=clear_all,
                     bg='#95a5a6', fg='white', font=("Arial", 10, "bold"),
                     relief=tk.RAISED, bd=2)
btn_clear.pack(side=tk.LEFT, padx=5)

# Reference text area with scrollbar
ref_text_frame = tk.Frame(left_frame)
ref_text_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
ref_text_frame.grid_rowconfigure(0, weight=1)
ref_text_frame.grid_columnconfigure(0, weight=1)

txt1 = tk.Text(ref_text_frame, wrap=tk.WORD, font=("Consolas", 11),
               bg='white', fg='black', insertbackground='red')
txt1.grid(row=0, column=0, sticky='nsew')

scrollbar1 = tk.Scrollbar(ref_text_frame, orient=tk.VERTICAL, command=txt1.yview)
scrollbar1.grid(row=0, column=1, sticky='ns')
txt1.configure(yscrollcommand=scrollbar1.set)

# Right panel - Typed text and results
right_frame = tk.Frame(main_frame, bg='#f0f0f0')
right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_rowconfigure(1, weight=1)
right_frame.grid_columnconfigure(0, weight=1)

# Typed text section
typed_frame = tk.LabelFrame(right_frame, text="Typed Text / Transferred Data", 
                           font=("Arial", 11, "bold"), bg='#f0f0f0')
typed_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
typed_frame.grid_rowconfigure(1, weight=1)
typed_frame.grid_columnconfigure(0, weight=1)

# Typed text buttons
typed_buttons_frame = tk.Frame(typed_frame, bg='#f0f0f0')
typed_buttons_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

btn_transfer = tk.Button(typed_buttons_frame, text="TRANSFER FILES", command=transfer_files,
                        bg='#27ae60', fg='white', font=("Arial", 10, "bold"),
                        relief=tk.RAISED, bd=2)
btn_transfer.pack(side=tk.LEFT, padx=5)

btn_compare = tk.Button(typed_buttons_frame, text="COMPARE TEXT", command=compare_user_input,
                       bg='#f39c12', fg='white', font=("Arial", 10, "bold"),
                       relief=tk.RAISED, bd=2)
btn_compare.pack(side=tk.LEFT, padx=5)

# Typed text area with scrollbar
typed_text_frame = tk.Frame(typed_frame)
typed_text_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
typed_text_frame.grid_rowconfigure(0, weight=1)
typed_text_frame.grid_columnconfigure(0, weight=1)

typed1 = tk.Text(typed_text_frame, wrap=tk.WORD, font=("Consolas", 11),
                bg='#f8f9fa', fg='black', insertbackground='blue')
typed1.grid(row=0, column=0, sticky='nsew')

scrollbar2 = tk.Scrollbar(typed_text_frame, orient=tk.VERTICAL, command=typed1.yview)
scrollbar2.grid(row=0, column=1, sticky='ns')
typed1.configure(yscrollcommand=scrollbar2.set)

# Results section
results_frame = tk.LabelFrame(right_frame, text="Analysis Results", 
                             font=("Arial", 11, "bold"), bg='#f0f0f0')
results_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
results_frame.grid_rowconfigure(1, weight=1)
results_frame.grid_columnconfigure(0, weight=1)

# Results buttons
results_buttons_frame = tk.Frame(results_frame, bg='#f0f0f0')
results_buttons_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

btn_result = tk.Button(results_buttons_frame, text="RUN ANALYSIS", command=result,
                      bg='#9b59b6', fg='white', font=("Arial", 10, "bold"),
                      relief=tk.RAISED, bd=2)
btn_result.pack(side=tk.LEFT, padx=5)

btn_save = tk.Button(results_buttons_frame, text="SAVE RESULTS", command=save_results,
                    bg='#34495e', fg='white', font=("Arial", 10, "bold"),
                    relief=tk.RAISED, bd=2)
btn_save.pack(side=tk.LEFT, padx=5)

# Results text area with scrollbar
results_text_frame = tk.Frame(results_frame)
results_text_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
results_text_frame.grid_rowconfigure(0, weight=1)
results_text_frame.grid_columnconfigure(0, weight=1)

result_text = tk.Text(results_text_frame, wrap=tk.WORD, font=("Consolas", 10),
                     bg='#2c3e50', fg='#ecf0f1', insertbackground='yellow')
result_text.grid(row=0, column=0, sticky='nsew')

scrollbar3 = tk.Scrollbar(results_text_frame, orient=tk.VERTICAL, command=result_text.yview)
scrollbar3.grid(row=0, column=1, sticky='ns')
result_text.configure(yscrollcommand=scrollbar3.set)

# Status bar
status_frame = tk.Frame(window, bg='#34495e', height=30)
status_frame.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
status_frame.grid_propagate(False)

status_label = tk.Label(status_frame, text="Ready - Load a reference file to begin", 
                       font=("Arial", 10), fg='white', bg='#34495e')
status_label.pack(side=tk.LEFT, padx=10, pady=5)

# Initialize with welcome message
welcome_msg = """Welcome to TakeNote - Braille Text Analysis Tool

📝 Instructions:
1. Click 'GET FILE' to load a reference text file
2. Use 'TRANSFER FILES' to receive text from TakeNote device via Bluetooth
3. Or manually type/paste text in the 'Typed Text' area
4. Click 'COMPARE TEXT' to analyze typing accuracy
5. Use 'RUN ANALYSIS' for detailed statistical analysis

🔧 Features:
• Bluetooth file transfer from TakeNote devices
• Real-time text comparison and accuracy measurement
• Braille pattern conversion for hardware testing
• Batch processing of multiple text files
• Detailed error analysis and corrections

Ready to start your analysis!"""

result_text.insert(tk.END, welcome_msg)

# Handle window closing
def on_closing():
    """Handle window closing event"""
    if messagebox.askokcancel("Quit", "Do you want to quit TakeNote?"):
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

# Center the window
window.update_idletasks()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - window.winfo_width()) // 2
y = (screen_height - window.winfo_height()) // 2
window.geometry(f"+{x}+{y}")

print("✅ TakeNote GUI initialized successfully!")
print("🖥️  Starting main event loop...")

# Start the GUI event loop
if __name__ == "__main__":
    try:
        window.mainloop()
    except KeyboardInterrupt:
        print("\n⏹️  Application interrupted by user")
    except Exception as e:
        print(f"❌ Application error: {e}")
    finally:
        print("👋 TakeNote application closed")
        


def get():
    """Load a text file using file dialog, convert hex to text, and show with line numbers"""
    try:
        # Use current directory as initial directory
        initial_dir = os.getcwd()
        
        filepath = askopenfilename(
            initialdir=initial_dir,
            title="Select a text file",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        
        if not filepath:
            return
            
        print(f"Selected file path: {filepath}")
        
        # Clear the main text area
        txt1.delete("1.0", tk.END)
        
        # Read the file
        with open(filepath, "r", encoding='utf-8') as input_file:
            text = input_file.read()
        
        print(f"Original content length: {len(text)} characters")
        
        # Detect and convert hex format to English text
        converted_text = convert_hex_content_to_english(text)
        
       
        
        # Display the numbered text
        txt1.insert(tk.END, converted_text )
        
        # Clear user input area on new file load
        typed1.delete("1.0", tk.END)
        
        # Show success message with line count
        status_label.config(text=f"Loaded: {os.path.basename(filepath)}  - Hex converted to English")
        print(f"✅ File loaded successfully with ")
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {str(e)}")
        status_label.config(text="Error loading file")
        print(f"❌ Error: {e}")


def convert_hex_content_to_english(content):
    """Convert hex format content to English text"""
    
    # First, try using the external converter if available
    if CONVERTER_AVAILABLE:
        try:
            converted = Hex2TxtTakenote_ENG1_aug_2021.convert_hex_to_text(content)
            if converted and converted != content:
                print("✅ Converted using Hex2TxtTakenote_ENG1_aug_2021")
                return converted
        except Exception as e:
            print(f"⚠️  External converter failed: {e}, trying built-in converter")
    
    # Built-in hex to text converter
    try:
        # Remove whitespace and check if content looks like hex
        cleaned = content.replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')
        
        # Check if content is predominantly hex characters
        hex_chars = sum(c in '0123456789ABCDEFabcdef' for c in cleaned)
        hex_percentage = (hex_chars / len(cleaned) * 100) if len(cleaned) > 0 else 0
        
        if hex_percentage > 80 and len(cleaned) >= 10:  # Likely hex content
            print(f"📊 Detected hex content ({hex_percentage:.1f}% hex characters)")
            
            # Try to convert hex pairs to ASCII
            converted_text = ""
            i = 0
            
            while i < len(cleaned) - 1:
                try:
                    # Take two hex characters at a time
                    hex_pair = cleaned[i:i+2]
                    
                    # Convert hex to decimal
                    decimal_value = int(hex_pair, 16)
                    
                    # Convert to ASCII character if in printable range
                    if 32 <= decimal_value <= 126:  # Printable ASCII
                        converted_text += chr(decimal_value)
                    elif decimal_value == 10:  # Newline
                        converted_text += '\n'
                    elif decimal_value == 13:  # Carriage return
                        converted_text += '\r'
                    elif decimal_value == 9:  # Tab
                        converted_text += '\t'
                    else:
                        # Non-printable, show as [HEX]
                        converted_text += f"[{hex_pair}]"
                    
                    i += 2
                    
                except ValueError:
                    # Not a valid hex pair, skip
                    converted_text += cleaned[i]
                    i += 1
            
            if converted_text.strip():
                print(f"✅ Converted hex to text: {len(converted_text)} characters")
                return converted_text
            else:
                print("⚠️  Hex conversion resulted in empty text")
        else:
            print(f"ℹ️  Content doesn't appear to be hex format ({hex_percentage:.1f}% hex)")
    
    except Exception as e:
        print(f"⚠️  Built-in hex conversion error: {e}")
    
    # If conversion failed or not hex, return original content
    print("ℹ️  Returning original content")
    return content


def transfer_files():
    """Transfer files via Bluetooth and automatically evaluate"""
    global version_number
    
    # Always simulate on macOS if Bluetooth is not available
    if not BLUETOOTH_AVAILABLE or platform.system() == "Darwin":
        messagebox.showwarning(
            "Bluetooth Not Available",
            "Bluetooth is not supported on macOS or required modules are missing. Simulating file transfer."
        )
        simulate_transfer()
        return

    try:
        print(f"🔍 Starting Bluetooth transfer for {TARGET_NAME}...")
        status_label.config(text="Searching for TakeNote device...")
        
        # Find the device
        addr = find_device(TARGET_NAME)
        if not addr:
            messagebox.showerror("Device Not Found", f"Could not find '{TARGET_NAME}' device!")
            status_label.config(text="Device not found")
            return
        
        version_number = TARGET_NAME
        label1.config(text=version_number)
        
        print(f"🔗 Connecting to {TARGET_NAME} at {addr}:{PORT}")
        status_label.config(text="Connecting to device...")
        
        # Create Bluetooth socket
        sock = socket.socket(
            socket.AF_BLUETOOTH,
            socket.SOCK_STREAM,
            socket.BTPROTO_RFCOMM,
        )
        
        # Connect to device
        sock.connect((addr, PORT))
        print("✅ Connected!")
        status_label.config(text="Connected! Requesting files...")
        
        # Send command to request all files
        cmd = b'0'  # Request all new files
        sock.send(cmd)
        print(f"📡 Sent {cmd!r} → requesting all new files")
        
        # Receive all data
        status_label.config(text="Receiving files...")
        data = receive_all(sock)
        
        if not data:
            messagebox.showwarning("No Data", "No data received from device.")
            status_label.config(text="No data received")
            return
        
        # Parse and save files
        status_label.config(text="Parsing and saving files...")
        saved_files = parse_and_save(data)
        
        if not saved_files:
            messagebox.showwarning("No Files", "No files were saved from the transfer.")
            status_label.config(text="No files saved")
            return
        
        # Process the received files
        status_label.config(text="Processing received files...")
        process_transferred_files(saved_files)
        
        # Show completion message
        messagebox.showinfo("Transfer Complete", f"Successfully transferred and processed {len(saved_files)} files.")
        status_label.config(text=f"Transfer completed: {len(saved_files)} files")
        
    except Exception as e:
        print(f"❌ Bluetooth transfer error: {e}")
        messagebox.showerror("Transfer Error", f"Bluetooth transfer failed: {e}")
        status_label.config(text="Transfer failed")

def simulate_transfer():
    """Simulate file transfer for testing when Bluetooth is not available"""
    print("Simulating file transfer...")
    status_label.config(text="Simulating file transfer...")
    
    # Look for existing NOTE files in current directory for simulation
    note_files = [f for f in os.listdir('.') if f.startswith('NOTE') and f.endswith('.txt')]
    
    if note_files:
        print(f"Found {len(note_files)} NOTE files for simulation")
        status_label.config(text=f"Found {len(note_files)} files for simulation")
        process_transferred_files(note_files)
    else:
        # Create a sample file for demonstration
        sample_content = "This is a simulated transfer file for testing purposes."
        sample_file = "NOTE1_simulated.txt"
        with open(sample_file, 'w') as f:
            f.write(sample_content)
        print(f"Created sample file: {sample_file}")
        process_transferred_files([sample_file])
    
    # Simulate delay
    window.after(2000, lambda: status_label.config(text="Transfer simulation completed"))

def process_transferred_files(file_list):
    """Process the transferred files and load them for evaluation"""
    if not file_list:
        return
    
    # Use the most recent file (or first one) as the typed input
    latest_file = file_list[0]  # You might want to sort by date/time
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if content appears to be hex data and convert if possible
        if content.strip().replace(' ', '').replace('\n', '').replace('\r', '').isalnum() and len(content) > 50:
            # Might be hex data, try to convert
            converted_content = convert_hex_content_to_english(content)
            if converted_content != content:
                print(f"✅ Converted hex data to text")
                content = converted_content
        
        # Load the content into the typing area
        typed1.delete("1.0", tk.END)
        typed1.insert(tk.END, content)
        
        print(f"✅ Loaded transferred file content: {latest_file}")
        
        # If we have reference text loaded, automatically start comparison
        if txt1.get("1.0", tk.END).strip():
            window.after(1000, compare_user_input)  # Small delay then auto-compare
        else:
            # Show message to load reference text
            txt1.delete("1.0", tk.END)
            txt1.insert(tk.END, f"✅ Transferred file loaded: {latest_file}\n\n")
            txt1.insert(tk.END, "Please use 'GET FILE' to load a reference text for comparison.\n\n")
            txt1.insert(tk.END, f"Transferred content preview:\n{content[:200]}{'...' if len(content) > 200 else ''}")
        
    except Exception as e:
        print(f"❌ Error processing transferred file {latest_file}: {e}")
        messagebox.showerror("File Processing Error", f"Error processing transferred file: {e}")


def compare_user_input():
    """Compare the typed text with the reference text"""
    reference_text = txt1.get("1.0", tk.END).strip()
    typed_text = typed1.get("1.0", tk.END).strip()
    
    if not reference_text:
        messagebox.showwarning("No Reference", "Please load a reference text file first using 'GET FILE'")
        return
    
    if not typed_text:
        messagebox.showwarning("No Input", "Please enter some text in the typing area")
        return
    
    # Clear results area
    result_text.delete("1.0", tk.END)

    # Comprehensive Braille number-key mapping
    braille_keys = {
        # Lowercase letters
        "a": "1",    "b": "12",   "c": "14",   "d": "145",  "e": "15",
        "f": "124",  "g": "1245", "h": "125",  "i": "24",   "j": "245",
        "k": "13",   "l": "123",  "m": "134",  "n": "1345", "o": "135",
        "p": "1234", "q": "12345","r": "1235", "s": "234",  "t": "2345",
        "u": "136",  "v": "1236", "w": "2456", "x": "1346", "y": "13456",
        "z": "1356",
        
        # Uppercase letters (Capital sign + letter)
        "A": "6-1",    "B": "6-12",   "C": "6-14",   "D": "6-145",  "E": "6-15",
        "F": "6-124",  "G": "6-1245", "H": "6-125",  "I": "6-24",   "J": "6-245",
        "K": "6-13",   "L": "6-123",  "M": "6-134",  "N": "6-1345", "O": "6-135",
        "P": "6-1234", "Q": "6-12345","R": "6-1235", "S": "6-234",  "T": "6-2345",
        "U": "6-136",  "V": "6-1236", "W": "6-2456", "X": "6-1346", "Y": "6-13456",
        "Z": "6-1356",
        
        # Numbers (Number sign + letter)
        "0": "3456-245", "1": "3456-1",   "2": "3456-12",  "3": "3456-14",  
        "4": "3456-145", "5": "3456-15",  "6": "3456-124", "7": "3456-1245",
        "8": "3456-125", "9": "3456-24",
        
        # Punctuation marks
        ",": "2",           # Comma
        ";": "23",          # Semicolon
        ":": "25",          # Colon
        ".": "256",         # Period
        "!": "235",         # Exclamation mark
        "?": "236",         # Question mark
        "'": "3",           # Apostrophe
        '"': "5",           # Quotation mark
        "-": "36",          # Hyphen
        "(": "2356",        # Opening parenthesis
        ")": "2356",        # Closing parenthesis
        "/": "34",          # Slash
        "@": "4-1",         # At sign
        "#": "3456",        # Number sign
        "$": "4-234",       # Dollar sign
        "%": "4-356",       # Percent sign
        "&": "4-12346",     # Ampersand
        "*": "5-35",        # Asterisk
        "+": "5-235",       # Plus sign
        "=": "5-2356",      # Equals sign
        " ": "0",           # Space
    }

    # Helper function to format braille keys with commas
    def format_braille_key(key):
        """Format braille key to show dots separated by commas (e.g., '1,2,3')"""
        if key == "?":
            return "?"
        # Replace hyphens with commas and add commas between individual digits
        # Handle cases like "6-1" -> "6,1" and "234" -> "2,3,4"
        formatted = key.replace("-", ",")
        # Add commas between consecutive digits if not already present
        result = []
        for char in formatted:
            if char.isdigit():
                result.append(char)
            elif char == ",":
                result.append(char)
        return ",".join([c for c in result if c != ","])

    # Helper function to get the word at a given character position
    def get_word_at_position(text, pos):
        """Return the whole word that contains character index 'pos'."""
        if pos >= len(text):
            return ""
        words = text.split()
        index = 0
        for w in words:
            start = index
            end = index + len(w)
            if start <= pos < end:
                return w
            index = end + 1   # +1 for space
        return ""
    
    # Helper function to get character type
    def get_char_type(char):
        """Identify character type"""
        if char.isalpha():
            return "Letter"
        elif char.isdigit():
            return "Number"
        elif char in ".,;:!?'\"":
            return "Punctuation"
        elif char in "@#$%&*+-=/()[]{}":
            return "Symbol"
        elif char == " ":
            return "Space"
        else:
            return "Character"

    matcher = difflib.SequenceMatcher(None, reference_text, typed_text)
    accuracy_percentage = matcher.ratio() * 100
    
    corrections = []
    total_errors = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():

        # REPLACEMENT
        if tag == "replace":
            typed_word = get_word_at_position(typed_text, j1)
            correct_word = get_word_at_position(reference_text, i1)

            wrong_char = correct_char = "?"
            char_type = "Character"
            for k in range(min(len(correct_word), len(typed_word))):
                if typed_word[k] != correct_word[k]:
                    wrong_char = typed_word[k]
                    correct_char = correct_word[k]
                    char_type = get_char_type(correct_char)
                    break

            wrong_braille = format_braille_key(braille_keys.get(wrong_char, "?"))
            correct_braille = format_braille_key(braille_keys.get(correct_char, "?"))

            corrections.append(
                f"Position {i1}:\n"
                f"  Typed word: '{typed_word}'\n"
                f"  Correct word: '{correct_word}'\n"
                f"  Wrong {char_type}: '{wrong_char}' → Correct {char_type}: '{correct_char}'\n"
                f"  Wrong braille key: {wrong_braille} → Correct braille key: {correct_braille}\n"
            )
            total_errors += 1

        # DELETE (Missing content - should have been typed)
        elif tag == "delete":
            missing_content = reference_text[i1:i2]
            missing_chars = [char for char in missing_content]
            char_types = [get_char_type(char) for char in missing_chars]

            correct_word = get_word_at_position(reference_text, i1)
            typed_word = get_word_at_position(typed_text, j1) if j1 < len(typed_text) else ""

            # Build missing characters info (character and type only)
            missing_chars_info = ', '.join(f"'{char}' ({char_type})" for char, char_type in zip(missing_chars, char_types))
            
            # Build braille keys separately on a new line
            missing_braille_keys = ', '.join(f"'{char}': {format_braille_key(braille_keys.get(char, '?'))}" for char in missing_chars)

            if missing_content.strip() and ' ' in missing_content:
                corrections.append(
                    f"Position {i1}:\n"
                    f"  Missing content (not typed): '{missing_content}'\n"
                    f"  Missing characters: {missing_chars_info}\n"
                    f"  Correct braille keys: {missing_braille_keys}\n"
                )
            else:
                corrections.append(
                    f"Position {i1}:\n"
                    f"  Typed word: '{typed_word}' (missing characters)\n"
                    f"  Correct word: '{correct_word}'\n"
                    f"  Missing characters: {missing_chars_info}\n"
                    f"  Correct braille keys: {missing_braille_keys}\n"
                )
            total_errors += 1

       # INSERT (Extra content - should NOT have been typed)
        elif tag == "insert":
            extra_content = typed_text[j1:j2]
            
            # Split the extra content by spaces to identify separate insertions
            parts = []
            current_part = ""
            part_start = j1
            
            for idx, char in enumerate(extra_content):
                if char == ' ':
                    if current_part:
                        parts.append((part_start, current_part, 'chars'))
                        part_start = j1 + idx + 1
                        current_part = ""
                else:
                    current_part += char
            
            if current_part:
                parts.append((part_start, current_part, 'chars'))
            
            # Process each part separately
            for part_pos, part_content, part_type in parts:
                extra_chars = [char for char in part_content]
                char_types = [get_char_type(char) for char in extra_chars]
                extra_chars_info = ', '.join(f"'{char}' ({char_type})" for char, char_type in zip(extra_chars, char_types))
                
                # Check if this part is a complete word or extra characters in a word
                is_surrounded_by_spaces = (
                    (part_pos > 0 and typed_text[part_pos - 1] == ' ') and 
                    (part_pos + len(part_content) < len(typed_text) and typed_text[part_pos + len(part_content)] == ' ')
                )
                
                if is_surrounded_by_spaces or len(parts) > 1:
                    # This is an extra word
                    corrections.append(
                        f"Position {i1}:\n"
                        f"  Extra word typed (should not be typed): '{part_content}'\n"
                        f"  Extra characters: {extra_chars_info}\n"
                    )
                else:
                    # Extra characters within a word
                    typed_word = get_word_at_position(typed_text, part_pos)
                    correct_word = ""
                    if i1 > 0:
                        correct_word = get_word_at_position(reference_text, i1 - 1)
                    if not correct_word and i1 < len(reference_text):
                        correct_word = get_word_at_position(reference_text, i1)
                    
                    corrections.append(
                        f"Position {i1}:\n"
                        f"  Typed word: '{typed_word}' (has extra characters)\n"
                        f"  Correct word: '{correct_word}'\n"
                        f"  Extra characters: {extra_chars_info}\n"
                    )
                
                total_errors += 1


    # Display results
    result_text.insert(tk.END, "=== TYPING ANALYSIS RESULTS ===\n\n")
    result_text.insert(tk.END, f"Accuracy: {accuracy_percentage:.2f}%\n")
    result_text.insert(tk.END, f"Total Errors: {total_errors}\n\n")

    if corrections:
        result_text.insert(tk.END, "=== DETAILED CORRECTIONS ===\n\n")
        for c in corrections[:30]:  # show first 30 corrections
            result_text.insert(tk.END, c + "\n")
        if len(corrections) > 30:
            result_text.insert(tk.END, f"...and {len(corrections)-30} more errors\n")
    else:
        result_text.insert(tk.END, "🎉 Perfect match! No corrections needed.\n")

    status_label.config(text=f"Analysis complete: {accuracy_percentage:.1f}% accuracy")
    print(f"Comparison completed: {accuracy_percentage:.2f}% accuracy")

def clear_all():
    """Clear all text areas"""
    txt1.delete("1.0", tk.END)
    typed1.delete("1.0", tk.END)
    result_text.delete("1.0", tk.END)
    status_label.config(text="All areas cleared")

def save_results():
    """Save the analysis results to a file"""
    results = result_text.get("1.0", tk.END).strip()
    if not results:
        messagebox.showwarning("No Results", "No analysis results to save")
        return
    
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"typing_analysis_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(results)
        
        messagebox.showinfo("Saved", f"Results saved to {filename}")
        status_label.config(text=f"Results saved: {filename}")
        
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save results: {e}")

#---------------------------GUI Setup-------------------------------
print("🚀 Initializing TakeNote GUI...")

# Create main window
window = tk.Tk()
window.title("TakeNote - Braille Text Analysis Tool")
window.geometry("1200x800")
window.configure(bg='#f0f0f0')

# Configure grid weights for responsive design
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

# Header frame
header_frame = tk.Frame(window, bg='#2c3e50', height=60)
header_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
header_frame.grid_propagate(False)

# Title and version label
title_font = tkFont.Font(family="Arial", size=16, weight="bold")
title_label = tk.Label(header_frame, text="TakeNote Analysis Tool", 
                      font=title_font, fg='white', bg='#2c3e50')
title_label.pack(side=tk.LEFT, padx=20, pady=15)

label1 = tk.Label(header_frame, text="Ready", font=("Arial", 12), 
                  fg='#ecf0f1', bg='#2c3e50')
label1.pack(side=tk.RIGHT, padx=20, pady=15)

# Main content frame
main_frame = tk.Frame(window, bg='#f0f0f0')
main_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

# Left panel - Reference text
left_frame = tk.LabelFrame(main_frame, text="Reference Text", 
                          font=("Arial", 11, "bold"), bg='#f0f0f0')
left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
left_frame.grid_rowconfigure(1, weight=1)
left_frame.grid_columnconfigure(0, weight=1)

# Reference text buttons
ref_buttons_frame = tk.Frame(left_frame, bg='#f0f0f0')
ref_buttons_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

btn_get = tk.Button(ref_buttons_frame, text="GET FILE", command=get,
                   bg='#3498db', fg='white', font=("Arial", 10, "bold"),
                   relief=tk.RAISED, bd=2)
btn_get.pack(side=tk.LEFT, padx=5)
btn_test_all = tk.Button(
    ref_buttons_frame,
    text="TEST TAKE NOTE",
    command=test_individual,
    bg='#e74c3c',
    fg='white',
    font=("Arial", 10, "bold"),
    relief=tk.RAISED,
    bd=2
)


btn_clear = tk.Button(ref_buttons_frame, text="CLEAR ALL", command=clear_all,
                     bg='#95a5a6', fg='white', font=("Arial", 10, "bold"),
                     relief=tk.RAISED, bd=2)
btn_clear.pack(side=tk.LEFT, padx=5)

# Reference text area with scrollbar
ref_text_frame = tk.Frame(left_frame)
ref_text_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
ref_text_frame.grid_rowconfigure(0, weight=1)
ref_text_frame.grid_columnconfigure(0, weight=1)

txt1 = tk.Text(ref_text_frame, wrap=tk.WORD, font=("Consolas", 11),
               bg='white', fg='black', insertbackground='red')
txt1.grid(row=0, column=0, sticky='nsew')

scrollbar1 = tk.Scrollbar(ref_text_frame, orient=tk.VERTICAL, command=txt1.yview)
scrollbar1.grid(row=0, column=1, sticky='ns')
txt1.configure(yscrollcommand=scrollbar1.set)

# Right panel - Typed text and results
right_frame = tk.Frame(main_frame, bg='#f0f0f0')
right_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_rowconfigure(1, weight=1)
right_frame.grid_columnconfigure(0, weight=1)

# Typed text section
typed_frame = tk.LabelFrame(right_frame, text="Typed Text / Transferred Data", 
                           font=("Arial", 11, "bold"), bg='#f0f0f0')
typed_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
typed_frame.grid_rowconfigure(1, weight=1)
typed_frame.grid_columnconfigure(0, weight=1)

# Typed text buttons
typed_buttons_frame = tk.Frame(typed_frame, bg='#f0f0f0')
typed_buttons_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

btn_transfer = tk.Button(typed_buttons_frame, text="TRANSFER FILES", command=transfer_files,
                        bg='#27ae60', fg='white', font=("Arial", 10, "bold"),
                        relief=tk.RAISED, bd=2)
btn_transfer.pack(side=tk.LEFT, padx=5)

btn_compare = tk.Button(typed_buttons_frame, text="COMPARE TEXT", command=compare_user_input,
                       bg='#f39c12', fg='white', font=("Arial", 10, "bold"),
                       relief=tk.RAISED, bd=2)
btn_compare.pack(side=tk.LEFT, padx=5)

# Typed text area with scrollbar
typed_text_frame = tk.Frame(typed_frame)
typed_text_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
typed_text_frame.grid_rowconfigure(0, weight=1)
typed_text_frame.grid_columnconfigure(0, weight=1)

typed1 = tk.Text(typed_text_frame, wrap=tk.WORD, font=("Consolas", 11),
                bg='#f8f9fa', fg='black', insertbackground='blue')
typed1.grid(row=0, column=0, sticky='nsew')

scrollbar2 = tk.Scrollbar(typed_text_frame, orient=tk.VERTICAL, command=typed1.yview)
scrollbar2.grid(row=0, column=1, sticky='ns')
typed1.configure(yscrollcommand=scrollbar2.set)

# Results section
results_frame = tk.LabelFrame(right_frame, text="Analysis Results", 
                             font=("Arial", 11, "bold"), bg='#f0f0f0')
results_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
results_frame.grid_rowconfigure(1, weight=1)
results_frame.grid_columnconfigure(0, weight=1)

# Results buttons
results_buttons_frame = tk.Frame(results_frame, bg='#f0f0f0')
results_buttons_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

btn_result = tk.Button(results_buttons_frame, text="RUN ANALYSIS", command=result,
                      bg='#9b59b6', fg='white', font=("Arial", 10, "bold"),
                      relief=tk.RAISED, bd=2)
btn_result.pack(side=tk.LEFT, padx=5)

btn_save = tk.Button(results_buttons_frame, text="SAVE RESULTS", command=save_results,
                    bg='#34495e', fg='white', font=("Arial", 10, "bold"),
                    relief=tk.RAISED, bd=2)
btn_save.pack(side=tk.LEFT, padx=5)

# Results text area with scrollbar
results_text_frame = tk.Frame(results_frame)
results_text_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
results_text_frame.grid_rowconfigure(0, weight=1)
results_text_frame.grid_columnconfigure(0, weight=1)

result_text = tk.Text(results_text_frame, wrap=tk.WORD, font=("Consolas", 10),
                     bg='#2c3e50', fg='#ecf0f1', insertbackground='yellow')
result_text.grid(row=0, column=0, sticky='nsew')

scrollbar3 = tk.Scrollbar(results_text_frame, orient=tk.VERTICAL, command=result_text.yview)
scrollbar3.grid(row=0, column=1, sticky='ns')
result_text.configure(yscrollcommand=scrollbar3.set)

# Status bar
status_frame = tk.Frame(window, bg='#34495e', height=30)
status_frame.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
status_frame.grid_propagate(False)

status_label = tk.Label(status_frame, text="Ready - Load a reference file to begin", 
                       font=("Arial", 10), fg='white', bg='#34495e')
status_label.pack(side=tk.LEFT, padx=10, pady=5)

# Initialize with welcome message
welcome_msg = """Welcome to TakeNote - Braille Text Analysis Tool

📝 Instructions:
1. Click 'GET FILE' to load a reference text file
2. Use 'TRANSFER FILES' to receive text from TakeNote device via Bluetooth
3. Or manually type/paste text in the 'Typed Text' area
4. Click 'COMPARE TEXT' to analyze typing accuracy
5. Use 'RUN ANALYSIS' for detailed statistical analysis

🔧 Features:
• Bluetooth file transfer from TakeNote devices
• Real-time text comparison and accuracy measurement
• Braille pattern conversion for hardware testing
• Batch processing of multiple text files
• Detailed error analysis and corrections

Ready to start your analysis!"""

result_text.insert(tk.END, welcome_msg)

# Handle window closing
def on_closing():
    """Handle window closing event"""
    if messagebox.askokcancel("Quit", "Do you want to quit TakeNote?"):
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

# Center the window
window.update_idletasks()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - window.winfo_width()) // 2
y = (screen_height - window.winfo_height()) // 2
window.geometry(f"+{x}+{y}")

print("✅ TakeNote GUI initialized successfully!")
print("🖥️  Starting main event loop...")

# Start the GUI event loop
if __name__ == "__main__":
    try:
        window.mainloop()
    except KeyboardInterrupt:
        print("\n⏹️  Application interrupted by user")
    except Exception as e:
        print(f"❌ Application error: {e}")
    finally:
        print("👋 TakeNote application closed")
        

