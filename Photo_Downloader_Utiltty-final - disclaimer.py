import csv
import requests
import shutil
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
import time
import sys

#decrement counter
def decrement_number():
    global counter
    #print(counter)
    counter -= 1
    label.config(text=counter, font=("Courier", 44))
    label.update()
    time.sleep(0.10)

def exit_program():
    window.destroy()
    sys.exit()

def run_program():
    window.destroy()


#Select Source CSV File
#Opens a file selection dialog.
window = tk.Tk()
window.geometry("500x500")

window.title("Disclaimer")
label3 = tk.Label(
    window,
    background="blue",
    width=150,
    height=20,
    font=("Courier", 12),
    fg="white",
    wraplength=500,
    text="\"Use at Your Own Risk Disclaimer\"\n\n"

"The Photo Download Utility is provided \"as is\", with no guarantee of completeness, accuracy, timeliness or of the results obtained from the use of this information, and without warranty of any kind, express or implied, including, but not limited to warranties of performance,merchantability and fitness for a particular purpose.\n\n"

"Joe\'s Tech Bits will not be liable to You or anyone else for any decision made or action taken in reliance on the information given by the Photo Download Utility or for any consequential, special or similar damages, even if advised of the possibility of such damages.\n\n"

"Backup your Source CSV file prior to running App."
)
label3.pack(anchor="w", pady=5)
# Create a button
button = tk.Button(window, text="Agree and Run APP", command=run_program)
button.pack(pady=20)
#window.title("Button Selection")

# Create a button
button_quit = tk.Button(window, text="Disagree and Exit Program", command=exit_program)
button_quit.pack()
window.mainloop()
window = tk.Tk()
window.withdraw()

file_path = filedialog.askopenfilename(
    title="Select Source File", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
)
if file_path:
    print("Selected file:", file_path)

#Select Target Directory
directory_path = filedialog.askdirectory()
if directory_path:
    print("Selected directory:", directory_path)

main_file = file_path

#Add Index Column to CSV File
df = pd.read_csv(file_path, index_col=False)
column_names = df.keys().tolist()
if not "index" in df.columns:
    #print("got to index")
    df.reset_index(inplace=True)
#Check that column is named 'Value'
if not column_names[7] == "Value":
    #print("got to value")
    df.rename(columns={"Value, USD (CoinSnap) ": "Value"}, inplace=True)
#Save CSV file
df.to_csv(file_path, index=False)

#Create counter from Max index
maxClm = df["index"].max()
#print("Max index value = " + str(maxClm))
#print(f"New Max Index = {maxClm}")
counter = (maxClm * 2) + 2
main_file = file_path
#print("Counter " + str(counter))

#Create window with labels
window = tk.Tk()
window.geometry("420x250")
label = tk.Label(window, background="lightblue", width=200, height=2, text=counter)
label.pack(anchor="w", pady=5)
label2 = tk.Label(
    window,
    background="lightblue",
    width=200,
    height=2,
    font=("Courier", 24),
    text="Joe's Tech Bits",
)
label2.pack(anchor="w", pady=5)



def download_image(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            shutil.copyfileobj(response.raw, f)
        #print(f"Image saved as {filename}")
        decrement_number()
    else:
        print(f"Failed to download image: {response.status_code}")

#Open CSV list and create file name to save
with open(main_file, "r") as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for key in csv_reader:
        front_image = (
            str(key["index"])
            + " "
            + str(key["Subject"])
            + " "
            + str(key["Year"])
            + " "
            + str(key["Denomination"])
            + " "
            + str(key["Value"])
            + " "
            + str(key["Mintmark"])
            + " "
            + str(key["Grading"])
            + " "
            + "Obverse photo.png"
        )
        back_image = (
            str(key["index"])
            + " "
            + str(key["Subject"])
            + " "
            + str(key["Year"])
            + " "
            + str(key["Denomination"])
            + " "
            + str(key["Value"])
            + " "
            + str(key["Mintmark"])
            + " "
            + str(key["Grading"])
            + " "
            + "Reverse photo.png"
        )
        front_url = str(key["Obverse photo"])
        back_url = str(key["Reverse photo"])


        filename = front_image
        directory = directory_path

        front_path = os.path.join(directory, filename)

        image_url = front_url
        filename = front_path
        download_image(image_url, filename)

        filename = back_image
        directory = directory_path

        back_path = os.path.join(directory, filename)
        image_url = back_url
        filename = back_path
#Call download_image function and pass coin photo URL and filename
        download_image(image_url, filename)

time.sleep(5)
window.after(150000, window.destroy)


#This App is copyright 2024 by Joe's Tech Bits