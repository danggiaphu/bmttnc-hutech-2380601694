class RailFenceCipher:
    def __init__(self):
        pass

    def _validate_rails(self, num_rails, text_len: int) -> int:
        """
        Hàm kiểm tra ràng buộc chặt chẽ cho Số hàng rào (num_rails).
        Ngăn chặn vòng lặp vô hạn và các giá trị toán học phi lý.
        """
        # 1. Kiểm tra rỗng
        if num_rails is None or str(num_rails).strip() == "":
            raise ValueError("Lỗi: Số hàng rào không được để trống! Vui lòng nhập lại.")

        # 2. Kiểm tra số âm và ký tự đặc biệt/chữ cái
        rails_str = str(num_rails).strip()
        if rails_str.startswith('-'):
            raise ValueError("Lỗi: Số hàng rào không được là số âm!\n Vui lòng nhập một số nguyên dương từ 2 trở lên.")
            
        if not rails_str.isdigit():
            raise ValueError("Lỗi: Số hàng rào phải là một số nguyên dương thuần túy!\n Vui lòng nhập lại.")

        valid_rails = int(rails_str)

        # 3. Ràng buộc điều kiện tối thiểu để thuật toán zigzag chạy (Bắt buộc phải >= 2)
        if valid_rails < 2:
            raise ValueError(
                f"Lỗi: Số hàng rào nhập vào là {valid_rails}.\n"
                f" Thuật toán mật mã đường ray bắt buộc phải có từ 2 hàng rào trở lên để tạo đường zigzag!"
            )

        # 4. Ràng buộc giới hạn tối đa theo độ dài văn bản (Tùy chọn tối ưu bài làm)
        if text_len > 0 and valid_rails >= text_len:
            raise ValueError(
                f"Lỗi: Số hàng rào ({valid_rails}) không được lớn hơn hoặc bằng độ dài văn bản ({text_len})!\n"
                f" Vui lòng hạ số hàng rào xuống nhỏ hơn độ dài chuỗi cần xử lý."
            )

        return valid_rails

    def rail_fence_encrypt(self, plain_text, num_rails):
        if not plain_text:
            return ""
            
        # ĐỒNG BỘ RÀNG BUỘC: Gọi hàm validate kiểm tra trước khi thực hiện vòng lặp
        clean_rails = self._validate_rails(num_rails, len(plain_text))
        
        rails = [[] for _ in range(clean_rails)]
        rail_index = 0
        direction = 1  # 1: xuống, -1: lên
        
        for char in plain_text:
            rails[rail_index].append(char)
            if rail_index == 0:
                direction = 1
            elif rail_index == clean_rails - 1:
                direction = -1
            rail_index += direction
            
        cipher_text = ''.join(''.join(rail) for rail in rails)
        return cipher_text

    def rail_fence_decrypt(self, cipher_text, num_rails):
        if not cipher_text:
            return ""
            
        # ĐỒNG BỘ RÀNG BUỘC: Gọi hàm validate kiểm tra lúc giải mã
        clean_rails = self._validate_rails(num_rails, len(cipher_text))
        
        rail_lengths = [0] * clean_rails  
        rail_index = 0
        direction = 1
        
        for _ in range(len(cipher_text)):
            rail_lengths[rail_index] += 1
            if rail_index == 0:
                direction = 1
            elif rail_index == clean_rails - 1:
                direction = -1
            rail_index += direction
            
        rails = []
        start = 0
        for length in rail_lengths:
            rails.append(cipher_text[start:start+length])
            start += length
        plain_text = ""
        rail_index = 0
        direction = 1
        
        for _ in range(len(cipher_text)):
            if rails[rail_index]: 
                plain_text += rails[rail_index][0]
                rails[rail_index] = rails[rail_index][1:]
            if rail_index == 0:
                direction = 1
            elif rail_index == clean_rails - 1:
                direction = -1
            rail_index += direction
        return plain_text