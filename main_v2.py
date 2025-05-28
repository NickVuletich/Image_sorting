# Programmer: Nicholas Vuletich
# File name: main_v1.py

""" 
Image Sorter v2
Sorts images in a folder based on size, name, or date.
It also sorts on ascending or descending order.
The program will also tell the user if the image 
is blurry based on the Laplacian Variance if the user would like.
"""

import os
import datetime
import cv2

#----------------------FOLDER PATH----------------------#

# You can ask user for folder Path or just have one set

#folder_path = input("Enter the folder path:" )
folder_path = "sort_img"


#-----------------------FUNCTIONS-----------------------#

# prints out the order prompts
def print_order():
    print("Sort in ascending (asc) or descending (desc) order? ")
    print("  Name: A → Z")
    print("  Size: Small → Large")
    print("  Date: Old → New")

    print("  Name: Z → A")
    print("  Size: Large → Small")
    print("  Date: New → Old")
    
# Detects blur using Laplacian
# then returns a list of dictionaries with the variance and blur value for each image
def blur(files, folder, threshold=100.0):
    
    variance_list = []
    blur_flags = []

    for file in files:
        path = os.path.join(folder, file['name'])
        photo = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if photo is not None:
            variance = cv2.Laplacian(photo, cv2.CV_64F).var()
            is_blurry = variance < threshold
            variance_list.append({
                'var' : variance,
                'blur' : is_blurry
            })
            blur_flags.append(is_blurry)
        else:
            print("ERROR! Image could not be loaded. Try again!")
    return variance_list, blur_flags

def file_info(folder_path):
    #makes array of image files
    image_files = []
    # checks to see if there are image files and will in turn write any image files to the list
    # it also stores name and size in mb
    for entry in os.scandir(folder_path):
        if entry.is_file() and entry.name.lower().endswith(('.jpg', '.png' , 'jpeg')):
            size_mb = entry.stat().st_size / (1024 * 1024)
            timestamp = entry.stat().st_mtime
            formatted_date = datetime.datetime.fromtimestamp(timestamp).strftime("%m/%d/%Y %H:%M:%S")
            image_files.append({
                "name": entry.name,
                "size": size_mb,
                "date": formatted_date,
                "timestamp" : timestamp
            })
    return image_files
    

# Prints the correct output for images that are blurry
def blur_print(files):
    variances, blur_flags = blur(files, folder_path)
    print()
    if choice in ("name", "size", "date"):
        print(f"Sorting by: {choice}")
    print()
    print((f"{'Name':<40} {'Sharpness':<10} {'Size (MB)':>12}    {'Date & Time'}"))
    print('-' * 114)
    for file, blur_data in zip(files, variances):
        if blur_data['blur']:
            print(f"{file['name']:<40} is blurry {file['size']:>9.2f} MB     {file['date']}    (Blur Variance: {blur_data['var']:>.2f})")
        else:
            print(f"{file['name']:<40} is Sharp {file['size']:>10.2f} MB     {file['date']}    (Blur Variance: {blur_data['var']:>.2f})")

# default output for printing the sorted list
def reg_print(files):
    print()
    if choice in ("name", "size", "date"):
        print(f"Sorting by: {choice}")
    print()
    print((f"{'Name':<40} {'Size (MB)':>13}    {'Time'}"))
    print('-' * 65)

    for img in files:
        print(f"{img['name']:<40}{img['size']:>10.2f} MB     {img['date']}")

def sort(image_files):
    # changes sort based on users choice of ascending (asc) or descending (desc)
    if sort_dec == "asc":
        name_sort = False
        size_sort = True
        date_sort = True
    elif sort_dec == "desc":
        name_sort = True
        size_sort = False
        date_sort = False
    else:
        print("Error:: Sort type not supported.")
        print("sorting by default sort: (asc)")
        name_sort = False
        size_sort = True
        date_sort = True

    # sorts the files based on users choice of 'name', 'size', or 'date'
    if choice == "name":
        image_files.sort(key=lambda x: x['name'], reverse=name_sort)
    elif choice == "size":
        image_files.sort(key=lambda x: x['size'], reverse=size_sort)
    elif choice == "date": 
        image_files.sort(key=lambda x: x['timestamp'], reverse=date_sort)
    else:
        print("Error:: Sort type not supported.")
        print("sorting by default sort: name")
        image_files.sort(key=lambda x: x['name'], reverse=name_sort)
    return image_files



#-------------------------START-------------------------#

if __name__ == "__main__":

    # prompts user to sort the file how they would like
    choice = input("What would you like to sort by: 'name', 'size', 'date': ").strip().lower()
    blur_choice = input("Do you want to know if the image is blurry or not: 'yes', 'no': ").strip().lower()

    print_order()
    sort_dec = input("").strip().lower()

    image_files = file_info(folder_path)
    image_files = sort(image_files)

    if blur_choice == "yes":
        blur_print(image_files)
    elif blur_choice == "no":
        reg_print(image_files)
    else:
        print("Error:: Choice type not supported.")
        print("Running regular print...") 
        reg_print(image_files)

