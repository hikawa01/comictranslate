import os
from google.cloud import vision
from google.cloud import vision_v1
from google.cloud import translate_v2 as translate
from PIL import Image, ImageDraw, ImageFont

def translate_images(input_folder, output_folder):
    # 設定 Google Cloud Vision API 的認證金鑰路徑
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/georgewang/Documents/key/GCP_STUDY_TRANSLATE/fresh-bloom-293108-914e1d599383.json"
    client = vision.ImageAnnotatorClient()
    translate_client = translate.Client()

    # 確保輸出資料夾存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    total_files = len([f for f in os.listdir(input_folder) if f.endswith(".jpg") or f.endswith(".png")])
    processed_files = 0

    # 遍歷輸入資料夾中的所有圖片
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'rb') as image_file:
                content = image_file.read()
                image = vision_v1.Image(content=content)
                response = client.text_detection(image=image)
                texts = response.text_annotations

                # 使用PIL處理圖片
                img = Image.open(file_path)
                draw = ImageDraw.Draw(img)
                font_path = "/Users/georgewang/Library/Fonts/NotoSansTC-Regular.ttf"  # 設定字體檔路徑
                font = ImageFont.truetype(font_path, 15)  # 設定使用的字體

                for text in texts[1:]:
                    vertices = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
                    draw.polygon(vertices, fill="white")
                    translated_text = translate_client.translate(text.description, target_language='zh-TW')['translatedText']
                    draw.text((vertices[0][0], vertices[0][1]), translated_text, fill="black", font=font)

                base_filename = os.path.splitext(filename)[0]  # 不包含副檔名的檔名
                output_path = os.path.join(output_folder, base_filename + ".png")
                img.save(output_path)
                processed_files += 1
                print(f"Processed {processed_files}/{total_files} files...")

if __name__ == "__main__":
    input_folder = "/Users/georgewang/dev/PythonDev/MangaTranslate/raw"  # 生肉路徑
    output_folder = "/Users/georgewang/dev/PythonDev/MangaTranslate/cooked"  # 熟肉路徑
    translate_images(input_folder, output_folder)
