# Tu Tiên (phase 1)

Game 2D top-down tu tiên bằng JavaScript thuần + HTML5 Canvas.
Chạy: `python3 -m http.server` trong thư mục này rồi mở `index.html`.

- Điều khiển: WASD / mũi tên, Shift chạy, Space nhảy, J chém, phím 1-4 đổi trang bị. Điện thoại: joystick ảo + nút Chém/Nhảy.
- Sprite: 64x64, 8 hướng. Skin là các lớp sheet cùng bố cục (xem `src/data/equipment.js`).
- `tools/`: script Python tạo sheet từ zip PixelLab, tạo skin và biến thể kiếm (đường dẫn trong script đang trỏ vào máy làm việc cũ, cần chỉnh khi chạy lại).

## Quyết định về trang phục (2026-10-09)

- **Chỉ một bộ đồ toàn thân mặc định** (thân + đồ liền nhau). Đồ trong kho chỉ đổi **chỉ số**, không đổi hình trên người.
- Mỗi món đồ có thể có trường tùy chọn `visual` (hiện để trống). Muốn món nào hiện ra thì điền sau, không sửa lại kho đồ.
- Phần nhìn thấy được, làm rẻ: **hào quang theo cảnh giới** (code), **đổi bảng màu bộ đồ theo cảnh giới**, **kiếm đổi hình theo vũ khí** (đã có sheet đổi màu), **áo choàng là phần thưởng mở khóa** (tùy chọn).
- **Không vẽ thêm skin** (hair/clothes/shoes mới) nếu người dùng chưa yêu cầu. Việc ghép lớp đã có sẵn trong code, dùng lại khi cần.
- Áo choàng: `assets/player/cape` (bản AI, chỉ walk) và `assets/player/cape_code` (bản sinh bằng code, idle/walk/run, 2 lớp back/front, ô 80×80, thân 64×64 ở giữa). Sinh lại bằng `tools/gen_cape_code.py`.
