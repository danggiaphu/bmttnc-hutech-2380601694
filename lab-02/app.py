from flask import Flask, render_template, request, json, jsonify 
import os 
import sys
import subprocess 
from ex01.cipher.caesar import CaesarCipher
from ex01.cipher.railfence import RailFenceCipher
from ex01.cipher.vigenere import VigenereCipher
from ex01.cipher.playfair import PlayfairCipher

# --- ĐỒNG BỘ ĐƯỜNG DẪN THƯ MỤC CHỨA CODE CỦA LAB_05 ---
stego_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lab_05', 'img_hidden'))
if stego_path not in sys.path:
    sys.path.append(stego_path)

# Import chính xác tên hàm thực tế từ file encrypt.py và decrypt.py của Phú
from encrypt import encode_image  
from decrypt import decode_image   
 
app = Flask(__name__)

#=============================================================================================================================
# --- MỤC 0: ĐIỀU HƯỚNG GIAO DIỆN CƠ BẢN ---

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/caesar")
def caesar():
    return render_template('caesar.html')

@app.route("/railfence")
def railfence():
    return render_template('railfence.html')

@app.route("/playfair")
def playfair():
    return render_template('playfair.html')

@app.route("/vigenere")
def vigenere():
    return render_template('vigenere.html')


#=============================================================================================================================
# --- MỤC 1: ROUTE XỬ LÝ CRYPTOGRAPHY (ĐÃ BỔ SUNG BẮT LỖI RÀNG BUỘC CHỮ ĐỎ) ---

# --- CAESAR CIPHER ---
@app.route("/caesar/encrypt", methods=['POST'])
def caesar_encrypt():
    try:
        text = request.form['inputPlainText']
        key = request.form['inputKeyPlain']  # Nhận chuỗi thô để hàm _validate_key tự xử lý
        caesar = CaesarCipher()
        encrypted_text = caesar.encrypt_text(text, key)
        return f"text: {text}<br>/key: {key}<br>/encrypted text: {encrypted_text}"
    except ValueError as error_msg:
        return f"<span style='color: red; font-weight: bold;'>{str(error_msg)}</span>"

@app.route("/caesar/decrypt", methods=['POST'])
def caesar_decrypt():
    try:
        text = request.form['inputCipherText']
        key = request.form['inputKeyCipher']
        caesar = CaesarCipher()
        decrypted_text = caesar.decrypt_text(text, key)
        return f"text: {text}<br>/key: {key}<br>/decrypted text: {decrypted_text}"
    except ValueError as error_msg:
        return f"<span style='color: red; font-weight: bold;'>{str(error_msg)}</span>"


# --- RAILFENCE CIPHER ---
@app.route("/railfence/encrypt", methods=['POST'])
def railfence_encrypt():
    try:
        text = request.form['inputPlainText']
        key = request.form['inputKeyPlain']
        railfence = RailFenceCipher()
        encrypted_text = railfence.rail_fence_encrypt(text, key)
        return f"text: {text}<br>/key: {key}<br>/encrypted text: {encrypted_text}"
    except ValueError as error_msg:
        return f"<span style='color: red; font-weight: bold;'>{str(error_msg)}</span>"

@app.route("/railfence/decrypt", methods=['POST'])
def railfence_decrypt():
    try:
        text = request.form['inputCipherText']
        key = request.form['inputKeyCipher']
        railfence = RailFenceCipher()
        decrypted_text = railfence.rail_fence_decrypt(text, key)
        return f"text: {text}<br>/key: {key}<br>/decrypted text: {decrypted_text}"
    except ValueError as error_msg:
        return f"<span style='color: red; font-weight: bold;'>{str(error_msg)}</span>"


# --- PLAYFAIR CIPHER ---
@app.route('/api/playfair/creatematrix', methods=['POST'])
def playfair_creatematrix():
    try:
        data = request.json  
        key = data.get('key', '') 
        playfair_cipher = PlayfairCipher()
        playfair_matrix = playfair_cipher.create_playfair_matrix(key) 
        return jsonify({"playfair_matrix": playfair_matrix})
    except ValueError as error_msg:
        return jsonify({"success": False, "message": str(error_msg)}), 400

@app.route("/playfair/encrypt", methods=['POST'])
def playfair_encrypt():
    try:
        text = request.form['inputPlainText']
        key = request.form['inputKeyPlain']
        playfair_cipher = PlayfairCipher()
        playfair_matrix = playfair_cipher.create_playfair_matrix(key)
        encrypted_text = playfair_cipher.playfair_encrypt(text, playfair_matrix)
        return f"text: {text}<br>/key: {key}<br>/encrypted text: {encrypted_text}"
    except ValueError as error_msg:
        return f"<span style='color: red; font-weight: bold;'>{str(error_msg)}</span>"

@app.route("/playfair/decrypt", methods=['POST'])
def playfair_decrypt():
    try:
        text = request.form['inputCipherText']
        key = request.form['inputKeyCipher']
        playfair_cipher = PlayfairCipher()
        playfair_matrix = playfair_cipher.create_playfair_matrix(key)
        decrypted_text = playfair_cipher.playfair_decrypt(text, playfair_matrix)
        return f"text: {text}<br>/key: {key}<br>/decrypted text: {decrypted_text}"
    except ValueError as error_msg:
        return f"<span style='color: red; font-weight: bold;'>{str(error_msg)}</span>"


# --- VIGENERE CIPHER ---
@app.route("/vigenere/encrypt", methods=['POST'])
def vigenere_encrypt():
    try:
        text = request.form['inputPlainText']
        key = request.form['inputKeyPlain']
        vigenere = VigenereCipher()
        encrypted_text = vigenere.vigenere_encrypt(text, key)
        return f"text: {text}<br>/key: {key}<br>/encrypted text: {encrypted_text}"
    except ValueError as error_msg:
        return f"<span style='color: red; font-weight: bold;'>{str(error_msg)}</span>"

@app.route("/vigenere/decrypt", methods=['POST'])
def vigenere_decrypt():
    try:
        text = request.form['inputCipherText']
        key = request.form['inputKeyCipher']
        vigenere = VigenereCipher()
        decrypted_text = vigenere.vigenere_decrypt(text, key)
        return f"text: {text}<br>/key: {key}<br>/decrypted text: {decrypted_text}"
    except ValueError as error_msg:
        return f"<span style='color: red; font-weight: bold;'>{str(error_msg)}</span>"


# --- KÍCH HOẠT POPUP DESKTOP PYQT5 ---
@app.route("/open_popup/<cipher_name>")
def open_popup(cipher_name):
    cipher_files = {
        "caesar": "caesar_cipher.py",      
        "railfence": "railfence_cipher.py",
        "playfair": "playfair_cipher.py",
        "vigenere": "vigenere_cipher.py"
    }
    
    filename = cipher_files.get(cipher_name)
    if not filename:
        return jsonify({"success": False, "message": "Thuật toán không hợp lệ"}), 400
        
    try:
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lab-03', filename))
        if not os.path.exists(script_path):
            return jsonify({"success": False, "message": f"Không tìm thấy file tại đường dẫn: {script_path}"}), 404
            
        subprocess.Popen(['python', script_path], shell=True)
        return jsonify({"success": True, "message": f"Đã mở popup {cipher_name}"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


#=============================================================================================================================
# --- MỤC 2: CÁC ROUTE XỬ LÝ GIẤU TIN VÀ GIẢI MÃ STEGANOGRAPHY ---

@app.route("/api/stego/encrypt", methods=['POST'])
def api_stego_encrypt():
    try:
        if 'image' not in request.files:
            return jsonify({"success": False, "message": "Không tìm thấy file ảnh gửi lên"}), 400
            
        file = request.files['image']
        secret_message = request.form.get('message', '')
        
        if file.filename == '':
            return jsonify({"success": False, "message": "Tên file ảnh trống"}), 400

        current_dir = os.path.dirname(os.path.abspath(__file__))
        upload_folder = os.path.abspath(os.path.join(current_dir, '..', 'lab_05', 'img_hidden'))
        
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        input_image_path = os.path.join(upload_folder, file.filename)
        output_image_path = os.path.join(upload_folder, "encoded_image.png")
        
        # Đọc ghi luồng an toàn bằng ngữ cảnh 'with' giải phóng file ngay sau khi ghi xong bytes thô
        file.seek(0)
        with open(input_image_path, 'wb') as f:
            f.write(file.read())
            f.flush()
            os.fsync(f.fileno())

        # ĐẢM BẢO CHẮC CHẮN: Xóa file kết quả cũ nếu có để tránh lỗi quyền ghi đè (PermissionError)
        if os.path.exists('encoded_image.png'):
            try: os.remove('encoded_image.png')
            except: pass
        if os.path.exists(output_image_path):
            try: os.remove(output_image_path)
            except: pass

        # Thực thi hàm giấu tin mã hóa gốc của Phú từ encrypt.py
        encode_image(input_image_path, secret_message)

        # Di chuyển tệp kết quả từ thư mục thực thi gốc (lab-02) về đúng lab_05/img_hidden
        if os.path.exists('encoded_image.png'):
            os.replace('encoded_image.png', output_image_path)

        return jsonify({
            "success": True, 
            "message": "Ảnh kết quả chứa mã ẩn đã được lưu tại thư mục lab_05/img_hidden với tên 'encoded_image.png'"
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"Lỗi phía Server: {str(e)}"}), 500


@app.route("/api/stego/decrypt", methods=['POST'])
def api_stego_decrypt():
    try:
        if 'image' not in request.files:
            return jsonify({"success": False, "message": "Không tìm thấy file ảnh giải mã"}), 400
            
        file = request.files['image']
        if file.filename == '':
            return jsonify({"success": False, "message": "Tên file ảnh trống"}), 400

        current_dir = os.path.dirname(os.path.abspath(__file__))
        upload_folder = os.path.abspath(os.path.join(current_dir, '..', 'lab_05', 'img_hidden'))
        
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            
        decrypt_image_path = os.path.join(upload_folder, "temp_to_decrypt.png")
        
        # Ghi luồng dữ liệu giải mã an toàn
        file.seek(0)
        with open(decrypt_image_path, 'wb') as f:
            f.write(file.read())
            f.flush()
            os.fsync(f.fileno())

        # Giải mã chuỗi nhị phân đồng bộ dùng cấu trúc ngữ cảnh mở ảnh (with) độc lập của Pillow
        # Việc bọc trong 'with' giúp Pillow giải phóng và un-lock file ngay lập tức, sửa triệt để lỗi identify
        from PIL import Image
        binary_message = ""
        with Image.open(decrypt_image_path) as img:
            width, height = img.size
            for row in range(height):
                for col in range(width):
                    pixel = img.getpixel((col, row))
                    for color_channel in range(3):
                        binary_message += format(pixel[color_channel], '08b')[-1]

        #end_marker = '1111111111111110'
        #if end_marker in binary_message:
        #   binary_message = binary_message.split(end_marker)[0]

        decrypted_text = ""
        for i in range(0, len(binary_message), 8):
            if i + 8 <= len(binary_message):
                decrypted_text += chr(int(binary_message[i:i+8], 2))

        # Giải phóng đĩa cứng bằng cách xóa file tạm thời
        if os.path.exists(decrypt_image_path):
            try: os.remove(decrypt_image_path)
            except: pass

        return jsonify({
            "success": True,
            "decrypted_text": decrypted_text if decrypted_text.strip() else "Không tìm thấy tin nhắn ẩn nào hoặc ảnh không đúng định dạng!"
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"Lỗi giải mã phía Server: {str(e)}"}), 500
    
# --- KHỞI ĐỘNG SERVER ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)