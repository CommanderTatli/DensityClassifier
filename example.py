from DensityClassifier.ClusterHolder import *
from DensityClassifier.Cluster import *
import csv
from tkinter import *

class ClassifiableVector:
    """
    User defined data
    """
    def __init__(self, attributes):
        self.attributes = attributes
    """
    :return the square of the distance.
    GPU calculation is advised.
    """
    def getSquareDistance(self, other):
        result = 0
        for i in range(len(self.attributes)):
            result += (self.attributes[i]-other.attributes[i])*(self.attributes[i]-other.attributes[i])
        return result

# -------------------------------------------------------------
data = []
for i in range(3):
    data.append([])
with open("iris.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        point = ClassifiableVector([float(row['petal_length'])*100, float(row['petal_width'])*100])
        if row['species'] == 'setosa':
            data[0].append(point)
        elif row['species'] == 'versicolor':
            data[1].append(point)
        else:
            data[2].append(point)
clusters = []
for i in range(len(data)):
    if 3<=len(data[i]):
        name = 'setosa'
        if i == 1:
            name = 'versicolor'
        elif i == 2:
            name = 'virginica'
        clusters.append(Cluster(i, data[i]))

# -----------------------------------------------------------
def render():
    global primary_colors, secondary_colors, can, c, pixelSize, clusters, data, height, width
    can.delete("all")
    can.create_line(5, height-5, 5, 5, arrow=LAST)
    can.create_line(5, height-5, width-5, height-5, arrow=LAST)

    clusters = []
    for i in range(len(data)):
        if 3<=len(data[i]):
            clusters.append(Cluster(str(i+1), data[i]))
    c = ClusterHolder(clusters)
    c.processAllClusters()

    for x in range(0, width, pixelSize):
        for y in range(0, height, pixelSize):
            cl = c.classifyPoint(ClassifiableVector([float(x), float(height - y)]))
            color = "gray80"
            if cl != "":
                color = secondary_colors[int(cl) - 1]
                can.create_rectangle(x, y, x + pixelSize, y - pixelSize, fill=color, outline=color)
    for clu in range(len(data)):
        color = primary_colors[clu]
        for p in data[clu]:
            x = p.attributes[0]
            y = p.attributes[1]
            can.create_oval(x - 5, height - y - 5, x + 5, height - y + 5, fill=color)
def nextColor():
    global color, primary_colors, b1
    color += 1
    if len(primary_colors)<=color:
        color = 0
    b1.config(bg=primary_colors[color])
def clear():
    global can, data, height, width
    can.delete("all")
    can.create_line(5, height-5, 5, 5, arrow=LAST)
    can.create_line(5, height-5, width-5, height-5, arrow=LAST)
    data = []
    for i in range(3):
        data.append([])
def addPoint(event):
    global color, can, primary_colors, height
    can.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, fill=primary_colors[color])
    data[color].append( ClassifiableVector([event.x, height-event.y]) )
    render()
def incrementPixelSize():
    global pixelSize
    pixelSize += 1
def decrementPixelSize():
    global pixelSize
    if pixelSize != 1:
        pixelSize -= 1

primary_colors = ["red", "blue", "green"]
secondary_colors = ["tomato", "light blue", "light green"]
pixelSize = 5
height = 600
width = 800
color = 0

win = Tk()
can = Canvas(win, width = width, height = height, bg="gray80")
can.grid(row=0, column=0, rowspan=100)
b1 = Button(win, command=nextColor, text="NextColor", bg=primary_colors[0])
b1.grid(row=0, column=1, columnspan=2)
b2 = Button(win, command=render, text="Render").grid(row=1, column=1, columnspan=2)
b3 = Button(win, command=clear, text="Clear").grid(row=2, column=1, columnspan=2)
l = Label(text="Change resolution").grid(row=3, column=1, columnspan=2)
b4 = Button(win, command=decrementPixelSize, text="+").grid(row=4, column=1)
b5 = Button(win, command=incrementPixelSize, text="-").grid(row=4, column=2)

can.bind("<Button-1>", addPoint)
render()
win.mainloop()