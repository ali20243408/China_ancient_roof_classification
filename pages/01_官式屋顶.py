import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# ------------------------------
# 页面配置
# ------------------------------
st.set_page_config(
    page_title="Chinese Ancient Roof Visualization",
    layout="wide",
    page_icon="🏯"
)

# ------------------------------
# 样式完全不变
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
# 乱码修复：全局使用英文，不依赖中文字体
# ------------------------------
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False

# ------------------------------
# 顶部标题（保留不变）
# ------------------------------
st.markdown('<p class="main_title"> Six Classical Imperial Roof Styles & Ancient Chinese Social Hierarchy</p >', unsafe_allow_html=True)

# ------------------------------
# 核心数据（图表文字改为英文）
# ------------------------------
button_order = [
    "Double Eave Hip Roof",
    "Double Eave Rested Roof",
    "Single Eave Hip Roof",
    "Single Eave Rested Roof",
    "Overhanging Gable Roof",
    "Flush Gable Roof"
]
roof_counts = [4, 9, 7, 14, 22, 38]

roof_info = {
    "Double Eave Hip Roof": {"img": "photos/images/重檐庑殿顶.jpg", "desc": "Highest-level roof in ancient Chinese architecture, exclusively for imperial palaces."},
    "Double Eave Rested Roof": {"img": "photos/images/重檐歇山顶.jpg", "desc": "Second-highest level, used for important palace gates and main halls."},
    "Single Eave Hip Roof": {"img": "photos/images/单檐庑殿顶.jpg", "desc": "Third-highest level, for secondary imperial halls and temples."},
    "Single Eave Rested Roof": {"img": "photos/images/单檐歇山顶.jpg", "desc": "Fourth level, for side halls and palace gates."},
    "Overhanging Gable Roof": {"img": "photos/images/悬山顶.jpg", "desc": "Fifth level, for official residences and auxiliary buildings."},
    "Flush Gable Roof": {"img": "photos/images/硬山顶.jpg", "desc": "Basic level, for ordinary houses and storage rooms."}
}

df_roof_level = pd.DataFrame({
    "Roof Style": button_order,
    "Level": ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6"]
})

# ------------------------------
# 初始化选中状态
# ------------------------------
if "selected" not in st.session_state:
    st.session_state.selected = None

# ------------------------------
# 三栏布局
# ------------------------------
col_left, col_mid, col_right = st.columns([1.2, 1.5, 1.5])

# ------------------------------
# 左侧1：饼图
# ------------------------------
with col_left:
    with st.container(border=False):
        st.markdown('<p class="chart_title">Distribution of Roof Styles in Forbidden City</p >', unsafe_allow_html=True)
        labels = button_order
        sizes = roof_counts
        red_palette = ["#8B0000", "#A52A2A", "#B22222", "#CD5C5C", "#F08080", "#FA8072"]
        explode = [0.0]*6
        if st.session_state.selected is not None and st.session_state.selected in labels:
            explode[labels.index(st.session_state.selected)] = 0.1
        fig, ax = plt.subplots(figsize=(8,8), facecolor="#E8D9C0")
        ax.set_facecolor("#E8D9C0")
        wedges, texts, autotexts = ax.pie(
            sizes,
            explode=explode,
            labels=labels,
            colors=red_palette,
            autopct="%1.2f%%",
            startangle=90,
            wedgeprops={"linewidth":2, "edgecolor":"white"},
            textprops={"fontsize": 8, "color": "#333"}
        )
        for t in autotexts:
            t.set_color("white")
            t.set_fontweight("bold")
        ax.axis("equal")
        st.pyplot(fig)

# ------------------------------
# 左侧2：图表英文
# ------------------------------
with col_left:
    with st.container(border=False):
        st.markdown('<p class="chart_title">Roof Level: Quantity & Percentage</p >', unsafe_allow_html=True)
        df_gugong_for_chart = pd.DataFrame({
            "Roof Style": button_order,
            "Count": roof_counts,
            "Level": ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6"],
            "Percentage": [round(c/sum(roof_counts)*100, 2) for c in roof_counts]
        })
        fig2 = make_subplots(specs=[[{"secondary_y": True}]])
        fig2.add_trace(go.Bar(x=df_gugong_for_chart["Level"], y=df_gugong_for_chart["Count"], name="Count", marker_color="#990000"), secondary_y=False)
        fig2.add_trace(go.Scatter(x=df_gugong_for_chart["Level"], y=df_gugong_for_chart["Percentage"], name="Percentage", mode='lines+markers', marker_color="#66B2FF"), secondary_y=True)
        fig2.update_layout(height=320, paper_bgcolor="#E8D9C0", plot_bgcolor="#E8D9C0")
        st.plotly_chart(fig2, width="stretch")

# ------------------------------
# 中间区域（图片不变，文字改为英文）
# ------------------------------
with col_mid:
    st.markdown('<p class="title">Six Classical Roof Styles</p >', unsafe_allow_html=True)
    row1 = st.columns(3)
    for i, name in enumerate(button_order[:3]):
        info = roof_info[name]
        with row1[i]:
            st.image(info["img"], caption=name)
            if st.button("Details", key=name):
                st.session_state.selected = name
                st.rerun()

    row2 = st.columns(3)
    for i, name in enumerate(button_order[3:]):
        info = roof_info[name]
        with row2[i]:
            st.image(info["img"], caption=name)
            if st.button("Details", key=f"b_{name}"):
                st.session_state.selected = name
                st.rerun()

    if st.session_state.selected is not None:
        s = st.session_state.selected
        build = {
            "Level 1": "Hall of Supreme Harmony",
            "Level 2": "Meridian Gate",
            "Level 3": "Hall of Mental Cultivation",
            "Level 4": "Eastern & Western Palaces",
            "Level 5": "Side Halls",
            "Level 6": "Storage & Service Rooms"
        }
        st.markdown(f"""
        <div class="analysis">
        <h3>{s}</h3>
        <p>Level: {df_roof_level[df_roof_level['Roof Style'] == s]['Level'].values[0]}</p >
        <p>Introduction: {roof_info[s]['desc']}</p >
        <p>Building: {build[df_roof_level[df_roof_level['Roof Style'] == s]['Level'].values[0]]}</p >
        </div>
        """, unsafe_allow_html=True)
        try:
            st.image(f"photos/images/{s}1.jpg", use_container_width=True)
        except:
            pass

# ------------------------------
# 右侧图表全部改为英文
# ------------------------------
with col_right:
    with st.container(border=False):
        st.markdown('<p class="chart_title">Comparison of Roof Styles Across Complexes</p >', unsafe_allow_html=True)
        df_compare_multi = pd.DataFrame([
            {"Roof Style": "Double Eave Hip Roof", "Forbidden City":4,"Shenyang":0,"Mansion":0,"Yamen":0,"Governor":0,"County":0},
            {"Roof Style": "Double Eave Rested Roof", "Forbidden City":9,"Shenyang":3,"Mansion":1,"Yamen":0,"Governor":0,"County":0},
            {"Roof Style": "Single Eave Hip Roof", "Forbidden City":7,"Shenyang":2,"Mansion":2,"Yamen":0,"Governor":0,"County":0},
            {"Roof Style": "Single Eave Rested Roof", "Forbidden City":14,"Shenyang":10,"Mansion":8,"Yamen":3,"Governor":4,"County":2},
            {"Roof Style": "Overhanging Gable Roof", "Forbidden City":22,"Shenyang":16,"Mansion":15,"Yamen":12,"Governor":10,"County":9},
            {"Roof Style": "Flush Gable Roof", "Forbidden City":38,"Shenyang":32,"Mansion":42,"Yamen":45,"Governor":40,"County":48},
        ]).melt(id_vars=["Roof Style"], var_name="Complex", value_name="Count")
        fig3 = px.bar(df_compare_multi, x="Roof Style", y="Count", color="Complex", barmode="group")
        fig3.update_layout(height=320, paper_bgcolor="#E8D9C0", plot_bgcolor="#E8D9C0")
        st.plotly_chart(fig3, width="stretch")

with col_right:
    with st.container(border=False):
        st.markdown('<p class="chart_title">Level Distribution</p >', unsafe_allow_html=True)
        df_merge = pd.merge(df_compare_multi, df_roof_level, left_on="Roof Style", right_on="Roof Style")
        fig4 = px.histogram(df_merge, x="Complex", y="Count", color="Level", barnorm="percent")
        fig4.update_layout(height=320, paper_bgcolor="#E8D9C0", plot_bgcolor="#E8D9C0")
        st.plotly_chart(fig4, width="stretch")