import torch.optim as optim
import random
from torch.utils.data import DataLoader
from rl_spotifyrecs.spotify_data.data import Spotify
from rl_spotifyrecs.spotify_agent.dqn_agent import (
    DQNAgent,
    ReplayMemoryDataset,
    Transition,
)
from rl_spotifyrecs.spotify_environment.environment import SpotifyGym
from tqdm import tqdm
import torch


def optimize_model(batch):
    (
        state_batch,  # [batch_size, num_item_features]
        action_batch,  # [batch_size, num_item_features]
        candidate_actions_batch,  # [batch_size, slate_size, num_item_features]
        next_state_batch,  # [batch_size, num_item_features]
        reward_batch,
    ) = batch

    optimizer.zero_grad()

    # Q(s, a): [batch_size, 1]
    q_val = agent.compute_q_values(
        state_batch, action_batch, use_policy_net=True
    )  # type: ignore
    cand_qtgt_list = []

    for b in range(next_state_batch.shape[0]):
        next_state = next_state_batch[b]
        candidates = candidate_actions_batch[b, :]
        next_state_rep = next_state.repeat((candidates.shape[0], 1))
        cand_qtgt = agent.compute_q_values(
            next_state_rep, candidates, use_policy_net=False
        ).squeeze()
        cand_qtgt = torch.max(cand_qtgt)
        cand_qtgt_list.append(cand_qtgt)
    cand_qtgt = torch.Tensor(cand_qtgt_list)

    q_tgt = torch.stack(cand_qtgt_list).unsqueeze(1)
    expected_q_values = q_tgt * GAMMA + reward_batch
    loss = criterion(q_val, expected_q_values)

    # Optimize the model
    loss.backward()
    optimizer.step()
    return loss


NUM_ITEM_FEATURES = 8
NUM_EPISODES = 500
BATCH_SIZE = 30
REPLAY_MEMORY_CAPACITY = 100
TAU = 0.001
LR = 0.01
DEVICE = "cpu"
WARMUP_BATCHES = 1
GAMMA = 1.0
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
    user_state, candidate_actions, response = env.reset()
    pushed_actions = candidate_actions
    done = False
    while not done:
        with torch.no_grad():
            user_state_rep = user_state.repeat((candidate_actions.shape[0], 1))

            q_val = agent.compute_q_values(
                state=user_state_rep,
                candidate_docs_repr=candidate_actions,
                use_policy_net=True,
            )
            q_val = q_val.squeeze()
            action_index = torch.argmax(q_val)

            (user_state, action, reward, done, info) = env.step(
                user_state, candidate_actions[action_index]
            )
            updated_user = user_state[NUM_ITEM_FEATURES:]
            next_user_state = torch.cat([updated_user, action])

            replay_memory_dataset.push(
                transition_cls(
                    user_state,  # type: ignore
                    action,
                    pushed_actions,
                    next_user_state,
                    reward,  # type: ignore
                )
            )
            candidate_actions = torch.cat(
                (
                    candidate_actions[:action_index],
                    candidate_actions[action_index + 1 :],
                ),
                dim=0,
            )
            user_state = next_user_state
    if len(replay_memory_dataset.memory) >= WARMUP_BATCHES * BATCH_SIZE:
        batch = next(iter(replay_memory_dataloader))
        for elem in batch:
            elem.to(DEVICE)
        batch_loss = optimize_model(batch)
        agent.soft_update_target_network()
