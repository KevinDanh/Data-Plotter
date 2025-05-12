"""
File: MplTools.py
Description: Wrapper for Matplotlib tools
"""

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import (
    QSizePolicy
)

def makeFigureCanvas(parent, figure):
    canvas = FigureCanvas(figure)
    canvas.setMinimumWidth(400)
    canvas.setMinimumHeight(400)
    canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    return canvas

def makeFigure(width, height):
    figure = Figure(figsize=(width,height))
    return figure

def makeNavigationToolBar(parent, canvas):
    toolbar = NavigationToolbar(canvas, parent)
    return toolbar
