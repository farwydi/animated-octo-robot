# -*- coding: utf-8 -*-
import asyncio
import base64

import wx
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from create_grail import CreateGrail
from login_page import LoginPage

VERSION_GRAIL = 1
HASH_ALGORITHM = 'SHA1'


async def unlock_grail(grail_bin, psswd):
    print("sleeping now")

    await asyncio.sleep(2)

    print('is finished')


class CreateGrailLogic(CreateGrail):

    def create(self, event):
        with open('grail.bin', 'wb') as grail:
            header = f"GRAIL VERSION;{VERSION_GRAIL}\r\nHASH ALGORITHM;{HASH_ALGORITHM}\r\n\r\n"

            header += "asdadas"

            msg_text = 'test some plain text here'.rjust(32)
            secret_key = '1234567890123456'  # create new & store somewhere safe

            # key = get_random_bytes(16)
            cipher = AES.new(secret_key, AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(data)

            file_out = open("encrypted.bin", "wb")
            [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]

            print(decoded.strip())

    def close(self, event):
        self.Destroy()


class LoginPageLogic(LoginPage):

    def on_unlock(self, event):
        self.m_textCtrl2.Disable()
        self.m_button2.Disable()
        self.m_button2.SetLabelText(u"Расшифровка...")

        pswd = self.m_textCtrl2.GetValue()

    def passwd_no_eq(self):
        self.m_staticText3.SetLabel(u"Неверный пароль")


async def app_runner():
    print('running...')

    ung = unlock_grail(None, None)

    print('skied...')

    wnd = LoginPageLogic(None)
    wnd.Show(True)

    await ung


if __name__ == "__main__":
    app = wx.App()

    try:
        with open('grail.bin', 'rb') as grail:
            g = grail.read()

            loop = asyncio.get_event_loop()
            loop.run_until_complete(app_runner())
            loop.close()
    except FileNotFoundError:
        print("file not find")
        dcg = CreateGrailLogic(None)
        #dcg.Show()
        wnd = LoginPageLogic(None)
        wnd.Show(True)

    app.MainLoop()
