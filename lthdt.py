import csv
import os
from Lop import Reader

class DataReader:
    def __init__(self, filename="readers.csv"):
        self.filename = filename
        self.readers = []
        self.load_from_file()

    # ================== ĐỌC / GHI FILE ==================
    def load_from_file(self):
        if not os.path.exists(self.filename):
            return
        with open(self.filename, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            self.readers = []
            for r in reader:
                books = r.get("borrowed_books", "").split(";") if r.get("borrowed_books") else []
                self.readers.append(Reader(
                    r["reader_id"],
                    r["full_name"],
                    r["class_name"],
                    r["register_date"],
                    books
                ))

    def save_to_file(self):
        with open(self.filename, mode="w", encoding="utf-8", newline="") as file:
            fieldnames = ["reader_id", "full_name", "class_name", "register_date", "borrowed_books"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for r in self.readers:
                writer.writerow({
                    "reader_id": r.reader_id,
                    "full_name": r.full_name,
                    "class_name": r.class_name,
                    "register_date": r.register_date,
                    "borrowed_books": ";".join(r.borrowed_books)
                })

    # ================== CHỨC NĂNG CHÍNH ==================
    def add_reader(self):
        reader = Reader()
        reader.input_info()
        if any(r.reader_id == reader.reader_id for r in self.readers):
            print(" Mã độc giả đã tồn tại.")
            return
        self.readers.append(reader)
        self.save_to_file()
        print(" Thêm độc giả thành công!")

    def update_reader(self, reader_id):
        for r in self.readers:
            if r.reader_id == reader_id:
                print("Nhập thông tin mới (nhấn Enter để bỏ qua):")
                new_name = input("Họ tên mới: ").strip()
                new_class = input("Lớp mới: ").strip()
                new_date = input("Ngày đăng ký mới (DD/MM/YYYY): ").strip()

                if new_name: r.full_name = new_name
                if new_class: r.class_name = new_class
                if new_date: r.register_date = new_date

                self.save_to_file()
                print(" Cập nhật độc giả thành công!")
                return
        print(" Không tìm thấy mã độc giả.")

    def delete_reader(self, reader_id):
        for r in self.readers:
            if r.reader_id == reader_id:
                self.readers.remove(r)
                self.save_to_file()
                print(" Xóa độc giả thành công!")
                return
        print(" Không tìm thấy mã độc giả cần xóa.")

    def search_reader(self, keyword):
        result = [
            r for r in self.readers
            if keyword.lower() in r.reader_id.lower() or keyword.lower() in r.full_name.lower()
        ]
        if result:
            print("\n KẾT QUẢ TÌM KIẾM:")
            for r in result:
                r.display_info()
        else:
            print("Không tìm thấy độc giả nào phù hợp.")

    def display_all(self):
    """Hiển thị toàn bộ danh sách độc giả"""
    if not self.readers:
        print("Danh sách trống.")
        return

    print("\n===== DANH SÁCH ĐỘC GIẢ =====")
    print(f"{'MÃ ĐỘC GIẢ':<12} | {'HỌ TÊN':<25} | {'LỚP':<8} | {'NGÀY ĐK':<12} | {'SÁCH ĐANG MƯỢN'}")
    print("-" * 80)

    for r in self.readers:
        borrowed_books = ", ".join(r.borrowed_books) if getattr(r, "borrowed_books", []) else "Không có"
        print(f"{r.reader_id:<12} | {r.full_name:<25} | {r.class_name:<8} | {r.register_date:<12} | {borrowed_books}")

