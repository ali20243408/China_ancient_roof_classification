import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# 页面基础配置
st.set_page_config(page_title="中国古代民居建筑样式屋顶可视化系统", layout="wide")
# Matplotlib中文显示设置
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 全局页面样式定义
st.markdown("""
<style>
/* 整体页面背景 */
.stApp {
    background-color: #d5e1e8 !important;
}
/* 顶部大标题 */
.top-main-title {
    text-align: center;
    font-size: 30px;
    color: #3c5c5e !important;
    font-weight: bold;
    margin-bottom:30px;
}
/* 顶部6列布局整体排版 */
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
/* 左侧三个图片白色边框 */
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) > div:nth-child(1) img,
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) > div:nth-child(2) img,
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) > div:nth-child(3) img {
    border: 2px solid #ffffff !important;
    border-radius: 6px !important;
    box-sizing: border-box !important;
}
/* 右侧三个图片蓝色边框 */
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) > div:nth-child(4) img,
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) > div:nth-child(5) img,
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) > div:nth-child(6) img {
    border: 2px solid #3176b9 !important;
    border-radius: 6px !important;
    box-sizing: border-box !important;
}
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) button {
    margin:auto 0 0 0 !important;
    width:100% !important;
}
/* 民居分类按钮样式 */
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) button {
    border-radius: 8px !important;
    font-weight: bold !important;
    background-color: #8AA2B7 !important;
    color: #ffffff !important;
}
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) button:hover {
    background-color: #3c5c5e !important;
    color: #ffffff !important;
}
/* 一级标题样式 */
.primary-title {
    font-size: 1.8rem !important;
    font-weight: bold !important;
    color: #3c5c5e !important;
    background-color: transparent !important;
    text-align: center !important;
    margin-bottom: 20px !important;
    padding: 0 !important;
}
/* 二级标题样式 */
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
/* 正文文字颜色 */
.stMarkdown p, .stMarkdown li {
    color: #61848e !important;
}
.js-plotly-plot .plotly {
    background-color: #d5e1e8 !important;
}
</style>
""", unsafe_allow_html=True)

# 页面主标题
st.markdown('<div class="top-main-title">中国古代民居建筑样式屋顶可视化系统</div>', unsafe_allow_html=True)

# 各类民居屋顶基础信息字典
roof_info = {
    "燕尾脊顶": {
        "intro": "**燕尾脊顶**是闽南红砖古厝标志性屋脊造型，屋脊两端高高上翘分叉形似燕尾；适配东南沿海强台风气候，兼具排水、抗风、礼制象征与美学作用，主要流传闽南、粤东、台湾一带，为东南地域古建特色符号。",
        "icon": "photos/images2/燕尾脊顶.jpg",
        "imgs": ["photos/images2/燕尾脊顶1.jpg","photos/images2/燕尾脊顶2.jpg"],
        "cmap": "Oranges"
    },
    "三川脊顶": {
        "intro": "**三川脊顶**是闽南民居高等级屋脊，三段式轮廓端庄规整，多见于祠堂与大户宅第，由燕尾脊发展而来，承载闽南宗族礼制文化，核心分布闽南，粤东、台湾少量留存。",
        "icon": "photos/images2/三川脊顶.jpg",
        "imgs": ["photos/images2/三川脊顶1.jpg","photos/images2/三川脊顶2.jpg"],
        "cmap": "Reds"
    },
    "马鞍脊顶": {
        "intro": "**马鞍脊顶**屋脊中凹两端翘起形似马鞍，闽南粤东台湾主流民居样式，造型稳固抗风排水优，适配沿海气候，北方中西部无原生分布。",
        "icon": "photos/images2/马鞍脊顶.jpg",
        "imgs": ["photos/images2/马鞍脊顶1.jpg","photos/images2/马鞍脊顶2.jpg"],
        "cmap": "YlOrBr"
    },
    "囤顶": {
        "intro": "**囤顶**辽西独有弧形微拱民居屋顶，灰土夯筑，防积雪抗风沙承重好，集中辽宁西部区域，南方及大部北方地区少见。",
        "icon": "photos/images2/囤顶.jpg",
        "imgs": ["photos/images2/囤顶1.jpg","photos/images2/囤顶2.jpg"],
        "cmap": "Blues"
    },
    "单坡顶": {
        "intro": "**单坡顶**最简单向排水民居屋面，构造简易造价低，集中晋陕黄土高原，多用作厢房附属房，东南平原少见原生样式。",
        "icon": "photos/images2/单坡顶.jpg",
        "imgs": ["photos/images2/单坡顶1.jpg","photos/images2/单坡顶2.jpg"],
        "cmap": "Greens"
    },
    "总览": {
        "intro": """
- **地域特征**：东南沿海以燕尾脊、马鞍脊、三川脊为主，侧重抗台风与装饰礼制；北方囤顶、单坡顶侧重防寒防风沙实用功能。
- **文化内核**：屋顶融合地域气候、宗族礼制与民俗审美，是古建地域文化直观载体。
- **分布规律**：样式高度属地聚集，伴随移民文化跨区域传播特征明显。
"""
    }
}

# 缓存读取Excel与全国地理边界数据
@st.cache_data
def load_data():
    df = pd.read_excel("data/民居.xlsx")
    df_sankey = pd.read_excel("data/民居总.xlsx")
    url = "https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json"
    china = gpd.read_file(url)
    return df, df_sankey, china

df, df_sankey, china = load_data()

# 初始化页面切换状态
if "current_page" not in st.session_state:
    st.session_state.current_page = "总览"

# 顶部六大屋顶分类导航按钮
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    st.image(roof_info["燕尾脊顶"]["icon"], use_container_width=True)
    if st.button("燕尾脊顶", use_container_width=True):
        st.session_state.current_page = "燕尾脊顶"
with c2:
    st.image(roof_info["三川脊顶"]["icon"], use_container_width=True)
    if st.button("三川脊顶", use_container_width=True):
        st.session_state.current_page = "三川脊顶"
with c3:
    st.image(roof_info["马鞍脊顶"]["icon"], use_container_width=True)
    if st.button("马鞍脊顶", use_container_width=True):
        st.session_state.current_page = "马鞍脊顶"
with c4:
    st.image(roof_info["单坡顶"]["icon"], use_container_width=True)
    if st.button("单坡顶", use_container_width=True):
        st.session_state.current_page = "单坡顶"
with c5:
    st.image(roof_info["囤顶"]["icon"], use_container_width=True)
    if st.button("囤顶", use_container_width=True):
        st.session_state.current_page = "囤顶"
with c6:
    st.image("photos/images2/总览.jpg", use_container_width=True)
    if st.button("总览", use_container_width=True):
        st.session_state.current_page = "总览"

st.markdown("---")

# 页面主体动态渲染逻辑
selected = st.session_state.current_page

# 单一屋顶详情页
if selected != "总览":
    st.markdown(f'<div class="primary-title">{selected}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col_sub1, col_sub2, col_sub3 = st.columns([3, 3, 2])
    with col_sub1:
        st.markdown('<div class="secondary-title">地域分布密度图</div>', unsafe_allow_html=True)
    with col_sub2:
        st.markdown('<div class="secondary-title">分析与介绍</div>', unsafe_allow_html=True)
    with col_sub3:
        st.markdown('<div class="secondary-title">真实建筑案例</div>', unsafe_allow_html=True)

    col_map, col_text, col_pic = st.columns([3, 3, 2])

    with col_map:
        df_roof = df[df["屋顶样式"] == selected]
        prov_count = df_roof.groupby("省份").size().reset_index(name="count")
        china_with_data = china.merge(prov_count, left_on="name", right_on="省份", how="left").fillna({"count": 0})
        fig, ax = plt.subplots(figsize=(10, 7), dpi=120)
        fig.patch.set_facecolor('#c4d2db')
        ax.set_facecolor('#c4d2db')
        china_with_data.plot(
            ax=ax, column="count", cmap=roof_info[selected]["cmap"],
            vmin=0, vmax=prov_count["count"].max() if not prov_count.empty else 1,
            edgecolor="white", linewidth=0.5, legend=True,
            legend_kwds={"label": "建筑数量", "shrink": 0.6}
        )
        ax.set_title(f"{selected} 分布密度", fontsize=14, color='#3c5c5e')
        ax.set_axis_off()
        st.pyplot(fig)

    with col_text:
        st.markdown(roof_info[selected]["intro"])

    with col_pic:
        st.image(roof_info[selected]["imgs"][0], use_container_width=True)
        st.image(roof_info[selected]["imgs"][1], use_container_width=True)

# 整体总览桑基图页面
else:
    st.markdown('<div class="primary-title">总览</div>', unsafe_allow_html=True)
    col_sankey, col_info = st.columns([3, 2])

    with col_sankey:
        st.markdown('<div class="secondary-title">🔗 屋顶样式-子区域-南北方 分布流向</div>', unsafe_allow_html=True)
        sankey_data = df_sankey.groupby(["屋顶样式", "子区域", "地域"]).size().reset_index(name="value")
        labels = []
        roof_labels = sankey_data["屋顶样式"].unique().tolist()
        labels.extend(roof_labels)
        region_labels = sankey_data["子区域"].unique().tolist()
        labels.extend(region_labels)
        ns_labels = sankey_data["地域"].unique().tolist()
        labels.extend(ns_labels)

        sources, targets, values = [], [], []
        for _, row in sankey_data.iterrows():
            src = roof_labels.index(row["屋顶样式"])
            tgt = len(roof_labels) + region_labels.index(row["子区域"])
            sources.append(src); targets.append(tgt); values.append(row["value"])
        for _, row in sankey_data.iterrows():
            src = len(roof_labels) + region_labels.index(row["子区域"])
            tgt = len(roof_labels) + len(region_labels) + ns_labels.index(row["地域"])
            sources.append(src); targets.append(tgt); values.append(row["value"])

        brown_colors = ["#f7f0e6","#e6d2b8","#d4b890","#b89572","#8a705a","#b89572","#796e58"]
        def hex_to_rgba(hex_color, alpha=1.0):
            hex_color = hex_color.lstrip('#')
            r,g,b = int(hex_color[0:2],16), int(hex_color[2:4],16), int(hex_color[4:6],16)
            return f'rgba({r},{g},{b},{alpha})'
        roof_color_map = {
            "燕尾脊顶": hex_to_rgba(brown_colors[1]), "三川脊顶": hex_to_rgba(brown_colors[2]),
            "马鞍脊顶": hex_to_rgba(brown_colors[3]), "单坡顶": hex_to_rgba(brown_colors[0]),
            "囤顶": hex_to_rgba(brown_colors[4])
        }
        region_color_list = [hex_to_rgba(brown_colors[1]), hex_to_rgba(brown_colors[2]),
                             hex_to_rgba(brown_colors[3]), hex_to_rgba(brown_colors[0]),
                             hex_to_rgba(brown_colors[4])]
        region_colors = [region_color_list[i % len(region_color_list)] for i in range(len(region_labels))]
        ns_colors = [hex_to_rgba(brown_colors[5]), hex_to_rgba(brown_colors[6])]
        node_colors = [roof_color_map[r] for r in roof_labels] + region_colors + ns_colors

        link_colors = []
        region_color_map = dict(zip(region_labels, region_colors))
        for _, row in sankey_data.iterrows():
            link_colors.append(str(roof_color_map[row["屋顶样式"]]).replace("1.0","0.7"))
        for _, row in sankey_data.iterrows():
            link_colors.append(str(region_color_map[row["子区域"]]).replace("1.0","0.7"))

        fig = go.Figure(go.Sankey(
            arrangement="snap",
            node=dict(pad=20, thickness=20, line=dict("#f7f0e6", width=0.3), label=labels, color=node_colors),
            link=dict(source=sources, target=targets, value=values, color=link_colors)
        ))
        fig.update_layout(title_text="", font_size=12, font_color="#6b574a", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=500)
        st.plotly_chart(fig, use_container_width=True)

    with col_info:
        st.markdown('<div class="secondary-title">中国民居屋顶样式总览</div>', unsafe_allow_html=True)
        st.markdown(roof_info["总览"]["intro"])