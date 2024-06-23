import torch
import torchvision.models as models

# VGG19モデルを定義し、出力サイズを16に変更
model = models.vgg19_bn(pretrained=False)
model.classifier[6] = torch.nn.Linear(in_features=4096, out_features=16)

# モデルの状態をロード
state_dict = torch.load('model/epoch24.pth', map_location=torch.device('cpu'))
model.load_state_dict(state_dict)

# 評価モードに設定
model.eval()

# テスト入力を作成
test_input = torch.randn(1, 3, 224, 224)

# モデルを実行し、出力を取得
output = model(test_input)

# 出力を表示
print(output)
