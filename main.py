from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
from tqdm import tqdm
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

# Função para recuperar todas as músicas da playlist
def get_all_playlist_tracks(sp, playlist_id, limit=100):
    tracks = []
    offset = 0
    while True:
        response = sp.playlist_tracks(playlist_id, limit=limit, offset=offset)
        tracks.extend(response['items'])
        if len(response['items']) < limit:
            break
        offset += limit
    return tracks

# Recuperar todas as músicas da playlist
playlist_tracks = get_all_playlist_tracks(sp, playlist_id)

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
yt_playlist_id = ytmusic.create_playlist(yt_playlist_name, f'Created by App Spot on YT - by Fernando Thompson | Playlist: {playlist_name}', 'PUBLIC')


# Tentativa de função para correção de bug => Músicas não salvas
def save_tracks_to_csv(tracks, filename):
    """Salva uma lista de faixas em um arquivo CSV."""
    fieldnames = ['name', 'artist', 'album']
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for track in tracks:
            writer.writerow(track)

# músicas não encontradas
not_found_tracks = []

# Adicionar músicas à playlist no YTMusic
for track in tqdm(playlist_data['tracks'], desc="Adicionando músicas à playlist no YouTube Music", unit="música"):
    search_results = ytmusic.search(f"{track['name']} {track['artist']}", filter='songs')
    if search_results:
        track_id = search_results[0]['videoId']
        ytmusic.add_playlist_items(yt_playlist_id, [track_id])
    else:
        not_found_tracks.append(track)

# Obter a lista de músicas da nova playlist do YouTube Music
yt_playlist_tracks = ytmusic.get_playlist(yt_playlist_id)['tracks']

# Criar um conjunto com os nomes das músicas adicionadas
added_track_names = set()

for track in yt_playlist_tracks:
    track_name = track.get('title', 'Unknown Title')
    artists = track.get('artists', [])
    artist_name = artists[0]['name'] if artists else 'Unknown Artist'
    added_track_names.add(f"{track_name} - {artist_name}")

# Comparar e coletar músicas não adicionadas
not_added_tracks = []
for track in playlist_data['tracks']:
    track_name_artist = f"{track['name']} - {track['artist']}"
    if track_name_artist not in added_track_names:
        not_added_tracks.append(track)

# Combinar listas de músicas não encontradas e não adicionadas
all_not_saved_tracks = not_found_tracks + not_added_tracks

# Salvar todas as músicas não salvas em um único CSV
if all_not_saved_tracks:
    save_tracks_to_csv(all_not_saved_tracks, 'not_saved_tracks.csv')

print(f"Playlist '{playlist_data['name']}' copiada para o YouTube Music com sucesso!")
print(f"Músicas não adicionadas foram salvas em 'not_saved_tracks.csv'.")
print(f"Link da playlist no YouTube Music: https://music.youtube.com/playlist?list={yt_playlist_id}")


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
