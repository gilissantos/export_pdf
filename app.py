import pandas as pd
import streamlit as st
import plotly.express as px # type: ignore
import config
from fpdf import FPDF # type: ignore

# Cache e função para carregar os dados:
@st.cache_data
def load_data(file_csv):
    df = pd.read_csv(file_csv, sep=';')
    return df

df = load_data(config.path_file_csv)

# Título da página
st.title("Report in PDF")

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
    xaxis_title=None,
    yaxis_title='Média de pontos'
)

# plota o gráfico:
st.plotly_chart(fig_jogador)

# Salvar o gráfico como uma imagem png:
fig_jogador.write_image(f'{config.path_save_files}/grafico.png',
                        width=780,
                        height=320,
                        scale=2
                        )


# Criando a classe para gerar o arquivo PDF
def gerar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(200, 10, txt="Relatório de Exemplo", ln=True, align='C')
    pdf.cell(200, 8, txt="Este é um exemplo de relatório gerado com Python.", ln=True, align='C')
    pdf.image(f'{config.path_save_files}\grafico.png', x=10, y=45, w=180)
    pdf.output('relatorio.pdf')
    return "relatorio.pdf"

# Criar o arquivo em PDF
path_pdf = gerar_pdf()

# Leitura do arquivo PDF:
with open(path_pdf, "rb") as file:
    pdf_em_bytes = file.read()

st.download_button(
    label="Baixar report em PDF",
    data=pdf_em_bytes,
    file_name="Report.pdf",
    mime="Application/PDF"
)
