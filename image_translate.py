import os
from google.cloud import vision
from google.cloud import vision_v1

def translate_images(input_folder, output_folder):
    # 設定 Google Cloud Vision API 的認證金鑰路徑
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/georgewang/Documents/key/GCP_STUDY_TRANSLATE/fresh-bloom-293108-914e1d599383.json"

    client = vision.ImageAnnotatorClient()

    # 確保輸出資料夾存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍歷輸入資料夾中的所有圖片
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'rb') as image_file:
                content = image_file.read()
                image = vision_v1.Image(content=content)
                response = client.text_detection(image=image)
                texts = response.text_annotations

                # 儲存翻譯結果
                base_filename = os.path.splitext(filename)[0]  # 不包含副檔名的檔名
                output_path = os.path.join(output_folder, base_filename + ".txt")
                with open(output_path, 'w') as output_file:
                    output_file.write(texts[0].description)  # 使用整個圖片中的文字

if __name__ == "__main__":
    input_folder = "/Users/georgewang/dev/PythonDev/MangaTranslate/raw" # 生肉路徑
    output_folder = "/Users/georgewang/dev/PythonDev/MangaTranslate/cooked" # 熟肉路徑
    translate_images(input_folder, output_folder)
