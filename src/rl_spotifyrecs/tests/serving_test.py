import torch.optim as optim
import random
from torch.utils.data import DataLoader
from rl_spotifyrecs.spotify_data.data import Spotify
from rl_spotifyrecs.spotify_environment.environment import SpotifyGym
from tqdm import tqdm
import torch
from dotenv import load_dotenv
from pathlib import Path
import os
from statistics import mean, stdev

load_dotenv()
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
response_columns = ["skip_1", "skip_2", "skip_3", "not_skipped"]
NUM_ITEM_FEATURES = 8
DQN_agent = torch.load(base_path / RUN_BASE_PATH / Path("rl_model.pt"))
CWM = torch.load(base_path / RUN_BASE_PATH / Path("model.pt"))

if __name__ == "__main__":
    env = SpotifyGym()

    test_sessions = Spotify.UserSessions(train=False)
    complete_reward = []
    print(len(test_sessions))
    for i in tqdm(range(len(test_sessions))):
        with torch.no_grad():
            env.reset()
            sess_reward = 0
            (
                user_state,
                candidate_actions,
                candidate_response,
            ) = Spotify.Feature_Vector(
                test_sessions, music_columns, response_columns, i
            )
            done = False
            while not done:
                user_state_rep = user_state.repeat((candidate_actions.shape[0], 1))

                q_val = DQN_agent.compute_q_values(
                    state=user_state_rep,
                    candidate_docs_repr=candidate_actions,
                    use_policy_net=True,
                )
                q_val = q_val.squeeze()
                action_index = torch.argmax(q_val)

                (user_state, action, reward, done, info) = env.step(
                    user_state, candidate_actions[action_index], CWM
                )
                updated_user = user_state[NUM_ITEM_FEATURES:]
                next_user_state = torch.cat([updated_user, action])

                candidate_actions = torch.cat(
                    (
                        candidate_actions[:action_index],
                        candidate_actions[action_index + 1 :],
                    ),
                    dim=0,
                )
                sess_reward += reward
        complete_reward.append(sess_reward.item())
    print(complete_reward)
    print("Mean Reward: ", mean(complete_reward))
    print("Standard Deviation: ", stdev(complete_reward))
