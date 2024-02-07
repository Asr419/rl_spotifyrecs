import torch
import torch.nn as nn
import torch.nn.functional as F


class SequentialLSTM(nn.Module):
    def __init__(self, input_size, output_size, hidden_sizes, BATCH_SIZE):
        super(SequentialLSTM, self).__init__()
        self.num_layers = len(hidden_sizes)
        self.lstm_layers = nn.ModuleList()
        self.hidden_sizes = hidden_sizes
        self.BATCH_SIZE = BATCH_SIZE

        # Input LSTM layer
        self.lstm_layers.append(nn.LSTM(input_size, hidden_sizes[0], batch_first=True))

        # Hidden LSTM layers
        for i in range(1, self.num_layers):
            self.lstm_layers.append(
                nn.LSTM(hidden_sizes[i - 1], hidden_sizes[i], batch_first=True)
            )

        # Fully connected layer
        self.fc = nn.Linear(hidden_sizes[-1], output_size)

    def forward(self, x):
        # Initial hidden and cell states
        for i in range(self.num_layers):
            h_t, c_t = torch.zeros(
                1, self.BATCH_SIZE, self.hidden_sizes[i]
            ), torch.zeros(1, self.BATCH_SIZE, self.hidden_sizes[i])
            x, (h_t, c_t) = self.lstm_layers[i](x, (h_t, c_t))

        # Take the output of the last LSTM layer
        x = x[:, :, :]

        # Fully connected layer
        x = self.fc(x)
        return x


class LSTMCWM(nn.Module):
    def __init__(
        self,
        input_size: int,
        output_size: int,
        hidden_sizes: list[int] = [750, 750, 750],
        BATCH_SIZE: int = 20,
        tau: float = 0.001,
    ) -> None:
        nn.Module.__init__(self)
        self.training_net = SequentialLSTM(
            input_size=input_size,
            output_size=output_size,
            hidden_sizes=hidden_sizes,
            BATCH_SIZE=BATCH_SIZE,
        )
        self.training_net.requires_grad_(True)

    def compute_prob(
        self,
        state: torch.Tensor,
        candidate_docs_repr: torch.Tensor,
        use_training_net: bool = True,
    ) -> torch.Tensor:
        # concatenate state and candidate docs

        input1 = torch.cat([state, candidate_docs_repr], dim=-1)

        # [num_candidate_docs, 1]
        if use_training_net:
            probability_val = self.training_net(input1)

            # probability_val=F.softmax(probability_val, dim=0)

        return probability_val
