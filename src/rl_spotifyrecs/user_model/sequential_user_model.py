from rl_spotifyrecs.spotify_data.data import Spotify
from rl_spotifyrecs.user_model.lstm import LSTMCWM
import torch.optim as optim
import torch
import random
import os
import requests
from dotenv import load_dotenv
from rl_spotifyrecs.utils import save_run_lstm
from tqdm import tqdm

load_dotenv()
if __name__ == "__main__":
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
    response_columns = ["not_skipped"]

    EPOCH = 20
    BATCH_SIZE = 20

    NUM_ITEM_FEATURES = 8
    # DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    DEVICE = torch.device("cpu")
    LR = 0.001
    sequential = LSTMCWM(
        input_size=6 * NUM_ITEM_FEATURES,
        output_size=1,
        hidden_sizes=[48, 30, 25],
        BATCH_SIZE=BATCH_SIZE,
    ).to(DEVICE)
    criterion = torch.nn.MSELoss()
    optimizer = optim.Adam(sequential.parameters(), lr=LR)
    optimizer.zero_grad()

    for i in range(0, EPOCH):
        context_tensor = torch.empty(0)
        action_tensor = torch.empty(0)
        tensor_train = torch.empty(0)
        # tensor_pred=torch.empty(0)
        batch_sample = random.sample(historic_users, BATCH_SIZE)
        for j in range(0, len(batch_sample)):

            context_feature_tensor, action_feature_tensor, res_feature_tensor = (
                Spotify.Feature_Vector(batch_sample, music_columns, response_columns, j)
            )

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
                tensor_train = torch.cat([tensor_train, res_feature_tensor])
            # if tensor_pred.numel==0:
            #     tensor_pred=y_pred
            # else:
            #     tensor_pred=torch.cat([tensor_pred,y_pred],dim=0)
        context_tensor = context_tensor.view(BATCH_SIZE, 15, 40)
        action_tensor = action_tensor.view(BATCH_SIZE, 15, 8)
        tensor_train = tensor_train.view(BATCH_SIZE, 15, 1)
        # print(context_tensor.shape)
        # print(action_tensor.shape)
        # print(tensor_train.shape)
        y_pred = sequential.compute_prob(context_tensor, action_tensor)
        # print(y_pred)
        tensor_train = tensor_train.float()
        loss = criterion(y_pred, tensor_train)
        print(loss)

        loss.backward()
        optimizer.step()
    directory = f"spotify_model"
    save_run_lstm(model=sequential, directory=directory)
