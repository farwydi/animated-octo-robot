import wx
import wx.dataview as dv


class DRCustomRenderer(dv.DataViewCustomRenderer):
    def __init__(self, *args, **kw):
        dv.DataViewCustomRenderer.__init__(self, *args, **kw)
        self.value = None
        self.EnableEllipsize(wx.ELLIPSIZE_END)

    def SetValue(self, value):
        self.value = value
        return True

    def GetValue(self):
        return self.value

    def GetSize(self):
        value = self.value if self.value else ""
        size = self.GetTextExtent(value)
        size += (2, 2)
        return size

    def Render(self, rect, dc, state):
        if not state & dv.DATAVIEW_CELL_SELECTED:
            dc.SetBrush(wx.Brush('#ffd0d0'))
            dc.SetPen(wx.TRANSPARENT_PEN)
            rect.Deflate(1, 1)
            dc.DrawRoundedRectangle(rect, 2)

        value = self.value if self.value else ""

        self.RenderText(value, 0, rect, dc, state)
        return True
