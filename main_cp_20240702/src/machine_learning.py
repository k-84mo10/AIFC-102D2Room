import torch
import torchvision.models as models
from torchvision import transforms
from PIL import Image


class MachineLearning:
    """Class for machine learning operations."""

    def __init__(self, model_path, model_type):
        """Initializes the model and loads the state dict.

        Args:
            model_path (str): Path to the model state dictionary.
            model_type (str): Type of the model to be used.
        """
        if model_type == "vgg19_bn":
            self.model = models.vgg19_bn(pretrained=False)
            self.model.classifier[6] = torch.nn.Linear(
                in_features=4096, out_features=16
            )
            state_dict = torch.load(model_path, map_location=torch.device("cpu"))
            self.model.load_state_dict(state_dict)
            self.model.eval()
            self.transform = transforms.Compose(
                [
                    transforms.Resize((224, 224)),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    transforms.Normalize(0.5, 0.5),
                ]
            )

    def inference(self, image_path):
        """Performs inference on an image.

        Args:
            image_path (str): Path to the input image.

        Returns:
            int: Predicted class index.
        """
        image = Image.open(image_path)
        image_tensor = self.transform(image)
        image_tensor = image_tensor.unsqueeze(0)
        output = self.model(image_tensor)
        predicted_test = torch.max(output, 1)[1]
        value = predicted_test.item()
        return value
