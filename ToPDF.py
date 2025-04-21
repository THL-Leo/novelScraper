import os
from fpdf import FPDF
import re

def create_novel_pdf(novel_id):
    # Setup PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.add_font("DejaVu", fname="../../Fonts/Noto_Sans_SC/static/NotoSansSC-Regular.ttf")
    pdf.set_font("DejaVu", size=12)

    # Define the directory path
    novel_dir = f"{novel_id}"
    if not os.path.exists(novel_dir):
        print(f"Error: Novel directory for ID {novel_id} not found")
        return

    # Get all chapter files and sort them naturally
    def natural_sort_key(s):
        return [int(text) if text.isdigit() else text.lower()
                for text in re.split('([0-9]+)', s)]

    chapter_files = [f for f in os.listdir(novel_dir) 
                     if f.endswith('.txt') and f != 'end_chapter.txt']
    chapter_files.sort(key=natural_sort_key)

    # Process each chapter
    for chapter_file in chapter_files:
        file_path = os.path.join(novel_dir, chapter_file)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Add chapter title
            chapter_title = chapter_file.replace('.txt', '')
            pdf.set_font("DejaVu", style="", size=14)  # Bold font for title
            pdf.cell(0, 10, f"Chapter {chapter_title}", ln=True, align='C')
            pdf.ln(5)
            
            # Add chapter content
            pdf.set_font("DejaVu", size=12)
            paragraphs = content.split('\n')
            for paragraph in paragraphs:
                if paragraph.strip():  # Only process non-empty paragraphs
                    pdf.multi_cell(0, 10, paragraph.strip())
                    pdf.ln(5)
            
            pdf.add_page()

    # Save the PDF
    output_path = f"{novel_id}/{novel_id}_complete.pdf"
    pdf.output(output_path)
    print(f"PDF created successfully at: {output_path}")


if __name__ == "__main__":
    # Example usage
    novel_id = input("Enter the novel ID: ")
    create_novel_pdf(novel_id)