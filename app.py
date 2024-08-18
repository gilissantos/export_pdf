import pandas as pd
import streamlit as st
from fpdf import FPDF
import plotly.express as px
import config

# Cache e função para carregar os dados:
@st.cache_data
def load_data(file_csv):
    df = pd.read_csv(file_csv, sep=';')
    return df

df = load_data(r'C:\Users\gilis.santos\OneDrive - Collinson Central Services Limited\Área de Trabalho\pdf_streamlit\nba_stats.csv')

# Objeto PDF com métodos de formatação do tíluo e corpo do PDF que será exportado:

# Criando um top 10 baseado no Ranking de pontos dos jogadores:
top_10_points = df[['RK', 'PLAYER', 'TEAM', 'PTS', 'MIN', '3PM']].sort_values(by='RK', ascending=True).head(10)


# Cria um gráfico de barras com o top 10 pontuadores:
fig_jogador = px.bar(top_10_points,
            x='PLAYER', 
            y='PTS'
             )

# Atualiza as edições do gráfico:
fig_jogador.update_layout(
    title='Top 10 média de pontos por jogadores',
    xaxis_title='Jogador',
    yaxis_title='Média de pontos'
)

# plota o gráfico:
st.plotly_chart(fig_jogador)

# Salvar o gráfico como uma imagem png:
fig_jogador.write_image(f'{config.path_save_pdf}/grafico.png')

# Criando o arquivo PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font('Helvetica', 'B', 18)

#
# Adicionar as os gráficos que foram exportados como png:
#for graf_arq_name in graf_arq_names:
#    pdf.ln(10)                      # Adicionando um Padding de 10px do título para a imagem do gráfico
#    pdf.image(graf_arq_name, x=None, y=None, w=pdf.w - 20, h=0)

# Exportar/salvar a página para o formato PDF
#pdf.output(r'C:\Users\gilis.santos\OneDrive - Collinson Central Services Limited\Área de Trabalho\pdf_streamlit\teste.pdf')
