import wx
import ConfigParser
import os

import eve_api

class Prefs(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, wx.GetApp().TopWindow, title='prefs')
        
        self.settings = {'keyid':None, 'vcode':None, 'default_character':None}
        self.characters = {}
        self.config = ConfigParser.ConfigParser()
        self.config_path = 'informative.config'


        # Load the info first so it appears when the GUI displays.
        self.load()
        
        self.panel = wx.Panel(self, wx.ID_ANY)

        self.text_vcode = wx.StaticText(self.panel, -1, 'vCode')
        self.text_keyid = wx.StaticText(self.panel, -1, 'keyID')
        
        self.character_box = wx.ComboBox(self.panel, 
                                         -1, 
                                         pos=(50,170), 
                                         size=(150,-1), 
                                         choices=self.characters.keys(), 
                                         style=wx.CB_READONLY)



        self.input_vcode = wx.TextCtrl(self.panel, size=(500,-1))
        self.input_keyid = wx.TextCtrl(self.panel, size=(500,-1))

        if self.settings['keyid']:
            self.input_keyid.write(self.settings['keyid'])

        if self.settings['vcode']:
            self.input_vcode.write(self.settings['vcode'])



        button = wx.Button(self.panel, label='Save')
        button.Bind(wx.EVT_BUTTON, self.save)

        sizer = wx.FlexGridSizer(2, 2, 5, 5)
        sizer.Add(self.text_vcode)
        sizer.Add(self.input_vcode)
        sizer.Add(self.text_keyid)
        sizer.Add(self.input_keyid)
        sizer.Add(button, 0, wx.ALL|wx.CENTER, 5)
        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 15)
        self.panel.SetSizerAndFit(border)
        self.Fit()




    def show(self, event):
        self.load()
        self.Show()


    def load(self):
        if os.path.exists(self.config_path):
            self.config.read(self.config_path)

        else:
            print 'could not load config: %s' % (self.config_path)
            return False
       
        if self.config.has_option('settings', 'keyid'):
            self.settings['keyid'] = self.config.get('settings', 'keyid')

        if self.config.has_option('settings', 'vcode'):
            self.settings['vcode'] = self.config.get('settings', 'vcode') 

        if self.config.has_option('settings', 'default_character'):
            self.settings['default_character'] = self.config.get('settings', 'default_character')
     

        # Tell the API the keys, then try to load the characters.
        api_singleton.set_api_key(self.settings['keyid'], vcode=self.settings['vcode'])
        api_singleton.set_default_character(self.settings['default_character'])

        
        char_list = api_singleton.import_characters()

        for d in char_list:
            if 'name' in d:
                self.characters[d['name']] = d['characterID']

        


    def save(self, event):
        self.config.set('settings', 'vcode', self.input_vcode.GetLineText(0))
        self.config.set('settings', 'keyid', self.input_keyid.GetLineText(0))
        self.config.set('settings', 'default_character', self.characters[self.character_box.GetValue()])
        
        with open(self.config_path, 'wb') as config_file:
            self.config.write(config_file)


        # Make sure we tell the API whats going on. 
        api_singleton.set_api_key(self.settings['keyid'], vcode=self.settings['vcode'])
        #api_singleton.set_default_character(character)


    
class GUI(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, 'tut')
        
        self.transactions = None
        self.prefs = Prefs(self)
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.status_bar = self.CreateStatusBar()
        self.index = 0
       
        ID_FILE_OPEN  = wx.NewId()
        ID_FILE_CLOSE = wx.NewId()
        ID_FILE_QUIT  = wx.NewId()
        ID_FILE_OPTIONS = wx.NewId()
    
        self.list_ctrl = wx.ListCtrl(self.panel, size=(-1,100),
                                 style=wx.LC_REPORT|wx.BORDER_SUNKEN)

        self.list_ctrl.InsertColumn(0, 'Item')
        self.list_ctrl.InsertColumn(1, 'Price')
        self.list_ctrl.InsertColumn(2, 'Client')
        self.list_ctrl.InsertColumn(3, 'Location', width=125)

        btn = wx.Button(self.panel, label='import transactions')
        btn.Bind(wx.EVT_BUTTON, self.display_transactions)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.list_ctrl, 0, wx.ALL|wx.EXPAND, 5)
        self.sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
        self.panel.SetSizer(self.sizer)


        self.file_menu = wx.Menu()
        self.file_menu.Append(ID_FILE_OPTIONS, 'options')
        self.file_menu.Append(ID_FILE_QUIT, 'quit')
        self.menu_bar = wx.MenuBar() 
        self.menu_bar.Append(self.file_menu, 'File')
        self.SetMenuBar(self.menu_bar)


        wx.EVT_MENU(self, ID_FILE_OPTIONS,  self.prefs.show)
        wx.EVT_MENU(self, ID_FILE_QUIT, self.gui_exit)




    def gui_exit(self, event):
        exit()


   
    def display_error(self, title='Error', message='Error'):
        m = wx.MessageDialog(None, title, message, wx.OK)
        m.ShowModal()



    def display_transactions(self, event):
        self.transactions = api_singleton.import_transactions()

        if not self.transactions:
            self.display_error('Could not import transactions')


        return False


    def add_line(self, event):
        line = 'line %s' % (self.index)
        self.list_ctrl.InsertStringItem(self.index, line)
        self.list_ctrl.SetStringItem(self.index, 1, 'what')
        self.list_ctrl.SetStringItem(self.index, 2, 'w')
        self.index += 1


    def display_server_status(self):
        server_status = api_singleton.import_server_status()

        if 'onlinePlayers' in server_status:
            self.status_bar.SetStatusText('Online players: %s' % (server_status['onlinePlayers']))

        else:
            self.status_bar.SetStatusText('Could not connect to server')



if __name__ == '__main__':
    api_singleton = eve_api.Eve_API()
    app = wx.App(False)
    frame = GUI()
    frame.Show()
    frame.display_server_status()
    app.MainLoop()

