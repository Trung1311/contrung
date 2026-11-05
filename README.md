# Trang trại Thanh Xuân — website

Website giới thiệu trang trại Thanh Xuân (dế mèn, tắc kè, bọ cạp), thiết kế ưu tiên cho điện thoại.

Xem trực tuyến: https://trung1311.github.io/contrung/

## Các trang
| File | Nội dung |
|---|---|
| `index.html` | Trang chủ |
| `de-men.html` | Dế mèn: giá, vòng đời, kỹ thuật nuôi, thu hoạch, video |
| `tac-ke.html` | Tắc kè: giá, đặc điểm, làm chuồng, kỹ thuật, video |
| `bo-cap.html` | Bọ cạp: giá, hồ nuôi, thức ăn, thu hoạch, video |
| `bang-gia.html` | Bảng giá, 8 gói bao tiêu, điều khoản, cam kết |
| `dau-ra.html` | Đầu ra, thu mua, xuất khẩu |
| `mua-hang.html` | Đặt hàng, thanh toán, chuẩn bị nuôi |
| `tin-tuc.html` | Video truyền hình, thư viện hơn 600 video, kênh YouTube, tin tức |
| `lien-he.html` | Địa chỉ, điện thoại |

## Video
Video lấy từ website cũ trangtraithanhxuan.com (đã kiểm tra còn xem được trên YouTube).
- `_build/video_sets.json`: các nhóm video chèn vào từng trang (mã YouTube, tiêu đề, dòng phụ).
- `_build/video_library.json`: toàn bộ thư viện video cho trang Video & tin tức.
- `js/video.js`: trình phát (chỉ tải YouTube khi khách bấm) và thư viện có tìm kiếm, lọc.

## Sửa nội dung
Nội dung từng trang nằm trong `_build/pages/`. Phần đầu trang, menu, chân trang nằm trong `_build/build.py`.
Sửa xong chạy `python3 _build/build.py` để tạo lại các file `.html`. Giao diện chung ở `css/style.css`.
