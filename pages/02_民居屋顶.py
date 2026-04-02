import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import os

# ------------------------------
# 页面配置
# ------------------------------
st.set_page_config(
    page_title="中国民居屋顶可视化",
    layout="wide",
    page_icon="🏠"
)

# ------------------------------
# 【核心修复：中文乱码 云端+本地双兼容】
# ------------------------------
plt.rcParams["font.sans-serif"] = ["WenQuanYi Zen Hei", "SimHei", "DejaVu Sans", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.family"] = "sans-serif"

# ------------------------------
# 样式（完全保持原版不变）
# ------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #F2E9D8 !important;
    background-image: url("https://img.baidu.com/it/u=3891156789,1234567890&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=800") !important;
    background-blend-mode: overlay !important;
    background-size: 200px 200px !important;
    background-repeat: repeat !important;
    opacity: 0.98 !important;
}
div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
    background-color: rgba(242,233,216,0.95) !important;
    border-radius: 8px !important;
}
div[data-testid="stContainer"] {
    border: none !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="stVerticalBlock"] {
    display: flex !important;
    flex-direction: column !important;
    min-height: 220px !important;
    justify-content: flex-start !important;
}
div[data-testid="stImage"] {
    margin-top: 0 !important;
}
div[data-testid="stVerticalBlock"] .element-container:nth-last-child(2) {
    margin-bottom: auto !important;
}

.stButton {
    display: flex !important;
    justify-content: center !important;
    margin-top: 8px !important;
}
.stButton > button {
    width: 90px !important;
    height: 38px !important;
    background-color: #D9B48B !important;
    border: none !important;
    border-radius: 4px !important;
    color: #4A2E2A !important;
    font-weight: bold !important;
    font-family: "SimHei", "KaiTi" !important;
    font-size: 14px !important;
}
.stButton > button:hover {
    background-color: #B22234 !important;
    border: none !important;
    color: white !important;
}

.main_title {
    font-size: 42px !important;
    font-weight: bold !important;
    color: #8B4513 !important;
    text-align: center !important;
    margin-bottom: 24px !important;
    font-family: "SimHei", "KaiTi", "STSong" !important;
    letter-spacing: 3px !important;
}
.chart_title {
    font-size: 18px !important;
    font-weight: bold !important;
    color: white !important;
    background-color: #8B4513 !important;
    padding: 8px 15px !important;
    border-radius: 4px !important;
    margin-bottom: 15px !important;
    font-family: "SimHei", "KaiTi" !important;
}
.title {
    font-size: 20px !important;
    font-weight: bold !important;
    color: #8B4513 !important;
    margin-bottom: 15px !important;
    font-family: "SimHei", "KaiTi" !important;
}
.analysis {
    font-size: 14px !important;
    color: #5C3317 !important;
    line-height: 1.6 !important;
    font-family: "SimHei", "KaiTi" !important;
    padding: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# 标题
# ------------------------------
st.markdown('<p class="main_title">中国传统民居屋顶样式与地域文化</p>', unsafe_allow_html=True)

# ------------------------------
# 民居屋顶数据
# ------------------------------
button_order = [
    "硬山顶",
    "悬山顶",
    "歇山顶",
    "攒尖顶",
    "卷棚顶",
    "平顶"
]

roof_counts = [38, 22, 14, 7, 9, 4]

roof_info = {
    "硬山顶": {"img": "photos/images/硬山顶.jpg", "desc": "最常见民居屋顶，两坡平直，山墙坚固，防火防盗，广泛用于北方四合院、南方民居"},
    "悬山顶": {"img": "photos/images/悬山顶.jpg", "desc": "两坡出山，屋檐外伸，利于排水通风，主要用于南方民居、商铺、祠堂"},
    "歇山顶": {"img": "photos/images/歇山顶.jpg", "desc": "等级较高的民居屋顶，多出现于富商、官宦住宅、宗祠、书院"},
    "攒尖顶": {"img": "photos/images/攒尖顶.jpg", "desc": "多用于亭子、阁楼、塔、园林建筑，民居中较少见，多见于景观建筑"},
    "卷棚顶": {"img": "photos/images/卷棚顶.jpg", "desc": "线条柔和，无正脊，多用于园林、书房、厢房，气质文雅"},
    "平顶": {"img": "photos/images/平顶.jpg", "desc": "干旱少雨地区主流屋顶，晾晒方便，多见于西北、黄土高原、新疆民居"}
}

df_roof_level = pd.DataFrame({
    "屋顶样式": button_order,
    "拼音": ["yìng shān dǐng", "xuán shān dǐng", "xiē shān dǐng", "cuán jiān dǐng", "juǎn péng dǐng", "píng dǐng"],
    "地域分布": ["全国通用", "南方为主", "官宦/富商", "园林/亭台", "文人/园林", "西北干旱区"]
})

# ------------------------------
# 状态
# ------------------------------
if "selected" not in st.session_state:
    st.session_state.selected = None

# ------------------------------
# 布局
# ------------------------------
col_left, col_mid, col_right = st.columns([1.2, 1.5, 1.5])

# ------------------------------
# 左侧1：饼图
# ------------------------------
with col_left:
    with st.container(border=False):
        st.markdown('<p class="chart_title">民居屋顶样式占比</p>', unsafe_allow_html=True)
        labels = button_order
        sizes = roof_counts
        palette = ["#8B4513", "#CD853F", "#D2B48C", "#A67C52", "#C8A272", "#876445"]
        explode = [0.0] * 6
        if st.session_state.selected is not None and st.session_state.selected in labels:
            explode[labels.index(st.session_state.selected)] = 0.1

        fig, ax = plt.subplots(figsize=(8, 8), facecolor="#E8D9C0")
        ax.set_facecolor("#E8D9C0")
        wedges, texts, autotexts = ax.pie(
            x=sizes,
            explode=explode,
            labels=labels,
            colors=palette,
            autopct="%1.2f%%",
            startangle=90,
            wedgeprops={"linewidth": 2, "edgecolor": "white"},
            textprops={"fontsize": 8, "family": "SimHei", "color": "#333"}
        )
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontweight("bold")
        ax.axis("equal")
        st.pyplot(fig, width="stretch")
        st.markdown("""<div class="analysis"><b>分析：</b><br>硬山顶与悬山顶是民居绝对主流，适应普通百姓居住需求；歇山顶、攒尖顶多用于身份较高家庭或公共建筑。</div>""", unsafe_allow_html=True)

# ------------------------------
# 左侧2：数量与占比
# ------------------------------
with col_left:
    with st.container(border=False):
        st.markdown('<p class="chart_title">民居屋顶数量与占比</p>', unsafe_allow_html=True)
        df_chart = pd.DataFrame({
            "屋顶样式": button_order,
            "数量": roof_counts,
            "占比": [round(c / sum(roof_counts) * 100, 2) for c in roof_counts]
        })
        fig2 = make_subplots(specs=[[{"secondary_y": True}]])
        fig2.add_trace(go.Bar(x=df_chart["屋顶样式"], y=df_chart["数量"], name="数量", marker_color="#8B4513"), secondary_y=False)
        fig2.add_trace(go.Scatter(x=df_chart["屋顶样式"], y=df_chart["占比"], name="占比", mode='lines+markers', marker_color="#1E90FF"), secondary_y=True)
        fig2.update_layout(
            height=320,
            xaxis_tickangle=-45,
            font=dict(family="SimHei"),
            legend=dict(orientation="h", y=1.02),
            paper_bgcolor="#E8D9C0",
            plot_bgcolor="#E8D9C0"
        )
        st.plotly_chart(fig2, width="stretch")
        st.markdown("""<div class="analysis"><b>分析：</b><br>民居屋顶以实用为主，等级限制宽松，更强调气候适应性与生活功能，体现民间建筑智慧。</div>""", unsafe_allow_html=True)

# ------------------------------
# 中间：图片 + 详情
# ------------------------------
with col_mid:
    st.markdown('<p class="title">六大民居屋顶样式</p>', unsafe_allow_html=True)
    row1 = st.columns(3)
    for i, name in enumerate(button_order[:3]):
        info = roof_info[name]
        with row1[i]:
            st.image(info["img"], width="stretch", caption=f"{name}\n{df_roof_level[df_roof_level['屋顶样式'] == name]['拼音'].values[0]}")
            if st.button("详情", key=name):
                st.session_state.selected = name
                st.rerun()

    row2 = st.columns(3)
    for i, name in enumerate(button_order[3:]):
        info = roof_info[name]
        with row2[i]:
            st.image(info["img"], width="stretch", caption=f"{name}\n{df_roof_level[df_roof_level['屋顶样式'] == name]['拼音'].values[0]}")
            if st.button("详情", key=f"b_{name}"):
                st.session_state.selected = name
                st.rerun()

    if st.session_state.selected is not None:
        s = st.session_state.selected
        region = df_roof_level[df_roof_level["屋顶样式"] == s]["地域分布"].values[0]
        st.markdown(f"""
        <div class="analysis">
        <h3>{s}</h3>
        <p>主要分布：{region}</p>
        <p>简介：{roof_info[s]['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        try:
            real_img_path = f"photos/images/{s}1.jpg"
            st.image(real_img_path, caption=f"{s} 真实建筑", width="stretch")
        except:
            st.warning(f"未找到真实图片：{real_img_path}")

# ------------------------------
# 右侧1：地域分布对比
# ------------------------------
with col_right:
    with st.container(border=False):
        st.markdown('<p class="chart_title">中国七大区域民居屋顶分布</p>', unsafe_allow_html=True)
        df_area = pd.DataFrame([
            {"屋顶":"硬山顶","华北":10,"东北":8,"华东":6,"华中":5,"华南":3,"西南":4,"西北":2},
            {"屋顶":"悬山顶","华北":2,"东北":1,"华东":9,"华中":8,"华南":10,"西南":7,"西北":1},
            {"屋顶":"歇山顶","华北":3,"东北":2,"华东":4,"华中":3,"华南":2,"西南":3,"西北":1},
            {"屋顶":"攒尖顶","华北":1,"东北":0,"华东":2,"华中":1,"华南":3,"西南":2,"西北":1},
            {"屋顶":"卷棚顶","华北":2,"东北":1,"华东":3,"华中":2,"华南":2,"西南":1,"西北":0},
            {"屋顶":"平顶","华北":1,"东北":1,"华东":0,"华中":0,"华南":0,"西南":0,"西北":9},
        ]).melt(id_vars=["屋顶"], var_name="区域", value_name="数量")

        color_map = {
            "华北":"#8B4513","东北":"#A0522D","华东":"#CD853F",
            "华中":"#D2B48C","华南":"#C8A272","西南":"#B8860B","西北":"#876445"
        }
        fig3 = px.bar(df_area, x="屋顶", y="数量", color="区域", barmode="group", color_discrete_map=color_map)
        fig3.update_layout(
            height=320,
            xaxis_tickangle=-45,
            font=dict(family="SimHei"),
            legend=dict(orientation="v", y=0.5, x=-0.25),
            paper_bgcolor="#E8D9C0",
            plot_bgcolor="#E8D9C0"
        )
        st.plotly_chart(fig3, width="stretch")
        st.markdown("""<div class="analysis"><b>分析：</b><br>北方多硬山、平顶；南方多悬山；西北以平顶为主；华东、华南多雨，排水优先。屋顶完全适配气候地理。</div>""", unsafe_allow_html=True)

# ------------------------------
# 右侧2：结构占比
# ------------------------------
with col_right:
    with st.container(border=False):
        st.markdown('<p class="chart_title">各区域屋顶结构占比</p>', unsafe_allow_html=True)
        fig4 = px.histogram(df_area, x="区域", y="数量", color="屋顶", barnorm="percent", color_discrete_map=color_map)
        fig4.update_layout(
            height=320,
            xaxis_tickangle=-45,
            font=dict(family="SimHei"),
            legend=dict(orientation="v", y=0.5, x=-0.25),
            paper_bgcolor="#E8D9C0",
            plot_bgcolor="#E8D9C0"
        )
        st.plotly_chart(fig4, width="stretch")
        st.markdown("""<div class="analysis"><b>分析：</b><br>民居屋顶无严格等级束缚，完全由气候、材料、生活方式决定，体现实用主义与地域智慧。</div>""", unsafe_allow_html=True)