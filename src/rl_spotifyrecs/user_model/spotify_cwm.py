import torch
import torch.nn as nn
import torch.nn.functional as F


class CWMnet(nn.Module):
    def __init__(self, input_size, hidden_dims: list[int], output_size):
        super(CWMnet, self).__init__()

        self.layers = nn.ModuleList()
        prev_dim = input_size
        for dim in hidden_dims:
            self.layers.append(nn.Linear(prev_dim, dim))
            self.layers.append(nn.ReLU())
            prev_dim = dim
        # add last layer
        self.layers.append(nn.Linear(prev_dim, output_size))

    def forward(self, x):
        for i, layer in enumerate(self.layers):
            x = layer(x)
        return x


class CWM(nn.Module):
    def __init__(
        self,
        input_size: int,
        output_size: int,
        hidden_dims: list[int] = [40, 24, 16, 8],
        tau: float = 0.001,
    ) -> None:
        nn.Module.__init__(self)
        self.training_net = CWMnet(
            input_size=input_size, output_size=output_size, hidden_dims=hidden_dims
        )
        self.training_net.requires_grad_(True)

    def compute_prob(
        self,
        state: torch.Tensor,
        candidate_docs_repr: torch.Tensor,
        use_training_net: bool = True,
        training: bool = False,
    ) -> torch.Tensor:
        # concatenate state and candidate docs
        if training:
            input1 = torch.cat([state, candidate_docs_repr], dim=1)
        else:
            input1 = torch.cat([state, candidate_docs_repr], dim=0)
        # [num_candidate_docs, 1]
        if use_training_net and training:
            probability_val = self.training_net(input1)
            probability_val = torch.sigmoid(probability_val)
        else:
            probability_val = self.training_net(input1)
            probability_val = torch.sigmoid(probability_val)
        return probability_val
