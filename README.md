# Rút Gỗ Số

Minigame rút gỗ (Jenga) có đánh số, vật lý thật, âm thanh và hiệu ứng. Chạy bằng Streamlit.

## Chạy thử trên máy
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Đưa lên GitHub
```bash
git init
git add .
git commit -m "Rut go so"
git branch -M main
git remote add origin https://github.com/<ten-ban>/rut-go-so.git
git push -u origin main
```

## Deploy lên Streamlit Community Cloud
1. Vào https://share.streamlit.io và đăng nhập bằng GitHub.
2. Chọn **Create app** → repo `rut-go-so`, branch `main`, file `app.py`.
3. Bấm **Deploy**, rồi gửi link cho bạn bè.

## Cấu trúc
- `app.py`: giao diện Streamlit (tên người chơi, số tầng, âm thanh).
- `game.html`: game (Three.js + cannon.js, âm thanh tạo bằng WebAudio, không cần file mp3).

## Chỉnh vật lý
Trong `game.html`, mục `PHYS`: ma sát (`FRICTION`), tốc độ rút (`SPEED`), độ nhạy phát hiện sập (`TILT`, `SAG`, `DRIFT`). Các ngưỡng này đo so với vị trí ổn định ở đầu mỗi lượt; tăng giá trị nếu muốn tháp "chịu đòn" hơn.
