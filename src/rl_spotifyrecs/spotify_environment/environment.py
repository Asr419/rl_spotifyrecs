import random as rand
from math import sqrt
from typing import Optional

import gymnasium as gym
import numpy as np
import random
import numpy.typing as npt
import pandas as pd
import torch


from rl_spotifyrecs.spotify_data.data import Spotify


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
response_columns = ["skip_3", "not_skipped"]
NUM_ITEM_FEATURES = 8


class SpotifyGym(gym.Env):
    def __init__(
        self,
        device: torch.device = torch.device("cpu"),
    ) -> None:
        self.data_loader = Spotify
        self.device = device

        # initialized by reset
        self.candidate_actions: torch.Tensor
        self.candidate_response: torch.Tensor

    def step(self, user_state: torch.Tensor, action: torch.Tensor, user_model):
        # select from the slate on item following the user choice model
        present_state = user_state
        response = user_model.compute_prob(user_state, action, use_training_net=True)
        print(response)
        response = response[1]

        info = {}
        self.step_iteration += 1
        if self.step_iteration == 15:
            done = True
        else:
            done = False

        return (
            present_state,
            action,
            response,
            done,
            info,
        )

    def reset(self) -> None:
        # 1) sample user
        self.step_iteration = 1
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
