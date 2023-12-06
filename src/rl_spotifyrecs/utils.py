import os
import pickle
import shutil
from datetime import datetime
from pathlib import Path

import torch
from dotenv import load_dotenv

load_dotenv()


def save_run(model, directory: str):
    save_path = Path(os.environ.get("DATA_PATH"))  # type: ignore
    save_path = Path.home() / save_path
    save_path.mkdir(parents=True, exist_ok=True)

    time_now = datetime.now().strftime("%m-%d_%H-%M-%S")
    directory = directory

    # Create the directory with the folder name
    path = Path(directory)
    save_dir = Path(save_path / path)
    save_dir.mkdir(parents=True, exist_ok=True)

    # Save the model
    model_save_name = f"model.pt"
    torch.save(model, save_dir / Path(model_save_name))

    print(f"Run saved successfully in: {save_dir}")


def save_run_rl(model, directory: str):
    save_path = Path(os.environ.get("DATA_PATH"))  # type: ignore
    save_path = Path.home() / save_path
    save_path.mkdir(parents=True, exist_ok=True)

    time_now = datetime.now().strftime("%m-%d_%H-%M-%S")
    directory = directory

    # Create the directory with the folder name
    path = Path(directory)
    save_dir = Path(save_path / path)
    save_dir.mkdir(parents=True, exist_ok=True)

    # Save the model
    model_save_name = f"rl_model.pt"
    torch.save(model, save_dir / Path(model_save_name))

    print(f"Run saved successfully in: {save_dir}")
