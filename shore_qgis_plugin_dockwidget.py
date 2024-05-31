# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ShoreDataCollectorDockWidget
                                 A QGIS plugin
 The tool collects recognized and refined shapes of water shore lines from satellite images and date lists
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2024-03-29
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Evgeny Cherkashin and Oksana Mazayeva
        email                : eugeneai@irnok.net, moks@crust.irk.ru
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal, QModelIndex
from qgis.PyQt.QtWidgets import QComboBox
from qgis.core import QgsMessageLog, Qgis, QgsApplication, QgsProject

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'shore_qgis_plugin_dockwidget_base.ui'))


class ShoreDataCollectorDockWidget(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(ShoreDataCollectorDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://doc.qt.io/qt-5/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self._iface = None
        self.setupUi(self)
        # QgsApplication.instance().focusChanged.connect(self.handleFocusChanged)

    @property
    def iface(self):
        return self._iface

    @iface.setter
    def iface(self, iface):
        self._iface = iface
        self.fillInLayerSelectionComboBox()

    def closeEvent(self, event):
        # try:
        #     QgsApplication.instance().focusChanged.disconnect(self.handleFocusChanged)
        # except TypeError:
        #     pass
        self.closingPlugin.emit()
        event.accept()

    def handleFocusChanged(self, old, new):
        def f(o):
            if o is None:
                return "NULL-OBJECT"
            on = o.objectName()
            return on

        s, o, n = [f(w) for w in [self, old, new]]

        # if new == self:
        #     QgsMessageLog.logMessage("Focus Changed: to me",
        #                              'shore_qgis_plugin', level=Qgis.Info)
        # QgsMessageLog.logMessage("Focus Changed: from {} to {}, self={}"
        #                          .format(o, n, s),
        #                          'shore_qgis_plugin', level=Qgis.Info)

        if n == "layerSelectionComboBox":
            self.fillInLayerSelectionComboBox()

    def fillInLayerSelectionComboBox(self):
        lcbb = self.findChild(QComboBox, "layerSelectionComboBox")
        if lcbb or self._iface is None is None:
            return

        # QgsMessageLog.logMessage("Found child: {}".format(name),
        #                          level=Qgis.Info)

        lcbb.clear()

        prj = QgsProject.instance()

        root = prj.layerTreeRoot()
        for g in root.findGroups():
            print(g, type(g))
            lcbb.addItem(format(g.name()))
        # groups = []
        # for k, c in prj.mapLayers().items():
        #     p = c.parent()
        #     if p is None:
        #         continue
        #     if p in groups:
        #         continue
        #     print(c, p)
        #     groups.append(p)
        # for g in groups:

        #     lcbb.addItem("G-{}".format(g.objectName()))


        # lv = self._iface.layerTreeView()
        # m = lv.model()
        # rowCount = m.rowCount()
        # for i in range(rowCount):
        #     idx = m.index(i, 0)
        #     d = m.data(idx)
        #     # t = m.data(idx,)
        #     for role in range(10):
        #         print(m.data(idx, role=role))
        #     lcbb.addItem(format(d))
        lcbb.update()
