def reverse (lst):
    return lst[::-1]
input_list = input("Nhập danh sách các số (cách nhau bằng dấu ','):")
numbers = list(map(int, input_list.split(',')))

reversed_list = reverse(numbers)
print("Danh sách sau khi đảo ngược là:",reversed_list)


