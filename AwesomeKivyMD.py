from tkinter import *
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import mplcyberpunk

matplotlib.style.use("cyberpunk")

import pandas as pd
import matplotlib.pyplot as plt

# Read json from String
json_str = '[{"Fee":"25000","Duration":"1-10-2022","Discount":"80"},\
{"Fee":"20000","Duration":"2-10-2022","Discount":"69.9"},\
{"Fee":"15000","Duration":"3-10-2022","Discount":"85"}, \
{"Fee":"25000","Duration":"1-11-2022","Discount":"88"},\
{"Fee":"20000","Duration":"2-11-2022","Discount":"90.2"},\
{"Fee":"15000","Duration":"3-11-2022","Discount":"100"}, \
{"Fee":"25000","Duration":"1-09-2022","Discount":"60"},\
{"Fee":"20000","Duration":"2-09-2022","Discount":"61.2"},\
{"Fee":"15000","Duration":"3-09-2022","Discount":"50.0"}, \
{"Fee":"25000","Duration":"4-10-2022","Discount":"80"},\
{"Fee":"20000","Duration":"5-10-2022","Discount":"69.9"},\
{"Fee":"15000","Duration":"6-10-2022","Discount":"85"}, \
{"Fee":"25000","Duration":"7-11-2022","Discount":"88"},\
{"Fee":"20000","Duration":"8-11-2022","Discount":"90.2"},\
{"Fee":"15000","Duration":"9-11-2022","Discount":"100"}, \
{"Fee":"25000","Duration":"10-09-2022","Discount":"60"},\
{"Fee":"20000","Duration":"11-09-2022","Discount":"61.2"},\
{"Fee":"15000","Duration":"12-09-2022","Discount":"50.0"}, \
{"Fee":"25000","Duration":"13-10-2022","Discount":"80"},\
{"Fee":"20000","Duration":"14-10-2022","Discount":"69.9"},\
{"Fee":"15000","Duration":"15-10-2022","Discount":"85"}, \
{"Fee":"25000","Duration":"20-11-2022","Discount":"88"},\
{"Fee":"20000","Duration":"21-11-2022","Discount":"90.2"},\
{"Fee":"15000","Duration":"22-11-2022","Discount":"100"}, \
{"Fee":"25000","Duration":"23-09-2022","Discount":"60"},\
{"Fee":"20000","Duration":"25-09-2022","Discount":"61.2"},\
{"Fee":"15000","Duration":"26-09-2022","Discount":"50.0"}]'
df = pd.read_json(json_str, orient='records')


df['Duration'] = pd.to_datetime(df['Duration'], format='%d-%m-%Y')
print(type(df.Duration[0]))
df = df.astype({'Discount':'float'})


df = df.sort_values(by='Duration',ascending=True)
print(df)



def plot():
    fig = Figure(figsize=(6, 6), dpi=100)
    plot1 = fig.add_subplot(111)
    plot1.plot(df['Duration'], df['Discount'], marker='o')
    plot1.fill_between(df['Duration'], df['Discount'], color='lightblue', alpha=0.5)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().pack()


window = Tk()
window.title('Plotting in Tkinter')
window.state('zoomed')  # zooms the screen to maxm whenever executed

plot_button = Button(master=window, command=plot, height=2, width=10, text="Plot")
plot_button.pack()
window.mainloop()







