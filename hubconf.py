# -*- coding: utf-8 -*-
"""islexam007.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZLYjwYFgL9JsMCRrVHTtpHQ9yhc4HrQ_
"""

# exercise 1 based on lsl lab on wed.. 26/oct/

import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor

device="cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

classes = [
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot",
]

# Define model

class cs21m007nn(nn.Module):
    def __init__(self,num_classes=10):
        super(cs21m007nn, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=5, padding=2),
            nn.RelU()
            nn.MaxPool2d(2))
        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(2))
        self.fc = nn.Linear(7*7*32, 10)
        
    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.fc(out)
        return out

    
# Define model simle model 
class cs21m007nn_simple(nn.Module):
    def __init__(self):
        super().__init__()
        self.A = nn.Flatten()
        self.B=nn.Linear(28*28,10)
        self.C=softmax()
        

    def forward(self, x):
        x = self.A(x)
        x=self.B(x)
        x=self.C(x)
        return x
    
    
def get_lossfn_and_optimizer(mymodel):
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(mymodel.parameters(), lr=1e-3)
    return loss_fn, optimizer

def load_data():

    # Download training data from open datasets.
    # using cifar10 dataset...
    training_data = datasets.mnist(
        root="data",
        train=True,
        download=True,
        transform=ToTensor(),
    )

    # Download test data from open datasets.
    test_data = datasets.mnist(
        root="data",
        train=False,
        download=True,
        transform=ToTensor(),
    )
    
    return training_data, test_data

def create_dataloaders(training_data, test_data, batch_size=64):

    # Create data loaders.
    train_dataloader = DataLoader(training_data, batch_size=batch_size)
    test_dataloader = DataLoader(test_data, batch_size=batch_size)

    for X, y in test_dataloader:
        print(f"Shape of X [N, C, H, W]: {X.shape}")
        print(f"Shape of y: {y.shape} {y.dtype}")
        break
        
    return train_dataloader, test_dataloader

def get_model():
    
    model = cs21m007nn().to(device)

    return model

def _train(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    model.train()
    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)

        # Compute prediction error
        pred = model(X)
        loss = loss_fn(pred, y)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch % 100 == 0:
            loss, current = loss.item(), batch * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")

def _test(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")

def train(train_dataloader, test_dataloader, model1, loss_fn1, optimizer1, epochs=5):
    for t in range(epochs):
        print(f"Epoch {t+1}\n-------------------------------")
        _train(train_dataloader, model1, loss_fn1, optimizer1)
        _test(test_dataloader, model1, loss_fn1)
    print("Done!")
    return model1





def sample_test(model1, test_data):
    model1.eval()
    x, y = test_data[0][0], test_data[0][1]
    with torch.no_grad():
        pred = model1(x)
        predicted, actual = classes[pred[0].argmax(0)], classes[y]
        print(f'Predicted: "{predicted}", Actual: "{actual}"')

        
        
def cross_entropy(y,y_predicted):
  loss=-np.sum(y*np.log(y_predicted))
  return loss/float(y_predicted.shape[0])


def softmax(x):
  return np.exp(x)/np.sum(np.exp(x),axis=0)
