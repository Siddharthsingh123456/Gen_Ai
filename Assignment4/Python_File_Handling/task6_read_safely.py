# Task 6: Read File Safely

import os

filename = input("Enter file name: ")

if os.path.exists(filename):
    file = open(filename, "r")
    print(file.read())
    file.close()
else:
    print("File not found. Please check the filename.")
