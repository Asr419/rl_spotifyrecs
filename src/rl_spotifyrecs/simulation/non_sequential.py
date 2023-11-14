from rl_spotifyrecs.spotify_data.data import DataLoader
from rl_spotifyrecs.user_model.spotify_cwm import CWM
import torch.optim as optim
import torch
import random


EPOCH = 10
BATCH_SIZE = 256
NUM_ITEM_FEATURES = 8
# DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DEVICE = torch.device("cpu")
LR = 0.001
if __name__ == "__main__":
    non_sequential = CWM(
        input_size=6 * NUM_ITEM_FEATURES,
        output_size=1,
    ).to(DEVICE)
    historic_users = DataLoader.UserSessions()
    music_columns = [
        "acousticness",
        "beat_strength",
        "bounciness",
        "danceability",
        "energy",
        "liveness",
        "speechiness",
        "valence",
    ]
    response_columns = ["skip_2"]
    criterion = torch.nn.SmoothL1Loss()
    optimizer = optim.Adam(non_sequential.parameters(), lr=LR)
    optimizer.zero_grad()


for i in range(0, EPOCH):
    tensor_train = torch.empty(0)
    tensor_pred = torch.empty(0)
    batch_sample = random.sample(historic_users, BATCH_SIZE)
    for j in range(0, len(batch_sample)):
        (
            context_feature_tensor,
            action_feature_tensor,
            res_feature_tensor,
        ) = DataLoader.Feature_Vector(batch_sample, music_columns, response_columns, j)

        y_pred = non_sequential.compute_prob(
            context_feature_tensor, action_feature_tensor
        )
        if tensor_train.numel == 0:
            tensor_train = res_feature_tensor
        else:
            tensor_train = torch.cat([tensor_train, res_feature_tensor], dim=0)
        if tensor_pred.numel == 0:
            tensor_pred = y_pred
        else:
            tensor_pred = torch.cat([tensor_pred, y_pred], dim=0)
    loss = criterion(tensor_pred, tensor_train)
    loss.backward()
    optimizer.step()
