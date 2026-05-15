def tinh_tong_chan (lst):
    tong = 0
    for i in lst:
        if i % 2 == 0:
            tong += i
    return tong

input_list = input ("Nhập danh sách các số (cách nhau bằng dấu ','):")
numbers = list(map(int, input_list.split(',')))

tong = tinh_tong_chan(numbers)
print(f"Tổng các số chẵn trong danh sách là: {tong}")