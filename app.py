from torchvision.transforms import ToTensor
from learning_functions import Net
from PIL import Image as im
import gradio as gr
import torch

TITLE = "MNIST Digit Identifier"
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
NEURAL_NET = Net().to(DEVICE)
NEURAL_NET.load_state_dict(torch.load('mnist_identifier.pth'))
NEURAL_NET.eval()

def predict(model):
    """_summary_
    Returns prediciton from inputted model
    Args:
        model (pickle file): Learner class produced in notebook
    """
    def predict_inner(sketch_image):
        # Process input
        data = sketch_image['composite']
        data = im.fromarray(data)
        data = data.resize((28, 28))
        data = data.convert("LA")
        image_tensor = ToTensor()(data)
        image_tensor = image_tensor[1:,:,:].unsqueeze(0).to(DEVICE)

        # Get Predicition and Probabilities
        with torch.no_grad():
            output = model(image_tensor).sigmoid() - 0.5
        output_sum = torch.sum(output)
        probability_tensor = torch.round((output / output_sum), decimals=2)
        return_labels = {}
        for i in range(10):
            num = probability_tensor.data[0].data[i]
            if num != 0.:
                return_labels[i] = num
        return return_labels
    return predict_inner

label = gr.Label()
sketchpad = gr.Sketchpad()

iface = gr.Interface(fn=predict(NEURAL_NET), inputs=sketchpad, outputs=label, title=TITLE)
iface.launch()
