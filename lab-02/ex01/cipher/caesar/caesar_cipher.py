# Sửa import tương đối để tránh lỗi ModuleNotFoundError
from . import ALPHABET

class CaesarCipher:
    def __init__(self):
        self.alphabet = ALPHABET
    
    def encrypt_text(self, text: str, key: int) -> str:
        alphabet_len = len(self.alphabet)
        text = text.upper()
        encrypt_text = []
        
        for letter in text:
            # Kiểm tra xem ký tự có nằm trong bảng chữ cái ma pháp không
            if letter in self.alphabet:
                letter_index = self.alphabet.index(letter)
                output_index = (letter_index + key) % alphabet_len
                output_letter = self.alphabet[output_index]
                encrypt_text.append(output_letter)
            else:
                # Nếu là khoảng trắng hoặc ký tự đặc biệt, giữ nguyên không mã hóa
                encrypt_text.append(letter)
                
        return "".join(encrypt_text)
    
    def decrypt_text(self, text: str, key: int) -> str:
        alphabet_len = len(self.alphabet)
        text = text.upper()
        decrypt_text = []
        
        for letter in text:
            # Kiểm tra xem ký tự có nằm trong bảng chữ cái ma pháp không
            if letter in self.alphabet:
                letter_index = self.alphabet.index(letter)
                output_index = (letter_index - key) % alphabet_len
                output_letter = self.alphabet[output_index]
                decrypt_text.append(output_letter)
            else:
                # Giữ nguyên khoảng trắng hoặc ký tự đặc biệt khi giải mã
                decrypt_text.append(letter)
                
        return "".join(decrypt_text)