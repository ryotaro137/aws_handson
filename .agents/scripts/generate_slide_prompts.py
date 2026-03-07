import os
import sys
import re

PROMPT_TEMPLATE = """# Nano Banana Pro 画像生成プロンプト

以下のスライド内容を基に、プレゼンテーション用スライドの背景画像または挿絵を生成してください。

## スライド内容
{slide_content}

## 画像生成の要件
- プロフェッショナルでクリーンなデザイン
- AWSやクラウド技術を連想させるIT/テック系のイメージ
- アスペクト比: 16:9
- 余白を十分に確保し、テキストが配置しやすい構図
"""

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_slide_prompts.py <input_marp_file> <output_dir>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
        
    os.makedirs(output_dir, exist_ok=True)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # '---' でスライドを分割 (フロントマターも含まれる)
    parts = re.split(r'^---\s*$', content, flags=re.MULTILINE)
    
    slides = [p.strip() for p in parts if p.strip()]
    
    # 最初の要素がフロントマター（marp設定など）の場合はスキップ
    if slides and 'marp:' in slides[0].lower():
        slides = slides[1:]
        
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    
    # プロンプトファイルの生成
    slide_count = 0
    for i, slide in enumerate(slides, 1):
        if not slide:
            continue
            
        slide_count += 1
        prompt_content = PROMPT_TEMPLATE.format(slide_content=slide)
        output_file = os.path.join(output_dir, f"{base_name}_prompt_{slide_count:02d}.md")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(prompt_content)
            
        print(f"Created: {output_file}")
        
    print(f"Total {slide_count} prompt files generated in '{output_dir}'.")

if __name__ == "__main__":
    main()
