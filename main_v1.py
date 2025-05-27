# Programmer: Nicholas Vuletich
# File name: main_v1.py

""" 
Image Sorter v1
Sorts images in a folder based on size, name, or date.
It also sorts on ascending or descending order.
"""

import os
import datetime


# prompts user to sort the file how they would like
choice = input("What would you like to sort by: 'name', 'size', 'date': ").strip().lower()
print("Sort in ascending (asc) or descending (desc) order? ")
print("(asc)")
print("  Name: A → Z")
print("  Size: Small → Large")
print("  Date: Old → New")

print("(desc)")
print("  Name: Z → A")
print("  Size: Large → Small")
print("  Date: New → Old")
sort_dec = input("").strip().lower()

#folder_path = input("Enter the folder path:" )
folder_path = "sort_img"


#makes array of image files
image_files = []
# checks to see if there are image files and will in turn write any image files to the list
# it also stores name and size in mb
for entry in os.scandir(folder_path):
    if entry.is_file() and entry.name.endswith(('.jpg', '.png' , 'jpeg')):
        size_mb = entry.stat().st_size / (1024 * 1024)
        timestamp = entry.stat().st_mtime
        formatted_date = datetime.datetime.fromtimestamp(timestamp).strftime("%m/%d/%Y %H:%M:%S")
        image_files.append({
            "name": entry.name,
            "size": size_mb,
            "date": formatted_date
        })
# changes sort based on users choice of ascending (asc) or descending (desc)
if sort_dec == "asc":
    name_sort = False
    size_sort = True
    date_sort = True
elif sort_dec == "desc":
    name_sort = True
    size_sort = False
    date_sort = False

# sorts the files based on users choice of 'name', 'size', or 'date'
if choice == "name":
    image_files.sort(key=lambda x: x['name'], reverse=name_sort)
elif choice == "size":
    image_files.sort(key=lambda x: x['size'], reverse=size_sort)
elif choice == "date": 
    image_files.sort(key=lambda x: x['date'], reverse=date_sort)
else:
    print("Error:: Sort type not supported.")
    print("sorting by default sort: name")
    image_files.sort(key=lambda x: x['name'], reverse=name_sort)

print(f"Sorting by: {choice}")
print()
print((f"{'Name':<40} {'Size (MB)':>13}    {'Time'}"))
print('-' * 65)

for img in image_files:
    print(f"{img['name']:<40}{img['size']:>10.2f} MB     {img['date']}")
    #print(f"Image: {img['name']} | Size: {img['size']:.2f} MB | Date: {img['date']}")

