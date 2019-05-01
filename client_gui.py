
import wx

APP = wx.App()


class MovieFrame(wx.Frame):
    def __init__(self):

        style = wx.DEFAULT_FRAME_STYLE & (~wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self, None, -1, "BenFlix", size=(1280, 720), style=style)

        self.panel = wx.Panel(self)

        movie_screen_background_path = "graphics\\movie_screen.png"
        movie_screen_background = wx.Image(movie_screen_background_path, wx.BITMAP_TYPE_ANY)
        image_ctrl = wx.StaticBitmap(self.panel, bitmap=wx.BitmapFromImage(movie_screen_background))

        self.Show()

        APP.MainLoop()


class MainFrame(wx.Frame):
    def __init__(self, client_socket):

        style = wx.DEFAULT_FRAME_STYLE & (~wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self, None, -1, "BenFlix", size=(1280, 720), style=style)

        self.panel = wx.Panel(self)

        movie_button = wx.Button(self.panel, pos=(50, 150), size=(150, 210)) # movie poster size (150, 170)
        self.Bind(wx.EVT_BUTTON, self.moviebutton, movie_button)
        movie_button.SetBitmap(wx.Bitmap("graphics\\avengers_poster.jpg"))

        main_screen_background_path = "graphics\\main_screen.png"
        main_screen_background = wx.Image(main_screen_background_path, wx.BITMAP_TYPE_ANY)
        image_ctrl = wx.StaticBitmap(self.panel, bitmap=wx.BitmapFromImage(main_screen_background))

        self.client_socket = client_socket

        self.Show()

        APP.MainLoop()

    def moviebutton(self, event):

        self.client_socket.send("PLAY")

        #MovieFrame()


class RegisterFrame(wx.Frame):
    def __init__(self, client_socket, error_message):

        style = wx.DEFAULT_FRAME_STYLE & (~wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self, None, -1, "BenFlix", size=(480, 720), style=style)

        panel = wx.Panel(self)

        confirm_button = wx.Button(panel, label="CONFIRM", pos=(37, 503), size=(228, 40))
        self.Bind(wx.EVT_BUTTON, self.confirmbutton, confirm_button)

        self.full_name_txt_box = wx.TextCtrl(panel, -1, size=(377, 27), pos=(39, 216))
        self.new_username_txt_box = wx.TextCtrl(panel, -1, size=(377, 27), pos=(38, 287))
        self.new_password_txt_box = wx.TextCtrl(panel, -1, size=(377, 27), pos=(39, 365))
        self.acpt_password_txt_box = wx.TextCtrl(panel, -1, size=(377, 27), pos=(38, 443))

        register_background_path = "graphics\\register_screen.png"  # image loading
        register_background = wx.Image(register_background_path, wx.BITMAP_TYPE_ANY)
        image_ctrl = wx.StaticBitmap(panel, bitmap=wx.BitmapFromImage(register_background))

        self.client_socket = client_socket

        self.Show()

        if error_message:
            box = wx.MessageDialog(None, error_message, "Error")
            box.ShowModal()

        APP.MainLoop()

    def confirmbutton(self, event):

        header = "REGISTER {} {} {} {}".format(self.full_name_txt_box.GetValue(), self.new_username_txt_box.GetValue(),
                                            self.new_password_txt_box.GetValue(), self.acpt_password_txt_box.GetValue())

        self.client_socket.send(header)

        self.Destroy()

        #   MainFrame()


class LoginFrame(wx.Frame):

    def __init__(self, client_socket, error_message):

        style = wx.DEFAULT_FRAME_STYLE & (~wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self, None, -1, "BenFlix", size=(480, 720), style=style)

        panel = wx.Panel(self)

        login_button = wx.Button(panel, label="LOGIN", pos=(140, 426), size=(200, 50))
        self.Bind(wx.EVT_BUTTON, self.loginbutton, login_button)

        register_button = wx.Button(panel, label="REGISTER", pos=(128, 558), size=(223, 56))
        self.Bind(wx.EVT_BUTTON, self.registerbutton, register_button)

        self.username_txt_box = wx.TextCtrl(panel, -1, size=(377, 27), pos=(33, 244))
        self.password_txt_box = wx.TextCtrl(panel, -1, size=(377, 27), pos=(33, 351))

        self.username = ""
        self.password = ""

        login_background_path = "graphics\\login_screen.png"  # image loading
        login_background = wx.Image(login_background_path, wx.BITMAP_TYPE_ANY)
        image_ctrl = wx.StaticBitmap(panel, bitmap=wx.BitmapFromImage(login_background))

        self.client_socket = client_socket

        self.Show()

        if error_message:
            box = wx.MessageDialog(None, error_message, "Error")
            box.ShowModal()

        APP.MainLoop()

    def loginbutton(self, event):

        self.username = self.username_txt_box.GetValue()
        self.password = self.password_txt_box.GetValue()

        self.client_socket.send("LOGIN {} {}".format(self.username, self.password))

        self.Destroy()

        #   MainFrame()

    def registerbutton(self, event):

        self.client_socket.send("REGISTER 0")

        self.Destroy()

        #   RegisterFrame()


def main():

    """
    app = wx.App()
    MainFrame()
    app.MainLoop()
    """

if __name__ == '__main__':
    main()




