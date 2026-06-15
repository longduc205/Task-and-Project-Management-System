import os
from pathlib import Path
from docling.document_converter import DocumentConverter

def main():
    pdf_dir = Path("/home/duc/TQT/OneDrive_1_6-15-2026")
    pdf_files = sorted(list(pdf_dir.glob("*.pdf")))
    
    if not pdf_files:
        print("Không tìm thấy file PDF nào trong thư mục OneDrive_1_6-15-2026.")
        return

    print(f"Tìm thấy {len(pdf_files)} file PDF cần chuyển đổi.")
    
    # Khởi tạo DocumentConverter (sẽ tải mô hình nếu chạy lần đầu)
    print("Đang khởi tạo Docling...")
    converter = DocumentConverter()
    
    for idx, pdf_path in enumerate(pdf_files, 1):
        md_path = pdf_path.with_suffix(".md")
        
        # Bỏ qua nếu đã chuyển đổi rồi
        if md_path.exists():
            print(f"[{idx}/{len(pdf_files)}] Bỏ qua (đã tồn tại): {pdf_path.name}")
            continue
            
        print(f"[{idx}/{len(pdf_files)}] Đang chuyển đổi: {pdf_path.name}...")
        try:
            result = converter.convert(pdf_path)
            markdown_content = result.document.export_to_markdown()
            
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            print(f" -> Hoàn thành! Đã lưu tại: {md_path.name}")
        except Exception as e:
            print(f" -> Lỗi khi chuyển đổi {pdf_path.name}: {e}")

if __name__ == "__main__":
    main()
