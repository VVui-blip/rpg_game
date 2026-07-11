# Pixel Realm RPG — C++/SDL2 rewrite

Viết lại từ Python/pygame sang C++ + SDL2, build APK qua GitHub Actions
(không cần Android Studio/Termux tự build).

## Cách hoạt động của CI

`android-project/` KHÔNG nằm trong repo này. Workflow tự tải khung Android
chuẩn từ repo chính thức `libsdl-org/SDL` lúc build, rồi ghép code trong
`src/` vào đó. Lý do: khung này gồm hàng ngàn dòng Java glue (SDLActivity)
và cấu hình Gradle rất dễ lệch version nếu tự chép tay — để CI tải bản gốc
mới nhất từ nguồn chính chủ là an toàn nhất.

Muốn build local (nếu có Android Studio/NDK): làm y hệt các bước trong
`.github/workflows/build-cpp.yml` phần "Ghép project".

## Roadmap theo pha

**Pha 1 (đã có trong lần này) — chứng minh toolchain chạy được:**
- [x] Build APK qua GitHub Actions bằng CMake + NDK
- [x] Di chuyển bằng nút chạm (4 hướng)
- [x] Nút tấn công (placeholder hình vuông trắng, chưa có PNG chém thật)
- [x] Nút né (dash + bất tử tạm thời trong lúc né)
- [x] Hiệu ứng nhấp nháy đỏ khi trúng đòn (`takeHit()` đã sẵn, chưa có ai gọi)

**Pha 2 — asset & animation thật:**
- [ ] Load PNG (SDL2_image), thay các hình chữ nhật placeholder bằng sprite
- [ ] Sprite sheet + animation state machine (idle/walk/attack/hurt/die) — tái dùng
      ý tưởng row_map như bản Python cũ
- [ ] PNG hiệu ứng chém/đâm theo loại vũ khí (kiếm, giáo, cung...)

**Pha 3 — chiến đấu & mob:**
- [ ] Entity system dùng chung cho Player/Mob (kế thừa struct hiện tại)
- [ ] Nhiều loại mob: Slime, Orc, Goblin (thổ phỉ), và loại "Godline" (elite/boss tier)
- [ ] AI cơ bản: phát hiện phạm vi, đuổi theo, tấn công
- [ ] Hurt/die animation cho mob khi trúng đòn slash

**Pha 4 — kinh tế:**
- [ ] Hệ thống tiền tệ (gold, drop từ mob)
- [ ] Shop: mua/bán vũ khí, item, NPC thương nhân

**Pha 5 — bản đồ lớn:**
- [ ] Camera theo player, chunk-based map
- [ ] Culling: chỉ render tile/entity nằm trong khung hình (đã có sẵn logic
      tương tự trong bản Python `TileMap.render()`, port thẳng sang C++)
- [ ] Nhiều vùng/quốc gia, hệ thống portal/loading zone giữa các map

**Pha 6 — asset môi trường:**
- [ ] Nhà, lâu đài, nền gạch, bụi cây, cây, sinh vật môi trường (cá, chim, thú rừng)
- [ ] Vẽ procedural bằng code (giữ đúng tinh thần "không dùng engine/asset có sẵn")
      hoặc sinh từ tool riêng như `tools/generate_assets.py` bản Python cũ

## Vì sao chia pha thay vì làm hết 1 lần

Danh sách tính năng đã yêu cầu (chém/đâm, mob nhiều loại, shop, tiền tệ,
map lớn có culling, nhiều quốc gia, hàng chục loại PNG môi trường) là khối
lượng công việc nhiều tuần, không phải 1 lần commit. Build sai toolchain ở
bước đầu (như đã dính với buildozer) mà cứ cắm đầu thêm feature lên trên
thì debug sẽ cực kỳ khó, vì không biết lỗi tới từ code mới hay từ nền build.
Nên pha 1 CHỈ có mục tiêu duy nhất: APK build xanh + chạy được trên máy thật.
