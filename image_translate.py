import os
from google.cloud import vision
from google.cloud import vision_v1
from google.cloud import translate_v2 as translate

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

                # 翻譯文字
                translated_text = translate_client.translate(texts[0].description, target_language='zh-TW')['translatedText']

                # 儲存翻譯結果
                base_filename = os.path.splitext(filename)[0]  # 不包含副檔名的檔名
                output_path = os.path.join(output_folder, base_filename + ".txt")
                with open(output_path, 'w') as output_file:
                    output_file.write(translated_text)

                processed_files += 1
                print(f"Processed {processed_files}/{total_files} files...")

if __name__ == "__main__":
    input_folder = "/Users/georgewang/dev/PythonDev/MangaTranslate/raw" # 生肉路徑
    output_folder = "/Users/georgewang/dev/PythonDev/MangaTranslate/cooked" # 熟肉路徑
    translate_images(input_folder, output_folder)
