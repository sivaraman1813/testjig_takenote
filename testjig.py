# ## *********************************************************************************************
# ## * File Name         : testjig.py (Linux version)
# ## * Python            : V3.12
# ## * Modified for      : Linux (Ubuntu/Debian)
# ## * Modified @date    : 2024
# ## **********************************************************************************************

# import os
# import tkinter as tk
# from tkinter.filedialog import askopenfilename
# from tkinter import messagebox
# import time
# import pyfirmata
# import numpy as np
# import sys
# import Hex2TxtTakenote_ENG1_aug_2021
# from tkinter import ttk
# import tkinter.font as tkFont
# import datetime
# import glob
# import serial.tools.list_ports

# # ===== LINUX PATH CONFIGURATION =====
# BASE_DIR = "/home/ae/take_note/Testjig"
# INPUT_DIR = os.path.join(BASE_DIR, "Input_files")
# OUTPUT_DIR = os.path.join(BASE_DIR, "output_from_takenote")
# RESULT_DIR = os.path.join(BASE_DIR, "result")

# # Create directories if they don't exist
# os.makedirs(INPUT_DIR, exist_ok=True)
# os.makedirs(OUTPUT_DIR, exist_ok=True)
# os.makedirs(RESULT_DIR, exist_ok=True)

# print(f"✅ Directories configured:")
# print(f"   Input: {INPUT_DIR}")
# print(f"   Output: {OUTPUT_DIR}")
# print(f"   Result: {RESULT_DIR}")

# # ===== GLOBAL VARIABLES =====
# board = None
# time_hour = 0
# time_minute = 0
# time_second = 0
# a = 0

# def find_arduino_port():
#     """Detect Arduino or USB-serial device."""
#     ports = serial.tools.list_ports.comports()

#     for port in ports:
#         desc = port.description.lower()
#         if ("arduino" in desc or 
#             "ch340" in desc or 
#             "usb" in desc or 
#             "ttyacm" in port.device.lower() or 
#             "ttyusb" in port.device.lower()):
#             return port.device

#     return None


# def connect_arduino():
#     """Try to connect using pyfirmata."""
#     global board
    
#     try:
#         import pyfirmata
#     except ImportError:
#         print("⚠️ pyfirmata not installed")
#         return None

#     arduino_port = find_arduino_port()

#     if not arduino_port:
#         print("⚠️ No Arduino detected")
#         return None

#     print(f"🔍 Trying to connect on: {arduino_port}")

#     try:
#         board = pyfirmata.Arduino(arduino_port)
#         print(f"✅ Connected to Arduino on {arduino_port}")
#         return board
#     except Exception as e:
#         print(f"❌ Failed to connect: {e}")
#         return None


# def result():
#     """Compare input and output files and produce result"""
#     global time_hour, time_minute, time_second, a
    
#     inp = nameEntered1.get()
#     b = a
#     i = 0
#     j = 0
    
#     print("###########################################################################")
#     print("TakeNote Number is:", inp)
#     current_time = datetime.datetime.now()
    
#     print("Date : ", end="")
#     print(current_time.day, "/", current_time.month, "/", current_time.year)
#     print("Time: ", end="")
#     print(current_time.hour, ":", current_time.minute, ":", current_time.second)
#     print("Time Taken by Testjig process is: %d hours:%d minutes:%d seconds" % (time_hour, time_minute, time_second))

#     count_to = 0
#     count_from = 0
    
#     for path in os.listdir(INPUT_DIR):
#         if os.path.isfile(os.path.join(INPUT_DIR, path)):
#             count_to += 1
#     print("Number of files given to testJig:", count_to - 1)
    
#     for path in os.listdir(OUTPUT_DIR):
#         if os.path.isfile(os.path.join(OUTPUT_DIR, path)):
#             count_from += 1
#     print("Number of files from takenote:", int((count_from / 2)), '\n')
    
#     c = b
#     d = int((count_from / 2))
#     count_from_testJig = b + d
    
#     for b in range(c, count_from_testJig):
#         i = i + 1
#         file1 = open(os.path.join(INPUT_DIR, f"{i}.txt"), 'r')
#         file2 = open(os.path.join(OUTPUT_DIR, f"{b}_op.txt"), 'r')
   
#         data1 = file1.read()
#         print('Number of characters used in file1:', len(data1))
#         data2 = file2.read()
#         print('Number of characters used in file2:', len(data2))
#         error = len(data1) - len(data2)
#         print("The missing characters are:", error)
#         score = (len(data2) / len(data1)) * 100
#         print("score in percentage: ", score, "%")
#         if error == 0:
#             print('-------PASS------\n')
#         else:
#             print('*******FAIL******\n')
        
#         file1.close()
#         file2.close()
    
#     print("Result will be stored as text file also")
    
#     original_stdout = sys.stdout
    
#     # Write to result file
#     with open(os.path.join(RESULT_DIR, 'TestJig_final_result.txt'), 'w') as f:
#         sys.stdout = f
#         print("###########################################################################")
#         print("TakeNote Number is:", inp)
#         current_time = datetime.datetime.now()
#         print("Date : ", end="")
#         print(current_time.day, "/", current_time.month, "/", current_time.year)
#         print("Time: ", end="")
#         print(current_time.hour, ":", current_time.minute, ":", current_time.second)
#         print("Time Taken by Testjig process is: %d hours:%d minutes:%d seconds" % (time_hour, time_minute, time_second))
        
#         count_to = 0
#         count_from = 0
        
#         for path in os.listdir(INPUT_DIR):
#             if os.path.isfile(os.path.join(INPUT_DIR, path)):
#                 count_to += 1
#         print("Number of files given to testJig:", count_to - 1)
        
#         for path in os.listdir(OUTPUT_DIR):
#             if os.path.isfile(os.path.join(OUTPUT_DIR, path)):
#                 count_from += 1
#         print("Number of files from takenote:", int((count_from / 2)), '\n')
        
#         e = b
        
#         for e in range(c, count_from_testJig):
#             j = j + 1
#             file1 = open(os.path.join(INPUT_DIR, f"{j}.txt"), 'r')
#             file2 = open(os.path.join(OUTPUT_DIR, f"{e}_op.txt"), 'r')
        
#             data1 = file1.read()
#             print('Number of characters used in file1:', len(data1))
#             data2 = file2.read()
#             print('Number of characters used in file2:', len(data2))
#             error = len(data1) - len(data2)
#             print("The missing characters are:", error)
#             score = (len(data2) / len(data1)) * 100
#             print("score in percentage: ", score, "%")
#             if error == 0:
#                 print('-------PASS------\n')
#             else:
#                 print('*******FAIL******\n')
            
#             file1.close()
#             file2.close()
        
#         sys.stdout = original_stdout


# def test_individual():
#     """Test individual file"""
#     global board
    
#     if board is None:
#         messagebox.showwarning("Board Error", "Arduino not connected. Please connect Arduino first.")
#         return
    
#     file_open()
#     time.sleep(5)
#     x = txt1.get("1.0", tk.END)
#     count = 0
#     num_flog = 0
    
#     while (count < (len(x) - 1)):
#         rec = x[count]
#         print(rec)
#         if(rec >= 'a' and rec <= 'z'):   
#             if(num_flog == 1):
#                 num_al()
#             num_flog = 0
#             outled = alplow_brl(rec)
#         elif(rec >= 'A' and rec <= 'Z'):
#             if(num_flog == 1):
#                 num_al()
#             num_flog = 0
#             capital()
#             outled = alpup_brl(rec)
#         elif(rec >= '0' and rec <= '9'):
#             if (num_flog == 0):
#                 al_num()
#             num_flog = 1
#             outled = num_brl(rec)
#         else:
#             outled = alplow_brl(rec)
#         dot_led(outled) 
#         count = count + 1
#     file_close()


# def alplow_brl(rec):
#     """Convert lowercase alphabet to braille"""
#     alp_lower_brl = {
#         "a": np.array([0,0,1,0,0,0,0,0,0], dtype=bool),
#         "b": np.array([0,1,1,0,0,0,0,0,0], dtype=bool),
#         "c": np.array([0,0,1,1,0,0,0,0,0], dtype=bool),
#         "d": np.array([0,0,1,1,1,0,0,0,0], dtype=bool),
#         "e": np.array([0,0,1,0,1,0,0,0,0], dtype=bool),
#         "f": np.array([0,1,1,1,0,0,0,0,0], dtype=bool),
#         "g": np.array([0,1,1,1,1,0,0,0,0], dtype=bool),
#         "h": np.array([0,1,1,0,1,0,0,0,0], dtype=bool),
#         "i": np.array([0,1,0,1,0,0,0,0,0], dtype=bool),
#         "j": np.array([0,1,0,1,1,0,0,0,0], dtype=bool),
#         "k": np.array([1,0,1,0,0,0,0,0,0], dtype=bool),
#         "l": np.array([1,1,1,0,0,0,0,0,0], dtype=bool),
#         "m": np.array([1,0,1,1,0,0,0,0,0], dtype=bool),
#         "n": np.array([1,0,1,1,1,0,0,0,0], dtype=bool),
#         "o": np.array([1,0,1,0,1,0,0,0,0], dtype=bool),
#         "p": np.array([1,1,1,1,0,0,0,0,0], dtype=bool),
#         "q": np.array([1,1,1,1,1,0,0,0,0], dtype=bool),
#         "r": np.array([1,1,1,0,1,0,0,0,0], dtype=bool),
#         "s": np.array([1,1,0,1,0,0,0,0,0], dtype=bool),
#         "t": np.array([1,1,0,1,1,0,0,0,0], dtype=bool),
#         "u": np.array([1,0,1,0,0,1,0,0,0], dtype=bool),
#         "v": np.array([1,1,1,0,0,1,0,0,0], dtype=bool),
#         "w": np.array([0,1,0,1,1,1,0,0,0], dtype=bool),
#         "x": np.array([1,0,1,1,0,1,0,0,0], dtype=bool),
#         "y": np.array([1,0,1,1,1,1,0,0,0], dtype=bool),
#         "z": np.array([1,0,1,0,1,1,0,0,0], dtype=bool),
#         "*": np.array([1,0,0,0,1,0,0,0,0], dtype=bool),
#         "@": np.array([1,0,0,1,1,0,0,0,0], dtype=bool),
#         ":": np.array([0,1,0,0,1,0,0,0,0], dtype=bool),
#         ",": np.array([0,1,0,0,0,0,0,0,0], dtype=bool),
#         "!": np.array([1,1,0,0,1,0,0,0,0], dtype=bool),
#         ".": np.array([0,1,0,0,1,1,0,0,0], dtype=bool),
#         "?": np.array([1,1,0,0,0,1,0,0,0], dtype=bool),
#         ";": np.array([1,1,0,0,0,0,0,0,0], dtype=bool),
#         "/": np.array([1,0,0,1,0,0,0,0,0], dtype=bool),
#         "non": np.array([0,0,0,0,0,0,0,0,0], dtype=bool),
#         " ": np.array([0,0,0,0,0,0,0,1,0], dtype=bool),
#         "\n": np.array([0,0,0,0,0,0,0,0,1], dtype=bool),
#         '"': np.array([1,0,0,0,1,1,0,0,0], dtype=bool),
#         "'": np.array([1,0,0,0,0,0,0,0,0], dtype=bool),
#         "(": np.array([1,1,1,0,1,1,0,0,0], dtype=bool),
#         ")": np.array([1,1,0,1,1,1,0,0,0], dtype=bool),
#         "&": np.array([1,1,1,1,0,1,0,0,0], dtype=bool),
#         "%": np.array([0,0,1,1,0,1,0,0,0], dtype=bool),
#         "+": np.array([1,0,0,1,0,1,0,0,0], dtype=bool),
#         "-": np.array([1,0,0,0,0,1,0,0,0], dtype=bool),
#     }
#     xx = alp_lower_brl.get(rec, alp_lower_brl["non"])
#     return xx


# def alpup_brl(rec):
#     """Convert uppercase alphabet to braille"""
#     alp_upper_brl = {
#         "A": np.array([0,0,1,0,0,0,0,0,0], dtype=bool),
#         "B": np.array([0,1,1,0,0,0,0,0,0], dtype=bool),
#         "C": np.array([0,0,1,1,0,0,0,0,0], dtype=bool),
#         "D": np.array([0,0,1,1,1,0,0,0,0], dtype=bool),
#         "E": np.array([0,0,1,0,1,0,0,0,0], dtype=bool),
#         "F": np.array([0,1,1,1,0,0,0,0,0], dtype=bool),
#         "G": np.array([0,1,1,1,1,0,0,0,0], dtype=bool),
#         "H": np.array([0,1,1,0,1,0,0,0,0], dtype=bool),
#         "I": np.array([0,1,0,1,0,0,0,0,0], dtype=bool),
#         "J": np.array([0,1,0,1,1,0,0,0,0], dtype=bool),
#         "K": np.array([1,0,1,0,0,0,0,0,0], dtype=bool),
#         "L": np.array([1,1,1,0,0,0,0,0,0], dtype=bool),
#         "M": np.array([1,0,1,1,0,0,0,0,0], dtype=bool),
#         "N": np.array([1,0,1,1,1,0,0,0,0], dtype=bool),
#         "O": np.array([1,0,1,0,1,0,0,0,0], dtype=bool),
#         "P": np.array([1,1,1,1,0,0,0,0,0], dtype=bool),
#         "Q": np.array([1,1,1,1,1,0,0,0,0], dtype=bool),
#         "R": np.array([1,1,1,0,1,0,0,0,0], dtype=bool),
#         "S": np.array([1,1,0,1,0,0,0,0,0], dtype=bool),
#         "T": np.array([1,1,0,1,1,0,0,0,0], dtype=bool),
#         "U": np.array([1,0,1,0,0,1,0,0,0], dtype=bool),
#         "V": np.array([1,1,1,0,0,1,0,0,0], dtype=bool),
#         "W": np.array([0,1,0,1,1,1,0,0,0], dtype=bool),
#         "X": np.array([1,0,1,1,0,1,0,0,0], dtype=bool),
#         "Y": np.array([1,0,1,1,1,1,0,0,0], dtype=bool),
#         "Z": np.array([1,0,1,0,1,1,0,0,0], dtype=bool),
#     }
#     xx = alp_upper_brl[rec]
#     return xx


# def num_brl(rec):
#     """Convert number to braille"""
#     number_brl = {
#         "1": np.array([0,0,1,0,0,0,0,0,0], dtype=bool),
#         "2": np.array([0,1,1,0,0,0,0,0,0], dtype=bool),
#         "3": np.array([0,0,1,1,0,0,0,0,0], dtype=bool),
#         "4": np.array([0,0,1,1,1,0,0,0,0], dtype=bool),
#         "5": np.array([0,0,1,0,1,0,0,0,0], dtype=bool),
#         "6": np.array([0,1,1,1,0,0,0,0,0], dtype=bool),
#         "7": np.array([0,1,1,1,1,0,0,0,0], dtype=bool),
#         "8": np.array([0,1,1,0,1,0,0,0,0], dtype=bool),
#         "9": np.array([0,1,0,1,0,0,0,0,0], dtype=bool),
#         "0": np.array([0,1,0,1,1,0,0,0,0], dtype=bool),
#     }
#     xx = number_brl[rec]
#     return xx


# def file_open():
#     """Open file signal to Arduino"""
#     global board
#     if board is None:
#         print("⚠️ Board not connected")
#         return
        
#     board.digital[5].write(0)
#     board.digital[6].write(0)
#     board.digital[7].write(0)
#     board.digital[8].write(0)
#     board.digital[9].write(0)
#     board.digital[10].write(0)
#     board.digital[2].write(1)
#     board.digital[3].write(0)
#     board.digital[4].write(1)
#     time.sleep(0.5)
#     board.digital[5].write(0)
#     board.digital[6].write(0)
#     board.digital[7].write(0)
#     board.digital[8].write(0)
#     board.digital[9].write(0)
#     board.digital[10].write(0)
#     board.digital[2].write(0)
#     board.digital[3].write(0)
#     board.digital[4].write(0)
#     time.sleep(0.5)


# def file_close():
#     """Close file signal to Arduino"""
#     global board
#     if board is None:
#         print("⚠️ Board not connected")
#         return
        
#     board.digital[5].write(0)
#     board.digital[6].write(0)
#     board.digital[7].write(0)
#     board.digital[8].write(0)
#     board.digital[9].write(0)
#     board.digital[10].write(0)
#     board.digital[2].write(1)
#     board.digital[3].write(1)
#     board.digital[4].write(0)
#     time.sleep(0.5)
#     board.digital[5].write(0)
#     board.digital[6].write(0)
#     board.digital[7].write(0)
#     board.digital[8].write(0)
#     board.digital[9].write(0)
#     board.digital[10].write(0)
#     board.digital[2].write(0)
#     board.digital[3].write(0)
#     board.digital[4].write(0)
#     time.sleep(0.5)


# def dot_led(outled):
#     """Send dot pattern to Arduino"""
#     global board
#     if board is None:
#         print("⚠️ Board not connected")
#         return
        
#     board.digital[5].write(outled[0])
#     board.digital[6].write(outled[1])
#     board.digital[7].write(outled[2])
#     board.digital[8].write(outled[3])
#     board.digital[9].write(outled[4])
#     board.digital[10].write(outled[5])
#     board.digital[2].write(outled[6])
#     board.digital[3].write(outled[7])
#     board.digital[4].write(outled[8])
    
#     time.sleep(0.5)
#     board.digital[5].write(0)
#     board.digital[6].write(0)
#     board.digital[7].write(0)
#     board.digital[8].write(0)
#     board.digital[9].write(0)
#     board.digital[10].write(0)
#     board.digital[2].write(0)
#     board.digital[3].write(0)
#     board.digital[4].write(0)
#     time.sleep(0.5)


# def al_num():
#     """Alphabet to number signal"""
#     global board
#     if board is None:
#         return
        
#     board.digital[5].write(1)
#     board.digital[6].write(0)
#     board.digital[7].write(0)
#     board.digital[8].write(1)
#     board.digital[9].write(1)
#     board.digital[10].write(1)
#     time.sleep(0.5)
#     board.digital[5].write(0)
#     board.digital[6].write(0)
#     board.digital[7].write(0)
#     board.digital[8].write(0)
#     board.digital[9].write(0)
#     board.digital[10].write(0)
#     time.sleep(0.5)


# def num_al():
#     """Number to alphabet signal"""
#     global board
#     if board is None:
#         return
        
#     board.digital[5].write(0)
#     board.digital[6].write(0)
#     board.digital[7].write(0)
#     board.digital[8].write(0)
#     board.digital[9].write(1)
#     board.digital[10].write(1)
#     time.sleep(0.5)
#     board.digital[5].write(0)
#     board.digital[6].write(0)
#     board.digital[7].write(0)
#     board.digital[8].write(0)
#     board.digital[9].write(0)
#     board.digital[10].write(0)
#     time.sleep(0.5)


# def capital():
#     """Capital letter signal"""
#     global board
#     if board is None:
#         return
        
#     board.digital[5].write(0)
#     board.digital[6].write(0)
#     board.digital[7].write(0)
#     board.digital[8].write(0)
#     board.digital[9].write(0)
#     board.digital[10].write(1)
#     time.sleep(0.5)
#     board.digital[5].write(0)
#     board.digital[6].write(0)
#     board.digital[7].write(0)
#     board.digital[8].write(0)
#     board.digital[9].write(0)
#     board.digital[10].write(0)
#     time.sleep(0.5)


# def get():
#     """Load a file for testing"""
#     filepath = askopenfilename(
#         initialdir=INPUT_DIR,
#         filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
#     )
    
#     if not filepath:
#         return
    
#     try:
#         with open(filepath, 'r', encoding='utf-8') as file:
#             text = file.read()
#             txt1.delete("1.0", tk.END)
#             txt1.insert(tk.END, text)
#             print(f"✅ Loaded file: {os.path.basename(filepath)}")
#     except Exception as e:
#         print(f"❌ Error loading file: {e}")
#         messagebox.showerror("File Error", f"Could not load file: {e}")


# def test_files_all():
#     """Test all files automatically"""
#     global time_hour, time_minute, time_second
    
#     start = time.time()
#     count_to = 0
#     j = 0
    
#     for path in os.listdir(INPUT_DIR):
#         if os.path.isfile(os.path.join(INPUT_DIR, path)):
#             count_to += 1
    
#     print("Number of files given to testJig:", count_to - 1)
#     print("\n")
    
#     for count in range(1, count_to):
#         j += 1
#         file_path = os.path.join(INPUT_DIR, f"{j}.txt")
        
#         if not os.path.exists(file_path):
#             print(f"⚠️ File not found: {file_path}")
#             continue
            
#         with open(file_path, 'r', encoding='utf-8') as file1:
#             print(file1.read())
        
#         txt1.delete("1.0", tk.END)
        
#         with open(file_path, 'r', encoding='utf-8') as input_file:
#             text = input_file.read()
#             txt1.insert(tk.END, text)
#             test_individual()
#             time.sleep(7)
    
#     end = time.time()
#     difference = end - start
#     hour = difference // 3600
#     difference %= 3600
#     minute = difference // 60
#     difference %= 60
#     second = difference
#     print("Time Taken by Testjig process is: %d hours:%d minutes:%d seconds" % (hour, minute, second))
#     time_hour = hour
#     time_minute = minute
#     time_second = second


# def transfer_files():
#     """Transfer files - Bluetooth not implemented for Linux"""
#     messagebox.showinfo("Transfer Files", "Bluetooth transfer not implemented in this Linux version.\nPlease manually place output files in the output directory.")


# def transfer_files_short():
#     """Transfer files short - Bluetooth not implemented for Linux"""
#     messagebox.showinfo("Transfer Files", "Bluetooth transfer not implemented in this Linux version.")


# # ===== GUI SETUP =====
# window = tk.Tk()
# window.title("TestJig Program (pass/fail) - Linux Version")
# window.minsize(600, 400)

# label1 = ttk.Label(window, text="TakeNote Number")
# name1 = tk.StringVar()
# nameEntered1 = ttk.Entry(window, width=20, textvariable=name1)

# txt1 = tk.Text(window, height=35, width=80, bd=2)

# button1 = tk.Button(window, text="RESULT", width=25, height=5, command=result)
# button2 = tk.Button(window, text="GET", width=20, height=2, command=get)
# button3 = tk.Button(window, text="TEST INDIVIDUAL", width=20, height=2, command=test_individual)
# button4 = tk.Button(window, text="TEST", width=25, height=3, command=test_files_all)
# button5 = tk.Button(window, text="TRANSFER", width=20, height=2, command=transfer_files)

# label1.grid(column=1, row=0)
# nameEntered1.grid(column=0, row=0)
# button1.grid(column=1, row=5)
# button2.grid(column=8, row=3)
# button3.grid(column=8, row=4)
# button4.grid(column=1, row=4)
# button5.grid(column=8, row=5)
# txt1.grid(row=4, column=6, sticky="nsew")

# # Connect to Arduino on startup
# connect_arduino()

# window.mainloop()## *********************************************************************************************
## * File Name         : testjig.py (Linux version)
## * Python            : V3.12
## * Modified for      : Linux (Ubuntu/Debian)
## * Modified @date    : 2024
## * Added             : Tamil Braille (Bharati Standard) support
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
import unicodedata

# ===== LINUX PATH CONFIGURATION =====
BASE_DIR = "/home/ae/take_note/Testjig"
INPUT_DIR = os.path.join(BASE_DIR, "Input_files")
OUTPUT_DIR = os.path.join(BASE_DIR, "output_from_takenote")
RESULT_DIR = os.path.join(BASE_DIR, "result")

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


# ===== TAMIL BRAILLE (BHARATI STANDARD) =====
# Dot numbering: [dot1, dot2, dot3, dot4, dot5, dot6, dot7, dot8, dot9]
# Bharati Braille uses 6 dots (dots 1-6); dots 7-9 used for control/space/newline
# Reference: Bharati Braille standard for Tamil (UNESCO / NCERT)

# ---- Tamil Vowels (உயிர் எழுத்து) ----
TAMIL_VOWELS_BRL = {
    'அ': np.array([1,0,0,0,0,0,0,0,0], dtype=bool),  # dot 1
    'ஆ': np.array([1,0,0,1,0,0,0,0,0], dtype=bool),  # dots 1,4
    'இ': np.array([0,1,0,0,0,0,0,0,0], dtype=bool),  # dot 2
    'ஈ': np.array([0,1,0,1,0,0,0,0,0], dtype=bool),  # dots 2,4
    'உ': np.array([1,1,0,0,0,0,0,0,0], dtype=bool),  # dots 1,2
    'ஊ': np.array([1,1,0,1,0,0,0,0,0], dtype=bool),  # dots 1,2,4
    'எ': np.array([1,0,0,0,1,0,0,0,0], dtype=bool),  # dots 1,5
    'ஏ': np.array([1,0,0,1,1,0,0,0,0], dtype=bool),  # dots 1,4,5
    'ஐ': np.array([0,1,0,0,1,0,0,0,0], dtype=bool),  # dots 2,5
    'ஒ': np.array([1,1,0,0,1,0,0,0,0], dtype=bool),  # dots 1,2,5
    'ஓ': np.array([1,1,0,1,1,0,0,0,0], dtype=bool),  # dots 1,2,4,5
    'ஔ': np.array([0,1,0,1,1,0,0,0,0], dtype=bool),  # dots 2,4,5
}

# ---- Tamil Consonants (மெய் எழுத்து) ----
TAMIL_CONSONANTS_BRL = {
    'க': np.array([1,0,1,0,0,0,0,0,0], dtype=bool),  # dots 1,3
    'ங': np.array([0,1,1,0,1,0,0,0,0], dtype=bool),  # dots 2,3,5
    'ச': np.array([0,0,1,1,0,0,0,0,0], dtype=bool),  # dots 3,4
    'ஞ': np.array([1,0,1,0,1,0,0,0,0], dtype=bool),  # dots 1,3,5
    'ட': np.array([0,0,1,0,0,1,0,0,0], dtype=bool),  # dots 3,6
    'ண': np.array([1,0,1,0,0,1,0,0,0], dtype=bool),  # dots 1,3,6
    'த': np.array([1,1,0,1,0,0,0,0,0], dtype=bool),  # dots 1,2,4
    'ந': np.array([0,1,0,1,0,1,0,0,0], dtype=bool),  # dots 2,4,6
    'ப': np.array([1,1,0,0,0,0,0,0,0], dtype=bool),  # dots 1,2
    'ம': np.array([1,0,1,1,0,0,0,0,0], dtype=bool),  # dots 1,3,4
    'ய': np.array([0,1,0,1,1,0,0,0,0], dtype=bool),  # dots 2,4,5
    'ர': np.array([1,1,1,0,0,0,0,0,0], dtype=bool),  # dots 1,2,3
    'ல': np.array([1,0,0,0,0,1,0,0,0], dtype=bool),  # dots 1,6
    'வ': np.array([0,1,1,1,0,0,0,0,0], dtype=bool),  # dots 2,3,4
    'ழ': np.array([0,1,1,0,0,1,0,0,0], dtype=bool),  # dots 2,3,6
    'ள': np.array([1,0,0,1,0,1,0,0,0], dtype=bool),  # dots 1,4,6
    'ற': np.array([0,0,1,1,0,1,0,0,0], dtype=bool),  # dots 3,4,6
    'ன': np.array([0,1,0,0,0,1,0,0,0], dtype=bool),  # dots 2,6
}

# ---- Vowel signs / matras (உயிர்மெய் suffix patterns) ----
# In Bharati Braille, compound characters = consonant cell + vowel sign cell
TAMIL_VOWEL_SIGNS_BRL = {
    '\u0bbe': np.array([1,0,0,1,0,0,0,0,0], dtype=bool),  # ா  (aa matra)
    '\u0bbf': np.array([0,1,0,0,0,0,0,0,0], dtype=bool),  # ி  (i matra)
    '\u0bc0': np.array([0,1,0,1,0,0,0,0,0], dtype=bool),  # ீ  (ii matra)
    '\u0bc1': np.array([1,1,0,0,0,0,0,0,0], dtype=bool),  # ு  (u matra)
    '\u0bc2': np.array([1,1,0,1,0,0,0,0,0], dtype=bool),  # ூ  (uu matra)
    '\u0bc6': np.array([1,0,0,0,1,0,0,0,0], dtype=bool),  # ெ  (e matra)
    '\u0bc7': np.array([1,0,0,1,1,0,0,0,0], dtype=bool),  # ே  (ee matra)
    '\u0bc8': np.array([0,1,0,0,1,0,0,0,0], dtype=bool),  # ை  (ai matra)
    '\u0bca': np.array([1,1,0,0,1,0,0,0,0], dtype=bool),  # ொ  (o matra)
    '\u0bcb': np.array([1,1,0,1,1,0,0,0,0], dtype=bool),  # ோ  (oo matra)
    '\u0bcc': np.array([0,1,0,1,1,0,0,0,0], dtype=bool),  # ௌ  (au matra)
    '\u0bcd': np.array([0,0,0,0,0,0,0,0,0], dtype=bool),  # ்  (pulli / virama - silence, no dots)
}

# ---- Tamil Numbers (தமிழ் இலக்கங்கள்) ----
TAMIL_NUMBERS_BRL = {
    '௧': np.array([0,0,1,0,0,0,0,0,0], dtype=bool),  # 1
    '௨': np.array([0,1,1,0,0,0,0,0,0], dtype=bool),  # 2
    '௩': np.array([0,0,1,1,0,0,0,0,0], dtype=bool),  # 3
    '௪': np.array([0,0,1,1,1,0,0,0,0], dtype=bool),  # 4
    '௫': np.array([0,0,1,0,1,0,0,0,0], dtype=bool),  # 5
    '௬': np.array([0,1,1,1,0,0,0,0,0], dtype=bool),  # 6
    '௭': np.array([0,1,1,1,1,0,0,0,0], dtype=bool),  # 7
    '௮': np.array([0,1,1,0,1,0,0,0,0], dtype=bool),  # 8
    '௯': np.array([0,1,0,1,0,0,0,0,0], dtype=bool),  # 9
    '௦': np.array([0,1,0,1,1,0,0,0,0], dtype=bool),  # 0
}

# ---- Tamil special punctuation ----
TAMIL_PUNCT_BRL = {
    '।': np.array([0,1,0,0,1,1,0,0,0], dtype=bool),  # danda (full stop)
    '॥': np.array([0,1,0,0,1,1,0,0,0], dtype=bool),  # double danda
}

# ---- Bharati Tamil indicator cell (signals Tamil mode) ----
TAMIL_MODE_INDICATOR = np.array([0,0,0,0,1,1,0,0,0], dtype=bool)  # dots 5,6


def tamil_brl(char):
    """
    Return the Bharati Braille dot pattern for a Tamil character.
    Handles vowels, consonants, vowel-signs (matras), and Tamil numerals.
    Returns None if unmapped.
    """
    if char in TAMIL_VOWELS_BRL:
        return TAMIL_VOWELS_BRL[char]
    if char in TAMIL_CONSONANTS_BRL:
        return TAMIL_CONSONANTS_BRL[char]
    if char in TAMIL_VOWEL_SIGNS_BRL:
        return TAMIL_VOWEL_SIGNS_BRL[char]
    if char in TAMIL_NUMBERS_BRL:
        return TAMIL_NUMBERS_BRL[char]
    if char in TAMIL_PUNCT_BRL:
        return TAMIL_PUNCT_BRL[char]
    return None


def is_tamil_char(char):
    """Return True if the character is in the Tamil Unicode block (U+0B80–U+0BFF)."""
    cp = ord(char)
    return 0x0B80 <= cp <= 0x0BFF


def tokenize_tamil(text):
    """
    Tokenize a Tamil string into logical units for Braille output.
    Each token is either:
      - A standalone vowel
      - A consonant optionally followed by a vowel-sign or virama (pulli)
      - A non-Tamil character (passed through as-is)
    """
    tokens = []
    i = 0
    while i < len(text):
        ch = text[i]
        if is_tamil_char(ch):
            # Check if it's a consonant followed by a vowel sign or virama
            if ch in TAMIL_CONSONANTS_BRL and i + 1 < len(text):
                next_ch = text[i + 1]
                if next_ch in TAMIL_VOWEL_SIGNS_BRL:
                    tokens.append((ch, next_ch))  # consonant + matra pair
                    i += 2
                    continue
            tokens.append((ch,))
        else:
            tokens.append((ch,))
        i += 1
    return tokens


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
        file1 = open(os.path.join(INPUT_DIR, f"{i}.txt"), 'r', encoding='utf-8')
        file2 = open(os.path.join(OUTPUT_DIR, f"{b}_op.txt"), 'r', encoding='utf-8')

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

    with open(os.path.join(RESULT_DIR, 'TestJig_final_result.txt'), 'w', encoding='utf-8') as f:
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
            file1 = open(os.path.join(INPUT_DIR, f"{j}.txt"), 'r', encoding='utf-8')
            file2 = open(os.path.join(OUTPUT_DIR, f"{e}_op.txt"), 'r', encoding='utf-8')

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
    """Test individual file — handles both English and Tamil text"""
    global board

    if board is None:
        messagebox.showwarning("Board Error", "Arduino not connected. Please connect Arduino first.")
        return

    file_open()
    time.sleep(5)
    x = txt1.get("1.0", tk.END)

    # Detect if the text contains Tamil characters
    has_tamil = any(is_tamil_char(ch) for ch in x)

    if has_tamil:
        print("🔤 Tamil text detected — using Tamil Braille (Bharati standard)")
        test_tamil_text(x)
    else:
        print("🔤 English text detected — using English Braille")
        test_english_text(x)

    file_close()


def test_english_text(x):
    """Send English text to Arduino as Braille dots"""
    count = 0
    num_flog = 0

    while count < (len(x) - 1):
        rec = x[count]
        print(rec)
        if rec >= 'a' and rec <= 'z':
            if num_flog == 1:
                num_al()
            num_flog = 0
            outled = alplow_brl(rec)
        elif rec >= 'A' and rec <= 'Z':
            if num_flog == 1:
                num_al()
            num_flog = 0
            capital()
            outled = alpup_brl(rec)
        elif rec >= '0' and rec <= '9':
            if num_flog == 0:
                al_num()
            num_flog = 1
            outled = num_brl(rec)
        else:
            outled = alplow_brl(rec)
        dot_led(outled)
        count += 1


def test_tamil_text(x):
    """
    Send Tamil text to Arduino as Bharati Braille dots.
    Tokenizes the text into logical Tamil units and sends each cell.
    Mixed Tamil+English passages are handled character-by-character.
    """
    # Send Tamil mode indicator once at the start
    dot_led(TAMIL_MODE_INDICATOR)

    tokens = tokenize_tamil(x)

    for token in tokens:
        if len(token) == 1:
            ch = token[0]

            # Handle whitespace and newlines via English braille map
            if ch == ' ':
                dot_led(alplow_brl(' '))
                continue
            if ch == '\n':
                dot_led(alplow_brl('\n'))
                continue

            # Tamil character
            if is_tamil_char(ch):
                pattern = tamil_brl(ch)
                if pattern is not None:
                    print(f"  Tamil char: {ch}  → dots: {np.where(pattern[:6])[0]+1}")
                    dot_led(pattern)
                else:
                    print(f"  ⚠️ No Braille mapping for Tamil char: {ch} (U+{ord(ch):04X}) — skipping")
            else:
                # Non-Tamil, non-whitespace — use English braille
                pattern = alplow_brl(ch)
                dot_led(pattern)

        elif len(token) == 2:
            # Consonant + vowel-sign pair
            consonant, matra = token
            print(f"  Tamil compound: {consonant}{matra}")

            con_pattern = tamil_brl(consonant)
            mat_pattern = tamil_brl(matra)

            if con_pattern is not None:
                dot_led(con_pattern)
            else:
                print(f"  ⚠️ No mapping for consonant: {consonant} — skipping")

            if mat_pattern is not None and not np.all(mat_pattern == 0):
                # Only send matra cell if it has dots (virama has no dots)
                dot_led(mat_pattern)


def alplow_brl(rec):
    """Convert lowercase alphabet / punctuation to braille"""
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
            # Show Tamil/English detection
            has_tamil = any(is_tamil_char(ch) for ch in text)
            print(f"   Script detected: {'Tamil 🔤' if has_tamil else 'English'}")
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
window.title("TestJig Program (pass/fail) - Linux Version [Tamil + English]")
window.minsize(600, 400)

label1 = ttk.Label(window, text="TakeNote Number")
name1 = tk.StringVar()
nameEntered1 = ttk.Entry(window, width=20, textvariable=name1)

txt1 = tk.Text(window, height=35, width=80, bd=2)

button1 = tk.Button(window, text="RESULT",          width=25, height=5, command=result)
button2 = tk.Button(window, text="GET",             width=20, height=2, command=get)
button3 = tk.Button(window, text="TEST INDIVIDUAL", width=20, height=2, command=test_individual)
button4 = tk.Button(window, text="TEST",            width=25, height=3, command=test_files_all)
button5 = tk.Button(window, text="TRANSFER",        width=20, height=2, command=transfer_files)

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