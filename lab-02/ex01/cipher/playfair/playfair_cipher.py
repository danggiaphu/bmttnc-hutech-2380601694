class PlayfairCipher:
    def __init__(self):
        # Định nghĩa trực tiếp ma trận chữ cái tại đây để CẮT ĐỨT HOÀN TOÀN circular import
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".replace("J", "I")

    def create_playfair_matrix(self, key: str):
        # Tiền xử lý Key: Viết hoa, thay J bằng I, lọc chỉ giữ lại chữ cái chuẩn
        key = key.upper().replace("J", "I")
        clean_key = []
        for letter in key:
            if letter in self.alphabet and letter not in clean_key:
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