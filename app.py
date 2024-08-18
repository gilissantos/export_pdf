import pandas as pd
import streamlit as st
from fpdf import FPDF

# Cache e função para carregar os dados:
@st.cache_data
def load_data(file_csv):
    df = pd.read_csv(file_csv, sep=';')
    return df

df = load_data(r'C:\Users\gilis.santos\OneDrive - Collinson Central Services Limited\Área de Trabalho\pdf_streamlit\nba_stats.csv')

# Objeto PDF com métodos de formatação do tíluo e corpo do PDF que será exportado:
class PDF(FPDF):
    ''' Cria o template e exporta arquivo em PDF '''
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'DataFrame Exportado', 0, 1, 'C')

    def format_title(self, col_names):
        self.set_font('Arial', 'B', 12)
        for col_name in col_names:
            self.cell(40, 10, col_name, 1)
        self.ln()

    def format_body(self, data):
        self.set_font('Arial', '', 12)
        for row in data:
            for item in row:
                self.cell(40, 10, str(item), 1)
            self.ln()

# Criando um top 10 baseado no Ranking de pontos dos jogadores:
top_10_points = df[['RK', 'PLAYER', 'TEAM', 'PTS', 'MIN']].sort_values(by='RK', ascending=True).head(10)

# Exibe o dataframe com o top 10 pontuadores:
st.write(top_10_points)

# Criando o arquivo PDF
pdf = PDF()
pdf.add_page()
pdf.format_title(top_10_points.columns)
pdf.format_body(top_10_points.values)
arquivo_pdf = pdf.output('arquivo.pdf')

st.download_button(
    label="Salvar PDF",
    data=arquivo_pdf,
    file_name="Arquivo em pdf",
    mime="arquivo salvo em PDF"
)

# Cria um gráfico de barras com o top 10 pontuadores:
st.bar_chart(top_10_points, x='PLAYER', y='PTS')





