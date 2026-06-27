# Watermark Pro 🖼️

**Công cụ thêm watermark (logo/chữ) hàng loạt cho ảnh sản phẩm — dành cho dân bán hàng online Việt Nam**

## Tính năng
- ✅ Watermark hàng loạt — vài trăm ảnh trong giây lát
- ✅ Thêm chữ: SĐT, tên shop, Facebook, Zalo...
- ✅ Thêm logo PNG (nền trong suốt)
- ✅ Tuỳ chỉnh vị trí: 4 góc + giữa
- ✅ Tuỳ chỉnh độ mờ
- ✅ Hỗ trợ JPG, PNG, WebP

## Cài đặt

```bash
pip install pillow
```

## Sử dụng

### Cơ bản — watermark chữ cho cả thư mục ảnh

```bash
python3 watermark_pro.py -i ./thu_muc_anh/ -t "SHOP ABC 0938 123 456"
```

### Thêm logo + chữ

```bash
python3 watermark_pro.py -i ./anh/ -t "FB.COM/SHOP" --logo logo.png
```

### Tuỳ chỉnh vị trí và độ mờ

```bash
python3 watermark_pro.py -i anh.jpg -t "0938 123 456" --position center --opacity 0.5
```

### Đầy đủ option

```
-i, --input      File ảnh hoặc thư mục chứa ảnh (bắt buộc)
-t, --text       Nội dung watermark (mặc định: © DUYEN SHOP)
-o, --output     Thư mục output (mặc định: ./watermarked)
--opacity        Độ mờ 0-1 (mặc định: 0.3)
--position       Vị trí: top-left, top-right, bottom-left, bottom-right, center
--logo           Đường dẫn logo PNG
```

## Yêu cầu

- Python 3.7+
- Pillow (`pip install pillow`)

## Donate 💖

Tool này miễn phí, nhưng nếu bạn thấy hữu ích và muốn ủng hộ dev:

**USDT (BEP20):** `0x904688a5e14Adc573aEc2191B594fe287c190Fea`
