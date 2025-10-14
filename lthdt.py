import csv
import re
from datetime import datetime, timedelta

DATA_FILE = "readers.csv"

class Reader:
    def __init__(self, reader_id, full_name, class_name, register_date):
        self.reader_id = reader_id
        self.full_name = full_name
        self.class_name = class_name
        self.register_date = datetime.strptime(register_date, "%d/%m/%Y")
        self.expiry_date = self.register_date + timedelta(days=365)

    def list(self):
        return [
            self.reader_id,
            self.full_name,
            self.class_name,
            self.register_date.strftime("%d/%m/%Y"),
            self.expiry_date.strftime("%d/%m/%Y")
        ]


def validate_reader_id(reader_id):
    return bool(re.match(r"^R\d{2}_\d{5}$", reader_id))

def validate_full_name(full_name):
    return bool(re.match(r"^[A-ZÀ-Ỹ][a-zà-ỹ]*(?:\s[A-ZÀ-Ỹ][a-zà-ỹ]*)*$", full_name))

def validate_class_name(class_name):
    return bool(re.match(r"^[A-Z]\d{2}[A-Z]\d*$", class_name))

def validate_date(date_str):
    try:
        date = datetime.strptime(date_str, "%d/%m/%Y")
        return date <= datetime.now()
    except:
        return False


def load_data():
    readers = []
    try:
        with open(DATA_FILE, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                readers.append(Reader(*row[:4]))
    except FileNotFoundError:
        pass
    return readers

def save_data(readers):
    with open(DATA_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ReaderID", "FullName", "Class", "RegisterDate", "ExpiryDate"])
        for r in readers:
            writer.writerow(r.to_list())


def add_reader(readers):
    reader_id = input("Nhập mã độc giả (VD: R24_00001): ")
    if not validate_reader_id(reader_id):
        print("Mã độc giả không hợp lệ!")
        return

    if any(r.reader_id == reader_id for r in readers):
        print("Mã độc giả đã tồn tại!")
        return

    full_name = input("Nhập họ tên: ").strip().title()
    if not validate_full_name(full_name):
        print("Họ tên không hợp lệ!")
        return

    class_name = input("Nhập lớp (VD: K60S): ").strip().upper()
    if not validate_class_name(class_name):
        print("Lớp không hợp lệ!")
        return

    register_date = input("Nhập ngày đăng ký (DD/MM/YYYY): ").strip()
    if not validate_date(register_date):
        print("Ngày đăng ký không hợp lệ hoặc lớn hơn hiện tại!")
        return

    new_reader = Reader(reader_id, full_name, class_name, register_date)
    readers.append(new_reader)
    save_data(readers)
    print("Thêm độc giả thành công!")


def edit_reader(readers):
    reader_id = input("Nhập mã độc giả cần sửa: ")
    for r in readers:
        if r.reader_id == reader_id:
            print(f"Đang chỉnh sửa {r.full_name}")
            new_name = input("Tên mới (Enter để bỏ qua): ").strip()
            if new_name:
                if validate_full_name(new_name):
                    r.full_name = new_name.title()
            new_class = input("Lớp mới (Enter để bỏ qua): ").strip()
            if new_class:
                if validate_class_name(new_class):
                    r.class_name = new_class.upper()
            save_data(readers)
            print("Đã cập nhật thông tin độc giả.")
            return
    print("Không tìm thấy mã độc giả.")


def delete_reader(readers):
    reader_id = input("Nhập mã độc giả cần xóa: ")
    for r in readers:
        if r.reader_id == reader_id:
            readers.remove(r)
            save_data(readers)
            print("Đã xóa độc giả.")
            return
    print("Không tìm thấy mã độc giả.")


def search_reader(readers):
    keyword = input("Nhập mã hoặc họ tên cần tìm: ").strip().lower()
    found = [r for r in readers if keyword in r.reader_id.lower() or keyword in r.full_name.lower()]
    if found:
        print(f"{'Mã':<12}{'Họ tên':<25}{'Lớp':<10}{'Đăng ký':<12}{'Hết hạn':<12}")
        for r in found:
            print(f"{r.reader_id:<12}{r.full_name:<25}{r.class_name:<10}"
                  f"{r.register_date.strftime('%d/%m/%Y'):<12}{r.expiry_date.strftime('%d/%m/%Y'):<12}")
    else:
        print("Không tìm thấy độc giả nào.")



def main():
    readers = load_data()
    while True:
        print("\n=== QUẢN LÝ ĐỘC GIẢ ===")
        print("1. Thêm độc giả mới")
        print("2. Chỉnh sửa thông tin")
        print("3. Xóa độc giả")
        print("4. Tra cứu độc giả")
        print("5. Thoát")
        choice = input("Chọn chức năng: ")

        if choice == "1":
            add_reader(readers)
        elif choice == "2":
            edit_reader(readers)
        elif choice == "3":
            delete_reader(readers)
        elif choice == "4":
            search_reader(readers)
        elif choice == "5":
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
