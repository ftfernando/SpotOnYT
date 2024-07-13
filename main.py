from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
import json
import csv
import os
from dotenv import load_dotenv

# Instale as bibliotecas com o comando "pip install spotipy ytmusicapi python-dotenv" no terminal

# Autenticação no YTMusic:
# Para criar o "oauth.json", utilize o comando "ytmusicapi oauth" no terminal e siga a orientação.
ytmusic = YTMusic("oauth.json")

# Carregar .env, se houver
load_dotenv()

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

# Solicitar novos valores do usuário se as variáveis de ambiente não estiverem definidas
if not client_id or not client_secret or not redirect_uri:
    client_id = input("Digite o Spotify Client ID: ")
    client_secret = input("Digite o Spotify Client Secret: ")
    redirect_uri = input("Digite o Spotify Redirect URI: ")

    # Criar ou atualizar o .env com os novos valores
    with open('.env', 'w') as f:
        f.write(f"SPOTIPY_CLIENT_ID={client_id}\n")
        f.write(f"SPOTIPY_CLIENT_SECRET={client_secret}\n")
        f.write(f"SPOTIPY_REDIRECT_URI={redirect_uri}\n")
        print("Arquivo .env criado com sucesso.")

else:
    print(f"Client ID: {client_id}")
    print(f"Client Secret: {client_secret}")
    print(f"Redirect URI: {redirect_uri}")

# Autenticar credenciais
sp = Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                       client_secret=client_secret,
                                       redirect_uri=redirect_uri,
                                       scope='playlist-read-private'))

# Solicitar o ID da playlist do Spotify
playlist_id = input("Digite o Link/ID da playlist do Spotify: ")

# Recuperar informações da playlist
playlist = sp.playlist(playlist_id)
playlist_name = playlist['name']
playlist_tracks = playlist['tracks']['items']

# Armazenar os dados da playlist do Spotify
tracks = []
for item in playlist_tracks:
    track = item['track']
    track_data = {
        'name': track['name'],
        'artist': track['artists'][0]['name'],
        'album': track['album']['name']
    }
    tracks.append(track_data)

# Armazenar os dados da playlist em um JSON
with open('playlist_data.json', 'w', encoding='utf-8') as f:
    json.dump({'name': playlist_name, 'tracks': tracks}, f, ensure_ascii=False, indent=4)

# Solicitar o nome da nova playlist
yt_playlist_name = input("Digite o nome da nova playlist no YouTube Music: ")

# Carregar os dados da playlist do JSON
with open('playlist_data.json', 'r', encoding='utf-8') as f:
    playlist_data = json.load(f)

# Criar uma playlist no YTMusic
yt_playlist_id = ytmusic.create_playlist(yt_playlist_name, 'Created by App Spot on YT - by Fernando Thompson', 'UNLISTED')

# músicas não encontradas
not_found_tracks = []

# Adicionar músicas à playlist no YTMusic
for track in playlist_data['tracks']:
    search_results = ytmusic.search(f"{track['name']} {track['artist']}", filter='songs')
    if search_results:
        track_id = search_results[0]['videoId']
        ytmusic.add_playlist_items(yt_playlist_id, [track_id])
    else:
        not_found_tracks.append(track)

# Salvar músicas não encontradas em .CSV
with open('not_found_tracks.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'artist', 'album']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for track in not_found_tracks:
        writer.writerow(track)

print(f"Playlist '{playlist_data['name']}' copiada para o YouTube Music com sucesso!")
print(f"Músicas não encontradas foram salvas em 'not_found_tracks.csv'.")


# Futuramente irei adicionar funções de atualização
# *** YTMusic.add_playlist_items (playlistId: str, videoIds: List[str] | None = None, source_playlist: str | None = None, duplicates: bool = False)
# *** - duplicates – false
#
#
# Futuramente pretendo adicionar mais interações:
# Tratamento de Erros
# Verificação de Playlists Existentes
# Songs/Playlists info
# Podcasts - Verificar disponibilidade no youtube
# Front-end da aplicação
# Feedback de Progresso
