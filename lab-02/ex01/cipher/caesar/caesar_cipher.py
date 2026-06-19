# Sửa import tương đối để tránh lỗi ModuleNotFoundError
from . import ALPHABET

class CaesarCipher:
    def __init__(self):
        self.alphabet = ALPHABET
    
    def _validate_key(self, key) -> int:
        """
        Hàm kiểm tra ràng buộc chặt chẽ cho Khóa (Key).
        Nếu lỗi sẽ bắn ra thông báo yêu cầu nhập lại kèm khoảng số hợp lệ.
        """
        alphabet_len = len(self.alphabet)
        
        # 1. Kiểm tra xem key có bị trống không
        if key is None or str(key).strip() == "":
            raise ValueError("Khóa (Key) không được để trống! Vui lòng nhập lại.")
            
        # 2. Kiểm tra nếu key chứa dấu trừ (số âm) hoặc không phải là số thuần túy
        key_str = str(key).strip()
        if key_str.startswith('-'):
            raise ValueError(
                f"Lỗi: Khóa (Key) không được là số âm!\n"
                f"👉 Vui lòng nhập lại một số nguyên dương trong khoảng từ [0 đến {alphabet_len - 1}]."
            )
            
        if not key_str.isdigit():
            raise ValueError(
                f"Lỗi: Khóa (Key) phải là một số nguyên dương thuần túy!\n"
                f"👉 Vui lòng nhập lại một số trong khoảng từ [0 đến {alphabet_len - 1}]."
            )
            
        # 3. Ép kiểu về số nguyên
        valid_key = int(key_str)
        
        # 4. Kiểm tra khoảng số hợp lệ (từ 0 đến độ dài bảng chữ cái - 1)
        if valid_key >= alphabet_len:
            raise ValueError(
                f"Lỗi: Khóa ({valid_key}) vượt quá giới hạn dịch chuyển tối đa!\n"
                f" Vui lòng nhập lại một số nằm trong khoảng cho phép từ [0 đến {alphabet_len - 1}]."
            )
            
        return valid_key
    
    def encrypt_text(self, text: str, key: any) -> str:
        alphabet_len = len(self.alphabet)
        text = text.upper()
        encrypt_text = []
        
        # Hàm validate sẽ tự động bắn lỗi lên Flask nếu key không đạt yêu cầu
        clean_key = self._validate_key(key)
        
        for letter in text:
            if letter in self.alphabet:
                letter_index = self.alphabet.index(letter)
                output_index = (letter_index + clean_key) % alphabet_len
                output_letter = self.alphabet[output_index]
                encrypt_text.append(output_letter)
            else:
                encrypt_text.append(letter)
                
        return "".join(encrypt_text)
    
    def decrypt_text(self, text: str, key: any) -> str:
        alphabet_len = len(self.alphabet)
        text = text.upper()
        decrypt_text = []
        
        clean_key = self._validate_key(key)
        
        for letter in text:
            if letter in self.alphabet:
                letter_index = self.alphabet.index(letter)
                output_index = (letter_index - clean_key) % alphabet_len
                output_letter = self.alphabet[output_index]
                decrypt_text.append(output_letter)
            else:
                decrypt_text.append(letter)
                
        return "".join(decrypt_text)