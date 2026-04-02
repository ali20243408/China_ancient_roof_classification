import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# ====================== 页面基础配置 ======================
st.set_page_config(page_title="Garden Roof Visualization", layout="wide")

# 全局字体防乱码（纯英文，无中文依赖，彻底不方框）
plt.rcParams["font.family"] = "DejaVu Sans"
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
st.title("Chinese Classical Garden Roof Visualization")

# ====================== 读取Excel ======================
df = pd.read_excel("data/园林总.xlsx")
build_types = ["Pavilion", "Tower", "Platform", "Veranda", "Hall", "Gallery"]

# ====================== 绘图函数（英文无乱码） ======================
def make_bar(roof_type, df_data, b_types, palette):
    sub_df = df_data[df_data["屋顶类型"] == roof_type]
    cnt = sub_df["建筑类型"].value_counts().reset_index(name="Count")
    cnt = cnt.set_index("建筑类型").reindex(b_types, fill_value=0).reset_index()

    fig, ax = plt.subplots(figsize=(6, 3))
    sns.barplot(x="建筑类型", y="Count", data=cnt, palette=palette, ax=ax)

    ax.set_title(f"Distribution of {roof_type}", fontsize=12)
    ax.set_xlabel("Building Type")
    ax.set_ylabel("Count")
    plt.xticks(rotation=0)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    return fig

# ====================== 三栏布局 ======================
col_left, col_mid, col_right = st.columns([1, 2, 1])

# 左侧菜单
with col_left:
    st.subheader("Roof Types")
    st.write("")
    st.image("photos/image3/攒尖顶.jpg", width=250)
    if st.button("Pyramid", key="zanjian"):
        st.session_state.view = "攒尖顶"

    st.write("")
    st.write("")
    st.write("")
    st.image("photos/image3/十字脊顶.jpg", width=250)
    if st.button("Cross", key="shizi"):
        st.session_state.view = "十字脊顶"

    st.write("")
    st.write("")
    st.write("")
    st.image("photos/image3/勾连搭顶.jpg", width=250)
    if st.button("Connected", key="goul"):
        st.session_state.view = "勾连搭顶"

# 右侧菜单
with col_right:
    st.subheader("Special Styles")
    st.write("")
    st.write("")
    st.image("photos/image3/扇面顶.jpg", width=250)
    if st.button("Fan", key="shanm"):
        st.session_state.view = "扇面顶"

    st.write("")
    st.write("")
    st.write("")
    st.image("photos/image3/万字顶.jpg", width=250)
    if st.button("Swastika", key="wanz"):
        st.session_state.view = "万字顶"

    st.write("")
    st.write("")
    st.write("")
    st.image("photos/image3/总览.jpg", width=250)
    if st.button("Overview", key="all_view"):
        st.session_state.view = "总览"

# 中间交互区
with col_mid:
    if "view" not in st.session_state:
        st.session_state.view = "总览"
    now_view = st.session_state.view

    if now_view == "总览":
        st.header("Overview")
        st.markdown("""
Garden roofs are designed for aesthetics, scenery, and culture.

Pyramid roofs for pavilions, Cross roofs for landmarks, Connected roofs for corridors,
Fan roofs for waterside views, Swastika roofs for royal symbolism.
""")
        try:
            roof_list = df["屋顶类型"].unique().tolist()
            build_list = ["Pavilion", "Tower", "Platform", "Veranda", "Hall", "Gallery"]
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
            st.plotly_chart(fig_s, width="stretch")
        except Exception as e:
            st.info(f"Display: {e}")

        col_img, col_text = st.columns([1, 1.5])
        with col_img:
            st.image("photos/image3/卷棚顶1.jpg", width=400)
        with col_text:
            st.markdown("""
**Curved Roof**: Soft, ridge-free design used in pavilions and corridors.
Creates elegant, natural harmony with the landscape.
""")

    elif now_view == "攒尖顶":
        st.header("Pyramid Roof")
        st.markdown("""
Light, pointed, open design used for viewing pavilions.
Ideal for enjoying scenery and blending with nature.
""")
        fig = make_bar("攒尖顶", df, build_types, "Blues")
        st.pyplot(fig, width="stretch")
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.image("photos/image3/攒尖顶1.jpg", width=400)

    elif now_view == "十字脊顶":
        st.header("Cross Roof")
        st.markdown("""
Cross-shaped, grand, and majestic.
Mostly used in royal gardens.
""")
        fig = make_bar("十字脊顶", df, build_types, "Reds")
        st.pyplot(fig, width="stretch")
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.image("photos/image3/十字脊顶1.jpg", width=400)

    elif now_view == "勾连搭顶":
        st.header("Connected Roof")
        st.markdown("""
Connected roofs for long corridors.
Creates smooth, continuous walking space.
""")
        fig = make_bar("勾连搭顶", df, build_types, "Purples")
        st.pyplot(fig, width="stretch")
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.image("photos/image3/勾连搭顶1.jpg", width=400)

    elif now_view == "扇面顶":
        st.header("Fan Roof")
        st.markdown("""
Fan-shaped, elegant, waterside style.
Symbolizes grace and nature in Jiangnan gardens.
""")
        fig = make_bar("扇面顶", df, build_types, "Oranges")
        st.pyplot(fig, width="stretch")
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.image("photos/image3/扇面顶1.jpg", width=400)

    elif now_view == "万字顶":
        st.header("Swastika Roof")
        st.markdown("""
Swastika shape for good fortune.
Exclusive to royal architecture.
""")
        fig = make_bar("万字顶", df, build_types, "Greens")
        st.pyplot(fig, width="stretch")
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.image("photos/image3/万字顶1.jpg", width=400)