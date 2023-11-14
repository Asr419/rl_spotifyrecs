from rl_spotifyrecs.spotify_data.data import DataLoader

if __name__=='__main__':
    context_features,sequence_features,response_features = DataLoader.SpotifyData(self = None)
    print(context_features)