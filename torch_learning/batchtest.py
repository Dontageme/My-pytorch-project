import torch
import torch.nn as nn
import torchvision
from torchvision import transforms, utils
import matplotlib.pyplot as plt
import os
import numpy as np
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
from torchvision.utils import save_image
from torch.utils.data import Dataset, DataLoader


###quantity data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.tensorboard import SummaryWriter
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing

def min_max_normalize(my_matrix):
    scaler = MinMaxScaler()
    scaler.fit(my_matrix)
    my_matrix_normorlize=scaler.transform(my_matrix)
    return my_matrix_normorlize

def normalize(my_matrix):
    scaler = preprocessing.StandardScaler().fit(my_matrix)
    my_matrix_normorlize=scaler.transform(my_matrix)
    return my_matrix_normorlize

###encode list
path='D:/PYTHON/螺桿單元'
img_data = torchvision.datasets.ImageFolder(path,
                                            transform=transforms.Compose([
                                                transforms.Scale(32),
                                                transforms.CenterCrop(28),
                                                transforms.ToTensor(),
                                                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
                                                ])
                                            )

print(img_data.imgs)
#print(len(img_data))
#print(len(data_loader))
print(img_data.class_to_idx)

img_loader = torch.utils.data.DataLoader(img_data, batch_size=30, num_workers=0,shuffle=False)

images,labels=next(iter(img_loader))
print(images.shape)
print(labels.shape)


classes=[
    'kL1-50-4', 'kL2-50-4', 'kL3-50-4', 'kR1-50-4', 'kR2-50-4', 'kR3-50-4',\
    'mL1c-50-15', 'mL1r-50-15', 'mL1t-50-15', 'mL2c-50-15', 'mL2r-50-15',\
    'mL2t-50-15', 'mL3c-50-15', 'mL3r-50-15', 'mL3t-50-15', 'mR1c-50-15',\
    'mR1r-50-15', 'mR1t-50-15', 'mR2c-50-15', 'mR2r-50-15', 'mR2t-50-15',\
    'mR3c-50-15', 'mR3r-50-15', 'mR3t-50-15', 'sL1-50-33', 'sL2-50-33',\
    'sL3-50-33', 'sR1-50-33', 'sR2-50-33', 'sR3-50-33'
]

def imshow(img):
    img = img.permute(1,2,0)
    img = torch.clamp(img,0,1)
    plt.imshow(img)
   
dataiter = iter(img_loader)
images, labels = dataiter.next()

encode_list={}
i=0
for item in classes:
    encode_list[item]=images.numpy()[i]
    i += 1

#print(encode_list)
def text_to_encode(item):
#     tmp = item.split('-')
    onehot_data = encode_list[item]
    return onehot_data

def matplotlib_imshow(img, one_channel=False):
    if one_channel:
        img = img.mean(dim=0)
    npimg = img.numpy()
    if one_channel:
        plt.imshow(npimg, cmap="Greys")
    else:
        plt.imshow(np.transpose(npimg, (1, 2, 0)))

def to_img(x):
    #x = 0.5 * (x + 1)
    x = x.clamp(0, 1)
    x = x.view(x.size(0), 3, 28, 28)
    return x


columns = ['Rotation_speed','Total_rate','one','two','three','RTD','Temperature']
train =pd.read_csv('D:/PYTHON/train_data.csv', names=columns)
#train=train.sample(frac=1)
train.head()
train.Temperature=pd.to_numeric(train.Temperature)
train.RTD=pd.to_numeric(train.RTD)
train2=pd.DataFrame(train, copy=True)

#Part4
### normalize speed
speed = np.array([train.Rotation_speed.values],dtype = np.float32).transpose(1,0)
print(speed.shape)
speed_min = min_max_normalize(speed)
print(speed_min[:4])
speed_nor = normalize(speed)
train.Rotation_speed=speed_min
# print(speed_nor[:4])

### normalize total rate
Total_rate = np.array([train.Total_rate.values],dtype = np.float32).transpose(1,0)
print(Total_rate.shape)
Total_rate_min = min_max_normalize(Total_rate)
print(Total_rate_min[:4])
Total_rate_nor = normalize(Total_rate)
train.Total_rate=Total_rate_min


### normalize RTD

RTD = np.array([train.RTD.values],dtype = np.float32).transpose(1,0)
RTD_min = min_max_normalize(RTD)
RTD_nor = normalize(RTD)
train.RTD=RTD_min


### normalize Temp
Temperature = np.array([train.Temperature.values],dtype = np.float32).transpose(1,0)
Temperature_min = min_max_normalize(Temperature)
Temperature_nor = normalize(Temperature)
train.Temperature=Temperature_min

train_one = np.array(train.one.values)
train_two = np.array(train.two.values)
train_three = np.array(train.three.values)

# test_one = np.concatenate((test.one.values,test.two.values,test.three.values))

#Part6
### prepare the training data
#quantity = np.concatenate((speed_nor,Total_rate_nor),1)
#print(quantity.shape)
# (3140,2)
train_y = np.concatenate((np.array([train.RTD.values]).transpose(1,0),
                         np.array([train.Temperature.values]).transpose(1,0)),axis = 1)

#print(train_y.shape)
# (3140,2)
def split_dataframe(df, chunk_size = 400): 
    chunks = list()
    num_chunks = len(df) // chunk_size + 1
    for i in range(num_chunks):
        chunks.append(df[i*chunk_size:(i+1)*chunk_size])
    return chunks

b=split_dataframe(train2)  #string
print(str(b[0].one))
print(type(str(b[0].one)))


'''
#meta_data = [] #存放标签
label1=b[0].one.values.tolist()
print(len(label1))
label2=b[0].two.values.tolist()
label3=b[0].three.values.tolist()


label1=label1+label2
label1=label1+label3   
print('meta3:',len(label1))
'''



for i in range(len(train_one)):
    train.one[i] = np.array(text_to_encode(train_one[i]))
    train.two[i] = np.array(text_to_encode(train_two[i]))
    train.three[i] = np.array(text_to_encode(train_three[i]))

#print(train)
#print(train.info())
#print(type(train))
#print(train.one[2])

a=split_dataframe(train)  #array
#print(type(a[0]))




###CNN model
class CNNAE(nn.Module):
    def __init__(self):
        super(CNNAE, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 16, 3, stride=3, padding=1),  #(16,10,10)
            nn.BatchNorm2d(16),
            nn.Tanh(),
            nn.MaxPool2d(2, stride=2)
        )  # (16,5,5)
        self.conv2 = nn.Sequential(
            nn.Conv2d(16, 3, 3, stride=2, padding=1),  # (1,3,3)
            nn.BatchNorm2d(3),
            nn.Tanh(),
            nn.MaxPool2d(2, stride=1)  #(1,2,2)
        )
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(3, 16, 3, stride=2),  # (16,5,5)
            nn.BatchNorm2d(16),
            nn.Tanh(),
            nn.ConvTranspose2d(16, 8, 5, stride=3, padding=1),  # (8,15,15)
            nn.BatchNorm2d(8),
            nn.Tanh(),
            nn.ConvTranspose2d(8, 3, 2, stride=2, padding=1),  # (3,28,38)
            nn.BatchNorm2d(3),
            nn.Tanh()
            
          
        )

    def forward(self, x):
        feature_map= self.conv1(x)
        encode = self.conv2(feature_map)
        encode2=torch.reshape(encode,(-1,4))
        decode = self.decoder(encode)
        return feature_map, encode, decode

### NN model
class Extrader(nn.Module):
    def __init__(self):
        super(Extrader, self).__init__()
        # 压缩
        self.model = nn.Sequential(
            nn.Linear(38, 64),
            nn.Dropout(0.5),
            nn.Tanh(),
            nn.Linear(64, 64),#
            nn.Dropout(0.5),
            nn.Tanh(),
            nn.Linear(64, 64),#
            nn.Dropout(0.5),
            nn.Tanh(),#
            nn.Linear(64, 1),   # 压缩成3个特征, 进行 3D 图像可视化
        )
        
    def forward(self, x):
        return(self.model(x))


###Combine Model
class IntegratedModel(nn.Module):
    def __init__(self):
        super(IntegratedModel, self).__init__()
        self.CNNAE = CNNAE()
        #self.CNNAE.load_state_dict(torch.load('D:/PYTHON/  CNNstd_rtd.pth'))
        self.extrater = Extrader()
        
    def forward(self, m1,m2,m3, quantity):
        feature1,encoded_1,decoded_1 = self.CNNAE(m1)
#         print(encoded_1.shape)
        feature2,encoded_2,decoded_2 = self.CNNAE(m2)
        feature3,encoded_3,decoded_3 = self.CNNAE(m3)
#         print(quantity[0,0].shape)
        e1=torch.reshape(encoded_1,(-1,12))
        e2=torch.reshape(encoded_2,(-1,12))
        e3=torch.reshape(encoded_3,(-1,12))

        input_value = torch.cat((e1, e2, e3,quantity),1)
#         print(input_value.shape)
        out = self.extrater(input_value)
        return e1,e2,e3,decoded_1,decoded_2,decoded_3,out




###Training Process
model = IntegratedModel()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=1e-5)
EPOCH = 101
loss_func = nn.MSELoss()
writer = SummaryWriter('rtd_batch5/NN_result')

for epoch in range(EPOCH):
    meta_data = [] #存放标签
    features = torch.zeros(0)  #PCA用
    model.train()
    for i in range(7):
        targetR = torch.FloatTensor(a[i].RTD.array).view(-1,1).detach()
        m1 = torch.FloatTensor(a[i].one.array)
        m2 = torch.FloatTensor(a[i].two.array)
        m3 = torch.FloatTensor(a[i].three.array)
        q1=torch.FloatTensor(a[i].Rotation_speed.array).view(-1,1)
        q2=torch.FloatTensor(a[i].Total_rate.array).view(-1,1)
        quantity=torch.cat([q1,q2],axis=1)

        #input_value = torch.cat((e11, e22, e33,quantity),1)
        #print(input_value.shape)


        e1,e2,e3,d1,d2,d3,out= model(m1,m2,m3,quantity)
        loss1 = loss_func(d1, m1) + loss_func(d2, m2) + loss_func(d3, m3)
        loss2= loss_func(out,targetR)
        loss= 1*loss1+ 1*loss2
         # apply gradients

        optimizer.zero_grad()               # clear gradients for this training step
        loss.backward()                     # backpropagation, compute gradients
        optimizer.step()     

        print('epoch [{}/{}],batch[{}/{}], cnn_loss:{:.4f}, nn_loss:{:.4f}'
          .format(epoch, EPOCH, i+1 , 7, loss1.item(),loss2.item()))

        features = torch.cat((features, e1))
        features = torch.cat((features, e2))
        features = torch.cat((features, e3))
        label1=b[i].one.values.tolist()
        label2=b[i].two.values.tolist()
        label3=b[i].three.values.tolist()
        meta_data = meta_data + label1 +label2 + label3
        #print(len(meta_data))

    

    if epoch % 10 == 0:
        for i in range(1):
            for i, (img, labels) in enumerate(img_loader):
    # ===================forward=====================
                feature,encoded,decoded = model.CNNAE(img)

            pic = to_img(decoded.data)
            save_image(pic, './img8/image_{}.png'.format(epoch))
    
    


    writer.add_embedding(features, metadata=meta_data, global_step=epoch)
    writer.add_scalar('CNNAE_loss', loss1, epoch)
    writer.add_scalar('MSE_loss', loss2, epoch)

    model.eval()

    targetR = torch.FloatTensor(a[7].RTD.array).view(-1,1).detach()
    m1 = torch.FloatTensor(a[7].one.array)
    m2 = torch.FloatTensor(a[7].two.array)
    m3 = torch.FloatTensor(a[7].three.array)
    q1=torch.FloatTensor(a[7].Rotation_speed.array).view(-1,1)
    q2=torch.FloatTensor(a[7].Total_rate.array).view(-1,1)
    quantity=torch.cat([q1,q2],axis=1)

        #input_value = torch.cat((e11, e22, e33,quantity),1)
        #print(input_value.shape)


    e1,e2,e3,d1,d2,d3,out= model(m1,m2,m3,quantity)
    loss1 = loss_func(d1, m1) + loss_func(d2, m2) + loss_func(d3, m3)
    loss2= loss_func(out,targetR)

    loss= 1*loss1+ 1*loss2
         # apply gradients

    optimizer.zero_grad()               # clear gradients for this training step
    loss.backward()                     # backpropagation, compute gradients
    optimizer.step()     
    print('epoch [{}/{}],batch[{}/{}], val_cnn_loss:{:.4f}, val_nn_loss:{:.4f}'
          .format(epoch, EPOCH, 7 , 7, loss1.item(),loss2.item()))


    writer.add_scalar('val_MSE_loss', loss2, epoch)
writer.close()

torch.save(model.state_dict(), './rtd_batch5.pth')
#tensorboard --logdir=runs
#http://localhost:6006/
