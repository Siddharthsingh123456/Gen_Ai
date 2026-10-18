filename = input("Enter filename: ")

try:
    file = open(filename, "r")
except FileNotFoundError:
    print("File not found.")
except PermissionError:
    print("Permission denied.")
else:
    lines = file.readlines()
    for line in lines[:3]:
        print(line.strip())
    file.close()
finally:
    print("File operation attempted.")
