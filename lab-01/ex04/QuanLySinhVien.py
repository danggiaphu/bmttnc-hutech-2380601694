from SinhVien import SinhVien

class QuanLySinhVien:
    listSinhVien = []
    
 #tao id sv   
    def generateID(self):
        maxId = 1
        if(self.so_luong_sv() > 0):
            maxId = self.listSinhVien[0]._id
            for sv in self.listSinhVien:
                if(sv._id > maxId):
                    maxId = sv._id
            maxId += 1
        return maxId
    
    def so_luong_sv(self):
        return self.listSinhVien.__len__()
    
#nhap thong tin sv 
    def nhap_sv(self):
        svId = self.generateID()
        name = input("Nhập tên sinh viên:")
        sex= input("Nhập giới tính:")
        major = input("Nhập chuyên ngành:")
        diemTB = float(input("Nhập điểm trung bình:"))
        sv = SinhVien(svId, name, sex, major, diemTB)
        self.xep_hoc_luc(sv)
        self.listSinhVien.append(sv)
#cn tt sv
    def updatesv(self, ID):
        sv:SinhVien = self.findByID(ID)
        if(sv != None):
            name = input("Nhập tên sinh viên:")
            sex= input("Nhập giới tính:")
            major = input("Nhập chuyên ngành:")
            diemTB = float(input("Nhập điểm trung bình:"))
            sv._name = name
            sv._sex = sex
            sv._major = major
            sv._diemTB = diemTB
            self.xep_hoc_luc(sv)
        else:
            print("sinh vien co ID: {} khong ton tai".format(ID))
# sort theo id, ten, diemTB        
    def sortbyID (self):
        self.listSinhVien.sort(key=lambda x: x._id, reverse = False)
    def sortbyName(self):
        self.listSinhVien.sort(key=lambda x: x._name, reverse = False)
    def sortbyDiemTB(self):
        self.listSinhVien.sort(key=lambda x: x._diemTB, reverse = False)
#tim ID sv       
    def findByID(self, ID):
        searchResult = None
        if(self.so_luong_sv() > 0):
            for sv in self.listSinhVien:
                if(sv._id == ID):
                    searchResult = sv
                    break
        return searchResult
#tim theo ten
    def findByName(self, keyword):
        listSearchResult = []
        if(self.so_luong_sv() > 0):
            for sv in self.listSinhVien:
                if(keyword.upper() in sv._name.upper()):
                    listSearchResult.append(sv)
        return listSearchResult   
#xoa theo id 
    def deletebyID(self, ID):
        isDeleted = False
        sv = self.findByID(ID)
        if sv is not None:
            self.listSinhVien.remove(sv)
        isDeleted = True
        return isDeleted

#xep hoc luc
    def xep_hoc_luc(self, sv:SinhVien):
        if(sv._diemTB >= 8):
            sv._hocluc = "Gioi"
        elif(sv._diemTB >= 6.5):
            sv._hocluc = "Kha"
        elif(sv._diemTB >= 5):
            sv._hocluc = "Trung binh"
        else:
            sv._hocluc = "Yeu"
#hien thi thong tin sv
    def show_sv(self, listSV):
        print("{:<8} {:<15} {:<10} {:<15} {:<10} {:<10}".format("ID", "Name", "Sex", "Major", "GPA", "Hoc Luc"))
        if len(listSV) > 0:
            for sv in listSV:
                print("{:<8} {:<15} {:<10} {:<15} {:<10} {:<10}".format(sv._id, sv._name, sv._sex, sv._major, sv._diemTB, sv._hocluc))
        print("\n")
    
    def getListSV(self):
        return self.listSinhVien