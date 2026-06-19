class VigenereCipher:
    def __init__(self):
        pass
    
    def _validate_key(self, key: any) -> str:
        """
        Hàm kiểm tra ràng buộc chặt chẽ cho Khóa (Key) của Vigenere.
        Bắn lỗi nếu key trống hoặc không chứa ký tự chữ cái hợp lệ.
        """
        if key is None:
            raise ValueError("Lỗi: Khóa (Key) không được để trống! Vui lòng nhập lại.")
            
        key_str = str(key).strip()
        if key_str == "":
            raise ValueError("Lỗi: Khóa (Key) không được để trống! Vui lòng nhập lại.")
            
        # Lọc chỉ giữ lại các ký tự chữ cái (A-Z, a-z)
        valid_chars = [char for char in key_str if char.isalpha()]
        
        # Nếu sau khi lọc chuỗi rỗng (ví dụ người dùng nhập toàn số "123" hoặc ký tự đặc biệt "@#$")
        if not valid_chars:
            raise ValueError(
                "Lỗi: Khóa (Key) của Vigenère bắt buộc phải chứa các ký tự chữ cái [A-Z]!\n"
                " Vui lòng nhập lại một chuỗi chữ cái (Ví dụ: KHANHMY, ANTOAN,...)."
            )
            
        return "".join(valid_chars)
    
    def vigenere_encrypt(self, plain_text, key):
        if not plain_text:
            return ""
            
        # ĐỒNG BỘ RÀNG BUỘC: Lọc và kiểm tra khóa trước khi mã hóa
        clean_key = self._validate_key(key)
        
        encrypted_text = ""
        key_index = 0
        for char in plain_text:
            if char.isalpha():
                key_shift = ord(clean_key[key_index % len(clean_key)].upper()) - ord('A')
                if char.isupper():
                    encrypted_text += chr((ord(char) - ord('A') + key_shift) % 26 + ord('A'))
                else:
                    encrypted_text += chr((ord(char) - ord('a') + key_shift) % 26 + ord('a'))
                key_index += 1
            else:
                encrypted_text += char
        return encrypted_text
    
    def vigenere_decrypt(self, encrypt_text, key):
        if not encrypt_text:
            return ""
            
        # ĐỒNG BỘ RÀNG BUỘC: Lọc và kiểm tra khóa trước khi giải mã
        clean_key = self._validate_key(key)
        
        decrypted_text = ""
        key_index = 0
        for char in encrypt_text:
            if char.isalpha():
                key_shift = ord(clean_key[key_index % len(clean_key)].upper()) - ord('A')
                if char.isupper():
                    decrypted_text += chr((ord(char) - ord('A') - key_shift) % 26 + ord('A'))
                else:
                    decrypted_text += chr((ord(char) - ord('a') - key_shift) % 26 + ord('a'))
                key_index += 1
            else:
                decrypted_text += char
        return decrypted_text