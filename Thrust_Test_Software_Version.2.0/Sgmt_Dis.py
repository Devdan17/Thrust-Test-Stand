from PyQt5.QtWidgets import QMainWindow, QApplication, QLCDNumber , QSlider , QStatusBar , QDial , QPushButton , QFileDialog
from PyQt5 import uic ,QtCore 
from PyQt5.QtGui import QIcon
import sys , random , serial.tools.list_ports , os , pandas as pd
from PyQt5.QtCore import QTime, QTimer , QFile, QTextStream
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg , NavigationToolbar2Tk
from matplotlib.figure import Figure


x_val1 = []
y_val1 = []
x_val2 = []
plt.style.use("dark_background")


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.getcwd()

    return os.path.join(base_path, relative_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        
        ui = resource_path("Thrust_Test_V.2.0_GUI.ui")
        uic.loadUi(ui,self)

        icon = resource_path("research.ico")
        self.setWindowIcon(QIcon(icon))

        #Options Menu
        self.actionSlider.triggered.connect(lambda: self.change_Wid("Slider"))
        self.actionDial.triggered.connect(lambda: self.change_Wid("Dial"))

        #File Menu
        self.actionSave.triggered.connect(lambda: self.save_file())
        self.actionOpen.triggered.connect(lambda: self.open_file())
        
        #Themes Menu
        self.action1_2.triggered.connect(lambda: self.change_theme("Themes/Combinear.qss"))
        self.action2.triggered.connect(lambda: self.change_theme("Themes/Darkeum.qss"))
        self.action3.triggered.connect(lambda: self.change_theme("Themes/Genetive.qss"))
        self.action4.triggered.connect(lambda: self.change_theme("Themes/Irrorater.qss"))
        self.action5.triggered.connect(lambda: self.change_theme("Themes/Orange_Blk.qss"))
        self.action6.triggered.connect(lambda: self.change_theme("Themes/Takezo.qss"))
        self.actionNone.triggered.connect(lambda: self.change_theme("None"))

        

        self.lcd1 = self.findChild(QLCDNumber,"lcdNumber_1")
        # self.lcd1.setDigitCount(7)

        self.lcd2 = self.findChild(QLCDNumber,"lcdNumber_2")
        # self.lcd2.setDigitCount(12)

        self.lcd3 = self.findChild(QLCDNumber,"lcdNumber_3")
        # self.lcd3.setDigitCount(12)

        self.slider = self.findChild(QSlider,"horizontalSlider")
        self.dial = self.findChild(QDial,"dial")
        

        self.statusbar = self.findChild(QStatusBar,"statusbar")
        self.setStatusBar(self.statusbar)

        self.button = self.findChild(QPushButton,"pushButton")
        self.button.clicked.connect(self.plt1)

        self.timer = QTimer()
        self.timer.timeout.connect(self.displays_update)
        self.timer.timeout.connect(self.com_check)

        self.change_Wid("Slider")
        self.timer.start(10)
        self.displays_update()
        self.com_check()
        
        self.show()

    def change_Wid(self,wid):
        if wid == "Slider":
            self.slider.setVisible(True)
            self.slider.setEnabled(True)
            self.dial.setVisible(False)
            self.dial.setEnabled(False)
        else:
            self.slider.setVisible(False)
            self.slider.setEnabled(False)
            self.dial.setVisible(True)
            self.dial.setEnabled(True)

    def change_theme(self,loc):
        file = resource_path(loc)
        if file == "None":
            return
        else:
            File = QtCore.QFile(file)
            if not File.open( QtCore.QFile.ReadOnly | QtCore.QFile.Text):
                return

        qss = QtCore.QTextStream(File)

        #setup stylesheet
        app.setStyleSheet(qss.readAll())

    def displays_update(self):
        x_val1.append(random.randint(500,10000))
        for i in range(len(x_val1)):
            a=str(x_val1[i])
        self.lcd1.display(a)

        x_val2.append(random.randint(500,10000))
        for i in range(len(x_val2)):
            b=str(x_val2[i])
        self.lcd2.display(b)

        if self.slider.isEnabled():
            num = self.slider.value()
        else:
            num = self.dial.value()
        self.lcd3.display(num)
        y_val1.append(num)

    def animate(self):
        
        plt.cla()  
        plt.tight_layout(pad=1.5)
        plt.subplot(2,2,1)
        plt.title("RPM")
        plt.plot(x_val1,y_val1,color = "red")
        plt.xlabel('RPM')
        plt.ylabel('Throttle')

        plt.subplot(2,2,2)
        plt.title("Thrust")
        plt.plot(x_val2,y_val1,color = "green")
        plt.xlabel('Thrust')
        plt.ylabel('Throttle')

        plt.subplot(2,1,2)
        plt.title("Thrust V/S RPM")
        plt.plot(x_val1,x_val2,color = "blue")
        plt.xlabel('RPM')
        plt.ylabel('Thrust')

    ani1 = FuncAnimation(plt.gcf(),animate,interval=500)

#To plot RPM graph
    def plt1(self):
        
        plt.tight_layout()
        plt.show()

    def com_check(self):
        ports = serial.tools.list_ports.comports()
        if(ports == []):
            com = "None"

        if ports != []:
            for port, desc, hwid in sorted(ports):
                com = "{}".format(port, desc, hwid)

        self.statusbar.showMessage(f"Connected To : {com}")

    def save_file(self):
        file_path= QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv)")
        try:
            if file_path:
                data={'RPM':x_val1,'Throttle':y_val1,'Thrust':x_val2}
                df = pd.DataFrame(data)
                df.to_csv(file_path[0])
        except:
            return

    def open_file(self):
        file = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file:
            df = pd.read_csv(file[0])
            lst = df.values.tolist()
            i = 0
            while(i<len(lst)):
                lst.remove(lst[i][0])
                i+1
            print(lst)
            
app = QApplication(sys.argv)
UIWindow = MainWindow()
status_bar = QStatusBar()
app.exec_()
