import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import requests
from ui.railfence import Ui_MainWindow 

class RailFenceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Kết nối nút bấm
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        # ĐỒNG BỘ PORT: Chuyển sang 5050
        url = "http://127.0.0.1:5050/railfence/encrypt"
        
        # ĐỒNG BỘ THAM SỐ VÀ SỬ DỤNG DATA= (FORM DATA)
        # spb_rails.value() lấy giá trị số nguyên từ ô SpinBox giao diện của Phú
        payload = {
            "inputPlainText": self.ui.txt_plain_text.toPlainText(),
            "inputKeyPlain": str(self.ui.spb_rails.value())
        }
        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                raw_response = response.text
                
                # BẮT LỖI RÀNG BUỘC TỪ BACKEND FLASK: Nếu phát hiện chuỗi lỗi chữ đỏ HTML
                if "color: red" in raw_response:
                    clean_error = raw_response.replace("<span style='color: red; font-weight: bold;'>", "").replace("</span>", "").replace("<br>", "\n")
                    self.show_error_message(clean_error)
                    return

                # Tách chuỗi lấy bản mã sạch đổ vào giao diện
                if "/encrypted text: " in raw_response:
                    encrypted_text = raw_response.split("/encrypted text: ")[1].strip()
                    self.ui.txt_cipher.setPlainText(encrypted_text)
                else:
                    self.ui.txt_cipher.setPlainText(raw_response)
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Thông báo")
                msg.setText("Encrypted Successfully")
                msg.exec_()
            else:
                QMessageBox.critical(self, "Lỗi hệ thống", f"API trả về mã lỗi: {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi kết nối", f"Không thể kết nối đến Server:\n{str(e)}")

    def call_api_decrypt(self):
        # ĐỒNG BỘ PORT: Chuyển sang 5050
        url = "http://127.0.0.1:5050/railfence/decrypt"
        
        payload = {
            "inputCipherText": self.ui.txt_cipher.toPlainText(),
            "inputKeyCipher": str(self.ui.spb_rails.value())
        }
        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                raw_response = response.text
                
                # BẮT LỖI RÀNG BUỘC KHI GIẢI MÃ
                if "color: red" in raw_response:
                    clean_error = raw_response.replace("<span style='color: red; font-weight: bold;'>", "").replace("</span>", "").replace("<br>", "\n")
                    self.show_error_message(clean_error)
                    return

                if "/decrypted text: " in raw_response:
                    decrypted_text = raw_response.split("/decrypted text: ")[1].strip()
                    self.ui.txt_plain_text.setPlainText(decrypted_text)
                else:
                    self.ui.txt_plain_text.setPlainText(raw_response)
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Thông báo")
                msg.setText("Decrypted Successfully")
                msg.exec_()
            else:
                QMessageBox.critical(self, "Lỗi hệ thống", f"API trả về mã lỗi: {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi kết nối", f"Không thể kết nối đến Server:\n{str(e)}")

    # --- Hàm hiển thị hộp thoại cảnh báo lỗi dữ liệu độc lập ---
    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Lỗi Ràng Buộc Dữ Liệu")
        msg.setText(message)
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RailFenceApp()
    window.show()
    sys.exit(app.exec_())