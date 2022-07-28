from ctypes import alignment
from email import header
import plotly.graph_objects as go
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
# Streamlit page configuration 
st.set_page_config(page_title="Dashboard Pelanggaran LANTAS dan Angkutan", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache #using cache to load data from axcel
def data():
    df = pd.read_csv("penindakan-pelanggaran-lantas-2021-juli.csv", nrows=7)
    return df

df = data()

st.sidebar.header("Please Filter Here : ")
Wilayah = st.sidebar.multiselect(
    "Select Wilayah : ",
    options=df["wilayah"].unique(),
    default=df["wilayah"].unique(),
)

df_selection = df.query("wilayah == @Wilayah")

st.title(":bar_chart: Dashboard Penindakan Pelanggaran LANTAS Bulan Juli Tahun 2021")
st.markdown("##")

# TOP KPI's
total_tilang = int(df_selection['bap_tilang'].sum())
total_operasi = int(df_selection['stop_operasi'].sum())
total_penderekan = int(df_selection['penderekan'].sum())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Tilang:")
    st.subheader(f"{total_tilang:,}")
with middle_column:
    st.subheader("Total Stop Operasi:")
    st.subheader(f"{total_operasi}")
with right_column:
    st.subheader("Total Penderekan:")
    st.subheader(f"{total_penderekan}")

st.markdown("""---""")

col1, col2 = st.columns(2)
all_wilayah = (
    df_selection.groupby(by=["wilayah"]).sum()[["bap_tilang","stop_operasi","bap_polisi","penderekan","ocp_roda_dua","ocp_roda_empat"]]
)

fig_tilang = px.bar(
    all_wilayah,
    x=all_wilayah.index,
    y="bap_tilang",
    orientation="v",
    title="<b>Tilang berdasarkan Wilayah</b>",
    color_discrete_sequence=["#b2182b"] * len(all_wilayah),
    template="plotly_white",
)
fig_tilang.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

col1.plotly_chart(fig_tilang, use_container_width=True)

fig_operasi = px.bar(
    all_wilayah,
    x=all_wilayah.index,
    y="stop_operasi",
    orientation="v",
    title="<b>Operasi berdasarkan Wilayah</b>",
    color_discrete_sequence=["#b2182b"] * len(all_wilayah),
    template="plotly_white",
)
fig_operasi.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

col2.plotly_chart(fig_operasi, use_container_width=True)

fig_penderekan = px.bar(
    all_wilayah,
    x=all_wilayah.index,
    y='penderekan',
    orientation="v",
    barmode='group',
    title="<b>Penderekan berdasarkan Wilayah</b>",
    color_discrete_sequence=["#b2182b"] * len(all_wilayah),
    template="plotly_white",
)
fig_penderekan.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

st.plotly_chart(fig_penderekan, use_container_width=True)

col3, col4 = st.columns(2)
fig_pie = px.pie(
    all_wilayah,
    names=all_wilayah.index,
    values='bap_polisi',
    title='<b>BAP POLISI</b>',
    color_discrete_sequence=px.colors.sequential.RdBu
)
fig_pie.update_traces(textposition='inside', textinfo='percent')
col3.plotly_chart(fig_pie, use_container_width=True)

fig_pie2 = px.pie(
    all_wilayah,
    names=all_wilayah.index,
    values='ocp_roda_dua',
    hover_data=['ocp_roda_empat'],
    labels={'ocp_roda_dua':'roda dua', 'ocp_roda_empat':'roda empat'},
    title='<b>OCP Roda 2 dan 4</b>',
    color_discrete_sequence=px.colors.sequential.RdBu
)
fig_pie2.update_traces(textposition='inside', textinfo='percent',hovertemplate = "wilayah:%{label}: <br>roda dua: %{value} <br>roda empat: %{customdata}")
col4.plotly_chart(fig_pie2, use_container_width=True)

st.subheader("Tabel Penindakan Pelanggaran LANTAS Juli 2021")
st.table(df) # view dataframe on page

