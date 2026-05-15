from QuanLySinhVien import QuanLySinhVien
qlsv = QuanLySinhVien()
while True:
    print("\nMenu:")
    print("1. Thêm sinh viên")
    print("2. Cập nhật thông tin sinh viên")
    print("3. Xóa sinh viên theo ID")
    print("4. Tim kiếm sinh viên theo tên")
    print("5. Sắp xếp sinh viên theo điểmTB")
    print("6. Sắp xếp sinh viên theo tên chuyên ngành")
    print("7. Hiển thị danh sách sinh viên")
    print("0. Thoát")
    
    key = int(input("Nhập tuỳ chọn:"))
    if(key ==1):
        print("\n1: thêm sinh viên")
        qlsv.nhap_sv()
        print("Thêm thành công")
        
    elif(key == 2):
        if(qlsv.so_luong_sv() > 0):
            print("\n2: Cập nhật thông tin sinh viên")
            print("Nhập ID")
            ID = int(input())
            qlsv.updatesv(ID)
        else:
            print("\nDanh sách sinh viên trống!")
            
    elif(key == 3):
        if(qlsv.so_luong_sv() > 0):
            print("\n3: Xoá sinh viên")
            print ("\nNhập ID:")
            ID = int(input())
            if(qlsv.deletebyID(ID)):
                print("Sinh viên có ID: ",ID," đã bị xoá")
            else: 
                print("Sinh viên có ID: ", ID," Không tồn tại!")
        else:
            print("Danh sách sinh viên trống!")
            
    elif(key==4):
        if(qlsv.so_luong_sv() > 0):
            print("\nTìm kiếm sinh viên theo tên")
            print("\nNhập tên:")
            name = input()
            searchresult = qlsv.findByName(name)
            QuanLySinhVien.show_sv(searchresult)
        else:
            print("Danh sách sinh viên trống!")
            
    elif (key ==5):
        if(qlsv.so_luong_sv() > 0):
            print("\nSắp xếp sinh viên theo điểm trung bình (GPA):")
            qlsv.sortbyDiemTB()
            qlsv.show_sv(qlsv.getListSV())
        else:
            print("Danh sách sinh viên trống!")
    elif (key == 6):
        if(qlsv.so_luong_sv() > 0):
            print("\nSắp xếp sinh viên theo Tên:")
            qlsv.sortbyName
            qlsv.show_sv(qlsv.getListSV())
        else:
            print("Danh sách sinh viên trống!")  
    elif (key == 7):
        if(qlsv.so_luong_sv() > 0):
            print("\nDanh sách sinh viên:")
            qlsv.show_sv(qlsv.getListSV())
        else:
            print("Danh sách sinh viên trống!")
    elif (key == 0):
        print("\nBạn đã chọn kết thúc!")
        break
    else:
        print("\nKhông có chức năng này!")
        print("\nHãy chọn các chức năng trên Menu!!!!")
    