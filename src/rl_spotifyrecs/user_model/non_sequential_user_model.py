from rl_spotifyrecs.spotify_data.data import Spotify
from rl_spotifyrecs.user_model.spotify_cwm import CWM
import torch.optim as optim
import torch
import random
import os
import requests
from dotenv import load_dotenv
from rl_spotifyrecs.utils import save_run
from tqdm import tqdm

load_dotenv()

EPOCH = 25
BATCH_SIZE = 32
NUM_ITEM_FEATURES = 8
# DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DEVICE = torch.device("cpu")
LR = 0.005


if __name__ == "__main__":
    non_sequential = CWM(
        input_size=6 * NUM_ITEM_FEATURES,
        output_size=4,
    ).to(DEVICE)
    historic_users = Spotify.UserSessions()
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
    response_columns = ["skip_1", "skip_2", "skip_3", "not_skipped"]
    criterion = torch.nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(non_sequential.parameters(), lr=LR, weight_decay=1e-3)
    optimizer.zero_grad()
for i in tqdm(range(0, EPOCH)):
    context_tensor = torch.empty(0)
    action_tensor = torch.empty(0)
    tensor_train = torch.empty(0)
    # tensor_pred=torch.empty(0)
    batch_sample = random.sample(historic_users, BATCH_SIZE)
    for j in range(0, len(batch_sample)):
        (
            context_feature_tensor,
            action_feature_tensor,
            res_feature_tensor,
        ) = Spotify.Feature_Vector(batch_sample, music_columns, response_columns, j)
        context_feature_tensor = context_feature_tensor.repeat(
            (action_feature_tensor.shape[0], 1)
        )

        if tensor_train.numel() == 0:
            context_tensor = context_feature_tensor
            action_tensor = action_feature_tensor
        else:
            context_tensor = torch.cat([context_tensor, context_feature_tensor])
            action_tensor = torch.cat([action_tensor, action_feature_tensor])

        if tensor_train.numel() == 0:
            tensor_train = res_feature_tensor
        else:
            tensor_train = torch.cat([tensor_train, res_feature_tensor], dim=0)
        # if tensor_pred.numel==0:
        #     tensor_pred=y_pred
        # else:
        #     tensor_pred=torch.cat([tensor_pred,y_pred],dim=0)
    # context_tensor = context_tensor.view(BATCH_SIZE, 15, 40)
    # action_tensor = action_tensor.view(BATCH_SIZE, 15, 8)
    # tensor_train = tensor_train.view(BATCH_SIZE, 15, 1)
    y_pred = non_sequential.compute_prob(context_tensor, action_tensor, training=True)
    tensor_train = tensor_train.float()
    loss = criterion(y_pred, tensor_train)
    print(y_pred)
    print(loss)
    loss.backward()

    optimizer.step()
directory = f"spotify_model"
save_run(model=non_sequential, directory=directory)


# for i in range(0, EPOCH):
#     tensor_train = torch.empty(0)
#     tensor_pred = torch.empty(0)
#     batch_sample = random.sample(historic_users, BATCH_SIZE)
#     for j in range(0, len(batch_sample)):
#         (
#             context_feature_tensor,
#             action_feature_tensor,
#             res_feature_tensor,
#         ) = DataLoader.Feature_Vector(batch_sample, music_columns, response_columns, j)
#         context_feature_tensor = context_feature_tensor.repeat(
#             (action_feature_tensor.shape[0], 1)
#         )
#         y_pred = non_sequential.compute_prob(
#             context_feature_tensor, action_feature_tensor
#         )
#         if tensor_train.numel == 0:
#             tensor_train = res_feature_tensor
#         else:
#             tensor_train = torch.cat([tensor_train, res_feature_tensor], dim=0)
#         if tensor_pred.numel == 0:
#             tensor_pred = y_pred
#         else:
#             tensor_pred = torch.cat([tensor_pred, y_pred], dim=0)
#     loss = criterion(tensor_pred, tensor_train)
#     loss.backward()
#     optimizer.step()
