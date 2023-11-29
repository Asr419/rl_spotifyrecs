import torch.optim as optim
import random
from rl_spotifyrecs.spotify_data.data import DataLoader
from rl_spotifyrecs.spotify_agent.dqn_agent import (
    DQNAgent,
    ReplayMemoryDataset,
    Transition,
)
from rl_spotifyrecs.spotify_environment.environment import SpotifyGym
from tqdm import tqdm
import torch

NUM_ITEM_FEATURES = 8
NUM_EPISODES = 500
BATCH_SIZE = 30
REPLAY_MEMORY_CAPACITY = 100
TAU = 0.001
LR = 0.01
DEVICE = "cpu"
transition_cls = Transition
replay_memory_dataset = ReplayMemoryDataset(
    capacity=REPLAY_MEMORY_CAPACITY, transition_cls=transition_cls
)
replay_memory_dataloader = DataLoader(
    replay_memory_dataset,
    batch_size=BATCH_SIZE,
    collate_fn=replay_memory_dataset.collate_fn,
    shuffle=False,
)
env = SpotifyGym()
agent = DQNAgent(
    input_size=6 * NUM_ITEM_FEATURES,
    output_size=1,
    tau=TAU,
).to(DEVICE)
criterion = torch.nn.SmoothL1Loss()
optimizer = optim.Adam(agent.parameters(), lr=LR)
for i_episode in tqdm(range(NUM_EPISODES)):
    # Initialize the environment and state
    user_state, actions, response = env.reset()
    user_state_rep = user_state.repeat((actions.shape[0], 1))

    q_val = agent.compute_q_values(
        state=user_state_rep,
        candidate_docs_repr=actions,
        use_policy_net=True,
    )
