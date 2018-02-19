# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jan 23 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class CreateGrail
###########################################################################

class CreateGrail(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"File not find", pos=wx.DefaultPosition,
                           size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer6 = wx.BoxSizer(wx.VERTICAL)

        bSizer7 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"У вас нету grail создать?", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)
        bSizer7.Add(self.m_staticText4, 0, wx.ALL, 15)

        self.m_textCtrl3 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TE_PASSWORD)
        bSizer7.Add(self.m_textCtrl3, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        bSizer6.Add(bSizer7, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer8 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button3 = wx.Button(self, wx.ID_ANY, u"Создать", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer8.Add(self.m_button3, 0, wx.ALL, 10)

        self.m_button4 = wx.Button(self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer8.Add(self.m_button4, 0, wx.ALL, 10)

        bSizer6.Add(bSizer8, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer6)
        self.Layout()
        bSizer6.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button3.Bind(wx.EVT_BUTTON, self.create)
        self.m_button4.Bind(wx.EVT_BUTTON, self.close)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def create(self, event):
        event.Skip()

    def close(self, event):
        event.Skip()
