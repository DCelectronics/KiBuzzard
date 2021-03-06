"""Subclass of dialog_base, which is generated by wxFormBuilder."""
import os
import re

import wx

from . import dialog_base

class Dialog(dialog_base.KiBuzzardDialog):
    def __init__(self, parent, config, buzzard_path, func):
        dialog_base.KiBuzzardDialog.__init__(self, parent)
        
        typeface_path = os.path.join(buzzard_path, 'typeface')
        for entry in os.listdir(typeface_path):
            entry_path = os.path.join(typeface_path, entry)
            
            if not entry_path.endswith('.ttf'):
                continue
            
            self.fontComboBox.Append(os.path.splitext(entry)[0])
        
        self.fontComboBox.SetSelection(0)

        best_size = self.BestSize
        # hack for some gtk themes that incorrectly calculate best size
        best_size.IncBy(dx=0, dy=30)
        self.SetClientSize(best_size)
        self.config = config
        self.func = func
        
        self.loadConfig()
        
    def loadConfig(self):
        self.config.SetPath('/')
        self.notebook.SetSelection(self.config.ReadInt('tab'))
        x = self.config.ReadInt('x', self.GetPosition().x)
        y = self.config.ReadInt('y', self.GetPosition().y)
        self.Move((x, y))
        
        self.config.SetPath('/gui')
        self.labelStartComboBox.SetSelection(self.config.ReadInt('labelStart'))
        self.labelEdit.SetValue(self.config.Read('label'))
        self.labelEndComboBox.SetSelection(self.config.ReadInt('labelEnd'))
        self.fontComboBox.SetStringSelection(self.config.Read('font'))
        self.scaleSpinCtrl.SetValue(self.config.ReadFloat('scale', 0.04))
        self.verticalAlignComboBox.SetSelection(self.config.ReadInt('valign', 1))
        self.horizontalAlignComboBox.SetSelection(self.config.ReadInt('halign', 1))
        
        self.config.SetPath('/cmdline')
        self.cmdLineEdit.SetValue(self.config.Read('cmd'))
        
    def saveConfig(self):
        self.config.SetPath('/')
        self.config.WriteInt('tab', self.notebook.GetSelection())
        self.config.WriteInt('x', self.GetPosition().x)
        self.config.WriteInt('y', self.GetPosition().y)
        
        self.config.SetPath('/gui')
        self.config.WriteInt('labelStart', self.labelStartComboBox.GetSelection())
        self.config.Write('label', self.labelEdit.GetValue())
        self.config.WriteInt('labelEnd', self.labelEndComboBox.GetSelection())
        self.config.Write('font', self.fontComboBox.GetStringSelection())
        self.config.WriteFloat('scale', self.scaleSpinCtrl.GetValue())
        self.config.WriteInt('valign', self.verticalAlignComboBox.GetSelection())
        self.config.WriteInt('halign', self.horizontalAlignComboBox.GetSelection())
        
        self.config.SetPath('/cmdline')
        self.config.Write('cmd', self.cmdLineEdit.GetValue())

    def labelEditOnTextEnter( self, event ):
        self.createButtonOnButtonClick(event)
        
    def createButtonOnButtonClick(self, event):
        text = self.labelStartComboBox.GetStringSelection() + self.labelEdit.GetValue() + self.labelEndComboBox.GetStringSelection()
        font = self.fontComboBox.GetStringSelection()
        scale = self.scaleSpinCtrl.GetValue()
        valign = self.verticalAlignComboBox.GetSelection()
        halign = self.horizontalAlignComboBox.GetSelection()
        align = ['t', 'c', 'b'][valign] + ['l', 'c', 'r'][halign]
        
        if len(text) == 0:
            wx.MessageBox("Label can't be empty!", 'Error', wx.OK | wx.ICON_ERROR)
            return
    
        self.labelStartComboBox.Disable()
        self.labelEdit.Disable()
        self.labelEndComboBox.Disable()
        self.fontComboBox.Disable()
        self.scaleSpinCtrl.Disable()
        self.verticalAlignComboBox.Disable()
        self.horizontalAlignComboBox.Disable()
        self.createButton.Disable()
    
        self.saveConfig()
        
        self.func('-a %s -s %s -f "%s" "%s"' % (align, scale, font, text))
        
    def cmdLineEditOnTextEnter(self, event):
        cmd = self.cmdLineEdit.GetValue()
        
        if len(cmd) == 0:
            wx.MessageBox("Command can't be empty!", 'Error', wx.OK | wx.ICON_ERROR)
            return

        self.cmdLineEdit.Disable()
        
        self.saveConfig()
        
        self.func(cmd)
