# -*- coding: utf-8 -*-
"""
/***************************************************************************
 multiPrint
                                 A QGIS plugin
 print multiple print composer views
                              -------------------
        begin                : 2014-06-24
        copyright            : (C) 2014 by enrico ferreguti
        email                : enricofer@gmail.com
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from multiprintdialog import multiPrintDialog
import os.path


class multiPrint:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'multiprint_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = multiPrintDialog()
        
    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/multiprint/icon.png"),
            u"print multiple print composer views", self.iface.mainWindow())
        # connect the action to the run method
        self.dlg.path.setText(QDesktopServices.storageLocation ( QDesktopServices.DocumentsLocation ))
        self.dlg.checkBox.stateChanged.connect(self.selectAllCheckbox)
        self.dlg.exportAsPdf.clicked.connect(self.pdfOut)
        self.dlg.exportAsImg.clicked.connect(self.imgOut)
        self.dlg.browse.clicked.connect(self.browseDir)
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&multiPrint", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&multiPrint", self.action)
        self.iface.removeToolBarIcon(self.action)

    def populateComposerList(self):
        #called to populate field list for WHERE statement
        wdgt=self.dlg.composerList
        wdgt.clear()
        for cView in self.iface.activeComposers ():
            item=QListWidgetItem()
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            item.setText(cView.composerWindow().windowTitle())
            wdgt.addItem(item)
        wdgt.sortItems()

    def selectAllCheckbox(self):
        for rowList in range(0,self.dlg.composerList.count()):
            self.dlg.composerList.item(rowList).setCheckState(self.dlg.checkBox.checkState())
            #rowCheckbox = self.dlg.composerList.item(rowList)
            #take only selected attributes by checkbox
            #if rowCheckbox.checkState() == Qt.Checked:

    def pdfOut(self):
        for rowList in range(0,self.dlg.composerList.count()):
            rowCheckbox = self.dlg.composerList.item(rowList)
            #take only checked checkbox
            if rowCheckbox.checkState() == Qt.Checked:
                for cView in self.iface.activeComposers ():
                    if cView.composerWindow().windowTitle() == rowCheckbox.text():
                        print "PDFOUT",rowCheckbox.text()
                        cView.composition().exportAsPDF(os.path.join(self.dlg.path.text(),rowCheckbox.text()+".pdf"))
                        rowCheckbox.setCheckState(Qt.Unchecked)

    def imgOut(self):
        for rowList in range(0,self.dlg.composerList.count()):
            rowCheckbox = self.dlg.composerList.item(rowList)
            #take only checked checkbox
            if rowCheckbox.checkState() == Qt.Checked:
                for cView in self.iface.activeComposers ():
                    if cView.composerWindow().windowTitle() == rowCheckbox.text():
                        print "IMGOUT",rowCheckbox.text()
                        imgOut = cView.composition().printPageAsRaster (0)
                        imgOut.save(os.path.join(self.dlg.path.text(),rowCheckbox.text()+".png"),"PNG")
                        rowCheckbox.setCheckState(Qt.Unchecked)

    def browseDir(self):
        fileDialog = QFileDialog.getExistingDirectory(None, "Select Download Folder",self.dlg.path.text(),QFileDialog.ShowDirsOnly| QFileDialog.DontResolveSymlinks)
        self.dlg.path.setText(fileDialog)

    # run method that performs all the real work
    def run(self):
        # show the dialog
        self.dlg.show()
        self.populateComposerList()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            pass
