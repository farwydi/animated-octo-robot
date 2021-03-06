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

class LoginPage ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 600,400 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_bitmap1 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"../img/mask.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.m_bitmap1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 25 )
		
		self.title_text = wx.StaticText( self, wx.ID_ANY, u"Для расшифровки введите пароль:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.title_text.Wrap( -1 )
		bSizer5.Add( self.title_text, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText5 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Логин:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		bSizer6.Add( self.m_staticText5, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.login_field = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		self.login_field.SetMaxLength( 35 ) 
		bSizer6.Add( self.login_field, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer8.Add( bSizer6, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		bSizer51 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText4 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Пароль:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		bSizer51.Add( self.m_staticText4, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.password_field = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), wx.TE_PASSWORD )
		self.password_field.SetMaxLength( 16 ) 
		bSizer51.Add( self.password_field, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer8.Add( bSizer51, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		
		self.m_panel1.SetSizer( bSizer8 )
		self.m_panel1.Layout()
		bSizer8.Fit( self.m_panel1 )
		bSizer5.Add( self.m_panel1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.lock_btn = wx.Button( self, wx.ID_ANY, u"Расшифровать", wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		bSizer5.Add( self.lock_btn, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.reg_btn = wx.Button( self, wx.ID_ANY, u"Регистрация", wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		bSizer5.Add( self.reg_btn, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.SetSizer( bSizer5 )
		self.Layout()
		self.status_bar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.lock_btn.Bind( wx.EVT_BUTTON, self.on_unlock )
		self.reg_btn.Bind( wx.EVT_BUTTON, self.on_reg )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_unlock( self, event ):
		event.Skip()
	
	def on_reg( self, event ):
		event.Skip()
	

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Grail", pos = wx.DefaultPosition, size = wx.Size( 1024,768 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
		
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.data_list = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 400,-1 ), wx.LC_REPORT )
		bSizer12.Add( self.data_list, 1, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, 5 )
		
		
		bSizer14.Add( bSizer12, 1, wx.EXPAND, 5 )
		
		bSizer13 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 900,-1 ), 0|wx.NO_BORDER )
		self.m_notebook1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
		
		self.m_panel4 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer17 = wx.BoxSizer( wx.VERTICAL )
		
		self.grail_text_ctrl = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		bSizer17.Add( self.grail_text_ctrl, 1, wx.EXPAND, 5 )
		
		
		self.m_panel4.SetSizer( bSizer17 )
		self.m_panel4.Layout()
		bSizer17.Fit( self.m_panel4 )
		self.m_notebook1.AddPage( self.m_panel4, u"Grail", False )
		self.m_panel5 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel5.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		bSizer19 = wx.BoxSizer( wx.VERTICAL )
		
		self.diff_text = wx.TextCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY )
		bSizer19.Add( self.diff_text, 1, wx.EXPAND, 5 )
		
		
		self.m_panel5.SetSizer( bSizer19 )
		self.m_panel5.Layout()
		bSizer19.Fit( self.m_panel5 )
		self.m_notebook1.AddPage( self.m_panel5, u"Diff", False )
		
		bSizer13.Add( self.m_notebook1, 1, wx.EXPAND|wx.ALL, 5 )
		
		
		bSizer14.Add( bSizer13, 1, wx.EXPAND, 5 )
		
		
		bSizer11.Add( bSizer14, 1, wx.EXPAND, 5 )
		
		bSizer111 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer16 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer16.SetMinSize( wx.Size( 400,-1 ) ) 
		self.push_btn = wx.Button( self, wx.ID_ANY, u"Push (0)", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer16.Add( self.push_btn, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer111.Add( bSizer16, 1, wx.EXPAND, 5 )
		
		bSizer171 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer171.SetMinSize( wx.Size( 900,-1 ) ) 
		self.commit_btn = wx.Button( self, wx.ID_ANY, u"Commit (0)", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer171.Add( self.commit_btn, 0, 0, 5 )
		
		
		bSizer111.Add( bSizer171, 1, wx.EXPAND|wx.LEFT, 5 )
		
		
		bSizer11.Add( bSizer111, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer11 )
		self.Layout()
		self.status_bar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.data_list.Bind( wx.EVT_LIST_ITEM_SELECTED, self.selected )
		self.grail_text_ctrl.Bind( wx.EVT_TEXT, self.grail_update )
		self.push_btn.Bind( wx.EVT_BUTTON, self.push )
		self.commit_btn.Bind( wx.EVT_BUTTON, self.commit )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def selected( self, event ):
		event.Skip()
	
	def grail_update( self, event ):
		event.Skip()
	
	def push( self, event ):
		event.Skip()
	
	def commit( self, event ):
		event.Skip()
	

