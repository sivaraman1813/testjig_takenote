## *********************************************************************************************
## * File Name         : testjig.py (Linux version)
## * Python            : V3.12
## * Modified for      : Linux (Ubuntu/Debian)
## * Modified @date    : 2024
## **********************************************************************************************

import os
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import time
import pyfirmata
import numpy as np
import sys
import Hex2TxtTakenote_ENG1_aug_2021
from tkinter import ttk
import tkinter.font as tkFont
import datetime
import glob
import serial.tools.list_ports

# ===== LINUX PATH CONFIGURATION =====
BASE_DIR = "/home/ae/take_note/Testjig"
INPUT_DIR = os.path.join(BASE_DIR, "Input_files")
OUTPUT_DIR = os.path.join(BASE_DIR, "output_from_takenote")
RESULT_DIR = os.path.join(BASE_DIR, "result")

# Create directories if they don't exist
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

print(f"✅ Directories configured:")
print(f"   Input: {INPUT_DIR}")
print(f"   Output: {OUTPUT_DIR}")
print(f"   Result: {RESULT_DIR}")

# ===== GLOBAL VARIABLES =====
board = None
time_hour = 0
time_minute = 0
time_second = 0
a = 0

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
    global board
    
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


def result():
    """Compare input and output files and produce result"""
    global time_hour, time_minute, time_second, a
    
    inp = nameEntered1.get()
    b = a
    i = 0
    j = 0
    
    print("###########################################################################")
    print("TakeNote Number is:", inp)
    current_time = datetime.datetime.now()
    
    print("Date : ", end="")
    print(current_time.day, "/", current_time.month, "/", current_time.year)
    print("Time: ", end="")
    print(current_time.hour, ":", current_time.minute, ":", current_time.second)
    print("Time Taken by Testjig process is: %d hours:%d minutes:%d seconds" % (time_hour, time_minute, time_second))

    count_to = 0
    count_from = 0
    
    for path in os.listdir(INPUT_DIR):
        if os.path.isfile(os.path.join(INPUT_DIR, path)):
            count_to += 1
    print("Number of files given to testJig:", count_to - 1)
    
    for path in os.listdir(OUTPUT_DIR):
        if os.path.isfile(os.path.join(OUTPUT_DIR, path)):
            count_from += 1
    print("Number of files from takenote:", int((count_from / 2)), '\n')
    
    c = b
    d = int((count_from / 2))
    count_from_testJig = b + d
    
    for b in range(c, count_from_testJig):
        i = i + 1
        file1 = open(os.path.join(INPUT_DIR, f"{i}.txt"), 'r')
        file2 = open(os.path.join(OUTPUT_DIR, f"{b}_op.txt"), 'r')
   
        data1 = file1.read()
        print('Number of characters used in file1:', len(data1))
        data2 = file2.read()
        print('Number of characters used in file2:', len(data2))
        error = len(data1) - len(data2)
        print("The missing characters are:", error)
        score = (len(data2) / len(data1)) * 100
        print("score in percentage: ", score, "%")
        if error == 0:
            print('-------PASS------\n')
        else:
            print('*******FAIL******\n')
        
        file1.close()
        file2.close()
    
    print("Result will be stored as text file also")
    
    original_stdout = sys.stdout
    
    # Write to result file
    with open(os.path.join(RESULT_DIR, 'TestJig_final_result.txt'), 'w') as f:
        sys.stdout = f
        print("###########################################################################")
        print("TakeNote Number is:", inp)
        current_time = datetime.datetime.now()
        print("Date : ", end="")
        print(current_time.day, "/", current_time.month, "/", current_time.year)
        print("Time: ", end="")
        print(current_time.hour, ":", current_time.minute, ":", current_time.second)
        print("Time Taken by Testjig process is: %d hours:%d minutes:%d seconds" % (time_hour, time_minute, time_second))
        
        count_to = 0
        count_from = 0
        
        for path in os.listdir(INPUT_DIR):
            if os.path.isfile(os.path.join(INPUT_DIR, path)):
                count_to += 1
        print("Number of files given to testJig:", count_to - 1)
        
        for path in os.listdir(OUTPUT_DIR):
            if os.path.isfile(os.path.join(OUTPUT_DIR, path)):
                count_from += 1
        print("Number of files from takenote:", int((count_from / 2)), '\n')
        
        e = b
        
        for e in range(c, count_from_testJig):
            j = j + 1
            file1 = open(os.path.join(INPUT_DIR, f"{j}.txt"), 'r')
            file2 = open(os.path.join(OUTPUT_DIR, f"{e}_op.txt"), 'r')
        
            data1 = file1.read()
            print('Number of characters used in file1:', len(data1))
            data2 = file2.read()
            print('Number of characters used in file2:', len(data2))
            error = len(data1) - len(data2)
            print("The missing characters are:", error)
            score = (len(data2) / len(data1)) * 100
            print("score in percentage: ", score, "%")
            if error == 0:
                print('-------PASS------\n')
            else:
                print('*******FAIL******\n')
            
            file1.close()
            file2.close()
        
        sys.stdout = original_stdout


def test_individual():
    """Test individual file"""
    global board
    
    if board is None:
        messagebox.showwarning("Board Error", "Arduino not connected. Please connect Arduino first.")
        return
    
    file_open()
    time.sleep(5)
    x = txt1.get("1.0", tk.END)
    count = 0
    num_flog = 0
    
    while (count < (len(x) - 1)):
        rec = x[count]
        print(rec)
        if(rec >= 'a' and rec <= 'z'):   
            if(num_flog == 1):
                num_al()
            num_flog = 0
            outled = alplow_brl(rec)
        elif(rec >= 'A' and rec <= 'Z'):
            if(num_flog == 1):
                num_al()
            num_flog = 0
            capital()
            outled = alpup_brl(rec)
        elif(rec >= '0' and rec <= '9'):
            if (num_flog == 0):
                al_num()
            num_flog = 1
            outled = num_brl(rec)
        else:
            outled = alplow_brl(rec)
        dot_led(outled) 
        count = count + 1
    file_close()


def alplow_brl(rec):
    """Convert lowercase alphabet to braille"""
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
    xx = alp_lower_brl.get(rec, alp_lower_brl["non"])
    return xx


def alpup_brl(rec):
    """Convert uppercase alphabet to braille"""
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
    xx = alp_upper_brl[rec]
    return xx


def num_brl(rec):
    """Convert number to braille"""
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
    xx = number_brl[rec]
    return xx


def file_open():
    """Open file signal to Arduino"""
    global board
    if board is None:
        print("⚠️ Board not connected")
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


def file_close():
    """Close file signal to Arduino"""
    global board
    if board is None:
        print("⚠️ Board not connected")
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


def dot_led(outled):
    """Send dot pattern to Arduino"""
    global board
    if board is None:
        print("⚠️ Board not connected")
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
    """Alphabet to number signal"""
    global board
    if board is None:
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
    """Number to alphabet signal"""
    global board
    if board is None:
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
    """Capital letter signal"""
    global board
    if board is None:
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


def get():
    """Load a file for testing"""
    filepath = askopenfilename(
        initialdir=INPUT_DIR,
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
    )
    
    if not filepath:
        return
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()
            txt1.delete("1.0", tk.END)
            txt1.insert(tk.END, text)
            print(f"✅ Loaded file: {os.path.basename(filepath)}")
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        messagebox.showerror("File Error", f"Could not load file: {e}")


def test_files_all():
    """Test all files automatically"""
    global time_hour, time_minute, time_second
    
    start = time.time()
    count_to = 0
    j = 0
    
    for path in os.listdir(INPUT_DIR):
        if os.path.isfile(os.path.join(INPUT_DIR, path)):
            count_to += 1
    
    print("Number of files given to testJig:", count_to - 1)
    print("\n")
    
    for count in range(1, count_to):
        j += 1
        file_path = os.path.join(INPUT_DIR, f"{j}.txt")
        
        if not os.path.exists(file_path):
            print(f"⚠️ File not found: {file_path}")
            continue
            
        with open(file_path, 'r', encoding='utf-8') as file1:
            print(file1.read())
        
        txt1.delete("1.0", tk.END)
        
        with open(file_path, 'r', encoding='utf-8') as input_file:
            text = input_file.read()
            txt1.insert(tk.END, text)
            test_individual()
            time.sleep(7)
    
    end = time.time()
    difference = end - start
    hour = difference // 3600
    difference %= 3600
    minute = difference // 60
    difference %= 60
    second = difference
    print("Time Taken by Testjig process is: %d hours:%d minutes:%d seconds" % (hour, minute, second))
    time_hour = hour
    time_minute = minute
    time_second = second


def transfer_files():
    """Transfer files - Bluetooth not implemented for Linux"""
    messagebox.showinfo("Transfer Files", "Bluetooth transfer not implemented in this Linux version.\nPlease manually place output files in the output directory.")


def transfer_files_short():
    """Transfer files short - Bluetooth not implemented for Linux"""
    messagebox.showinfo("Transfer Files", "Bluetooth transfer not implemented in this Linux version.")


# ===== GUI SETUP =====
window = tk.Tk()
window.title("TestJig Program (pass/fail) - Linux Version")
window.minsize(600, 400)

label1 = ttk.Label(window, text="TakeNote Number")
name1 = tk.StringVar()
nameEntered1 = ttk.Entry(window, width=20, textvariable=name1)

txt1 = tk.Text(window, height=35, width=80, bd=2)

button1 = tk.Button(window, text="RESULT", width=25, height=5, command=result)
button2 = tk.Button(window, text="GET", width=20, height=2, command=get)
button3 = tk.Button(window, text="TEST INDIVIDUAL", width=20, height=2, command=test_individual)
button4 = tk.Button(window, text="TEST", width=25, height=3, command=test_files_all)
button5 = tk.Button(window, text="TRANSFER", width=20, height=2, command=transfer_files)

label1.grid(column=1, row=0)
nameEntered1.grid(column=0, row=0)
button1.grid(column=1, row=5)
button2.grid(column=8, row=3)
button3.grid(column=8, row=4)
button4.grid(column=1, row=4)
button5.grid(column=8, row=5)
txt1.grid(row=4, column=6, sticky="nsew")

# Connect to Arduino on startup
connect_arduino()

window.mainloop()