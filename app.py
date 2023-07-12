import streamlit as st
import pandas as pd
from scipy import stats
import plotly.express as px

# reduce l/r margins
st.set_page_config(layout="wide")

# file load ui component
benchmarks = st.sidebar.file_uploader(
    "Upload file with before and after columns of times", type={"csv", "txt"}
)
if benchmarks is not None:
    # load data and run stats
    df = pd.read_csv(benchmarks)
    U1, p_mann = stats.mannwhitneyu(
        df["before"], df["after"], method="exact", alternative="greater"
    )
    p_ttest = stats.ttest_rel(df["before"], df["after"], alternative="greater")[1]

    # first column is stats with 1/4 of width
    # second column is histograms with 3/4 of width
    cols = st.columns([1, 3])
    with cols[0]:
        st.markdown("### Stats")
        st.markdown(
            f"""
            * ttest p value = {p_ttest:.2f}
            * Mann-Whitney U p value = {p_mann:.2f}
            * means
                * before {df["before"].mean():.2f}
                * after {df["after"].mean():.2f}
            * medians
                * before {df["before"].median():.2f}
                * after {df["after"].median():.2f}
            """
        )

    with cols[1]:
        st.markdown("### Histograms")
        fig = px.histogram(df, x="before", title="Before", height=200)
        fig.update_layout(
            margin=dict(l=20, r=20, t=25, b=5),
        )
        st.plotly_chart(fig, use_container_width=True)
        fig = px.histogram(df, x="after", title="After", height=200)
        fig.update_layout(
            margin=dict(l=20, r=20, t=25, b=5),
        )
        st.plotly_chart(fig, use_container_width=True)
