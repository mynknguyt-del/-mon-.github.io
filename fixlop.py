import re
from datetime import datetime

# Book
class Book:
    def __init__(self, book_id="", title="", author="", publisher="", status=""):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.publisher = publisher
        self.status = status

    def input_info(self):
        # BookID: 1 ký tự in hoa + 4 số, duy nhất
        while True:
            bid = input("Nhập mã sách (VD: A0001): ").strip()
            if re.match(r"^[A-Z]\d{4}$", bid):
                self.book_id = bid
                break
            print("Mã sách không hợp lệ.")

        # Title: Ít nhất 2 ký tự, chữ cái đầu viết hoa
        while True:
            title = input("Nhập tên sách: ").strip()
            if len(title) >= 2 and re.match(r"^[A-ZÀ-Ỹ][A-Za-zÀ-ỹ\s]*$", title):
                self.title = title
                break
            print("Tên sách không hợp lệ.")

        # Author: Viết hoa chữ cái đầu, không chứa số/ký tự đặc biệt
        while True:
            author = input("Nhập tác giả: ").strip()
            if author and author[0].isupper() and re.match(r"^[A-ZÀ-Ỹ][A-Za-zÀ-ỹ\s]*$", author):
                self.author = author
                break
            print("Tác giả không hợp lệ.")

        # Publisher: Không để trống
        while True:
            publisher = input("Nhập nhà xuất bản: ").strip()
            if publisher != "":
                self.publisher = publisher
                break
            print("Nhà xuất bản không được để trống.")

        # Status: Chỉ nhận 1 trong các giá trị cho phép
        while True:
            status = input("Nhập tình trạng (Còn/Đã mượn/Hư hỏng/Mất):").strip()
            if status in ["Còn","Đã mượn","Hư hỏng","Mất"]:
                self.status = status
                break
            print("Tình trạng không hợp lệ.")

    def display_info(self):
        print("\n===== THÔNG TIN SÁCH =====")    
        print(f"Mã sách: {self.book_id}")
        print(f"Tên sách: {self.title}")
        print(f"Tác giả: {self.author}")
        print(f"Nhà xuất bản: {self.publisher}")
        print(f"Tình trạng: {self.status}")
# Reader
class Reader:
    def __init__(self, reader_id="", full_name="", class_name="", register_date=""):
        self.reader_id = reader_id
        self.full_name = full_name
        self.class_name = class_name
        self.register_date = register_date
        self.borrowed_books = borrowed_books or []

    def input_info(self):
        # ReaderID: R[Khóa/Năm][5 số] (VD: R24_00001)
        while True:
            rid = input("Nhập mã độc giả (VD: R24_00001): ").strip()
            if re.match(r"^R\d{2}_\d{5}$", rid):
                self.reader_id = rid
                break
            print("Mã độc giả không hợp lệ.")

        # FullName: Viết hoa chữ cái đầu mỗi từ, không chứa số/ký tự đặc biệt
        while True:
            name = input("Nhập họ tên: ").strip()
            if re.match(r"^[A-ZÀ-Ỹ][a-zà-ỹ]*(\s[A-ZÀ-Ỹ][a-zà-ỹ]*)*$", name):
                self.full_name = name
                break
            print("Họ tên không hợp lệ.")

        # Class: Không để trống, đúng định dạng (VD: K60S)
        while True:
            class_name = input("Nhập lớp (VD: K60S): ").strip()
            if class_name and re.match(r"^[A-Z]\d{2,3}[A-Z]\d?$", class_name):
                self.class_name = class_name
                break
            print("Lớp không hợp lệ.")

        # RegisterDate: Đúng định dạng ngày, nhỏ hơn hoặc bằng hiện tại
        while True:
            date = input("Nhập ngày đăng ký (DD/MM/YYYY): ").strip()
            try:
                reg_date = datetime.strptime(date, "%d/%m/%Y")
                if reg_date <= datetime.now():
                    self.register_date = date
                    break
                else:
                    print("Ngày đăng ký không được lớn hơn ngày hiện tại.")
            except:
                print("Ngày đăng ký sai định dạng (DD/MM/YYYY).")

    def display_info(self):
        print("\n===== THÔNG TIN ĐỘC GIẢ =====")
        print(f"Mã độc giả: {self.reader_id}")
        print(f"Họ tên: {self.full_name}")
        print(f"Lớp: {self.class_name}")
        print(f"Ngày đăng ký: {self.register_date}")
        if self.borrowed_books:
            print(f"Sách đang mượn: {', '.join(self.borrowed_books)}")
        else:
            print("Sách đang mượn: Không có")
            
    def add_borrowed_book(self, book_id):
        if book_id not in self.borrowed_books:
            self.borrowed_books.append(book_id)

    def return_borrowed_book(self, book_id):
        if book_id in self.borrowed_books:
            self.borrowed_books.remove(book_id)
# BorrowSlip
class BorrowSlip:
    def __init__(self, borrow_id="", book_id="", reader_id="", borrow_date="", return_date=""):
        self.borrow_id = borrow_id
        self.book_id = book_id
        self.reader_id = reader_id
        self.borrow_date = borrow_date
        self.return_date = return_date

    def input_info(self):
        # BorrowID: P[YYYYMMDD]_[4 số]
        while True:
            bid = input("Nhập mã phiếu mượn (VD: P20251009_0001): ").strip()
            if re.match(r"^P\d{8}_\d{4}$", bid):
                self.borrow_id = bid
                break
            print("Mã phiếu mượn không hợp lệ.")

        # BookID: 1 chữ in hoa + 4 số
        while True:
            bookid = input("Nhập mã sách mượn (VD: A0001): ").strip()
            if re.match(r"^[A-Z]\d{4}$", bookid):
                self.book_id = bookid
                break
            print("Mã sách không hợp lệ.")

        # ReaderID: R[Khóa/Năm]_[5 số]
        while True:
            rid = input("Nhập mã độc giả (VD: R24_00001): ").strip()
            if re.match(r"^R\d{2}_\d{5}$", rid):
                self.reader_id = rid
                break
            print("Mã độc giả không hợp lệ")

        # BorrowDate: Đúng định dạng ngày, nhỏ hơn hoặc bằng hôm nay
        while True:
            date = input("Nhập ngày mượn (DD/MM/YYYY): ").strip()
            try:
                borrow_date = datetime.strptime(date, "%d/%m/%Y")
                if borrow_date <= datetime.now():
                    self.borrow_date = date
                    break
                else:
                    print("Ngày mượn không được lớn hơn ngày hiện tại.")
            except:
                print("Ngày mượn sai định dạng (DD/MM/YYYY).")

        # ReturnDate: Có thể để trống, nếu nhập thì phải lớn hơn ngày mượn
        while True:
            rdate = input("Nhập ngày trả (DD/MM/YYYY, có thể bỏ trống): ").strip()
            if rdate == "":
                self.return_date = ""
                break
            try:
                return_date = datetime.strptime(rdate, "%d/%m/%Y")
                borrow_date = datetime.strptime(self.borrow_date, "%d/%m/%Y")
                if return_date > borrow_date:
                    self.return_date = rdate
                    break
                else:
                    print("Ngày trả phải lớn hơn ngày mượn.")
            except:
                print("Ngày trả sai định dạng (DD/MM/YYYY), hoặc lớn hơn ngày mượn.")

    def display_info(self):
        print("\n===== THÔNG TIN PHIẾU MƯỢN =====")
        print(f"Mã phiếu mượn: {self.borrow_id}")
        print(f"Mã sách mượn: {self.book_id}")
        print(f"Mã độc giả: {self.reader_id}")
        print(f"Ngày mượn: {self.borrow_date}")
        print(f"Ngày trả: {self.return_date if self.return_date else 'Chưa trả'}")

        
