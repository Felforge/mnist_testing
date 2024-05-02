from torchvision.transforms import ToTensor, Grayscale
from learning_functions import Net
from PIL import Image as im
import gradio as gr
import torch
import cv2

# Look at this link and make my own API whenever
# https://github.com/fastai/tinypets/tree/master

TITLE = "MNIST Digit Identifier"
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
NEURAL_NET = Net().to(DEVICE)
NEURAL_NET.load_state_dict(torch.load('digit_identifier.pth'))
NEURAL_NET.eval()

def predict(model):
    """_summary_
    Returns prediciton from inputted model
    Args:
        model (pickle file): Learner class produced in notebook
    """
    def predict_inner(sketch_image):
        data = sketch_image['composite']
        # #data = im.fromarray(sketch_image['composite'])
        #data = cv2.resize(data, (28, 28))
        data = im.fromarray(data)
        data = data.resize((28, 28))
        data = data.convert("LA")
        # image_tensor = ToTensor()(grayscale_image).unsqueeze(0)
        image_tensor = ToTensor()(data)
        # image_tensor = image_tensor.shape[0][0]
        # return image_tensor
        # print(image_tensor.shape)
        # # image_tensor = image_tensor.reshape([1, 1, 28, 28])
        # # image_tensor = torch.tensor(grayscale_image, dtype=torch.float32).unsqueeze(0) / 255.
        print(image_tensor.shape)
        with torch.no_grad():
            output = model(image_tensor.to(DEVICE))
        print(output)
        prediction = output.argmax(dim=1, keepdim=True).item()
        return {prediction: 1.}
    return predict_inner

label = gr.Label()
sketchpad = gr.Sketchpad()

iface = gr.Interface(fn=predict(NEURAL_NET), inputs=sketchpad, outputs=label, title=TITLE)
iface.launch()
