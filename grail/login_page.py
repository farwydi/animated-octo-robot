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
## Class LoginPage
###########################################################################

class LoginPage(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))

        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        self.m_bitmap1 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(u"../img/mask.png", wx.BITMAP_TYPE_ANY),
                                         wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer5.Add(self.m_bitmap1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 25)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"Для расшифровки введите пароль:", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer5.Add(self.m_staticText1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_textCtrl2 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200, -1),
                                       wx.TE_CENTRE | wx.TE_PASSWORD)
        bSizer5.Add(self.m_textCtrl2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_button2 = wx.Button(self, wx.ID_ANY, u"Расшифровать", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer5.Add(self.m_button2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        self.m_staticText3.SetForegroundColour(wx.Colour(255, 0, 0))

        bSizer5.Add(self.m_staticText3, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer5.Add((0, 0), 1, wx.EXPAND, 5)

        self.SetSizer(bSizer5)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button2.Bind(wx.EVT_BUTTON, self.on_unlock)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def on_unlock(self, event):
        event.Skip()
