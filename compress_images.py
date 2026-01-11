"""
均衡压缩图片 - 优化版本 (针对 CDN 托管，提高清晰度)
"""

from PIL import Image
import os

def compress_images(source_dir):
    """压缩所有图片，优化清晰度"""
    
    total_original = 0
    total_compressed = 0
    
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                filepath = os.path.join(root, file)
                original_size = os.path.getsize(filepath)
                total_original += original_size
                
                try:
                    img = Image.open(filepath)
                    
                    # 转换为 RGB (处理 RGBA)
                    if img.mode == 'RGBA':
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[3])
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # 动态分辨率策略
                    # 如果原始图片很小，不要强行放大（避免模糊）
                    # 如果原始图片很大，缩小到 800px 宽度
                    max_width = 800
                    if img.width > max_width:
                        ratio = max_width / img.width
                        new_height = int(img.height * ratio)
                        img = img.resize((max_width, new_height), Image.LANCZOS)
                    
                    # 保存为 JPEG 格式，提高质量到 90
                    output_path = filepath.rsplit('.', 1)[0] + '.jpg'
                    
                    # 使用 90 质量 (CDN 模式下，单张 50-100KB 是完美的)
                    img.save(output_path, 'JPEG', quality=90, optimize=True, progressive=True)
                    
                    # 如果是 PNG 且已经生成了 JPG，删除原始 PNG
                    if output_path != filepath and os.path.exists(output_path):
                        os.remove(filepath)
                    
                    compressed_size = os.path.getsize(output_path)
                    total_compressed += compressed_size
                    
                except Exception as e:
                    print(f"  Error: {file}: {e}")
                    total_compressed += original_size
    
    print(f"\n✅ 图片优化完成!")
    print(f"   原始大小: {total_original/1024/1024:.2f} MB")
    print(f"   当前大小: {total_compressed/1024/1024:.2f} MB")

if __name__ == "__main__":
    # 优先压缩 drills，因为它们似乎被压缩过度了
    compress_images("public/images")
