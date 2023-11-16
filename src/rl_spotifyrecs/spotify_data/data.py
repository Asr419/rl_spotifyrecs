import pandas as pd
import random
import pandas as pd
import numpy as np
import datetime as dt
import itertools
import csv
import time
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import torch
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

df = pd.read_csv("~/spotify_session_data/log_mini.csv")
track_df = pd.read_csv("~/spotify_session_data/tf_mini.csv")


class DataLoader:
    def sample_history(
        user_histo,
        action_ratio=0.25,
        max_samp_by_user=10,
        max_state=10,
        max_action=5,
        nb_states=[],
        nb_actions=[],
    ):
        n = len(user_histo)
        sep = int(action_ratio * n)
        nb_sample = 1
        # nb_sample = random.randint(1, max_samp_by_user)
        if not nb_states:
            nb_states = [sep for i in range(nb_sample)]
        if not nb_actions:
            nb_actions = [n - sep for i in range(nb_sample)]
        assert len(nb_states) == len(nb_actions), "Given array must have the same size"

        states = []
        actions = []

        # Select samples in histo
        for i in range(len(nb_states)):
            sample_states = user_histo.iloc[0:sep]

            sample_actions = user_histo.iloc[-(n - sep) :]

            sample_state = []
            sample_action = []

            for j in range(nb_states[i]):
                row = sample_states.iloc[j]
                # Formate State
                state = row.loc["track_id"]  # TODO: REWARD SHAPING
                sample_state.append(state)

            for j in range(nb_actions[i]):
                row = sample_actions.iloc[j]
                # Formate Action
                action = row.loc["track_id"]
                sample_action.append(action)

            states.append(sample_state)
            actions.append(sample_action)

        return sample_state, sample_action

    def SpotifyData():
        df = pd.read_csv("~/spotify_session_data/log_mini.csv")
        track_df = pd.read_csv("~/spotify_session_data/tf_mini.csv")

        merged_df = pd.merge(
            track_df, df, left_on="track_id", right_on="track_id_clean", how="inner"
        )
        merged_df
        sample_df = merged_df[merged_df["session_length"] == 20].reset_index(drop=True)
        sample_df["session_id"] = LabelEncoder().fit_transform(sample_df["session_id"])
        sample_df["track_id"] = LabelEncoder().fit_transform(sample_df["track_id"])
        columns_to_convert = ["skip_1", "skip_2", "skip_3", "not_skipped"]

        # Convert the selected columns to binary (0/1)
        sample_df[columns_to_convert] = sample_df[columns_to_convert].astype(int)
        historic_users, user_state, action = [], [], []
        for i, u in enumerate(sample_df["session_id"].unique()):
            temp = sample_df[sample_df["session_id"] == u]
            temp = temp.sort_values("session_position").reset_index()
            temp.drop("index", axis=1, inplace=True)
            historic_users.append(temp)

        for i in range(0, len(historic_users)):
            user_features, action_features = DataLoader.sample_history(
                user_histo=historic_users[i],
                action_ratio=0.25,
                max_samp_by_user=10,
                max_state=1,
                max_action=15,
                nb_states=[],
                nb_actions=[],
            )
            user_state.append(user_features)
            action.append(action_features)
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
        context_feature_vectors, sequence_feature_vectors = {}, {}

        # Loop through the track_ids and collect the values for selected columns
        for i in range(0, len(historic_users)):
            for track_id in user_state[i]:
                context_features = (
                    historic_users[i]
                    .loc[historic_users[i]["track_id"] == track_id, music_columns]
                    .values[0]
                )
                context_feature_vectors[track_id] = context_features
        sequence_feature_vectors = {}

        # Loop through the track_ids and collect the values for selected columns
        for i in range(0, len(historic_users)):
            for track_id in action[i]:
                sequence_features = (
                    historic_users[i]
                    .loc[historic_users[i]["track_id"] == track_id, music_columns]
                    .values[0]
                )
                sequence_feature_vectors[track_id] = sequence_features

        response_columns = ["skip_2"]
        response_feature_vectors = {}

        # Loop through the track_ids and collect the values for selected columns
        for i in range(0, len(historic_users)):
            for track_id in action[i]:
                response_features = (
                    historic_users[i]
                    .loc[historic_users[i]["track_id"] == track_id, response_columns]
                    .values[0]
                )
                response_feature_vectors[track_id] = response_features
        return (
            context_feature_vectors,
            sequence_feature_vectors,
            response_feature_vectors,
        )

    def Feature_Vector(df, music_columns, response_columns, j: int):
        user_features, action_features = DataLoader.sample_history(
            action_ratio=0.25,
            user_histo=df[j],
            max_samp_by_user=10,
            max_state=1,
            max_action=15,
            nb_states=[],
            nb_actions=[],
        )
        filtered_data = df[j][df[j]["track_id"].isin(user_features)]

        filtered_data = filtered_data.head(5)
        extracted_data = filtered_data[music_columns]
        # Convert the extracted data to a list of lists
        extracted_data_list = extracted_data.values.tolist()
        context_feature_tensor = torch.tensor(extracted_data_list)
        context_feature_tensor = context_feature_tensor.flatten()

        a_filtered_data = df[j][df[j]["track_id"].isin(action_features)]
        a_filtered_data = a_filtered_data.tail(15)
        a_extracted_data = a_filtered_data[music_columns]
        # Convert the extracted data to a list of lists
        a_extracted_data_list = a_extracted_data.values.tolist()
        action_feature_tensor = torch.tensor(a_extracted_data_list)

        res_filtered_data = df[j][df[j]["track_id"].isin(action_features)]
        res_filtered_data = res_filtered_data.tail(15)
        res_extracted_data = res_filtered_data[response_columns]
        # Convert the extracted data to a list of lists
        res_extracted_data_list = res_extracted_data.values.tolist()
        res_feature_tensor = torch.tensor(res_extracted_data_list)

        return context_feature_tensor, action_feature_tensor, res_feature_tensor

    def UserSessions():
        merged_df = pd.merge(
            track_df, df, left_on="track_id", right_on="track_id_clean", how="inner"
        )
        merged_df
        sample_df = merged_df[merged_df["session_length"] == 20].reset_index(drop=True)
        sample_df["session_id"] = LabelEncoder().fit_transform(sample_df["session_id"])
        sample_df["track_id"] = LabelEncoder().fit_transform(sample_df["track_id"])
        columns_to_convert = ["skip_1", "skip_2", "skip_3", "not_skipped"]

        # Convert the selected columns to binary (0/1)
        sample_df[columns_to_convert] = sample_df[columns_to_convert].astype(int)
        historic_users = []
        for i, u in enumerate(sample_df["session_id"].unique()):
            temp = sample_df[sample_df["session_id"] == u]
            temp = temp.sort_values("session_position").reset_index()
            temp.drop("index", axis=1, inplace=True)
            historic_users.append(temp)
        return historic_users
