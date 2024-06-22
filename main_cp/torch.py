import torch
import torchvision.models as models

model = models.vgg19_bn(pretrained=False)
state_dict = torch.load('path_to_your_model.pth')
model.load_state_dict(state_dict)

model.eval()

test_input = torch.randn(1, 3, 224, 224)
output = model(test_input)