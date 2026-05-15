def dao_chuoi(chuoi):
    return chuoi[::-1]
input_str = input ("Mời nhập chuỗi cần đảo ngược:")
print(f"Chuỗi sau khi đã đảo ngược: {dao_chuoi(input_str)}")