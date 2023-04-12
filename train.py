
# import modules
import torch
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('dark_background')
from architecture import *
from plot_fct import *



if torch.cuda.is_available():
    device = "cuda" 
else:
    raise('No GPU !')

date = datetime.now().strftime("%m_%d_%H:%M_")

# load data

data_path = "/usr/home/mwemaere/neuro/Data/"
ssh3 = torch.load(data_path + "SSH_MERCATOR_1%3.pt")
ssh6 = torch.load(data_path + "SSH_MERCATOR_1%6.pt")[:,:,:134]
ssh12 = torch.load(data_path + "SSH_MERCATOR_1%12.pt")[:,:,:268]
sst6 = torch.load(data_path + "SST_MERCATOR_1%6.pt")[:,:,:134]
sst12 = torch.load(data_path + "SST_MERCATOR_1%12.pt")[:,:,:268]
u12 = torch.load(data_path + "U_MERCATOR_1%12.pt")[:,:,:268]
v12 = torch.load(data_path + "V_MERCATOR_1%12.pt")[:,:,:268]


ssh3 = torch.unsqueeze(ssh3,1)
ssh6 = torch.unsqueeze(ssh6,1)
ssh12 = torch.unsqueeze(ssh12,1)
sst6 = torch.unsqueeze(sst6,1)
sst12 = torch.unsqueeze(sst12,1)
u12 = torch.unsqueeze(u12,1)
v12 = torch.unsqueeze(v12,1)

# prepare data
train_loader,valid_loader,test_loader = prepare_loaders(ssh3,ssh6,ssh12,sst6,sst12,u12,v12)

# create model
model = RESAC_MERCATOR()


if False:
    saved_path = '/usr/home/mwemaere/neuro/resac_mercator/Save/04_11_18:16_model.pth'
    model.load_state_dict(torch.load(saved_path))
    model = model.to(device)


if True:


    # training 
    lr = 5e-5
    optimizer = torch.optim.Adam(model.parameters(),lr=lr)
    #scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, custom_scheduler)
    criterion = RMSELoss()
    num_epochs = 30

    train_accuracy, valid_accuracy = train_resac(model, device, optimizer, criterion, train_loader,valid_loader, num_epochs, scheduler=False)


    #save model weights
    save_path = "/usr/home/mwemaere/neuro/resac_mercator/Save/"
   
    torch.save(model.state_dict(), save_path+date+'model.pth')

    #display loss
    plot_train_loss(train_accuracy,save_path,date)
    plot_valid_loss(valid_accuracy,save_path,date)





# Test
mean,std, l_im = test_resac(model,test_loader,device, get_im=[15,58,245])


print(mean)
print(std)
with open('test_result.txt', 'a') as f:
    f.write('\n'+date+'\n')
    f.write(str(mean)+'\n')
    f.write(str(std)+'\n')

    f.close()
plot_test_uv(l_im)
plot_test_ssh(l_im)
