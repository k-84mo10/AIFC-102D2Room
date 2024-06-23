import torch
import torchvision.models as models
import os
from torchvision import transforms
from PIL import Image

# VGG19モデルを定義し、出力サイズを16に変更
model = models.vgg19_bn(pretrained=False)
model.classifier[6] = torch.nn.Linear(in_features=4096, out_features=16)

# モデルの状態をロード
state_dict = torch.load('model/epoch24.pth', map_location=torch.device('cpu'))
model.load_state_dict(state_dict)

# 評価モードに設定
model.eval()

# 画像が保存されているディレクトリのパス
directory = 'test_image'

# ディレクトリ内のファイルを取得
files = os.listdir(directory)
image_files = [file for file in files if file.endswith(('.jpg', '.png', '.jpeg'))]

for image_filename in image_files:
    # ファイルのフルパスを作成
    image_path = os.path.join(directory, image_filename)

    # 画像を読み込み、テンソルに変換
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(0.5, 0.5),
    ])

    image = Image.open(image_path)
    image_tensor = transform(image)
    image_tensor = image_tensor.unsqueeze(0)  # バッチの次元を追加

    # モデルにテンソルを入力して予測を取得
    output = model(image_tensor)
    predicted_test = torch.max(output, 1)[1]
    value = predicted_test.item()

    # 出力を表示
    print(f"File: {image_filename}, Predicted Num: {predicted_test}, Predicted Class: {value}")
