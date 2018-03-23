# -*- coding: utf-8 -*-

import wx

from grail import Grail
from pages import LoginPage, MainFrame
from protocol import GrailProtocol, GrailException


class MainFrameLogic(MainFrame):

    def __init__(self, login, password):
        super().__init__(None)

        # self.m_notebook1.SetBackgroundColour(wx.NullColour)

        self.grail = Grail()
        self.grail.open(login, password)

        self._change_counter = 0
        self._push_counter = 0

        self.grail_text_ctrl.SetLabelText(self.grail.get())
        self.commit_btn.Disable()
        self.push_btn.Disable()

        self.data_list.InsertColumn(0, 'ID')
        self.data_list.InsertColumn(1, 'Hash', width=300)

        self.push_row(self.grail.get_header_hash())

        for chain in self.grail.get_hash_list():
            self.push_row(chain)

        self.grail_text_ctrl.SetValue(self.grail.get())

        self._selected = 0
        try:
            self.diff_text.SetLabel(self.grail.get_diff(self._selected))
        except ValueError:
            pass

    def grail_update(self, e):
        diff = e.GetString()
        self._change_counter = 0

        match = len(self.grail.get()) >= len(diff)

        max_diff = self.grail.get() if match else diff
        watch_diff = diff if match else self.grail.get()

        for i, litter in enumerate(max_diff):
            try:
                if watch_diff[i] != litter:
                    self._change_counter += 1
            except IndexError:
                self._change_counter += 1

        if self._change_counter > 0:
            self.commit_btn.Enable()
        else:
            self.commit_btn.Disable()

        self.commit_btn.SetLabelText(f"Commit ({self._change_counter})")

    def selected(self, event):
        self._selected = int(self.data_list.GetItemText(event.Index))

        self.grail_text_ctrl.SetValue(self.grail.get(self._selected + 1))
        self.diff_text.SetLabel(self.grail.get_diff(self._selected))

    def commit(self, event):
        try:
            self.grail.update(self.grail_text_ctrl.GetValue())

            chain = self.grail.get_last_hash()

            id = self.push_row(chain)

            self.status_bar.SetStatusText(f'Запись #{id} добавлена, ожидается подтверждение клиентом.')

            self.commit_btn.Disable()
            self.commit_btn.SetLabelText("Commit (0)")

            self._push_counter += 1
            self.push_btn.Enable()
            self.push_btn.SetLabelText(f"Push ({self._push_counter})")
        except GrailException as gp:
            self.status_bar.SetStatusText(str(gp))

    def push(self, event):
        self.grail.save()

        self._push_counter = 0
        self.push_btn.Disable()
        self.push_btn.SetLabelText("Push (0)")

    def push_row(self, item):
        index = self.data_list.GetItemCount()
        index = self.data_list.InsertItem(self.data_list.GetItemCount(), str(index))
        self.data_list.SetItem(index, 1, item.hex())

        return index


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

        self.__protocol = GrailProtocol()

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
        self.status_bar.SetStatusText(wx.EmptyString)
        if self.page == 1:
            # PAGE CREATE
            password = self.password_field.GetValue()
            login = self.login_field.GetValue()

            if len(password) == 0 or len(login) == 0:
                self.status_bar.SetStatusText(self.M_ERROR_FIELD)
            else:
                form = MainFrameLogic(login, password)
                form.Show()

                self.Close()

        elif self.page == 2:
            # PAGE LOGIN

            login = self.login_field.GetValue()
            password = self.password_field.GetValue()

            if len(password) == 0 and len(login) == 0:
                self.status_bar.SetStatusText(self.M_ERROR_FIELD)
            else:
                if not self.__protocol.check(login, password):
                    self.status_bar.SetStatusText(self.M_ERROR_PWD)
                else:
                    form = MainFrameLogic(login, password)
                    form.Show()

                    self.Close()

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

    wnd = LoginPageLogic()
    wnd.Show()

    app.MainLoop()
