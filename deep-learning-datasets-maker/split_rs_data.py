# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SplitRSData
                                 A QGIS plugin
 tools to handle raster and vector data to split it into small pieces equaled in size for machine learning datasets
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-12-08
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Youssef Harby
        email                : youssef_harby@yahoo.com
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
from numpy import double
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis.core import (QgsMapLayerProxyModel, QgsProject, QgsProcessingFeedback, QgsMessageLog, Qgis)
# import processing, tempfile

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .split_rs_data_dialog import SplitRSDataDialog
import os.path
from qgis.utils import iface
import os
import os.path as osp
from .utils import *
# import argparse
from easydict import EasyDict as edict


class SplitRSData:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'SplitRSData_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Deep Learning Datasets Maker')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None
    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('SplitRSData', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/split_rs_data/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Deep Learning Datasets Maker'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Deep Learning Datasets Maker'),
                action)
            self.iface.removeToolBarIcon(action)

    # def select_output_rasterize(self):
    #     filenameVR, _filter = QFileDialog.getSaveFileName(self.dlg, "Select Output Rasterized File","",'*.tif')
    #     self.dlg.lineEditV_R.setText(filenameVR)
    # def select_output_images(self):
    #     # filenameIM, _filter = QFileDialog.getSaveFileName(self.dlg, "Select Output Images Files","",'*.jpg') 
    #     filenameIM = QFileDialog.getExistingDirectory(self.dlg, 'Select Empty Folder For Images')
    #     self.dlg.lineEditImages.setText(filenameIM)
    # def select_output_labels(self):
    #     # filenameLB, _filter = QFileDialog.getSaveFileName(self.dlg, "Select Output Labels Files","",'*.png')
    #     filenameLB = QFileDialog.getExistingDirectory(self.dlg, 'Select Empty Folder For Labels')
    #     self.dlg.lineEditLabels.setText(filenameLB)

    def state_changed(self, state):
            """ Set the visibility of mQfwLabels_InSeg

            Args:
                state (int): Output the current status of three check boxes:
                           0 selected
                           1 half selected 
                           2 unchecked
            """
            if state == 2:
                self.dlg.mQfwLabels_InSeg.setEnabled(True)  # We also can use .setHidden(False)
                self.dlg.label_7.setEnabled(True)
            else : 
                self.dlg.mQfwLabels_InSeg.setEnabled(False)
                self.dlg.label_7.setEnabled(False)

    def state_changed_paddle(self, state):
            if state == 2:
                self.dlg.mOpacityWidget_Training.setEnabled(True)
                self.dlg.mOpacityWidget_Validating.setEnabled(True)
                self.dlg.label_8.setEnabled(True)
                self.dlg.label_9.setEnabled(True)
                self.dlg.label_10.setEnabled(True)
            else :
                self.dlg.mOpacityWidget_Training.setEnabled(False)
                self.dlg.mOpacityWidget_Validating.setEnabled(False)
                self.dlg.label_8.setEnabled(False)
                self.dlg.label_9.setEnabled(False)
                self.dlg.label_10.setEnabled(False)
    
    def state_changed_training(self, state):
            # testing_set = 1.0 - (double(self.dlg.mOpacityWidget_Training.opacity()) + double(self.dlg.mOpacityWidget_Validating.opacity()))
            Training_Set = self.dlg.mOpacityWidget_Training.opacity()
            Val_Set =  self.dlg.mOpacityWidget_Validating.opacity()
            Testing_Set = self.dlg.mOpacityWidget_Testing.opacity()
            if Testing_Set == 0:
                self.dlg.mOpacityWidget_Validating.setOpacity(1.0 - Training_Set)
            self.dlg.mOpacityWidget_Testing.setOpacity(1.0 - (Training_Set+Val_Set))


    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = SplitRSDataDialog()
            # if not self.dlg.isVisible():
            #     self.dlg.show()
            # self.dlg.pushButtonVR.clicked.connect(self.select_output_rasterize)
            # self.dlg.pushButtonImg.clicked.connect(self.select_output_images)
            # self.dlg.pushButtonLabl.clicked.connect(self.select_output_labels)
        
        # Fetch the currently loaded layers
        # Set filewidget

        self.dlg.mQfwRasterized.setFilter("*.tif")
        self.dlg.mQfwRasterized.setDialogTitle("Select Output Rasterized File")
        self.dlg.mQfwImages.setDialogTitle("Select Output Images Files")
        self.dlg.mQfwLabels.setDialogTitle("Select Output Labels Files")
        self.dlg.mQfwLabels_InSeg.setDialogTitle("Select Output Inst Seg Labels Files")
        # Populate the comboBox with names of all the loaded layers
        self.dlg.mMapLayerComboBoxR.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.dlg.mMapLayerComboBoxV.setFilters(QgsMapLayerProxyModel.PolygonLayer)
        self.dlg.comboBoxImgSize.clear()
        self.dlg.comboBoxImgSize.addItems(["64", "128", "256", "512", "1024"])
        self.dlg.comboBoxImgSize.setCurrentIndex(3)
        self.dlg.checkBoxInSeg.setChecked(True)
        self.dlg.checkBoxPaddle.setChecked(True)
        self.dlg.checkBoxInSeg.stateChanged.connect(self.state_changed)
        self.dlg.checkBoxPaddle.stateChanged.connect(self.state_changed_paddle)
        self.dlg.mOpacityWidget_Training.opacityChanged.connect(self.state_changed_training)
        self.dlg.mOpacityWidget_Validating.opacityChanged.connect(self.state_changed_training)

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            currentrasterlay = self.dlg.mMapLayerComboBoxR.currentText()  # Get the selected raster layer
            rlayers = QgsProject.instance().mapLayersByName(currentrasterlay)
            fn_ras = rlayers[0]
            currentvectorlay = self.dlg.mMapLayerComboBoxV.currentText()  # Get the selected raster layer
            vlayers = QgsProject.instance().mapLayersByName(currentvectorlay)
            fn_vec = vlayers[0]
            # ttt = (tempfile.NamedTemporaryFile(suffix='.shp'))
            # output = str(self.dlg.lineEditV_R.text())
            output = str(self.dlg.mQfwRasterized.filePath())
            SplittingSize = int(self.dlg.comboBoxImgSize.currentText()) # $$$$$$$$$$$$$$$$$$$$$
            # SplittingSize = self.dlg.label.setText(str(index_SplittingSize))

            # Log for files
            ras_path = str(fn_ras.dataProvider().dataSourceUri())
            vec_path = str(fn_vec.dataProvider().dataSourceUri())

            feedback = QgsProcessingFeedback()
            feedback.pushInfo(ras_path)
            feedback.pushInfo(vec_path)
            feedback.pushInfo(output)
            feedback.pushInfo(str(SplittingSize))

            # import os.path as ops
            # print(ops.exists(vec_path))

            # iface.messageBar().pushMessage(output, level=Qgis.Critical)
            # TODO: if shp in memory, it can't work
            
            rasterize(ras_path, vec_path, output)
            iface.messageBar().pushMessage("You will find the rasterized file in " + output, level=Qgis.Info, duration=5)
            iface.addRasterLayer(output, "0-1-class")

            # feedback.pushInfo(str(fn_ras.dataProvider().dataSourceUri()))
            # feedback.pushInfo(str(fn_vec.dataProvider().dataSourceUri()))
            # do it 
            # image_folder_path = str(self.dlg.lineEditImages.text())
            # label_folder_path = str(self.dlg.lineEditLabels.text())
            image_folder_path = str(self.dlg.mQfwImages.filePath())
            label_folder_path = str(self.dlg.mQfwLabels.filePath())
            fn_ras_path = fn_ras.dataProvider().dataSourceUri()
            splitting(fn_ras_path, image_folder_path, "jpg", "JPEG", "", SplittingSize, SplittingSize, currentrasterlay)
            splitting(output, label_folder_path, "png", "PNG", "", SplittingSize, SplittingSize, currentrasterlay) #should be the same name of image. vector name if needed-> currentvectorlay

            save_path_InSeg = str(self.dlg.mQfwLabels_InSeg.filePath())
            # names = os.listdir(label_folder_path)
            names = [f for f in os.listdir(label_folder_path) if f.endswith('.png')]
            if self.dlg.checkBoxInSeg.isChecked():
                for name in names:
                    label = osp.join(label_folder_path, name)
                    saver = osp.join(save_path_InSeg, name)
                    segMaskB2I(label, saver)
            else :
                feedback.pushInfo("Option instance segmentation is not selected")

            if self.dlg.checkBoxPaddle.isChecked():
                dataset_path = os.path.dirname(image_folder_path)
                Training_Set = self.dlg.mOpacityWidget_Training.opacity()
                Val_Set =  self.dlg.mOpacityWidget_Validating.opacity()
                Testing_Set = self.dlg.mOpacityWidget_Testing.opacity()
                
                args = edict()
                args.dataset_root = dataset_path
                args.images_dir_name = image_folder_path
                args.labels_dir_name = label_folder_path
                args.split = [Training_Set, Val_Set, Testing_Set]
                args.label_class = ['__background__', '__foreground__']
                args.separator = " "
                args.format = ['jpg', 'png']
                args.postfix = ['', '']
                print(args)  # test
                generate_list(args)

            iface.messageBar().pushMessage("You will find the dataset in " + dataset_path, level=Qgis.Success, duration=5)