import sys
from flask import json
import random
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from fbs_runtime.application_context import ApplicationContext
# from PyQt5.QtGui import Q
from PyQt5.QtCore import *
from dateutil import parser
import pandas as pd
from pandas import DataFrame as df
from plotly.offline import plot
import plotly.figure_factory as ff

try:
    import Model
except ModuleNotFoundError:
    pass


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.originalPalette = QApplication.palette()
        self.screen = QDesktopWidget().availableGeometry()
        self.screenWidth = 2560
        self.screenHeight = 1440
        self.showAmount = 10

        with open("availableMaterials.json", "r") as _:
            self.availableMaterials = json.load(_)["availableMaterials"]

        try:
            self.model = Model()
        except:
            self.orderDF = df(pd.read_csv("data_csv/order.csv", sep="\t"))
            self.equipmentDF = df(pd.read_csv("data_csv/equipment_2.csv"))

            # with open("hackatonExample.json", "r") as _:
            #     self.hackatonExample = json.load(_)
            #     self.df = self.hackatonExample["data"]
            #     self.colors = self.hackatonExample["colors"]

            self.hackatonExample = dict(
                Task="Machine #1",
                Start='2019-01-01',
                Finish='2019-02-02',
                Resource='Material #1'
            )

        self.createOrderBox()
        self.createPlotEditBox()

        try:
            self.createWebPlot(scheduleData=self.model)
        except:
            self.createWebPlot()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.plotEditBox, 1, 0)
        mainLayout.addWidget(self.webPlot, 2, 0, 2, 2)
        mainLayout.addWidget(self.orderBox, 1, 1)

        self.plotEditBox.setDisabled(True)

        mainLayout.setRowStretch(2, 1)
        mainLayout.setRowStretch(2, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Расписание заказов")

        self.forceOrderButton.clicked.connect(self.addOrder)

    def createPlotEditBox(self):
        self.plotEditBox = QGroupBox()

        materialID = QLineEdit()

        materialAmount = QLineEdit(self.plotEditBox)
        materialAmount.setReadOnly(True)

        dateTimeSince = QDateTimeEdit(self.plotEditBox)
        dateTimeSince.setDateTime(QDateTime.currentDateTime())

        dateTimeTo = QDateTimeEdit(self.plotEditBox)
        dateTimeTo.setDateTime(QDateTime.currentDateTime())

        flatPushButton = QPushButton("Применить")
        flatPushButton.setFlat(True)

        layout = QGridLayout()
        layout.addWidget(QLabel("ID материала:"), 0, 0, 1, 2)
        layout.addWidget(materialID, 1, 0, 1, 2)
        layout.addWidget(QLabel("Оставшееся количество материала:"), 2, 0, 1, 2)
        layout.addWidget(materialAmount, 3, 0, 1, 2)
        layout.addWidget(QLabel("Начала периода:"), 4, 0, 1, 2)
        layout.addWidget(dateTimeSince, 5, 0, 1, 2)
        layout.addWidget(QLabel("Конец периода:"), 6, 0, 1, 2)
        layout.addWidget(dateTimeTo, 7, 0, 1, 2)
        layout.addWidget(flatPushButton)
        layout.setRowStretch(5, 1)
        self.plotEditBox.setLayout(layout)

    def fillPriorityOrder(self):
        changeOrderID = self.orderID.currentText()

        # ordermaterial =
        # orderAmount =
        # currentDeadline =

    def createOrderBox(self):
        self.orderBox = QGroupBox()

        self.orderID = QComboBox(self.orderBox)

        try:
            self.orderIDs = self.model.data.order_df["_id"]
            for id in self.orderIDs:
                self.orderID.addItem(id)
        except AttributeError:
            self.orderID.addItem("Material #1")
            self.orderID.activated.connect(self.fillPriorityOrder)

        self.orderMaterial = QLineEdit(self.orderBox)
        self.orderMaterial.setReadOnly(True)

        self.orderMaterialAmount = QLineEdit(self.orderBox)
        self.orderMaterialAmount.setReadOnly(True)

        self.neccessaryMaterialDeadline = QDateEdit(self.orderBox)
        self.neccessaryMaterialDeadline.setDate(QDate.currentDate())

        self.currentDeadline = QLineEdit(self.orderBox)
        self.currentDeadline.setReadOnly(True)

        self.forceOrderButton = QPushButton("Изменить дату поставки(принудительно)")
        self.forceOrderButton.setFlat(False)

        layout = QGridLayout()

        layout.addWidget(QLabel("ID заказа:"), 0, 0, 1, 3)
        layout.addWidget(self.orderID, 1, 0, 1, 2)

        layout.addWidget(QLabel("Материал заказа:"), 2, 0, 1, 2)
        layout.addWidget(self.orderMaterial, 3, 0, 1, 2)

        layout.addWidget(QLabel("Количество материала:"), 2, 2, 1, 2)
        layout.addWidget(self.orderMaterialAmount, 3, 2, 1, 2)

        layout.addWidget(QLabel("Текущий срок поставки:"), 4, 0, 1, 2)
        layout.addWidget(self.currentDeadline, 5, 0, 1, 2)

        layout.addWidget(QLabel("Необходимый срок поставки:"), 4, 2, 1, 2)
        layout.addWidget(self.neccessaryMaterialDeadline, 5, 2, 1, 2)

        layout.addWidget(self.forceOrderButton)
        layout.setRowStretch(6, 1)
        self.orderBox.setLayout(layout)

    def createWebPlot(self, **kwargs):
        self.webPlotBox = QGroupBox()
        self.webPlot = QWebEngineView()
        if kwargs:
            self.df = kwargs["scheduleData"].schedule
            self.color = kwargs["scheduleData"].colors
        else:
            self.df = [self.hackatonExample]
            self.colors = {self.hackatonExample["Resource"]: "#{:06x}".format(random.randint(0, 0xFFFFFF))}

        self.figure = ff.create_gantt(self.df,
                                      colors=self.colors,
                                      index_col='Resource',
                                      show_colorbar=True,
                                      group_tasks=True,
                                      showgrid_x=True,
                                      showgrid_y=True,
                                      title="Загруженность станков",
                                      width=self.screenWidth*0.6,
                                      height=self.screenHeight*0.5
                                      )
        self.dataPlot = plot(self.figure, include_plotlyjs=False, output_type='div')
        self.raw_html = (
            '<html><head><meta charset="utf-8" />'
            '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script></head>'
            '<body>'
            '{}'
            '</body></html>'
            )
        self.webPlot.setHtml(self.raw_html.format(self.dataPlot))

        layout = QGridLayout()
        layout.addWidget(self.webPlot, 0, 0, 0, 0)
        self.webPlotBox.setLayout(layout)

    def addOrder(self):
        self.orderInfo = self.model.data.order_df["_id"]
        # orderMaterial = self.orderInfo[]
        # orderMaterialAmount
        # materialDeadline

    def updateWebPlot(self, **kwargs):
        if kwargs:
            self.df = kwargs["scheduleData"].schedule
            self.color = kwargs["scheduleData"].colors
        else:
            self.df = [dict(
                Task="Machine #11",
                Start='2019-01-01',
                Finish='2019-02-02',
                Resource='Material #1')]
            self.colors = {'5c94953dc9e77c0001d5e130': "#{:06x}".format(random.randint(0, 0xFFFFFF))}

        self.figure = ff.create_gantt(self.df,
                                      colors=self.colors,
                                      index_col='Resource',
                                      show_colorbar=True,
                                      group_tasks=True,
                                      showgrid_x=True,
                                      showgrid_y=True,
                                      title="Загруженность производства",
                                      width=self.screenWidth * 0.6,
                                      height=self.screenHeight * 0.5
                                      )
        self.dataPlot = plot(self.figure, include_plotlyjs=False, output_type='div')
        self.webPlot.setHtml(self.raw_html.format(self.dataPlot))


class AppContext(ApplicationContext):
    def run_(self):
        app = QApplication(sys.argv)
        interface = MainWindow()
        interface.showFullScreen()
        return (app.exec_())


if __name__ == '__main__':
    appctxt = AppContext()
    exit_code = appctxt.run_()
    sys.exit(exit_code)
