import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import requests

# 1. ĐỒNG BỘ: Thay đổi sang import class Ui_MainWindow theo cấu trúc file XML mới
from ui.caesar import Ui_MainWindow

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # 2. ĐỒNG BỘ: Khởi tạo đúng class Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Kết nối sự kiện nút bấm
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5050/caesar/encrypt"
        
        # plainTextEdit_2 chính là ô nhập Key trong giao diện của bạn
        key_raw = self.ui.plainTextEdit_2.toPlainText().strip()

        # plainTextEdit chính là ô nhập Plain Text
        payload = {
            "inputPlainText": self.ui.plainTextEdit.toPlainText(),
            "inputKeyPlain": key_raw
        }
        try:
            response = requests.post(url, data=payload)
            
            if response.status_code == 200:
                raw_response = response.text
                
                # BẮT LỖI RÀNG BUỘC BACKEND: Nếu Flask trả về mã lỗi HTML chữ đỏ từ bộ lọc ValueError
                if "color: red" in raw_response:
                    # Trích xuất và làm sạch chuỗi HTML thành dạng chữ thô để đưa vào MessageBox
                    clean_error = raw_response.replace("<span style='color: red; font-weight: bold;'>", "").replace("</span>", "").replace("<br>", "\n")
                    QMessageBox.warning(self, "Lỗi Ràng Buộc Dữ Liệu", clean_error)
                    return

                if "/encrypted text: " in raw_response:
                    encrypted_text = raw_response.split("/encrypted text: ")[1].strip()
                    # plainTextEdit_3 là ô Cipher Text
                    self.ui.plainTextEdit_3.setPlainText(encrypted_text)
                else:
                    self.ui.plainTextEdit_3.setPlainText(raw_response)
                    
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Thông báo")
                msg.setText("Encrypted Successfully")
                msg.exec_()
            else:
                QMessageBox.critical(self, "Lỗi hệ thống", f"API trả về mã lỗi: {response.status_code}")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi kết nối", f"Không thể kết nối API:\n{str(e)}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5050/caesar/decrypt"
        
        # plainTextEdit_2 chính là ô nhập Key
        key_raw = self.ui.plainTextEdit_2.toPlainText().strip()

        # plainTextEdit_3 chính là ô chứa Cipher Text để giải mã
        payload = {
            "inputCipherText": self.ui.plainTextEdit_3.toPlainText(),
            "inputKeyCipher": key_raw
        }
        try:
            response = requests.post(url, data=payload)

            if response.status_code == 200:
                raw_response = response.text
                
                # BẮT LỖI RÀNG BUỘC BACKENDkhi giải mã
                if "color: red" in raw_response:
                    clean_error = raw_response.replace("<span style='color: red; font-weight: bold;'>", "").replace("</span>", "").replace("<br>", "\n")
                    QMessageBox.warning(self, "Lỗi Ràng Buộc Dữ Liệu", clean_error)
                    return

                if "/decrypted text: " in raw_response:
                    decrypted_text = raw_response.split("/decrypted text: ")[1].strip()
                    # Trả kết quả giải mã về lại ô plainTextEdit
                    self.ui.plainTextEdit.setPlainText(decrypted_text)
                else:
                    self.ui.plainTextEdit.setPlainText(raw_response)
                    
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Thông báo")
                msg.setText("Decrypted Successfully")
                msg.exec_()
            else:
                QMessageBox.critical(self, "Lỗi hệ thống", f"API trả về mã lỗi: {response.status_code}")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi kết nối", f"Không thể kết nối API:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())