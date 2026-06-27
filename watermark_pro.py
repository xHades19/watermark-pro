#!/usr/bin/env python3
"""
Watermark Pro - Công cụ watermark ảnh hàng loạt
==============================================
Dành cho dân bán hàng online, chụp ảnh sản phẩm cần thêm logo.

Cài đặt:
  pip install pillow

Dùng:
  python3 watermark_pro.py --input ./thu_muc_anh/ --text "SHOP ABC" --output ./da_watermark/
  python3 watermark_pro.py -i anh.jpg -t "0938 123 456" -o ./out/ --opacity 0.5

Ủng hộ: 0x904688a5e14Adc573aEc2191B594fe287c190Fea (USDT BEP20)
"""

import os
import argparse
from PIL import Image, ImageDraw, ImageFont
import glob

VERSION = "1.0"

def get_font(size=36):
    """Try to load a Unicode font, fallback to default"""
    font_paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:\\Windows\\Fonts\\arial.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except:
                pass
    return ImageFont.load_default()

def add_watermark(image_path, text, output_path, opacity=0.3, position="bottom-right", logo_path=None):
    """Add watermark text/logo to image"""
    img = Image.open(image_path).convert("RGBA")
    
    # Create watermark layer
    watermark = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)
    
    # Calculate font size based on image width
    font_size = max(20, img.width // 25)
    font = get_font(font_size)
    
    # Get text bounds
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    # Position
    margin = 20
    positions = {
        "top-left": (margin, margin),
        "top-right": (img.width - tw - margin, margin),
        "bottom-left": (margin, img.height - th - margin),
        "bottom-right": (img.width - tw - margin, img.height - th - margin),
        "center": ((img.width - tw) // 2, (img.height - th) // 2),
    }
    x, y = positions.get(position, positions["bottom-right"])
    
    # Draw text with outline for readability
    outline_color = (0, 0, 0, int(255 * opacity))
    text_color = (255, 255, 255, int(255 * opacity))
    
    for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
        draw.text((x+dx, y+dy), text, font=font, fill=outline_color)
    draw.text((x, y), text, font=font, fill=text_color)
    
    # Add logo if provided
    if logo_path and os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo.thumbnail((img.width // 6, img.height // 6))
            logo_x = img.width - logo.width - margin
            logo_y = margin
            watermark.paste(logo, (logo_x, logo_y), logo)
        except:
            pass
    
    # Composite
    result = Image.alpha_composite(img, watermark)
    result = result.convert("RGB")
    
    # Save
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    result.save(output_path, "JPEG", quality=95)
    return True

def main():
    parser = argparse.ArgumentParser(
        description="🖼️ Watermark Pro - Thêm watermark hàng loạt",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  %(prog)s -i anh.jpg -t "SHOP ABC" -o ./out/
  %(prog)s -i ./thu_muc/ -t "0938 123 456" --opacity 0.5
  %(prog)s -i ./anh/ -t "FB.COM/SHOP" --logo logo.png --position top-left

Ủng hộ: 0x904688a5e14Adc573aEc2191B594fe287c190Fea (USDT BEP20)
        """
    )
    parser.add_argument("-i", "--input", required=True, help="File ảnh hoặc thư mục chứa ảnh")
    parser.add_argument("-t", "--text", default="© DUYEN SHOP", help="Nội dung watermark (mặc định: © DUYEN SHOP)")
    parser.add_argument("-o", "--output", default="./watermarked", help="Thư mục output (mặc định: ./watermarked)")
    parser.add_argument("--opacity", type=float, default=0.3, help="Độ mờ 0-1 (mặc định: 0.3)")
    parser.add_argument("--position", default="bottom-right", 
                        choices=["top-left", "top-right", "bottom-left", "bottom-right", "center"],
                        help="Vị trí watermark")
    parser.add_argument("--logo", help="Đường dẫn logo (png có nền trong suốt)")
    parser.add_argument("--version", action="version", version=f"%(prog)s v{VERSION}")
    
    args = parser.parse_args()
    
    # Collect images
    if os.path.isfile(args.input):
        images = [args.input]
    elif os.path.isdir(args.input):
        exts = ["*.jpg", "*.jpeg", "*.png", "*.webp"]
        images = []
        for ext in exts:
            images.extend(glob.glob(os.path.join(args.input, ext)))
            images.extend(glob.glob(os.path.join(args.input, ext.upper())))
    else:
        print(f"❌ Không tìm thấy: {args.input}")
        return 1
    
    if not images:
        print(f"❌ Không có ảnh nào trong: {args.input}")
        return 1
    
    os.makedirs(args.output, exist_ok=True)
    
    print(f"\n{'='*50}")
    print(f"  Watermark Pro v{VERSION}")
    print(f"  Xử lý {len(images)} ảnh...")
    print(f"  Text: \"{args.text}\"")
    print(f"  Vị trí: {args.position}")
    print(f"{'='*50}\n")
    
    success = 0
    for img_path in images:
        try:
            fname = os.path.basename(img_path)
            name, ext = os.path.splitext(fname)
            out_path = os.path.join(args.output, f"{name}_wm.jpg")
            add_watermark(img_path, args.text, out_path, args.opacity, args.position, args.logo)
            success += 1
            print(f"  ✅ {fname} → {out_path}")
        except Exception as e:
            print(f"  ❌ {fname}: {e}")
    
    print(f"\n{'='*50}")
    print(f"  ✅ Hoàn tất: {success}/{len(images)} ảnh")
    print(f"  📁 Output: {os.path.abspath(args.output)}")
    print(f"{'='*50}")
    print(f"\n  💖 Nếu thấy hữu ích, ủng hộ dev tại:")
    print(f"  0x904688a5e14Adc573aEc2191B594fe287c190Fea (USDT BEP20)")
    print()
    
    return 0

if __name__ == "__main__":
    exit(main())
