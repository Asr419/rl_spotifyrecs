import os
import random as rand
from math import sqrt
from typing import Optional

import gymnasium as gym
import numpy as np
import random
import numpy.typing as npt
import pandas as pd
import torch
from pathlib import Path

from rl_spotifyrecs.spotify_data.data import DataLoader
from rl_spotifyrecs.user_model.spotify_cwm import CWM

base_path = Path.home() / Path(os.environ.get("DATA_PATH"))
RUN_BASE_PATH = Path(f"spotify_model")
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
NUM_ITEM_FEATURES = 8
CWM = torch.load(base_path / RUN_BASE_PATH / Path("model.pt"))


class SpotifyGym(gym.Env):
    def __init__(
        self,
        device: torch.device = torch.device("cpu"),
    ) -> None:
        self.data_loder = DataLoader
        self.device = device
        self.user_model = CWM

        # initialized by reset
        self.candidate_actions: torch.Tensor
        self.candidate_response: torch.Tensor

    def step(self, action: torch.Tensor):
        # select from the slate on item following the user choice model
        present_state = self.curr_user
        response = self.user_model.compute_prob(
            self.curr_user, action, use_training_net=True
        )
        updated_user = self.curr_user[NUM_ITEM_FEATURES:]
        self.curr_user = torch.cat([updated_user, action])
        info = {}

        return (
            present_state,
            action,
            self.curr_user,
            response,
            False,
            info,
        )

    def reset(self) -> None:
        # 1) sample user
        historic_users = self.data_loader.UserSessions()
        user = random.sample(historic_users, 1)
        (
            user,
            self.candidate_actions,
            self.candidate_response,
        ) = self.data_loader.Feature_Vector(user, music_columns, response_columns, 0)
        self.curr_user = user
        return self.curr_user, self.candidate_actions, self.candidate_response

    def render(self):
        raise NotImplementedError()
