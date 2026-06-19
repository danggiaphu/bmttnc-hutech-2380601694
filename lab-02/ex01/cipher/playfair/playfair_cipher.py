class PlayfairCipher:
    def __init__(self):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".replace("J", "I")

    def _validate_key(self, key: any) -> str:
        """
        Hàm kiểm tra ràng buộc chặt chẽ cho Khóa (Key) của Playfair.
        Bắn lỗi nếu key trống hoặc không chứa chữ cái hợp lệ.
        """
        if key is None:
            raise ValueError("Lỗi: Khóa (Key) không được để trống! Vui lòng nhập lại.")
            
        # Chuyển về chuỗi ký tự chữ, viết hoa và loại bỏ khoảng trắng thừa
        key_str = str(key).upper().strip().replace("J", "I")
        
        if key_str == "":
            raise ValueError("Lỗi: Khóa (Key) không được để trống! Vui lòng nhập lại.")
            
        # Lọc lấy danh sách các ký tự chữ cái hợp lệ nằm trong bảng chữ cái (A-Z)
        valid_chars = [letter for letter in key_str if letter in self.alphabet]
        
        # Nếu sau khi lọc mà chuỗi bị rỗng (ví dụ người dùng nhập toàn số "123" hoặc ký tự đặc biệt "@#$")
        if not valid_chars:
            raise ValueError(
                "Lỗi: Khóa (Key) của Playfair bắt buộc phải chứa các ký tự chữ cái [A-Z]!\n"
                " Vui lòng nhập lại (Ví dụ: HUTECH, BAOMAT,...)."
            )
            
        return "".join(valid_chars)

    def create_playfair_matrix(self, key: str):
        # ĐỒNG BỘ RÀNG BUỘC: Gọi hàm validate trước khi xử lý tạo ma trận
        clean_key_str = self._validate_key(key)
        
        clean_key = []
        for letter in clean_key_str:
            if letter not in clean_key:
                clean_key.append(letter)

        # Điền các ký tự còn lại trong alphabet vào ma trận
        matrix_flat = list(clean_key)
        for letter in self.alphabet:
            if letter not in matrix_flat:
                matrix_flat.append(letter)
            if len(matrix_flat) == 25:
                break

        # Cấu trúc lại thành ma trận 5x5
        return [matrix_flat[i:i+5] for i in range(0, 25, 5)]

    def find_letter_coords(self, matrix, letter):
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == letter:
                    return row, col
        return None, None

    def playfair_encrypt(self, plain_text: str, matrix) -> str:
        plain_text = plain_text.upper().replace("J", "I")
        clean_text = "".join([l for l in plain_text if l in self.alphabet])
        
        if not clean_text:
            return ""

        prepared_text = ""
        i = 0
        while i < len(clean_text):
            letter1 = clean_text[i]
            if i + 1 < len(clean_text):
                letter2 = clean_text[i+1]
                if letter1 == letter2:
                    prepared_text += letter1 + "X"
                    i += 1
                else:
                    prepared_text += letter1 + letter2
                    i += 2
            else:
                prepared_text += letter1 + "X"
                i += 1

        encrypted_text = ""
        for i in range(0, len(prepared_text), 2):
            pair = prepared_text[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]

        return encrypted_text

    def playfair_decrypt(self, cipher_text: str, matrix) -> str:
        cipher_text = cipher_text.upper().replace("J", "I")
        clean_cipher = "".join([l for l in cipher_text if l in self.alphabet])

        if not clean_cipher or len(clean_cipher) % 2 != 0:
            return clean_cipher

        decrypted_text = ""
        for i in range(0, len(clean_cipher), 2):
            pair = clean_cipher[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2] + matrix[row2][col1]

        banro = ""
        length = len(decrypted_text)
        i = 0
        while i < length:
            if i + 2 < length and decrypted_text[i+1] == "X" and decrypted_text[i] == decrypted_text[i+2]:
                banro += decrypted_text[i]
                i += 2
            else:
                banro += decrypted_text[i]
                i += 1
                
        if banro.endswith("X"):
            banro = banro[:-1]

        return banro