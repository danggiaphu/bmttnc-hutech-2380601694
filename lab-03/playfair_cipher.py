import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt
from ui.playfair import Ui_MainWindow 
import requests

class PlayfairApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Kết nối sự kiện click của nút bấm với hàm xử lý
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_get_matrix(self):
        """Hàm phụ trợ gọi API lấy ma trận về để hiển thị lên bảng"""
        key = self.ui.txt_key.toPlainText().strip()
        if not key:
            self.ui.table_playfair.clearContents()
            return False # Trả về False nếu không có key
            
        url = "http://127.0.0.1:5050/api/playfair/creatematrix"
        payload = {"key": key}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if "playfair_matrix" in data:
                    self.display_matrix(data["playfair_matrix"])
                    return True
            else:
                # Bắt thông báo lỗi ràng buộc trả về từ Flask Server (lỗi 400)
                error_data = response.json()
                error_msg = error_data.get("message", "Khóa không hợp lệ!")
                self.show_error_message(error_msg)
                self.ui.table_playfair.clearContents() # Xóa bảng cũ nếu key lỗi
                return False
        except Exception as e:
            print(f"Lỗi nạp ma trận: {e}")
            return False

    def call_api_encrypt(self):
        # 1. KIỂM TRA RÀNG BUỘC MA TRẬN TRƯỚC
        # Nếu lấy ma trận thất bại (Key sai), dừng tiến trình mã hóa ngay lập tức
        if not self.call_api_get_matrix():
            return

        url = "http://127.0.0.1:5050/playfair/encrypt"
        payload = {
            "inputPlainText": self.ui.txt_plain_text.toPlainText(),
            "inputKeyPlain": self.ui.txt_key.toPlainText()
        }
        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                raw_response = response.text
                
                # Kiểm tra nếu Flask trả về một chuỗi lỗi HTML chữ đỏ (do bộ lọc try-except bên app.py)
                if "color: red" in raw_response:
                    # Trích xuất đoạn text lỗi thô để hiển thị lên hộp thoại Desktop
                    clean_error = raw_response.replace("<span style='color: red; font-weight: bold;'>", "").replace("</span>", "").replace("<br>", "\n")
                    self.show_error_message(clean_error)
                    return

                if "/encrypted text: " in raw_response:
                    encrypted_text = raw_response.split("/encrypted text: ")[1].strip()
                    self.ui.txt_cipher.setPlainText(encrypted_text)
                else:
                    self.ui.txt_cipher.setPlainText(raw_response)
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def call_api_decrypt(self):
        # 1. KIỂM TRA RÀNG BUỘC MA TRẬN TRƯỚC
        if not self.call_api_get_matrix():
            return

        url = "http://127.0.0.1:5050/playfair/decrypt"
        payload = {
            "inputCipherText": self.ui.txt_cipher.toPlainText(),
            "inputKeyCipher": self.ui.txt_key.toPlainText()
        }
        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                raw_response = response.text
                
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
                msg.setText("Decrypted Successfully")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    # --- Hàm hiển thị hộp thoại báo lỗi cảnh báo dữ liệu ---
    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Lỗi Ràng Buộc Dữ Liệu")
        msg.setText(message)
        msg.exec_()

    # --- Hàm hỗ trợ hiển thị ma trận khóa 5x5 lên giao diện ---
    def display_matrix(self, matrix):
        for row in range(5):
            for col in range(5):
                item = QTableWidgetItem(str(matrix[row][col]))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.table_playfair.setItem(row, col, item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlayfairApp()
    window.show()
    sys.exit(app.exec_())