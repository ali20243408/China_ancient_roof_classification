import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
# 【全局Matplotlib中文修复，必须放在代码最顶部】
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'WenQuanYi Micro Hei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
# ------------------------------
# 页面配置
# ------------------------------
st.set_page_config(
    page_title="中国古建筑屋顶等级可视化",
    layout="wide",
    page_icon="🏯"
)

# ------------------------------
# 样式：只去掉按钮边框，其余完全不变
# ------------------------------
st.markdown("""
<style>
/* 全局页面底色：仿做旧米黄色，匹配参考图风格 */
.stApp {
    background-color: #F2E9D8 !important;
    background-image: url("https://img.baidu.com/it/u=3891156789,1234567890&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=800") !important;
    background-blend-mode: overlay !important;
    background-size: 200px 200px !important;
    background-repeat: repeat !important;
    opacity: 0.98 !important;
}
/* 容器底色：半透米黄，保证内容清晰 */
div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
    background-color: rgba(242,233,216,0.95) !important;
    border-radius: 8px !important;
}
/* 隐藏st.container的边框（分隔线） */
div[data-testid="stContainer"] {
    border: none !important;
}
/* 单个单元格统一高度 + 顶部对齐 → 所有图片上边缘齐平 */
div[data-testid="stHorizontalBlock"] > div[data-testid="stVerticalBlock"] {
    display: flex !important;
    flex-direction: column !important;
    min-height: 220px !important;
    justify-content: flex-start !important;
}
/* 图片顶部紧贴，保证上边框一条线 */
div[data-testid="stImage"] {
    margin-top: 0 !important;
}
/* 汉字+拼音文字区块底部统一截止对齐 */
div[data-testid="stVerticalBlock"] .element-container:nth-last-child(2) {
    margin-bottom: auto !important;
}

/* 详情按钮：只去掉边框，颜色、大小、文字全部不变 */
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
    font-family: "WenQuanYi Zen Hei", "SimHei", "KaiTi" !important;
    font-size: 14px !important;
}
.stButton > button:hover {
    background-color: #B22234 !important;
    border: none !important;
    color: white !important;
}

/* 顶部大标题样式：只改这里，变得更大更国风 */
.main_title {
    font-size: 42px !important;
    font-weight: bold !important;
    color: #8B4513 !important;
    text-align: center !important;
    margin-bottom: 24px !important;
    font-family: "WenQuanYi Zen Hei", "SimHei", "KaiTi", "STSong" !important;
    letter-spacing: 3px !important;
}
/* 图表标题样式：深色底白字，同色系深棕 */
.chart_title {
    font-size: 18px !important;
    font-weight: bold !important;
    color: white !important;
    background-color: #8B4513 !important;
    padding: 8px 15px !important;
    border-radius: 4px !important;
    margin-bottom: 15px !important;
    font-family: "WenQuanYi Zen Hei", "SimHei", "KaiTi" !important;
}
/* 中间区域标题样式 */
.title {
    font-size: 20px !important;
    font-weight: bold !important;
    color: #8B4513 !important;
    margin-bottom: 15px !important;
    font-family: "WenQuanYi Zen Hei", "SimHei", "KaiTi" !important;
}
.analysis {
    font-size: 14px !important;
    color: #5C3317 !important;
    line-height: 1.6 !important;
    font-family: "WenQuanYi Zen Hei", "SimHei", "KaiTi" !important;
    padding: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# 【已修复】Matplotlib云端通用中文字体
# ------------------------------
plt.rcParams["font.sans-serif"] = ["WenQuanYi Zen Hei", "WenQuanYi Micro Hei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# ------------------------------
# 顶部大标题
# ------------------------------
st.markdown('<p class="main_title"> 六大主流官式屋顶样式 映射中国古代封建等级制度文化</p >', unsafe_allow_html=True)

# ------------------------------
# 核心数据
# ------------------------------
button_order = [
    "重檐庑殿顶",
    "重檐歇山顶",
    "单檐庑殿顶",
    "单檐歇山顶",
    "悬山顶",
    "硬山顶"
]
roof_counts = [4, 9, 7, 14, 22, 38]

roof_info = {
    "重檐庑殿顶": {"img": "photos/images/重檐庑殿顶.jpg", "desc": "中国古建筑最高等级屋顶，五脊四坡，重檐为至尊形制；仅用于皇宫主殿"},
    "重檐歇山顶": {"img": "photos/images/重檐歇山顶.jpg", "desc": "第二等级屋顶，九脊四坡，重檐建制；用于皇宫重要门殿、坛庙正殿"},
    "单檐庑殿顶": {"img": "photos/images/单檐庑殿顶.jpg", "desc": "第三等级屋顶，五脊四坡，单檐建制；用于皇宫次要殿堂、皇家坛庙"},
    "单檐歇山顶": {"img": "photos/images/单檐歇山顶.jpg", "desc": "第四等级屋顶，九脊四坡，单檐建制；用于皇宫配殿、宫门、王府主殿"},
    "悬山顶": {"img": "photos/images/悬山顶.jpg", "desc": "第五等级屋顶，两坡出山；用于皇家附属建筑、王府配殿、官员住宅"},
    "硬山顶": {"img": "photos/images/硬山顶.jpg", "desc": "最低等级屋顶，两坡平直；用于普通房屋、库房、杂役房等基础建筑"}
}

df_roof_level = pd.DataFrame({
    "屋顶样式": button_order,
    "拼音": ["chóng yán wǔ diàn dǐng", "chóng yán xiē shān dǐng", "dān yán wǔ diàn dǐng", "dān yán xiē shān dǐng", "xuán shān dǐng", "yìng shān dǐng"],
    "等级定位": ["至尊（1级）", "高级（2级）", "中高（3级）", "中级（4级）", "普通（5级）", "基础（6级）"]
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
# 左侧1：饼图（终极修复，双重兜底，云端必显中文）
# ------------------------------
with col_left:
    with st.container(border=False):
        st.markdown('<p class="chart_title">故宫屋顶样式占比</p >', unsafe_allow_html=True)
        labels = button_order
        sizes = roof_counts
        red_palette = ["#8B0000", "#A52A2A", "#B22222", "#CD5C5C", "#F08080", "#FA8072"]
        explode = [0.0] * 6
        if st.session_state.selected is not None:
            explode[labels.index(st.session_state.selected)] = 0.1

        # 【第一步：强制重置Matplotlib全局字体，确保饼图读取】
        plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'WenQuanYi Micro Hei', 'SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False

        # 【第二步：创建画布，强制指定字体】
        fig, ax = plt.subplots(figsize=(8, 8), facecolor="#E8D9C0")
        ax.set_facecolor("#E8D9C0")

        # 【第三步：饼图绘制，三重字体兜底】
        wedges, texts, autotexts = ax.pie(
            sizes,
            explode=explode,
            labels=labels,
            colors=red_palette,
            autopct="%1.2f%%",
            startangle=90,
            wedgeprops={"linewidth": 2, "edgecolor": "white"},
            textprops={
                "fontsize": 8,
                "fontfamily": "WenQuanYi Zen Hei",  # 核心：强制指定云端字体
                "color": "#333",
                "fontweight": "normal"
            }
        )

        # 【第四步：单独给标签+百分比设置字体，彻底兜底】
        for text in texts:
            text.set_fontfamily("WenQuanYi Zen Hei")
            text.set_fontsize(8)
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontweight("bold")
            autotext.set_fontfamily("WenQuanYi Zen Hei")

        ax.axis("equal")
        st.pyplot(fig)
        st.markdown(
            """<div class="analysis"><b>分析：</b><br>硬山、悬山等样式占比超六成，构成故宫建筑主体；庑殿、歇山等样式占比极低，仅用于核心殿宇。</div>""",
            unsafe_allow_html=True)
# ------------------------------
# 左侧2：故宫屋顶等级-数量与占比（Plotly字体已修复）
# ------------------------------
    with st.container(border=False):
        st.markdown('<p class="chart_title">故宫屋顶等级-数量与占比</p >', unsafe_allow_html=True)
        df_gugong_for_chart = pd.DataFrame({
            "屋顶样式": button_order,
            "数量": roof_counts,
            "等级名称": ["至尊（1级）", "高级（2级）", "中高（3级）", "中级（4级）", "普通（5级）", "基础（6级）"],
            "占比": [round(c/sum(roof_counts)*100, 2) for c in roof_counts]
        })
        fig2 = make_subplots(specs=[[{"secondary_y": True}]])
        fig2.add_trace(go.Bar(x=df_gugong_for_chart["等级名称"], y=df_gugong_for_chart["数量"], name="数量", marker_color="#990000"), secondary_y=False)
        fig2.add_trace(go.Scatter(x=df_gugong_for_chart["等级名称"], y=df_gugong_for_chart["占比"], name="占比", mode='lines+markers', marker_color="#66B2FF"), secondary_y=True)
        fig2.update_layout(
            height=320,
            xaxis_tickangle=-45,
            font=dict(family="WenQuanYi Zen Hei"),
            legend=dict(orientation="h", y=1.02),
            paper_bgcolor="#E8D9C0",
            plot_bgcolor="#E8D9C0"
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("""<div class="analysis"><b>分析：</b><br>屋顶等级与数量呈反比；等级越低数量越多，高等级屋顶严格限量，体现了封建等级制度。</div>""", unsafe_allow_html=True)

# ------------------------------
# 中间区域
# ------------------------------
with col_mid:
    st.markdown('<p class="title">六大屋顶样式</p >', unsafe_allow_html=True)
    row1 = st.columns(3)
    for i, name in enumerate(button_order[:3]):
        info = roof_info[name]
        with row1[i]:
            st.image(info["img"], caption=f"{name}\n{df_roof_level[df_roof_level['屋顶样式'] == name]['拼音'].values[0]}")
            if st.button("详情", key=name):
                st.session_state.selected = name
                st.rerun()

    row2 = st.columns(3)
    for i, name in enumerate(button_order[3:]):
        info = roof_info[name]
        with row2[i]:
            st.image(info["img"], caption=f"{name}\n{df_roof_level[df_roof_level['屋顶样式'] == name]['拼音'].values[0]}")
            if st.button("详情", key=f"b_{name}"):
                st.session_state.selected = name
                st.rerun()

    if st.session_state.selected is not None:
        s = st.session_state.selected
        build = {
            "至尊（1级）": "太和殿、乾清宫",
            "高级（2级）": "午门、神武门",
            "中高（3级）": "体仁阁、弘义阁",
            "中级（4级）": "东西六宫主殿",
            "普通（5级）": "配殿、厢房",
            "基础（6级）": "库房、杂役房"
        }
        st.markdown(f"""
        <div class="analysis">
        <h3>{s}</h3>
        <p>等级：{df_roof_level[df_roof_level['屋顶样式'] == s]['等级定位'].values[0]}</p >
        <p>简介：{roof_info[s]['desc']}</p >
        <p>代表建筑：{build[df_roof_level[df_roof_level['屋顶样式'] == s]['等级定位'].values[0]]}</p >
        </div>
        """, unsafe_allow_html=True)
        real_img_path = f"photos/images/{s}1.jpg"
        try:
            st.image(real_img_path, caption=f"{s} 真实建筑", use_container_width=True)
        except:
            st.warning(f"未找到真实图片：{real_img_path}")

# ------------------------------
# 右侧1：六大建筑群屋顶全景对比（Plotly字体修复）
# ------------------------------
with col_right:
    with st.container(border=False):
        st.markdown('<p class="chart_title">六大建筑群屋顶全景对比</p >', unsafe_allow_html=True)
        df_compare_multi = pd.DataFrame([
            {"屋顶样式": "重檐庑殿顶", "故宫":4,"沈阳故宫":0,"王府":0,"南阳府衙":0,"直隶总督署":0,"平遥县衙":0},
            {"屋顶样式": "重檐歇山顶", "故宫":9,"沈阳故宫":3,"王府":1,"南阳府衙":0,"直隶总督署":0,"平遥县衙":0},
            {"屋顶样式": "单檐庑殿顶", "故宫":7,"沈阳故宫":2,"王府":2,"南阳府衙":0,"直隶总督署":0,"平遥县衙":0},
            {"屋顶样式": "单檐歇山顶", "故宫":14,"沈阳故宫":10,"王府":8,"南阳府衙":3,"直隶总督署":4,"平遥县衙":2},
            {"悬山顶": "悬山顶", "故宫":22,"沈阳故宫":16,"王府":15,"南阳府衙":12,"直隶总督署":10,"平遥县衙":9},
            {"屋顶样式": "硬山顶", "故宫":38,"沈阳故宫":32,"王府":42,"南阳府衙":45,"直隶总督署":40,"平遥县衙":48},
        ]).melt(id_vars=["屋顶样式"], var_name="建筑群", value_name="数量")
        palace_colors = {
            "故宫": "#872907",
            "沈阳故宫": "#1B4E2F",
            "王府": "#CF721B",
            "南阳府衙": "#CF8D46",
            "直隶总督署": "#5D0F03",
            "平遥县衙": "#2F2F2F"
        }
        fig3 = px.bar(df_compare_multi, x="屋顶样式", y="数量", color="建筑群", barmode="group", color_discrete_map=palace_colors)
        fig3.update_layout(
            height=320,
            xaxis_tickangle=-45,
            font=dict(family="WenQuanYi Zen Hei"),
            legend=dict(orientation="v", y=0.5, x=-0.25, xanchor="right"),
            paper_bgcolor="#E8D9C0",
            plot_bgcolor="#E8D9C0"
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("""<div class="analysis"><b>分析：</b><br>高等级屋顶（重檐庑殿顶、重檐歇山顶）仅存于故宫与沈阳故宫，体现皇家建筑的等级特权；地方衙署以硬山、悬山为主，横向对比映射等级规制。</div>""", unsafe_allow_html=True)

# ------------------------------
# 右侧2：屋顶等级结构占比（Plotly字体修复）
# ------------------------------
    with st.container(border=False):
        st.markdown('<p class="chart_title">屋顶等级结构占比</p >', unsafe_allow_html=True)
        df_merge = pd.merge(df_compare_multi, df_roof_level[["屋顶样式", "等级定位"]], on="屋顶样式")
        level_colors = {
            "至尊（1级）": "#872907",
            "高级（2级）": "#CF721B",
            "中高（3级）": "#5D0F03",
            "中级（4级）": "#CF8D46",
            "普通（5级）": "#A67C52",
            "基础（6级）": "#2F2F2F"
        }
        fig4 = px.histogram(df_merge, x="建筑群", y="数量", color="等级定位", barnorm="percent", color_discrete_map=level_colors)
        fig4.update_layout(
            height=320,
            xaxis_tickangle=-45,
            font=dict(family="WenQuanYi Zen Hei"),
            legend=dict(orientation="v", y=0.5, x=-0.25, xanchor="right"),
            paper_bgcolor="#E8D9C0",
            plot_bgcolor="#E8D9C0"
        )
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("""<div class="analysis"><b>分析：</b><br>建筑规制越高，屋顶样式种类越丰富。皇家建筑群样式最全，地方官署、县衙样式逐级减少，彰显古代建筑礼制的层级秩序。</div>""", unsafe_allow_html=True)