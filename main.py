import plotly.express as px
import os
import webbrowser
import sqlite3
import pandas as pd


df = pd.read_csv('data/top_50_2023.csv')

print('Olá! Curiosidades sobre o top 50, 2023 do Spotify')
top_artista = df['artist_name'].value_counts()
artista_top = top_artista.index[0]
qtd_musicas = top_artista.iloc[0]
print(f" Artista que mais aparece: {artista_top} ({qtd_musicas} músicas)")
duracao_media_seg = df['duration_ms'].mean() / 1000
minutos = int(duracao_media_seg // 60)
segundos = int(duracao_media_seg % 60)
print(f"Duração média das músicas: {minutos}m{segundos}s")

print("\n ANÁLISE DE CARACTERÍSTICAS MUSICAIS ")
musicas_mais_dancante = {df.loc[df['danceability'].idxmax(), 'track_name']}
print(f"Música mais dançante:{musicas_mais_dancante}")
print(f"Música mais energética: {df.loc[df['energy'].idxmax(), 'track_name']}")
print(f"Música mais 'feliz' (valence): {df.loc[df['valence'].idxmax(), 'track_name']}")

print("\n ESTATÍSTICAS GERAIS ")
print(f"BPM médio: {df['tempo'].mean():.1f}")
print(f"Popularidade média: {df['popularity'].mean():.1f}")
print(f"Energia média: {df['energy'].mean():.2f}")

print("\n" + "="*50)
print("FILTROS E BUSCAS ESPECÍFICAS")
print("="*50)

artista_busca = "The Weeknd"
musicas_artista = df[df['artist_name'].str.contains(artista_busca, case=False, na=False)]
print(f"\nMúsicas de {artista_busca}:")
if not musicas_artista.empty:
    for _, musica in musicas_artista.iterrows():
        print(f"  - {musica['track_name']}")
else:
    print("  Nenhuma música encontrada")


super_populares = df[df['popularity'] > 90]
print(f"\nMúsicas SUPER populares (popularidade > 90): {len(super_populares)} músicas")

# Filtrar músicas muito dançantes (danceability > 0.8)
muito_dancantes = df[df['danceability'] > 0.8]
print(f"Músicas MUITO dançantes (danceability > 0.8): {len(muito_dancantes)} músicas")



# Criar pasta se não existir
if not os.path.exists('resultados'):
    os.makedirs('resultados')
    print(" Pasta 'resultados' criada!")

print("\n" + "="*50)
print("SALVANDO RESULTADOS EM ARQUIVOS CSV")
print("="*50)


top_artistas = df['artist_name'].value_counts().head(10).reset_index()
top_artistas.columns = ['artista', 'quantidade_musicas']
top_artistas.to_csv('resultados/top_artistas.csv', index=False)
print(" Salvo: resultados/top_artistas.csv")


super_populares = df[df['popularity'] > 90]
super_populares[['artist_name', 'track_name', 'popularity']].to_csv('resultados/musicas_super_populares.csv', index=False)
print(" Salvo: resultados/musicas_super_populares.csv")

# 3.músicas do The Weeknd
weeknd_musicas = df[df['artist_name'].str.contains('The Weeknd', case=False, na=False)]
weeknd_musicas[['track_name', 'popularity', 'danceability', 'energy']].to_csv('resultados/the_weeknd_musicas.csv', index=False)
print(" Salvo: resultados/the_weeknd_musicas.csv")

print(f"\n {len(os.listdir('resultados'))} arquivos salvos na pasta 'resultados/'!")



print("\n" + "=" * 50)
print("CRIANDO GRÁFICOS COM PLOTLY")
print("=" * 50)

#pasta para os gráficos
pasta_graficos = "graficos_spotify"
if not os.path.exists(pasta_graficos):
    os.makedirs(pasta_graficos)
    print(f" Pasta '{pasta_graficos}' criada!")

print(" Gerando gráficos...")


print("    Criando: Top 10 Artistas...")
top_artistas = df['artist_name'].value_counts().head(10)
fig1 = px.bar(
    x=top_artistas.values,
    y=top_artistas.index,
    orientation='h',
    title=' Top 10 Artistas com Mais Músicas',
    labels={'x': 'Número de Músicas', 'y': 'Artista'},
    color=top_artistas.values,
    color_continuous_scale='viridis'
)
fig1.update_layout(
    width=800,
    height=500,
    showlegend=False
)
# Salvar como HTML
arquivo1 = os.path.join(pasta_graficos, "01_top_artistas.html")
fig1.write_html(arquivo1)


print("    Criando: Distribuição de Popularidade...")
fig2 = px.histogram(
    df,
    x='popularity',
    nbins=15,
    title=' Distribuição de Popularidade das Músicas',
    labels={'popularity': 'Popularidade (0-100)', 'count': 'Quantidade de Músicas'},
    color_discrete_sequence=['#1f77b4']
)
fig2.update_layout(
    width=800,
    height=500,
    bargap=0.1
)
# Salvar como HTML
arquivo2 = os.path.join(pasta_graficos, "02_distribuicao_popularidade.html")
fig2.write_html(arquivo2)


print("    Criando: Top 10 Músicas Mais Populares...")
top_musicas = df.nlargest(10, 'popularity')
fig3 = px.bar(
    top_musicas,
    x='popularity',
    y='track_name',
    orientation='h',
    title=' Top 10 Músicas Mais Populares',
    labels={'popularity': 'Popularidade', 'track_name': 'Música'},
    hover_data=['artist_name'],
    color='popularity',
    color_continuous_scale='plasma'
)
fig3.update_layout(
    width=900,
    height=600,
    showlegend=False
)
# Salvar como HTML
arquivo3 = os.path.join(pasta_graficos, "03_top_musicas.html")
fig3.write_html(arquivo3)


print("    Criando: Energia vs Dançabilidade...")
fig4 = px.scatter(
    df,
    x='energy',
    y='danceability',
    hover_data=['track_name', 'artist_name', 'popularity'],
    title=' Energia vs Dançabilidade das Músicas',
    labels={'energy': 'Energia (0-1)', 'danceability': 'Dançabilidade (0-1)'},
    color='popularity',
    color_continuous_scale='sunset',
    size='popularity',
    size_max=10
)
fig4.update_layout(
    width=800,
    height=600
)
# Salvar como HTML
arquivo4 = os.path.join(pasta_graficos, "04_energia_vs_danceability.html")
fig4.write_html(arquivo4)

print("\n" + "=" * 50)
print(" GRÁFICOS CRIADOS COM SUCESSO!")
print("=" * 50)
print(f" Todos os gráficos foram salvos na pasta: {pasta_graficos}/")
print("\n Arquivos criados:")
print(f"   1. {arquivo1}")
print(f"   2. {arquivo2}")
print(f"   3. {arquivo3}")
print(f"   4. {arquivo4}")
print("\n Como visualizar:")
print("    Abra qualquer arquivo .html no seu navegador")
print("    Os gráficos são interativos (zoom, hover, etc.)")
print("    Você pode compartilhar os arquivos HTML facilmente")



def abrir_graficos():

    arquivos = [arquivo1, arquivo2, arquivo3, arquivo4]

    resposta = input("\n Deseja abrir os gráficos automaticamente no navegador? (s/n): ")
    if resposta.lower() in ['s', 'sim', 'y', 'yes']:
        print(" Abrindo gráficos no navegador...")
        for arquivo in arquivos:
            webbrowser.open('file://' + os.path.abspath(arquivo))
        print("✅ Gráficos abertos!")
    if resposta.lower() in ['n', 'nao', 'n', 'not']:
        print("Você pode abrir manualmente quando quiser.")

abrir_graficos()

print("\n" + "="*50)
print(" QUERY SQL")


conn = sqlite3.connect('spotify_facil.db')
df.to_sql('musicas', conn, if_exists='replace', index=False)
print(" Dados salvos no banco!")
"""
"""


print("\n" + "="*50)
print(" QUERY SQL")


conn = sqlite3.connect('spotify_facil.db')
df.to_sql('musicas', conn, if_exists='replace', index=False)
print(" Dados salvos no banco!")



print("\n1️⃣ QUAIS ARTISTAS TÊM MAIS MÚSICAS?")
print("-"*40)

# GROUP BY artista + COUNT()
query1 = """
SELECT artist_name as Artista, 
       COUNT() as Quantas_Musicas
FROM musicas 
GROUP BY artist_name 
ORDER BY COUNT(*) DESC 
LIMIT 5;
"""
print("Quantas músicas cada artista tem?")
print("SQL:", query1.strip())

resultado1 = pd.read_sql_query(query1, conn)
print("\n RESPOSTA:")
print(resultado1.to_string(index=False))

# WHERE popularity > número
query2 = """
SELECT track_name as Musica, 
       artist_name as Artista, 
       popularity as Popularidade
FROM musicas 
WHERE popularity >= 80
ORDER BY popularity DESC 
LIMIT 7;
"""
print("🔍 Pergunta: Quais músicas têm popularidade >= 80?")
print(" SQL:", query2.strip())

resultado2 = pd.read_sql_query(query2, conn)
print(f"\n📊 RESPOSTA: {len(resultado2)} músicas populares")
print(resultado2.to_string(index=False))


print("\n\n3️⃣ QUAL A MÉDIA DE POPULARIDADE?")
print("-"*35)


#  AVG
query3 = """
SELECT ROUND(AVG(popularity), 1) as Popularidade_Media,
       ROUND(AVG(energy), 2) as Energia_Media,
       COUNT(*) as Total_Musicas
FROM musicas;
"""
print("🔍 Pergunta: Qual a média de popularidade e energia?")
print(" SQL:", query3.strip())

resultado3 = pd.read_sql_query(query3, conn)
print("\n RESPOSTA:")
print(resultado3.to_string(index=False))


print("\n\n4️⃣ QUAIS MÚSICAS SÃO MAIS DANÇANTES?")
print("-"*40)


# WHERE danceability > 0.8
query4 = """
SELECT track_name as Musica,
       artist_name as Artista,
       ROUND(danceability, 2) as Danceability
FROM musicas 
WHERE danceability > 0.8
ORDER BY danceability DESC 
LIMIT 6;
"""
print("🔍 Pergunta: Quais músicas têm danceability > 0.8?")
print(" SQL:", query4.strip())

resultado4 = pd.read_sql_query(query4, conn)
print(f"\n RESPOSTA: {len(resultado4)} músicas super dançantes")
print(resultado4.to_string(index=False))


print("\n\n5️⃣ COMO ESTÃO OS ARTISTAS EM MÉDIA?")
print("-"*38)


# GROUP BY + HAVING
query5 = """
SELECT artist_name as Artista,
       COUNT(*) as Total_Musicas,
       ROUND(AVG(popularity), 1) as Popularidade_Media
FROM musicas 
GROUP BY artist_name 
HAVING COUNT(*) >= 2
ORDER BY AVG(popularity) DESC 
LIMIT 4;
"""
print("🔍 Pergunta: Média de popularidade por artista (com 2+ músicas)?")
print(" SQL:", query5.strip())

resultado5 = pd.read_sql_query(query5, conn)
print(f"\n RESPOSTA: {len(resultado5)} artistas comparados")
print(resultado5.to_string(index=False))


