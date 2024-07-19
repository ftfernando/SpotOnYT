<link rel="stylesheet" href="path/to/font-awesome/css/font-awesome.min.css">



![Captura de tela 2024-07-13 012859](https://github.com/user-attachments/assets/7ea3c74c-5e53-4436-83fe-ba519b0dbc61)




# Spot on YT App - Transferência de Playlists do Spotify para YouTube Music

Esta aplicação surgiu de uma necessidade pessoal: como usuário ativo do Spotify e do YouTube Music, percebi que transferir playlists entre essas plataformas era um processo tedioso e, muitas vezes, frustrante. 
Dessa forma, decidi unir o útil ao agradável, criando uma solução prática e eficiente que me permitisse mover minhas músicas de uma plataforma para outra sem perder tempo (além das horas que passei codando rsrs).

No mais, desenvolver esta ferramenta foi uma experiência tanto divertida quanto desafiadora, já que foi o primeiro projeto que criei do zero por conta própria. 
Até o momento, estou satisfeito com minha primeira aplicação em Python, mas futuramente planejo aperfeiçoar o código e implementar funcionalidades.

Caso queiram utilizar o código, seguem algumas instruções:

# Configurando Ambiente

### Instalação das Bibliotecas ###

Para configurar o ambiente e instalar as bibliotecas necessárias, execute o seguinte comando no terminal:

```
pip install spotipy ytmusicapi python-dotenv pandas
```



### Autenticação no YTMusic ###

Para autenticar sua aplicação com o YTMusic, execute o seguinte comando no terminal e siga as instruções:
```
ytmusicapi oauth
```
Isso abrirá um navegador onde você poderá fazer login na sua conta Google e conceder permissões necessárias para a API YTMusic.




### Obtendo Credenciais da API Spotify ###

Para obter as credenciais da API do Spotify, siga os passos abaixo:

<ol class="lista-ordenada">
    <li>Acesse o <a href="https://developer.spotify.com/dashboard/">Dashboard do Desenvolvedor Spotify</a>.</li>
    <li>Faça login na sua conta Spotify (ou crie uma, se necessário).</li>
    <li>Crie um novo aplicativo clicando em "Criar um Aplicativo".</li>
    <li>Preencha os detalhes necessários do aplicativo, como nome, descrição e URL de redirecionamento.</li>
    <li>Após criar o aplicativo, você encontrará o Client ID e Client Secret, que serão solicitados pela aplicação.</li>
</ol>


### Considerações Finais ###
Imagino que algumas instruções sejam básicas, mas como falei "Foi minha primeira aplicação" e sei que teria economizado algum tempo se tivesse essas informações na mão 😅

Caso tenham dúvidas, dicas, queiram trocar experiências, ou jogar conversa fora, podem me chamar em qualquer uma das minhas redes!

<h3>Redes Sociais</h3>
<ul>
        <li>
            <i class="fab fa-linkedin"></i>
            <a href="https://www.linkedin.com/in/fernandofthompson/" target="_blank">
                LinkedIn
            </a>
        </li>
        <li>
            <i class="fab fa-instagram"></i>
            <a href="https://www.instagram.com/f.fthompson/" target="_blank">
                Instagram
            </a>
        </li>
</ul>
