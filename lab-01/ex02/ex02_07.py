print("Nhập các dòng văn bản (kết thúc bằng cách nhập 'done'):")
lines = []
while True:
    line = input()
    if line.lower() == 'done':
        break
    lines.append(line)
    
print("\nCác dòng văn bản đã nhập đã được in hoa:")
for line in lines:
    print(line.upper())