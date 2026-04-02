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
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# ====================== 页面基础配置 ======================
st.set_page_config(page_title="园林屋顶样式可视化", layout="wide")

# 全局字体防乱码
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 页面背景 + 小标题背景 + 大标题颜色 + 按钮样式 + 图片边框
st.markdown("""
<style>
/* 整体页面底色 */
.stApp {
    background-color: #878162;
}
/* 屋顶选型 / 特色形制 小标题底色 */
.stColumn h3 {
    background-color: #676B56 !important;
    color: white !important;
    padding: 6px 12px !important;
    border-radius: 6px !important;
}
/* 所有大标题文字颜色 #685542 */
h1, h2 {
    color: #685542 !important;
}
/* 按钮样式：背景色 #C8A16D，文字深棕色 #685542 */
.stButton > button {
    background-color: #C8A16D !important;
    color: #685542 !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: bold !important;
}
.stButton > button:hover {
    background-color: #b8915d !important;
}

/* 图片统一加边框：颜色 #4A5B5E */
img {
    border: 3px solid #4A5B5E !important;
    border-radius: 8px !important;
    padding: 3px !important;
    background-color: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# ========== 顶部标题 & 简介 ==========
st.title("中国古典园林屋顶数据可视化系统")

# ====================== 读取Excel ======================
df = pd.read_excel("data/园林总.xlsx")
build_types = ["亭", "阁", "榭", "轩", "馆", "廊"]

# ====================== 绘图函数 ======================
def make_bar(roof_type, df_data, b_types, palette):
    sub_df = df_data[df_data["屋顶类型"] == roof_type]
    cnt = sub_df["建筑类型"].value_counts().reset_index(name="数量")
    cnt = cnt.set_index("建筑类型").reindex(b_types, fill_value=0).reset_index()

    fig, ax = plt.subplots(figsize=(6, 3))
    sns.barplot(x="建筑类型", y="数量", data=cnt, palette=palette, ax=ax)

    ax.set_title(f"【{roof_type}】各园林建筑数量分布", fontsize=12, fontfamily="SimHei")
    ax.set_xlabel("建筑类型", fontfamily="SimHei")
    ax.set_ylabel("统计数量", fontfamily="SimHei")
    plt.xticks(rotation=0, fontfamily="SimHei")
    plt.yticks(fontfamily="SimHei")

    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    return fig

# ====================== 三栏布局 ======================
col_left, col_mid, col_right = st.columns([1, 2, 1])

# 左侧菜单
with col_left:
    st.subheader("屋顶选型")
    st.write("")
    st.write("")
    st.image("photos/image3/攒尖顶.jpg", width=250)
    if st.button("攒尖顶", key="zanjian"):
        st.session_state.view = "攒尖顶"

    st.write("")
    st.write("")
    st.write("")
    st.image("photos/image3/十字脊顶.jpg", width=250)
    if st.button("十字脊顶", key="shizi"):
        st.session_state.view = "十字脊顶"

    st.write("")
    st.write("")
    st.write("")
    st.image("photos/image3/勾连搭顶.jpg", width=250)
    if st.button("勾连搭顶", key="goul"):
        st.session_state.view = "勾连搭顶"

# 右侧菜单
with col_right:
    st.subheader("特色形制")
    st.write("")
    st.write("")
    st.image("photos/image3/扇面顶.jpg", width=250)
    if st.button("扇面顶", key="shanm"):
        st.session_state.view = "扇面顶"

    st.write("")
    st.write("")
    st.write("")
    st.image("photos/image3/万字顶.jpg", width=250)
    if st.button("万字顶", key="wanz"):
        st.session_state.view = "万字顶"

    st.write("")
    st.write("")
    st.write("")
    st.image("photos/image3/总览.jpg", width=250)
    if st.button("整体总览", key="all_view"):
        st.session_state.view = "总览"

# 中间交互区
with col_mid:
    if "view" not in st.session_state:
        st.session_state.view = "总览"
    now_view = st.session_state.view

    if now_view == "总览":
        st.header("园林屋顶全局总览")
        st.markdown("""
园林以功能适配、审美造境、文化赋能为核心逻辑，选用特色屋顶：

**攒尖顶**适配亭阁，造观景之美；**十字脊顶**适配高地标，造地标之美；**勾连搭顶**适配长廊，造游线之美；**扇面顶**适配临水轩亭，造江南灵动之美；**万字顶**专属皇家，造礼制吉祥之美。

各类屋顶以形制适配建筑功能，既满足园林造景需求，又承载地域文化与礼制内涵，共同塑造了园林“功能、审美、文化”三位一体的综合之美，是古典园林“虽由人作，宛自天开”造园思想的极致体现。
""")
        try:
            roof_list = df["屋顶类型"].unique().tolist()
            build_list = df["建筑类型"].unique().tolist()
            src = []
            tgt = []
            val = []
            clr = []
            node_colors = []

            color_map = {
                "攒尖顶": "rgba(213, 225, 232, 0.8)",
                "勾连搭顶": "rgba(97, 132, 142, 0.8)",
                "扇面顶": "rgba(85, 117, 111, 0.8)",
                "十字脊顶": "rgba(60, 92, 94, 0.8)",
                "万字顶": "rgba(60, 92, 94, 0.8)"
            }

            for roof in roof_list:
                node_colors.append(color_map[roof])
            for _ in build_list:
                node_colors.append("rgba(60, 92, 94, 0.9)")

            for i, row in df.iterrows():
                roof_type = row["屋顶类型"]
                s_idx = roof_list.index(roof_type)
                t_idx = len(roof_list) + build_list.index(row["建筑类型"])
                src.append(s_idx)
                tgt.append(t_idx)
                val.append(1)
                clr.append(color_map[roof_type])

            # 桑基图背景与页面完全一致，融为一体
            fig_s = go.Figure(go.Sankey(
                node=dict(
                    label=roof_list + build_list,
                    pad=12,
                    thickness=20,
                    color=node_colors
                ),
                link=dict(
                    source=src,
                    target=tgt,
                    value=val,
                    color=clr
                )
            ))
            fig_s.update_layout(
                paper_bgcolor="#878162",
                plot_bgcolor="#878162"
            )
            st.plotly_chart(fig_s, use_container_width=True)
        except Exception as e:
            st.info(f"桑基图展示: {e}")

        # 整体总览：图片左对齐，文字在右侧
        col_img, col_text = st.columns([1, 1.5])
        with col_img:
            st.image("photos/image3/卷棚顶1.jpg", width=400)
        with col_text:
            st.markdown("""
**卷棚顶**：卷棚顶：无正脊、屋面呈柔和弧线，可与硬山、悬山、歇山等组合成卷棚硬山、卷棚歇山等复合形制。流畅线条适配亭、轩、廊、房等建筑，弱化棱角、柔化空间，是南北园林共通的美学核心，体现“以形适配造境，以线融于自然”的灵动之美，契合“虽由人作，宛自天开”的造园思想。
""")

    elif now_view == "攒尖顶":
        st.header("攒尖顶")
        st.markdown("""
**攒尖顶简介**：屋面向上收拢，集中于顶部宝顶，无正脊（以宝顶为视觉中心）。造型轻盈、向上、通透，不压抑空间，多为单檐，线条柔和，色彩素雅，与山水自然相融，常见于园林亭、阁等观景建筑。

**图表分析**：
以亭为绝对主体、阁为补充，攒尖顶向上收束的轻盈造型，完美适配亭、阁“登高望远、借景框景”的功能，其他建筑类型（榭、轩、馆、廊）中几乎不用。
以通透无压的空间感，实现建筑与山水自然相融，是园林“天人合一”的灵动之美。
""")
        fig = make_bar("攒尖顶", df, build_types, "Blues")
        st.pyplot(fig)
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.image("photos/image3/攒尖顶1.jpg", width=400)

    elif now_view == "十字脊顶":
        st.header("十字脊顶")
        st.markdown("""
**十字脊顶简介**：两坡顶十字相交而成，层次丰富、大气庄重，多见于北方皇家园林与高地标建筑，体现皇家威严与礼制秩序。

**图表分析**：
集中用于北方园林亭、阁，十字相交的层次造型，以视觉冲击力打造园林高地标；
彰显皇家威严与礼制秩序，是北方园林“大气庄重、礼制森严”的雄浑之美。
""")
        fig = make_bar("十字脊顶", df, build_types, "Reds")
        st.pyplot(fig)
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.image("photos/image3/十字脊顶1.jpg", width=400)

    elif now_view == "勾连搭顶":
        st.header("勾连搭顶")
        st.markdown("""
**勾连搭顶简介**：勾连搭顶是由两座及以上屋顶相连、共用屋檐形成的组合式屋顶，核心分为并列式、一殿一卷式、带抱厦式三大样式；
可形成连续通透的长条形空间，是园林长廊、游廊的专用屋顶，便于行走观景，同时保持建筑整体的流畅感，是园林游线的核心载体。

**图表分析**：
几乎专属长廊、游廊，多顶相连的组合形制，串联起园林游线，满足行走观景的功能；
形成连续舒展的屋面景观，是园林“步移景异、空间流转”的韵律之美。
""")
        fig = make_bar("勾连搭顶", df, build_types, "Purples")
        st.pyplot(fig)
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.image("photos/image3/勾连搭顶1.jpg", width=400)

    elif now_view == "扇面顶":
        st.header("扇面顶")
        st.markdown("""
**扇面顶简介**：扇面顶平面呈扇形，曲线优美，屋顶随平面呈弧形，最初为江南园林临水小亭、赏景轩的特色形制，营造“借景”“框景”的视觉效果，
体现江南水乡的灵动与雅致；后传入北方皇家园林，成为南北园林共有的特色形制。

**图表分析**：
扇面顶在江南园林中主要用于**亭**与**轩**，数量不多但辨识度极高；
现存完整古建扇面顶建筑南北园林均有遗存，是南北园林风格融合的重要标志；
它的扇形平面与水面、山石等自然元素完美融合，是江南园林“师法自然，灵动雅致”的婉约之美。
""")
        fig = make_bar("扇面顶", df, build_types, "Oranges")
        st.pyplot(fig)
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.image("photos/image3/扇面顶1.jpg", width=400)

    elif now_view == "万字顶":
        st.header("万字顶")
        st.markdown("""
**万字顶简介**：平面呈“卍”字形，寓意万福万寿，属皇家园林特殊形制，象征吉祥与皇权，多见于颐和园，圆明园等皇家园林，体现皇家的富贵与吉祥寓意。圆明园“万方安和”‌：建于雍正初年，为皇帝寝宫之一，四面环水，33间殿宇曲折相连，1860年毁于英法联军之手 ；
国内‌唯一保存完好的万字顶建筑‌是位于山西‌太原文瀛公园内的万字楼‌，体现皇家的富贵与吉祥寓意。

**图表分析**：
万字顶仅在皇家园林中少量出现，主要用于楼阁，殿宇；
它的复杂造型与吉祥寓意，使其成为园林中极具特色的“礼制造型”；
以“卍”字为平面原型，将汉字符号转化为建筑造型，以复杂形制承载吉祥寓意，是皇家园林“字筑相融、尊卑有序”的华贵之美。
""")
        fig = make_bar("万字顶", df, build_types, "Greens")
        st.pyplot(fig)
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.image("photos/image3/万字顶1.jpg", width=400)