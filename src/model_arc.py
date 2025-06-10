import torch
from torch.optim import Adam
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from tqdm import tqdm
from src.data_processing import GunData
from src.logger import get_logger
from src.custom_exception import CustomException



logger = get_logger(__name__)
class FasterRCNNModel:
    def __init__(self, num_classes=2,device=None):
        self.num_classes = num_classes
        self.device = device
        self.optimizer = None
        self.model = self.create_model().to(self.device)
        logger.info("Initializing FasterRCNNModel with num_classes: {}".format(num_classes))
    def create_model(self):
        try:
            model = fasterrcnn_resnet50_fpn(pretrained=True)
            in_features = model.roi_heads.box_predictor.cls_score.in_features

            model.roi_heads.box_predictor = FastRCNNPredictor(in_features , self.num_classes)

            return model
        except Exception as e:
            logger.error("Error in create_model: {}".format(e))
            raise CustomException("Error in create_model: {}".format(e))
        
    def compile(self, learning_rate=0.0001):
        try:
            self.optimizer = Adam(self.model.parameters(), lr=learning_rate)
            logger.info("Model compiled with learning rate: {}".format(learning_rate))
        except Exception as e:
            logger.error("Error in compile: {}".format(e))
            raise CustomException("Error in compile: {}".format(e))
    def train(self,train_loader,num_epochs=10):
        try:
            self.model.train()
            for epoch in range(num_epochs):
                total_loss = 0
                logger.info(f"Starting epoch {epoch+1}/{num_epochs}")
                for images, targets in tqdm(train_loader, desc=f"Epoch {epoch+1}"):
                    images = [image.to(self.device) for image in images]
                    targets = [{k: v.to(self.device) for k, v in t.items()} for t in targets]

                    loss_dict = self.model(images, targets)
                    losses = sum(loss for loss in loss_dict.values())

                    self.optimizer.zero_grad()
                    losses.backward()
                    self.optimizer.step()

                    total_loss += losses.item()

                logger.info(f"Epoch {epoch+1}/{num_epochs}, Loss: {total_loss/len(train_loader)}")
        except Exception as e:
            logger.error("Error in train: {}".format(e))
            raise CustomException("Error in train: {}".format(e))