from tkinter import * 
# from tkinter.filedialog import filedialog , asksaveasfile 
import random , csv , os , sys , pandas as pd , serial.tools.list_ports
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg , NavigationToolbar2Tk
from matplotlib.figure import Figure

ports = serial.tools.list_ports.comports()
if(ports == []):
    com = "None"
for port, desc, hwid in sorted(ports):
    com = "{}".format(port, desc, hwid)

try:
    serialcomm = serial.Serial(com, 9600)
    serialcomm.timeout = 1

except:
    pass

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Initialization and declaration of variables

win = Tk()
x_val1 = []
y_val1 = []
x_val2 = []
y_val2 = []
index = count()
onfil=resource_path("assests/onn.png")
off_file=resource_path("assests/offf.png")
on = PhotoImage(file=onfil)
off = PhotoImage(file=off_file)
plt.style.use("dark_background")
global is_on 
is_on = False
var = IntVar()
sel = ""

#To update RPM display
def update_rpm():
    x_val1.append(random.randint(500,1000))
    y_val1.append(sl.get())
    for i in range(len(x_val1)):
        a=str(x_val1[i])
        
    l1.config(text="RPM : "+a)
    l1.after(1000,update_rpm)

#To update Thrust display
def update_thrust():
    x_val2.append(random.randint(500,1000))
    y_val2.append(sl.get())
    for i in range(len(x_val2)):
        b=str(x_val2[i])

    l2.config(text="Thrust : "+b)
    l2.after(1000,update_thrust)

def update_throttle():

    l3.config(text="Throttle : "+str(sl.get())+"%")
    l3.after(1000,update_throttle)

#Control the toggle switch
def switch():
    global is_on
    if is_on:
        tb.config(image=off)
        is_on = False
        if(com!='None'):
            serialcomm.write(str(is_on).encode())
            serialcomm.close()
        exit()
        
    else:
        tb.config(image=on)
        is_on = True
        if(com!='None'):
            serialcomm.write(str(is_on).encode())
        update_rpm()
        update_thrust()
        update_throttle()

#fig = Figure(figsize=(5, 4), dpi=100)

        
#To animate graph for RPM
def animate(i):

    #ax = fig.add_subplot(111)

    plt.cla()  
    plt.tight_layout(pad=1.5)
    plt.subplot(2,2,1)
    plt.title("RPM")
    plt.plot(x_val1,y_val1,color = "red")
    plt.xlabel('RPM')
    plt.ylabel('Throttle')

    plt.subplot(2,2,2)
    plt.title("Thrust")
    plt.plot(x_val2,y_val2,color = "green")
    plt.xlabel('Thrust')
    plt.ylabel('Throttle')

    plt.subplot(2,1,2)
    plt.title("Thrust V/S RPM")
    plt.plot(x_val1,x_val2,color = "blue")
    plt.xlabel('RPM')
    plt.ylabel('Thrust')

ani1 = FuncAnimation(plt.gcf(),animate,interval=500)

#To plot RPM graph
def plt1():
    plt.tight_layout()
    plt.show()


def save_file():
    data={'RPM':x_val1,'y1':y_val1,'Thrust':x_val2,'y2':y_val2}
    df = pd.DataFrame(data)
    f = (asksaveasfile(initialfile = 'Untitled.csv',defaultextension=".csv",filetypes=[("All Files","*.*"),("Text Documents","*.txt"),("CSV","*.csv")]))
    df.to_csv(f)

def open_file():
    input = filedialog.askopenfile(initialdir="/")
    plots = csv.reader(input, delimiter = ',')
    for row in plots:
        if len(row) >= 2:
            x_val1.append(row[0])
            y_val1.append(row[1])
            x_val2.append(row[3])
            y_val2.append(row[4])

    plt.cla() 
    plt.plot(x_val1,y_val1,x_val2,y_val2)
    plt.show()

def about():
    new_win = Toplevel(win)
    lab = Label(new_win,text="This Software is used to test RPM and Thurst of a motor \nMADE BY ASHISH",font=(24))
    lab.grid(row=0,column=0,padx=10,pady=10)

# inizialize GUI elements
l1 = Label(win,text="RPM :",font=("Seven Segment",48),fg="red",borderwidth=5, relief="sunken",bg="black")
l2 = Label(win,text="Thrust :",font=("Seven Segment",48),fg="red",borderwidth=5, relief="sunken",bg="black")
l3 = Label(win,text="Throttle :",font=("Seven Segment",48),fg="red",borderwidth=5, relief="sunken",bg="black")
b1 = Button(win,text="Graphs",font=(24),bg="#3cbef6",bd=1,command=plt1)
tb = Button(win,image=off,bd=0,command=switch)
sl = Scale(win,from_=0,to=100,orient=HORIZONTAL,length=200,width=30,cursor='dot',troughcolor='black')
l4 = Label(win,text="Connected to : "+com)

#adding menu bar

mbar = Menu(win)
win.config(menu=mbar)

main_menu = Menu(mbar,tearoff="off")
mbar.add_cascade(label ="Options",menu=main_menu)
main_menu.add_separator()
main_menu.add_command(label = "Save",command=lambda:save_file())
main_menu.add_command(label = "Open",command=lambda:open_file())
main_menu.add_separator()
main_menu.add_command(label = "Port: "+com,command=lambda:save_file())
main_menu.add_separator()
main_menu.add_command(label="About",command=about)
main_menu.add_command(label="Exit",command=win.quit)

# canvas = FigureCanvasTkAgg(fig, master=win)
# canvas.draw()
# canvas.get_tk_widget().grid(row=0,column=1)

#To place gUI elements 
l1.grid(row=0,column=0,padx=10,pady=10)
l2.grid(row=0,column=1,padx=10,pady=10)
l3.grid(row=1,column=0,padx=10,pady=10,columnspan=10)
b1.grid(row=2,column=0,padx=50,pady=10,columnspan=10)
tb.grid(row=3,column=0,padx=50,columnspan=10)
sl.grid(row=4,column=0,columnspan=10)
l4.grid(row=5,column=1,columnspan=10)

win.mainloop()