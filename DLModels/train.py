import codecs, json
import numpy as np
import cv2
import torch
import torch.nn as nn
import os
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
import torch.optim as optim
import glob
import time
import matplotlib.pyplot as plt
from tqdm import tqdm as tqdm
from sklearn.model_selection import train_test_split

dir_cls = glob.glob("C:/Users/손찬우/Desktop/proj/proj_pill/pill_data/pill_data_croped/*")[:10]

list_json = []
list_image = []
list_label = []

for i in tqdm(range(len(dir_cls))):
    
    cls_name = dir_cls[i].split('\\')[-1]
    all_list_json = glob.glob(dir_cls[i] + '/*.json')
    all_list_image = glob.glob(dir_cls[i] + '/*.png')
    for j in range(len(all_list_json)):
        if all_list_json[j].split('\\')[-1].split('_')[4] == '1':
            list_json.append(all_list_json[j])
            list_image.append(all_list_image[j])
            list_label.append(i)

def read_dict_from_json(filejson):
    if not os.path.isfile(filejson) :
        return None
    with codecs.open(filejson, 'r', encoding='utf-8') as f:
        obj = json.load(f)
        return obj

def open_opencv_file(filename):
    img_array = np.fromfile(filename, np.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return image

#%%
class PillDataset(Dataset):
    def __init__(self, list_json, list_image, list_label, transform):

        self.json_path = list_json
        self.img_path = list_image
        self.label_path = list_label
        self.transform = transform

    def __len__(self):
        return len(self.label_path)

    def __getitem__(self, idx):
        json = self.json_path[idx]
        image_path = self.img_path[idx]
        label = self.label_path[idx]
        label = nn.functional.one_hot(torch.tensor(label), num_classes=100)
        dict_png_info = read_dict_from_json(json)
        pill_cls = dict_png_info['images'][0]['dl_mapping_code'] 
        pill_name = dict_png_info['images'][0]['dl_name'] 
        image = open_opencv_file(image_path)

        if self.transform:
            image = self.transform(image)
        return image, label, pill_name, pill_cls
    
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

j_train, j_valid, x_train, x_valid, y_train, y_valid = train_test_split(list_json, list_image, list_label, test_size=0.2, shuffle=True, stratify=list_label, random_state=34)
j_test, j_valid, x_test, x_valid, y_test, y_valid = train_test_split(j_valid, x_valid, y_valid, test_size=0.5, shuffle=True, stratify=y_valid, random_state=34)

train_dataset = PillDataset(j_train, x_train, y_train, transform)
valid_dataset = PillDataset(j_valid, x_valid, y_valid, transform)
test_dataset = PillDataset(j_test, x_test, y_test, transform)

batch_size = 5  # cpu
# batch_size = 100  # gpu

train_dataloader = DataLoader(train_dataset, shuffle=False,batch_size=batch_size, num_workers=0, drop_last=True, pin_memory=True)
valid_dataloader = DataLoader(valid_dataset, shuffle=False,batch_size=batch_size, num_workers=0, drop_last=True, pin_memory=True)
test_dataloader = DataLoader(test_dataset, shuffle=False,batch_size=batch_size, num_workers=0, drop_last=True, pin_memory=True)
#%%
class EarlyStopping:
    """주어진 patience 이후로 validation loss가 개선되지 않으면 학습을 조기 중지"""
    def __init__(self, patience=10, verbose=True, delta=0, path='checkpoints/checkpoint_' + '1' + '_best.pt'):
        """
        Args:
            patience (int): validation loss가 개선된 후 기다리는 기간
                            Default: 7
            verbose (bool): True일 경우 각 validation loss의 개선 사항 메세지 출력
                            Default: False
            delta (float): 개선되었다고 인정되는 monitered quantity의 최소 변화
                            Default: 0
            path (str): checkpoint저장 경로
                            Default: 'checkpoint.pt'
        """
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_loss_min = np.Inf
        self.delta = delta
        self.path = path

    def __call__(self, val_loss, model):

        score = -val_loss

        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
        elif score < self.best_score + self.delta:
            self.counter += 1
            print(f'EarlyStopping counter: {self.counter} out of {self.patience} \n')
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
            self.counter = 0

    def save_checkpoint(self, val_loss, model):
        '''validation loss가 감소하면 모델을 저장한다.'''
        if self.verbose:
            print(f'Validation loss decreased ({self.val_loss_min:.6f} --> {val_loss:.6f}).  Saving model ... \n')
        torch.save(model.state_dict(), self.path)
        self.val_loss_min = val_loss

#%%
import gc

torch.cuda.empty_cache()
gc.collect()
np.seterr(divide='ignore', invalid='ignore')

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("[INFO] training the network...")
startTime = time.time()
early_stopping = EarlyStopping()

################        # 재학습 시 주석 해제
# checkpoint = torch.load('checkpoints/checkpoint_' + '1' + '_last.pt')   # 마지막으로 저장된 checkpoint 파일 경로
model = models.resnet152(num_classes=len(np.unique(np.array(list_label))))
# model.load_state_dict(checkpoint['model_state_dict']) 
optimizer = optim.Adam(model.parameters(), lr=1e-3)
# optimizer.load_state_dict(checkpoint['optimizer_state_dict']) 
################

scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'max', factor=0.9, patience = 3)
criterion = nn.BCEWithLogitsLoss()

trainSteps = len(train_dataloader)
validSteps = len(valid_dataloader)
num_epochs = 100
# Initialize the lists for storing the loss, accuracy, and IoU values
train_loss = []
train_acc = []
train_miou = []
train_dice = []
val_loss = []
val_acc = []
val_miou = []
val_dice = []

for epoch in range(num_epochs):
    # Initialize the training and validation losses, accuracies, and IoUs
    running_train_loss = 0.0
    running_train_acc = 0.0
    running_val_loss = 0.0
    running_val_acc = 0.0
    #코랩에서 실행 시 2시간 리미트 대비용 코드

    model.train()
    for (x, y, n, c) in tqdm(train_dataloader, desc = f'Epoch: {epoch+1}'):
        # Forward pass
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        
        outputs = model(x)       
        preds = torch.sigmoid(outputs)
        loss = criterion(preds, y.float())
        
        loss.backward()
        optimizer.step()
        
        acc = (torch.argmax(preds) == torch.argmax(y)).sum().item()

        # Update the running losses, accuracies, and IoUs
        running_train_loss += loss.item() * x.size(0)
        running_train_acc += acc * x.size(0)
    
    model.eval()
    with torch.no_grad():
        for (x, y, n, c) in tqdm(valid_dataloader, desc = f'Epoch: {epoch+1}'):
            # Forward pass
            x, y = x.to(device), y.to(device)
            
            outputs = model(x)
            preds = torch.sigmoid(outputs)
            loss = criterion(preds, y.float())

            acc = (torch.argmax(preds) == torch.argmax(y)).sum().item()

            # Update the running losses, accuracies, and IoUs
            running_val_loss += loss.item() * x.size(0)
            running_val_acc += acc * x.size(0)            
         
    # Compute the average losses, accuracies, and IoUs for the epoch
    epoch_train_loss = running_train_loss / len(train_dataset)
    epoch_train_acc = running_train_acc / len(train_dataset)
    epoch_val_loss = running_val_loss / len(valid_dataset)
    epoch_val_acc = running_val_acc / len(valid_dataset)
    
    scheduler.step(epoch_val_loss)
    
    print("[INFO] EPOCH: {}/{}".format(epoch + 1, num_epochs))
    print("Train loss: {:.6f}, Validation loss: {:.6f}".format(epoch_train_loss, epoch_val_loss))
    print("Train Accuracy: {:.4f}, Validation Accuracy: {:.4f}".format(epoch_train_acc, epoch_val_acc))
    print("lr: {:5f}".format(optimizer.param_groups[0]['lr']))
    
    # Append the average losses, accuracies, and IoUs to the lists
    train_loss.append(epoch_train_loss)
    train_acc.append(epoch_train_acc)
    val_loss.append(epoch_val_loss)
    val_acc.append(epoch_val_acc)
    
    early_stopping(epoch_val_loss, model)
    
    if early_stopping.early_stop:
        print("Early stopping")
        break

torch.save(model.state_dict(), 'checkpoints/checkpoint_' + '1' + '_last.pt')
test_acc = 0
model.eval()
for (x, y, n, c) in tqdm(test_dataloader):
    x, y = x.to(device), y.to(device)
            
    outputs = model(x)
    preds = torch.sigmoid(outputs)
    acc = (torch.argmax(preds) == torch.argmax(y)).sum().item()

    # Update the running losses, accuracies, and IoUs
    test_acc += acc * x.size(0)            
    
final_acc = test_acc / len(test_dataset)


col_name = ['train_loss', 'train_accuracy', 'val_loss', 'val_accuracy']
history = list(map(list, zip(*[train_loss,train_acc,val_loss,val_acc])))
df_history = pd.DataFrame(history, columns=col_name)
df_history.to_csv('results/results_' + '1' + '.csv')
# display the total time needed to perform the training
endTime = time.time()
print("[INFO] total time taken to train the model: {:.2f}s".format(endTime - startTime))

def plot_results(result, metrics):
    
    path = 'output_reg/'
    if result == 0:
        category = 'loss/'
    else:
        category = 'acc/'
    
    plot_path = os.path.sep.join([path + category, "result_" + '1' + "_" + metrics + ".png"])
    plt.style.use("seaborn-paper")
    plt.figure()
    plt.plot(H["train_" + metrics], label = ("train_" + metrics))
    plt.plot(H["test_" + metrics], label = ("test_" + metrics))
    plt.title("Training " + metrics + " on " + "Regression")
    plt.xlabel("Epoch #")
    plt.ylabel(metrics)
    plt.legend(loc="lower left")
    plt.savefig(plot_path)
    
plot_results(0, 'Loss')
plot_results(1, 'Acc')

# %%
