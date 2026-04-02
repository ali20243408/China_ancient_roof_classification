import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# --------------------------
# 页面配置
# --------------------------
st.set_page_config(page_title="Chinese Folk Roof Visualization", layout="wide")

# 乱码修复：使用英文默认字体，彻底不依赖中文
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False

# --------------------------
# 【全局样式】完全不变
# --------------------------
st.markdown("""
<style>
.stApp {
    background-color: #d5e1e8 !important;
}
.top-main-title {
    text-align: center;
    font-size: 30px;
    color: #3c5c5e !important;
    font-weight: bold;
    margin-bottom:30px;
}
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) {
    width:100% !important;
}
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) > div {
    display:flex !important;
    flex-direction:column !important;
    min-height:220px !important;
    justify-content: flex-start !important;
    align-items:center !important;
}
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) img {
    height:130px !important;
    width:auto !important;
    object-fit:contain !important;
    margin:0 auto 10px auto !important;
}
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) > div:nth-child(1) img,
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) > div:nth-child(2) img,
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) > div:nth-child(3) img {
    border: 2px solid #ffffff !important;
    border-radius: 6px !important;
    box-sizing: border-box !important;
}
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) > div:nth-child(4) img,
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) > div:nth-child(5) img,
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) > div:nth-child(6) img {
    border: 2px solid #3176b9 !important;
    border-radius: 6px !important;
    box-sizing: border-box !important;
}
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) button {
    margin-top:auto !important;
    width:100% !important;
    border-radius: 8px !important;
    font-weight: bold !important;
    background-color: #8AA2B7 !important;
    color: #ffffff !important;
}
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) button:hover {
    background-color: #3c5c5e !important;
    color: #ffffff !important;
}
.primary-title {
    font-size: 1.8rem !important;
    font-weight: bold !important;
    color: #3c5c5e !important;
    background-color: transparent !important;
    text-align: center !important;
    margin-bottom: 20px !important;
    padding: 0 !important;
}
.secondary-title {
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    color: #ffffff !important;
    background-color: #61848e !important;
    padding: 8px 16px !important;
    border-radius: 6px !important;
    text-align: center !important;
    margin-bottom: 12px !important;
    display: inline-block !important;
    width: 100% !important;
}
.stMarkdown p, .stMarkdown li {
    color: #61848e !important;
}
.js-plotly-plot .plotly {
    background-color: #d5e1e8 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="top-main-title">Chinese Ancient Folk Roof Visualization</div>', unsafe_allow_html=True)

# --------------------------
# 屋顶数据（只改图表用到的名称）
# --------------------------
roof_info = {
    "SwallowTail": {
        "intro": "Swallow Tail Roof is a classic style in Fujian, Taiwan, and Guangdong. It resists typhoons and drains rainwater quickly.",
        "icon": "photos/images2/燕尾脊顶.jpg",
        "imgs": ["photos/images2/燕尾脊顶1.jpg", "photos/images2/燕尾脊顶2.jpg"],
        "cmap": "Oranges"
    },
    "ThreeRiver": {
        "intro": "Three River Roof is a formal style for ancestral halls. It represents hierarchy in southern Fujian culture.",
        "icon": "photos/images2/三川脊顶.jpg",
        "imgs": ["photos/images2/三川脊顶1.jpg", "photos/images2/三川脊顶2.jpg"],
        "cmap": "Reds"
    },
    "Saddle": {
        "intro": "Saddle Roof has a smooth, curved shape. It is widely used in coastal areas for wind resistance and beauty.",
        "icon": "photos/images2/马鞍脊顶.jpg",
        "imgs": ["photos/images2/马鞍脊顶1.jpg", "photos/images2/马鞍脊顶2.jpg"],
        "cmap": "YlOrBr"
    },
    "ArcRoof": {
        "intro": "Arc Roof is unique to western Liaoning. It resists snow and sandstorms, ideal for cold northern climates.",
        "icon": "photos/images2/囤顶.jpg",
        "imgs": ["photos/images2/囤顶1.jpg", "photos/images2/囤顶2.jpg"],
        "cmap": "Blues"
    },
    "SingleSlope": {
        "intro": "Single Slope Roof is simple and low-cost. Common in Shanxi and Shaanxi loess plateaus.",
        "icon": "photos/images2/单坡顶.jpg",
        "imgs": ["photos/images2/单坡顶1.jpg", "photos/images2/单坡顶2.jpg"],
        "cmap": "Greens"
    },
    "Overview": {
        "intro": "Southern roofs focus on decoration; Northern roofs focus on weather resistance."
    }
}

name_map = {
    "燕尾脊顶": "SwallowTail",
    "三川脊顶": "ThreeRiver",
    "马鞍脊顶": "Saddle",
    "囤顶": "ArcRoof",
    "单坡顶": "SingleSlope",
    "总览": "Overview"
}
reverse_map = {v: k for k, v in name_map.items()}


# --------------------------
# 加载数据
# --------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("data/民居.xlsx")
    df_sankey = pd.read_excel("data/民居总.xlsx")
    url = "https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json"
    china = gpd.read_file(url)
    return df, df_sankey, china


df, df_sankey, china = load_data()

if "current_page" not in st.session_state:
    st.session_state.current_page = "Overview"

# --------------------------
# 顶部按钮
# --------------------------
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    st.image(roof_info["SwallowTail"]["icon"], use_container_width=True)
    if st.button("SwallowTail", use_container_width=True):
        st.session_state.current_page = "SwallowTail"
with c2:
    st.image(roof_info["ThreeRiver"]["icon"], use_container_width=True)
    if st.button("ThreeRiver", use_container_width=True):
        st.session_state.current_page = "ThreeRiver"
with c3:
    st.image(roof_info["Saddle"]["icon"], use_container_width=True)
    if st.button("Saddle", use_container_width=True):
        st.session_state.current_page = "Saddle"
with c4:
    st.image(roof_info["SingleSlope"]["icon"], use_container_width=True)
    if st.button("SingleSlope", use_container_width=True):
        st.session_state.current_page = "SingleSlope"
with c5:
    st.image(roof_info["ArcRoof"]["icon"], use_container_width=True)
    if st.button("ArcRoof", use_container_width=True):
        st.session_state.current_page = "ArcRoof"
with c6:
    st.image("photos/images2/总览.jpg", use_container_width=True)
    if st.button("Overview", use_container_width=True):
        st.session_state.current_page = "Overview"

st.markdown("---")

# --------------------------
# 内容区
# --------------------------
selected = st.session_state.current_page

if selected != "Overview":
    st.markdown(f'<div class="primary-title">{selected}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col_sub1, col_sub2, col_sub3 = st.columns([3, 3, 2])
    with col_sub1:
        st.markdown('<div class="secondary-title">Distribution Map</div>', unsafe_allow_html=True)
    with col_sub2:
        st.markdown('<div class="secondary-title">Description</div>', unsafe_allow_html=True)
    with col_sub3:
        st.markdown('<div class="secondary-title">Examples</div>', unsafe_allow_html=True)

    col_map, col_text, col_pic = st.columns([3, 3, 2])

    with col_map:
        original_name = reverse_map[selected]
        df_roof = df[df["屋顶样式"] == original_name]
        prov_count = df_roof.groupby("省份").size().reset_index(name="count")
        china_with_data = china.merge(prov_count, left_on="name", right_on="省份", how="left").fillna({"count": 0})

        fig, ax = plt.subplots(figsize=(10, 7), dpi=120)
        fig.patch.set_facecolor('#c4d2db')
        ax.set_facecolor('#c4d2db')

        china_with_data.plot(
            ax=ax, column="count", cmap=roof_info[selected]["cmap"],
            vmin=0, vmax=prov_count["count"].max() if not prov_count.empty else 1,
            edgecolor="white", linewidth=0.5, legend=True,
            legend_kwds={"label": "Count", "shrink": 0.6}
        )
        ax.set_title(f"{selected} Distribution", fontsize=14, color='#3c5c5e')
        ax.set_axis_off()
        st.pyplot(fig)

    with col_text:
        st.markdown(roof_info[selected]["intro"])

    with col_pic:
        st.image(roof_info[selected]["imgs"][0], use_container_width=True)
        st.image(roof_info[selected]["imgs"][1], use_container_width=True)

else:
    st.markdown('<div class="primary-title">Overview</div>', unsafe_allow_html=True)
    col_sankey, col_info = st.columns([3, 2])

    with col_sankey:
        st.markdown('<div class="secondary-title">Roof - Region - Flow</div>', unsafe_allow_html=True)
        sankey_data = df_sankey.groupby(["屋顶样式", "子区域", "地域"]).size().reset_index(name="value")

        # 桑基图全英文
        labels = []
        roof_labels = ["SwallowTail", "ThreeRiver", "Saddle", "SingleSlope", "ArcRoof"]
        region_labels = ["Fujian", "Guangdong", "Taiwan", "Shanxi", "Liaoning"]
        ns_labels = ["South", "North"]
        labels = roof_labels + region_labels + ns_labels

        sources, targets, values = [], [], []
        roof_map = {"燕尾脊顶": "SwallowTail", "三川脊顶": "ThreeRiver", "马鞍脊顶": "Saddle", "单坡顶": "SingleSlope",
                    "囤顶": "ArcRoof"}
        region_map = {"闽南": "Fujian", "粤东": "Guangdong", "台湾": "Taiwan", "晋陕": "Shanxi", "辽西": "Liaoning"}
        ns_map = {"南方": "South", "北方": "North"}

        for _, row in sankey_data.iterrows():
            r = roof_map[row["屋顶样式"]]
            reg = region_map[row["子区域"]]
            n = ns_map[row["地域"]]
            v = row["value"]
            sources.append(roof_labels.index(r))
            targets.append(len(roof_labels) + region_labels.index(reg))
            values.append(v)

        for _, row in sankey_data.iterrows():
            reg = region_map[row["子区域"]]
            n = ns_map[row["地域"]]
            v = row["value"]
            sources.append(len(roof_labels) + region_labels.index(reg))
            targets.append(len(roof_labels) + len(region_labels) + ns_labels.index(n))
            values.append(v)

        fig = go.Figure(go.Sankey(
            node=dict(pad=20, thickness=20, label=labels),
            link=dict(source=sources, target=targets, value=values)
        ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=500)
        st.plotly_chart(fig, width="stretch")

    with col_info:
        st.markdown('<div class="secondary-title">Overview</div>', unsafe_allow_html=True)
        st.markdown(roof_info["Overview"]["intro"])