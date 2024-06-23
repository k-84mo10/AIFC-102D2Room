import torch
import torchvision.models as models
import os
from torchvision import transforms
from PIL import Image

class MachineLearning:
    def __init__ (self):
        self.model = models.vgg19_bn(pretrained=False)
        self.model.classifier[6] = torch.nn.Linear(in_features=4096, out_features=16)
        state_dict = torch.load('model/epoch24.pth', map_location=torch.device('cpu'))
        self.model.load_state_dict(state_dict)
        self.model.eval()

    def get_latest_image_path(self):
        directory = 'test'
        files = os.listdir(directory)
        if not files:
            return -1
        else:
            latest_image = os.path.join(directory, files[-1])
            return latest_image
    
    def test_image(self, image_path):
        state_list = [
            "0000",
            "0001",
            "0010",
            "0011",
            "0100",
            "0101",
            "0110",
            "0111",
            "1000",
            "1001",
            "1010",
            "1011",
            "1100",
            "1101",
            "1110",
            "1111",
        ]

        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(0.5, 0.5),
        ])

        if not os.path.exists(image_path):
            return -1

        try:    
            image = Image.open(image_path)
            image_tensor = transform(image)
            image_tensor = image_tensor.unsqueeze(0)       
            
            output = self.model(image_tensor)
            predicted_test = torch.max(output, 1)[1]
            value = predicted_test.item()

            return state_list[value]
        except Exception as e:
            return -1
        