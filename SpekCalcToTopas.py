import os
import sys
import numpy as np
import tkinter as tk
from tkinter import filedialog
np.set_printoptions(threshold=sys.maxsize)


"""Conversion
import matplotlib.pyplot as plt
from topas2numpy import read_ntuple
from scipy import stats
np.set_printoptions(threshold=np.nan)"""

""""#Turn SpekCalc file lines into array
with open('100kVp0mm0_05keV.spec', 'r') as output:
    output = output.read().splitlines()
    fileArray = np.array([])
    for line in output:
        fileArray = np.append(fileArray, line)"""


"""#if the file has not been edited, spectrum data starts after line 18
spectrum = fileArray[18:fileArray.size]

#seperate energy and fluence
spectrum = np.array(' '.join(spectrum).split(' '))

#Energy is every 3rd index, fluence is every 2nd
energySpectrum = spectrum[0::3]
energySpectrum = energySpectrum.astype(np.float)

fluenceSpectrum = spectrum[2::3]
fluenceSpectrum = fluenceSpectrum.astype(np.float)

#Total fluence (not used but icluded)
totalFluence = np.sum(fluenceSpectrum)

#print(energySpectrum)
#print(fluenceSpectrum)
#print(totalFluence)

weightedFluence = []
for value in range(np.size(fluenceSpectrum)):
    weightedFluence.append(fluenceSpectrum[value]/totalFluence)

print(np.sum(weightedFluence))

#Saved weights in topas format
np.set_printoptions(suppress=True)
weightedFluence = np.asarray(weightedFluence)
weightedFluence = np.insert(weightedFluence, 0, weightedFluence.size)
energySpectrum = np.insert(energySpectrum, 0, energySpectrum.size)
#energySpectrum = np.insert(energySpectrum, energySpectrum.size, "keV")
print(weightedFluence)
print(energySpectrum)

energySpectrum = np.delete(energySpectrum, 0)
weightedFluence = np.delete(weightedFluence, 0)

convertedFile = "dv:So/Demo/BeamEnergySpectrumValues = " + str(energySpectrum.size) + "\n " \
                + str(energySpectrum)[1:-1] + " keV \n" \
                + "\n uv:So/Demo/BeamEnergySpectrumWeights = " + str(weightedFluence.size) + "\n "\
                + str(weightedFluence)[1:-1]

f = open("ConvertedTopasFile.txt", "w+")
f.write(convertedFile)
f.close"""
#Conversion End




# Tkinter GUI

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.main_window()



    def main_window(self):
        self.pack(fill=None, expand=1)
        uploadButton = tk.Button(self, text="Upload SpekCalc File", command=self.upload)
        uploadButton.grid(column=1, row=0, pady=20)

        convertButton = tk.Button(self, text="Convert File", command=self.convert)
        convertButton.grid(column=1, row=2, pady=20)

        global status
        status = tk.Label(self, text="Waiting for upload", bd="2", relief="ridge")
        status.grid(column=1, row=3, pady=20)

    def upload(self):
        global filename
        filename = filedialog.askopenfilename(
            initialdir=os.getcwd(), title="Select file", filetypes=(("SpekCalc files","*.spec"),("all files","*.*")))
        #print(filename)
        status.config(text="File Uploaded")

    def convert(self):
        with open(filename, 'r') as output:
            output = output.read().splitlines()
            fileArray = np.array([])
            for line in output:
                fileArray = np.append(fileArray, line)
        # if the file has not been edited, spectrum data starts after line 18
        spectrum = fileArray[18:fileArray.size]

        # seperate energy and fluence
        spectrum = np.array(' '.join(spectrum).split(' '))

        # Energy is every 3rd index, fluence is every 2nd
        energySpectrum = spectrum[0::3]
        energySpectrum = energySpectrum.astype(np.float)

        fluenceSpectrum = spectrum[2::3]
        fluenceSpectrum = fluenceSpectrum.astype(np.float)

        # Total fluence
        totalFluence = np.sum(fluenceSpectrum)

        # print(energySpectrum)
        # print(fluenceSpectrum)
        print(totalFluence)

        weightedFluence = []
        for value in range(np.size(fluenceSpectrum)):
            weightedFluence.append(fluenceSpectrum[value] / totalFluence)

        print(np.sum(weightedFluence))

        # Saved weights in topas format
        np.set_printoptions(suppress=True)
        weightedFluence = np.asarray(weightedFluence)
        weightedFluence = np.insert(weightedFluence, 0, weightedFluence.size)
        energySpectrum = np.insert(energySpectrum, 0, energySpectrum.size)
        # energySpectrum = np.insert(energySpectrum, energySpectrum.size, "keV")
        print(weightedFluence)
        print(energySpectrum)

        energySpectrum = np.delete(energySpectrum, 0)
        weightedFluence = np.delete(weightedFluence, 0)

        convertedFile = "dv:So/Demo/BeamEnergySpectrumValues = " + str(energySpectrum.size) + "\n " \
                        + str(energySpectrum)[1:-1] + " keV \n" \
                        + "\n uv:So/Demo/BeamEnergySpectrumWeights = " + str(weightedFluence.size) + "\n " \
                        + str(weightedFluence)[1:-1]

        f = open(filename[:-5] + "_TOPAS.txt", "w+")
        f.write(convertedFile)
        f.close
        status.config(text="File Converted")

root = tk.Tk()
root.title('SpekCalc to TOPAS')
root.geometry('300x300')
img = tk.Image("photo", file="icon.gif")
root.call('wm','iconphoto',root._w,img)
root.resizable(False, False)
app = Application(root)
root.mainloop()

#create application instance
# Tkinter End