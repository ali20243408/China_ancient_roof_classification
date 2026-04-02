import streamlit as st

# 👇 直接粘贴在这里 👇
# 全局修复中文乱码
import plotly.io as pio
pio.templates["cloud_cn"] = pio.templates["plotly"]
pio.templates["cloud_cn"].layout.font.update(
    family="WenQuanYi Micro Hei, SimHei, Microsoft YaHei, sans-serif"
)
pio.templates.default = "cloud_cn"

import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["WenQuanYi Micro Hei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False
import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# --------------------------
# 页面配置
# --------------------------
st.set_page_config(page_title="中国古代民居建筑样式屋顶可视化系统", layout="wide")
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# --------------------------
# 【全局样式】
# --------------------------
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
/* 顶部6列布局 */
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
/* 左边三个图片（第1,2,3列）白色边框 */
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) > div:nth-child(1) img,
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) > div:nth-child(2) img,
div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)) > div:nth-child(3) img {
    border: 2px solid #ffffff !important;
    border-radius: 6px !important;
    box-sizing: border-box !important;
}
/* 右边三个图片（第4,5,6列）蓝色边框 */
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
}

/* 👇 只控制民居自己内部6个按钮，不影响主页 👇 */
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

/* 一级标题样式：深色字体 + 无背景 */
.primary-title {
    font-size: 1.8rem !important;
    font-weight: bold !important;
    color: #3c5c5e !important;
    background-color: transparent !important;
    text-align: center !important;
    margin-bottom: 20px !important;
    padding: 0 !important;
}

/* 二级标题样式：白色字体 + 背景色 #61848e */
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

/* 正文颜色 */
.stMarkdown p, .stMarkdown li {
    color: #61848e !important;
}
.js-plotly-plot .plotly {
    background-color: #d5e1e8 !important;
}
</style>
""", unsafe_allow_html=True)

# 顶部标题
st.markdown('<div class="top-main-title">中国古代民居建筑样式屋顶可视化系统</div>', unsafe_allow_html=True)

# --------------------------
# 屋顶数据（不变）
# --------------------------
roof_info = {
    "燕尾脊顶": {
        "intro": "**燕尾脊顶**是闽南红砖古厝标志性屋脊造型，屋脊两端高高上扬分叉，形似燕尾得名；适配东南沿海强台风气候，兼具快速排水、抗风稳固、礼制象征、吉祥美学多重作用。形制起源闽南通泉州地区，明清成熟定型，随闽南移民迁徙传播至粤东、台湾、海南、浙南一带；属于闽南海洋商贸文化、侨乡文化、民间等级礼制共同孕育的特色屋脊，北方官式、西北民居、江南平原主流建筑均不采用。学界公认燕尾脊是东南沿海地域辨识度最高的古建筑“第五立面”符号之一。",
        "icon": "photos/images2/燕尾脊顶.jpg",
        "imgs": ["photos/images2/燕尾脊顶1.jpg","photos/images2/燕尾脊顶2.jpg"],
        "cmap": "Oranges"
    },
    "三川脊顶": {
        "intro": "**三川脊顶**是闽南民居中等级较高的屋脊样式，屋脊中段下沉、两端上翘，形成三段式轮廓，常见于祠堂、大户宅第。它在燕尾脊基础上发展而来，强调庄重与秩序，是闽南宗族文化与建筑等级的直观体现，核心分布于福建闽南地区，粤东、台湾有少量遗存。",
        "icon": "photos/images2/三川脊顶.jpg",
        "imgs": ["photos/images2/三川脊顶1.jpg","photos/images2/三川脊顶2.jpg"],
        "cmap": "Reds"
    },
    "马鞍脊顶": {
        "intro": "**马鞍脊顶**又称马背脊，屋脊中间下沉、两端高翘，形似马鞍，是闽南、粤东、台湾地区极具辨识度的民居屋脊造型。造型柔美且结构稳固，适配沿海台风气候，兼具排水、抗风与装饰美学，属于闽南红砖建筑体系核心符号，北方与中西部地区基本无原生分布。",
        "icon": "photos/images2/马鞍脊顶.jpg",
        "imgs": ["photos/images2/马鞍脊顶1.jpg","photos/images2/马鞍脊顶2.jpg"],
        "cmap": "YlOrBr"
    },
    "囤顶": {
        "intro": "**囤顶**是中国北方辽西地区特有的民居屋顶样式，屋顶微拱呈弧形、中央稍高、前后略低，无瓦，多以灰背、土坯抹成。核心功能为防积雪、抗风沙、抗压，适应辽西寒冷多雪、风沙大的气候，全国90%以上集中在辽宁西部（朝阳、兴城、锦州），南方及北方大部分地区基本无分布。",
        "icon": "photos/images2/囤顶.jpg",
        "imgs": ["photos/images2/囤顶1.jpg","photos/images2/囤顶2.jpg"],
        "cmap": "Blues"
    },
    "单坡顶": {
        "intro": "**单坡顶**是最简单原始的民居坡屋顶，整体仅一面排水坡面，构造极简、造价低廉。核心集中于黄土高原晋陕两地，华北、西北、西南山地为辅，多用于厢房、附属用房或山地窄巷，东南沿海平原几乎无原生传统单坡民居分布。",
        "icon": "photos/images2/单坡顶.jpg",
        "imgs": ["photos/images2/单坡顶1.jpg","photos/images2/单坡顶2.jpg"],
        "cmap": "Greens"
    },
    "总览": {
        "intro": """
- **地域特征**：东南沿海以燕尾脊、马鞍脊、三川脊为代表，强调装饰性与抗台风；北方以囤顶、单坡顶为代表，强调功能性与抗寒抗风沙。
- **文化内核**：屋顶不仅是建筑结构，更是地域文化、宗族礼制、气候适应的综合载体。
- **分布规律**：核心样式高度集中于特定文化圈，跨区域传播痕迹明显，体现移民与文化扩散。
"""
    }
}

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

# 会话状态
if "current_page" not in st.session_state:
    st.session_state.current_page = "总览"

# --------------------------
# 顶部6个按钮
# --------------------------
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

# --------------------------
# 动态内容
# --------------------------
selected = st.session_state.current_page

if selected != "总览":
    # 一级标题：深色无背景
    st.markdown(f'<div class="primary-title">{selected}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # 二级标题：白色+背景
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

else:
    # ========= 总览页面 =========
    st.markdown('<div class="primary-title">总览</div>', unsafe_allow_html=True)

    col_sankey, col_info = st.columns([3, 2])

    with col_sankey:
        st.markdown('<div class="secondary-title">🔗 屋顶样式-子区域-南北方 分布流向</div>', unsafe_allow_html=True)
        # 桑基图代码
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
            node=dict(pad=20, thickness=20, line=dict(color="#f7f0e6", width=0.3), label=labels, color=node_colors),
            link=dict(source=sources, target=targets, value=values, color=link_colors)
        ))
        fig.update_layout(title_text="", font_size=12, font_color="#6b574a", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=500)
        st.plotly_chart(fig, use_container_width=True)

    with col_info:
        st.markdown('<div class="secondary-title">中国民居屋顶样式总览</div>', unsafe_allow_html=True)
        st.markdown(roof_info["总览"]["intro"])