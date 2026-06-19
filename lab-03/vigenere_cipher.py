import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

import requests

from ui.vigenere import Ui_MainWindow



class VigenereApp(QMainWindow):

    def __init__(self):

        super().__init__()

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

       

        # Kết nối nút bấm

        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)

        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)



    def call_api_encrypt(self):

        url = "http://127.0.0.1:5000/api/vigenere/encrypt"

        payload = {

            "plain_text": self.ui.txt_plain_text.toPlainText(),

            "key": self.ui.txt_key.toPlainText()

        }

        try:

            response = requests.post(url, json=payload)

            if response.status_code == 200:

                data = response.json()

                self.ui.txt_cipher.setPlainText(data["encrypted_message"])

               

                msg = QMessageBox()

                msg.setIcon(QMessageBox.Information)

                msg.setText("Encrypted Successfully")

                msg.exec_()

            else:

                print(f"Error while calling API: {response.status_code}")

        except requests.exceptions.RequestException as e:

            print(f"Error: {e}")



    def call_api_decrypt(self):

        url = "http://127.0.0.1:5000/api/vigenere/decrypt"

        payload = {

            "cipher_text": self.ui.txt_cipher.toPlainText(),

            "key": self.ui.txt_key.toPlainText()

        }

        try:

            response = requests.post(url, json=payload)

            if response.status_code == 200:

                data = response.json()

                self.ui.txt_plain_text.setPlainText(data["decrypted_message"])

               

                msg = QMessageBox()

                msg.setIcon(QMessageBox.Information)

                msg.setText("Decrypted Successfully")

                msg.exec_()

            else:

                print(f"Error while calling API: {response.status_code}")

        except requests.exceptions.RequestException as e:

            print(f"Error: {e}")



if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = VigenereApp()
    window.show()
    sys.exit(app.exec_()) 

