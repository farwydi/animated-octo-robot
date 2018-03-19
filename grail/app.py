# -*- coding: utf-8 -*-

import os.path

import wx

from pages import LoginPage, MainFrame
from protocol import GrailProtocol


class MainFrameLogic(MainFrame):

    def __init__(self):
        super().__init__(None)

        self.data_list.AppendTextColumn('ID', width=40)
        self.data_list.AppendTextColumn('artist', width=170)
        self.data_list.AppendTextColumn('title', width=260)
        self.data_list.AppendTextColumn(u'Статус', width=80)

    def add_row(self, e):
        self.data_list.AppendItem(["id", "artist", "title", "genre"])


class LoginPageLogic(LoginPage):
    M_LABEL_NEW = u"Регистрация в сети"
    M_LABEL_LOGIN = u"Авторизация"
    M_LABEL_UNLOCK = u"Для расшифровки введите пароль:"

    M_BTN_REG = u"Регистрация"
    M_BTN_UNLOCK = u"Расшифровать"
    M_BTN_REG_PROC = u"Запрос принят..."

    M_ERROR_FIELD = u"Не все поля заполнены"
    M_ERROR_REG = u"Вы не зарегистрированы"
    M_ERROR_PWD = u"Не верный пароль"

    def __init__(self):
        super().__init__(None)

        self.page = None
        self.page_login()

    def on_reg(self, event):
        if self.page == 1:
            # PAGE CREATE
            self.page_login()
            self.reg_btn.SetLabelText(self.M_BTN_REG)
            pass
        elif self.page == 2:
            # PAGE LOGIN
            self.page_create()
            self.reg_btn.SetLabelText(self.M_LABEL_LOGIN)

    def on_unlock(self, event):
        self.error_text.SetLabelText(wx.EmptyString)
        if self.page == 1:
            # PAGE CREATE
            pswd = self.password_field.GetValue()
            lgn = self.login_field.GetValue()

            if len(pswd) == 0 and len(lgn) == 0:
                self.error_text.SetLabelText(self.M_ERROR_FIELD)
            else:
                # self.lock_btn.Disable()
                # self.password_field.Disable()
                # self.login_field.Disable()
                # self.reg_btn.Disable()
                self.lock_btn.SetLabelText(self.M_BTN_REG_PROC)

                GrailProtocol.create_new_grail(lgn, pswd)

        elif self.page == 2:
            # PAGE LOGIN

            lgn = self.login_field.GetValue()
            pswd = self.password_field.GetValue()

            if len(pswd) == 0 and len(lgn) == 0:
                self.error_text.SetLabelText(self.M_ERROR_FIELD)
            else:
                if os.path.isfile(lgn + '.grail'):
                    try:
                        grail = GrailProtocol.unlock_grail(lgn, pswd)
                        header, body = GrailProtocol.parse_grail(grail)
                        print(header)
                    except ValueError:
                        self.error_text.SetLabelText(self.M_ERROR_PWD)
                else:
                    self.error_text.SetLabelText(self.M_ERROR_REG)

    def passwd_no_eq(self):
        pass
        # self.m_staticText3.SetLabel(u"Неверный пароль")

    def page_create(self):
        self.page = 1

        self.title_text.SetLabelText(self.M_LABEL_NEW)
        self.lock_btn.SetLabelText(self.M_BTN_REG)
        self.login_field.Enable()
        self.password_field.Enable()

        self.Layout()

    def page_login(self):
        self.page = 2

        self.title_text.SetLabelText(self.M_LABEL_LOGIN)
        self.lock_btn.SetLabelText(self.M_BTN_UNLOCK)
        self.login_field.Enable()
        self.password_field.Enable()

        self.Layout()


if __name__ == "__main__":
    app = wx.App()

    # wnd = LoginPageLogic()
    wnd = MainFrameLogic()
    wnd.Show(True)

    app.MainLoop()
