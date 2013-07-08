import wx
import informative
import ConfigParser
import os


class Prefs(wx.Frame):
    def __init__(self, parent):
        self.api_keys = {'keyid':None, 'vcode':None}
        self.config = ConfigParser.ConfigParser()
        self.config_path = 'informative.config'

        self.load_api_keys()

        wx.Frame.__init__(self, wx.GetApp().TopWindow, title='prefs')
        panel = wx.Panel(self, wx.ID_ANY)

        self.text_vcode = wx.StaticText(panel, -1, 'vCode')
        self.text_keyid = wx.StaticText(panel, -1, 'keyID')

        self.input_vcode = wx.TextCtrl(panel, size=(500,-1))
        self.input_keyid = wx.TextCtrl(panel, size=(500,-1))

        if self.api_keys['keyid']:
            self.input_vcode.write(self.api_keys['keyid'])

        if self.api_keys['vcode']:
            self.input_keyid.write(self.api_keys['vcode'])



        self.panel = panel


        button = wx.Button(panel, label='Save')
        button.Bind(wx.EVT_BUTTON, self.save_api)

        sizer = wx.FlexGridSizer(2, 2, 5, 5)
        sizer.Add(self.text_vcode)
        sizer.Add(self.input_vcode)
        sizer.Add(self.text_keyid)
        sizer.Add(self.input_keyid)
        sizer.Add(button, 0, wx.ALL|wx.CENTER, 5)

        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 15)
        panel.SetSizerAndFit(border)
        self.Fit()
        self.Show()



    def load_api_keys(self):
        if os.path.exists(self.config_path):
            self.config.read(self.config_path)

        else:
            return False
       
        if self.config.has_option('settings', 'keyid'):
            self.api_keys['keyid'] = self.config.get('settings', 'keyid')

        if self.config.has_option('settings', 'vcode'):
            self.api_keys['vcode'] = self.config.get('settings', 'vcode')




    def save_api(self, event):
        self.input_vcode.GetLineText(0)
        self.input_keyid.GetLineText(0)
       
        self.config.set('settings', 'keyid', self.input_vcode.GetLineText(0))
        self.config.set('settings', 'vcode', self.input_keyid.GetLineText(0))
        
        with open(self.config_path, 'wb') as config_file:
            self.config.write(config_file)


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

