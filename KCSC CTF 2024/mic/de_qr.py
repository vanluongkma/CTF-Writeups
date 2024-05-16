import cv2
from pyzxing import BarCodeReader

# Tạo đối tượng đọc mã vạch
reader = BarCodeReader()

# Đọc hình ảnh QR code
img = cv2.imread('qr_flag.png')

# Lưu tạm thời hình ảnh QR code để ZXing có thể đọc
temp_filename = 'temp_qr_code.png'
cv2.imwrite(temp_filename, img)

# Giải mã QR code
results = reader.decode(temp_filename)

# Kiểm tra và in dữ liệu giải mã được
if results:
    for result in results:
        print('Type:', result.get('format'))
        print('Data:', result.get('raw'))
else:
    print('Không thể giải mã QR code.')

# Xóa tệp tạm thời nếu cần thiết
import os
os.remove(temp_filename)