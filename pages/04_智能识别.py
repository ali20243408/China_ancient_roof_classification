# ====================== 全局中文乱码修复（必须放在文件最开头） ======================
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["WenQuanYi Micro Hei", "SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.family"] = "WenQuanYi Micro Hei"

import plotly.io as pio
pio.templates["custom_font"] = pio.templates["plotly"]
pio.templates["custom_font"].layout.font.update(
    family="WenQuanYi Micro Hei, SimHei, Microsoft YaHei",
    size=12
)
pio.templates.default = "custom_font"
# ========================================================================
# 1. 最顶部：屏蔽所有警告（包含Streamlit废弃参数警告）
import warnings
warnings.filterwarnings("ignore")

# 2. 补全所有必要导入
from PIL import Image
import time
import streamlit as st
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
import os
from typing import Tuple

# 3. 页面配置
st.set_page_config(
    page_title="古建筑屋顶智能识别系统",
    page_icon="🏯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 4. 国风CSS美化（保持视觉效果）
st.markdown("""
<style>
/* 全局背景 */
.stApp {
    background: linear-gradient(135deg, #FFF9E6 0%, #F5EFE0 100%);
    font-family: "Microsoft YaHei", "SimHei", sans-serif;
}

/* 主标题 */
h1 {
    font-family: "STKaiti", "KaiTi", serif !important;
    color: #8C2318 !important;
    text-align: center;
    font-size: 3rem !important;
    font-weight: bold !important;
    margin-bottom: 0.5rem !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

/* 副标题 */
h2 {
    font-family: "STKaiti", "KaiTi", serif !important;
    color: #333333 !important;
    text-align: center;
    font-size: 1.8rem !important;
    margin-bottom: 2rem !important;
}

/* 卡片样式 */
.stContainer {
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
    border: 1px solid #E8DCC8 !important;
    background: rgba(255,255,255,0.85) !important;
    padding: 1.5rem !important;
    margin-bottom: 1.5rem !important;
}

/* 按钮样式 */
.stButton>button {
    background: linear-gradient(135deg, #8C2318 0%, #A63429 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.8rem 2rem !important;
    font-size: 1.1rem !important;
    font-weight: bold !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 8px rgba(140,35,24,0.3) !important;
    width: 100% !important;
}
.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 12px rgba(140,35,24,0.4) !important;
    background: linear-gradient(135deg, #A63429 0%, #C44536 100%) !important;
}

/* 上传组件 */
.stFileUploader {
    border: 2px dashed #C8B6A6 !important;
    border-radius: 12px !important;
    background: rgba(255,255,255,0.6) !important;
    padding: 1.5rem !important;
}

/* 结果卡片 */
.stMetric {
    background: linear-gradient(135deg, #FFF9E6 0%, #F5EFE0 100%) !important;
    border-radius: 8px !important;
    padding: 1rem !important;
    border: 1px solid #E8DCC8 !important;
    margin: 0.5rem 0 !important;
}
.stMetric label {
    color: #8C2318 !important;
    font-weight: bold !important;
    font-size: 1.1rem !important;
}
.stMetric value {
    color: #333333 !important;
    font-size: 1.5rem !important;
    font-weight: bold !important;
}

/* 分割线 */
hr {
    border: none !important;
    height: 2px !important;
    background: linear-gradient(to right, transparent, #8C2318, transparent) !important;
    margin: 2rem 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ====================== 【云端修复关键】 ======================
DEVICE = torch.device("cpu")

# 正确相对路径 → 本地/云端 100% 找到
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "roof_final_best.pth")

# 17个类别
CLASSES = [
    '万字顶', '三川脊顶', '勾连搭顶', '阁顶', '庑殿顶', '悬山顶',
    '扇面顶', '攒尖顶', '歇山顶', '燕尾顶', '盝顶', '盔顶',
    '硬山顶', '马鞍脊顶', '类别15', '类别16', '类别17'
]
NUM_CLASSES = len(CLASSES)

# 6. 模型加载
@st.cache_resource(show_spinner="🔄 正在加载古建筑识别模型...")
def load_model() -> nn.Module:
    model = models.mobilenet_v2(weights=None)
    model.classifier = nn.Sequential(
        nn.Dropout(0.6),
        nn.Linear(model.classifier[1].in_features, NUM_CLASSES)
    )
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model = model.to(DEVICE)
    model.eval()
    return model

main_model = load_model()

# 7. 图像预处理
def preprocess_image(image_pil: Image.Image) -> torch.Tensor:
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return transform(image_pil).unsqueeze(0).to(DEVICE)

# 8. 模型推理
def predict_single_image(model: nn.Module, input_tensor: torch.Tensor) -> Tuple[str, float]:
    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted_idx = torch.max(probabilities, dim=1)

    pred_class = CLASSES[predicted_idx.item()]
    confidence_score = confidence.item() * 100
    return pred_class, confidence_score

# -------------------------- 9. 页面UI --------------------------
st.markdown("<h1>古建筑屋顶智能识别</h1>", unsafe_allow_html=True)
st.markdown("<h2>上传屋顶图片，一键识别古建筑屋顶类型</h2>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1], gap="large")

with col1:
    with st.container(border=True):
        st.subheader("图片上传")
        uploaded_file = st.file_uploader(
            "选择屋顶图片",
            type=["jpg", "png", "jpeg"],
            label_visibility="collapsed"
        )

    if uploaded_file is not None:
        if st.button("开始识别", type="primary", use_container_width=True):
            with st.spinner("正在识别古建筑屋顶类型..."):
                start_time = time.time()
                img = Image.open(uploaded_file).convert("RGB")
                input_tensor = preprocess_image(img)
                pred_class, conf_score = predict_single_image(main_model, input_tensor)
                elapsed_time = time.time() - start_time

                with st.container(border=True):
                    st.subheader("识别结果")
                    col_img, col_text = st.columns(2)
                    with col_img:
                        st.image(img, caption="上传的屋顶图片", use_column_width=True)
                    with col_text:
                        st.metric(label="小类别识别", value=pred_class)
                        st.metric(label="置信度", value=f"{conf_score:.2f}%")
                        class_to_large = {
                            '万字顶': '园林顶（艺术型）',
                            '三川脊顶': '园林顶（艺术型）',
                            '勾连搭顶': '组合顶（复合型）',
                            '阁顶': '官式顶（殿堂型）',
                            '庑殿顶': '官式顶（殿堂型）',
                            '悬山顶': '民居顶（民间型）',
                            '扇面顶': '园林顶（艺术型）',
                            '攒尖顶': '官式顶（殿堂型）',
                            '歇山顶': '官式顶（殿堂型）',
                            '燕尾顶': '民居顶（民间型）',
                            '盝顶': '官式顶（殿堂型）',
                            '盔顶': '园林顶（艺术型）',
                            '硬山顶': '民居顶（民间型）',
                            '马鞍脊顶': '民居顶（民间型）',
                            '类别15': '未知大类',
                            '类别16': '未知大类',
                            '类别17': '未知大类'
                        }
                        large_class = class_to_large.get(pred_class, "未知大类")
                        st.metric(label="大类别归属", value=large_class)
                        st.info(f"⚡ 识别耗时：{elapsed_time:.3f} 秒")

with col2:
    with st.container(border=True):
        st.subheader("识别说明")
        st.markdown("""
- **模型架构**：MobileNetV2 轻量级深度学习架构
- **识别范围**：覆盖17种典型中国古建筑屋顶类型
- **图片要求**：分辨率清晰、屋顶无遮挡、光线均匀
- **结果判读**：置信度 > 90% 代表识别结果极具参考价值
        """)

        st.markdown("---")
        st.subheader("屋顶文化小知识")
        st.markdown("""
- **庑殿顶**：建筑等级最高，象征皇权（如故宫太和殿）
- **歇山顶**：次高等级，兼具庑殿顶与悬山顶特点
- **攒尖顶**：多用于亭、台、楼、阁，造型灵动优美
        """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #666; font-size: 0.9rem'>© 2026古建筑屋顶智能识别系统 | 传承中式美学 · 赋能文化数字化</p>", unsafe_allow_html=True)