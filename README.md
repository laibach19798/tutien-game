# Tu Tiên (phase 1)

Game 2D top-down tu tiên bằng JavaScript thuần + HTML5 Canvas.
Chạy: `python3 -m http.server` trong thư mục này rồi mở `index.html`.

- Điều khiển: WASD / mũi tên, Shift chạy, Space nhảy, J chém, phím 1-4 đổi trang bị. Điện thoại: joystick ảo + nút Chém/Nhảy.
- Sprite: 64x64, 8 hướng. Skin là các lớp sheet cùng bố cục (xem `src/data/equipment.js`).
- `tools/`: script Python tạo sheet từ zip PixelLab, tạo skin và biến thể kiếm (đường dẫn trong script đang trỏ vào máy làm việc cũ, cần chỉnh khi chạy lại).
