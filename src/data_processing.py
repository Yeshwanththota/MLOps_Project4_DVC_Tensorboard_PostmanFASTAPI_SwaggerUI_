import os
import cv2
import torch
import numpy as np
from torch.utils.data import Dataset
from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

class GunData(Dataset):

    def __init__(self,root:str,device:str="cpu"):
        self.image_path = os.path.join(root,"Images")
        self.labels_path = os.path.join(root,"Labels")
        self.device = device

        self.img_name = sorted(os.listdir(self.image_path))
        self.label_name = sorted(os.listdir(self.labels_path))

        logger.info("dataprocessing: gun dataset loaded")
    def __getitem__(self,idx):
        try:
            logger.info("loading data for indes idx: {}".format(idx))
            image_path =  os.path.join(self.image_path , str(self.img_name[idx]))
            image = cv2.imread(image_path)
            img_rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB).astype(np.float32)

            img_res = img_rgb/255
            img_res = torch.as_tensor(img_res).permute(2,0,1)

            label_name  = self.img_name[idx].rsplit('.',1)[0]+ ".txt"
            label_path = os.path.join(self.labels_path , str(label_name))

            if not os.path.exists(label_path):
                raise FileNotFoundError(f"Label file not found: {label_path}")
            
            target = {
                "boxes": torch.tensor([]), 
                "area": torch.tensor([]),
                "image_id": torch.tensor([idx]),
                "labels": torch.tensor([], dtype=torch.int64)
            }
            with open(label_path,"r") as label_file:
                l_count = int(label_file.readline())
                box=[list(map(int, label_file.readline().split())) for _ in range(l_count)]
            
            if box:
                area = [(b[2] - b[0]) * (b[3] - b[1]) for b in box]
                labels = [1]*len(box)
                

         

                target["boxes"] = torch.tensor(box, dtype=torch.float32)
                target["area"] =  torch.tensor(area, dtype=torch.float32)

                target["labels"] = torch.tensor(labels, dtype=torch.int64)

            img_res = img_res.to(self.device)
            for key in target:
               
                    target[key] = target[key].to(self.device)

            return img_res,target

        except Exception as e:
            logger.error(f"Error loading data for index {idx}: {e}")
            raise CustomException(f"Error loading data for index {idx}: {e}")
    def __len__(self):
        return len(self.img_name)
if __name__ == "__main__":
    root = "artifacts/raw"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dataset = GunData(root, device)
    image, target = dataset[0]
    print(f"Image shape: {image.shape}")
    print(f"Target: {target.keys()}")
    print("bounding boxes:", target["boxes"])