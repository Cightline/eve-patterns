import wx
import informative


class Prefs(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, wx.GetApp().TopWindow, title='prefs')
        panel = wx.Panel(self, wx.ID_ANY)
        text_vcode = wx.StaticText(panel, -1, 'vCode')
        text_keyid = wx.StaticText(panel, -1, 'keyID')

        self.sizeCtrl = wx.TextCtrl(panel, -1, '')
        self.posCtrl  = wx.TextCtrl(panel, -1, '')

        self.panel = panel

        sizer = wx.FlexGridSizer(2, 2, 5, 5,)
        sizer.Add(text_vcode)
        sizer.Add(self.sizeCtrl)
        sizer.Add(text_keyid)
        sizer.Add(self.posCtrl)

        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 15)
        panel.SetSizerAndFit(border)
        self.Fit()
        self.Show()

    


class GUI(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, 'tut')
        panel = wx.Panel(self, wx.ID_ANY)

        self.index = 0
       
        ID_FILE_OPEN  = wx.NewId()
        ID_FILE_CLOSE = wx.NewId()
        ID_FILE_QUIT  = wx.NewId()
        ID_FILE_OPTIONS = wx.NewId()
    
        self.list_ctrl = wx.ListCtrl(panel, size=(-1,100),
                                 style=wx.LC_REPORT|wx.BORDER_SUNKEN)

        self.list_ctrl.InsertColumn(0, 'Item')
        self.list_ctrl.InsertColumn(1, 'Price')
        self.list_ctrl.InsertColumn(2, 'Client')
        self.list_ctrl.InsertColumn(3, 'Location', width=125)

        btn = wx.Button(panel, label='Add Line')
        btn.Bind(wx.EVT_BUTTON, self.add_line)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list_ctrl, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
        panel.SetSizer(sizer)


        file_menu = wx.Menu()
        file_menu.Append(ID_FILE_OPTIONS, 'options')
        file_menu.Append(ID_FILE_QUIT, 'quit')
        menu_bar = wx.MenuBar() 
        menu_bar.Append(file_menu, 'File')
        self.SetMenuBar(menu_bar)


        wx.EVT_MENU(self, ID_FILE_OPTIONS,  Prefs)
        wx.EVT_MENU(self, ID_FILE_QUIT, self.gui_exit)




    def gui_exit(self, event):
        exit()

    def import_transactions(self):
        informative.yeild_transactions()
        


    def add_line(self, event):
        line = 'line %s' % (self.index)
        self.list_ctrl.InsertStringItem(self.index, line)
        self.list_ctrl.SetStringItem(self.index, 1, 'what')
        self.list_ctrl.SetStringItem(self.index, 2, 'w')
        self.index += 1









if __name__ == '__main__':
    app = wx.App(False)
    frame = GUI()
    frame.Show()
    app.MainLoop()

