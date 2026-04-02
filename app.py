# -*- coding: utf-8 -*-
"""
瑶医养生古语AI智能训诂模型 - 可视化界面
Streamlit Web应用
from dotenv import load_dotenv
load_dotenv()
"""
import streamlit as st
import json
import sys
import os

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agents.agent import build_agent
from langchain_core.messages import HumanMessage

# 页面配置
st.set_page_config(
    page_title="瑶医养生古语AI智能训诂模型",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-size: 1rem;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .dimension-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .dimension-title {
        color: #667eea;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
    }
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .example-button {
        background: white;
        border: 1px solid #667eea;
        color: #667eea;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        margin: 0.3rem;
        cursor: pointer;
        transition: all 0.3s;
        font-size: 0.9rem;
    }
    .example-button:hover {
        background: #667eea;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# 初始化Session State
if 'agent' not in st.session_state:
    st.session_state.agent = build_agent()
if 'history' not in st.session_state:
    st.session_state.history = []
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

# 主标题
st.markdown("""
<div class="main-header">
    <h1>🌿 瑶医养生古语AI智能训诂模型</h1>
    <h3>AI赋能瑶医养生古语数字化解读与传承</h3>
    <p>项目：AI赋能瑶医养生古语训诂数字化解读传承与文创创新实践</p>
    <p>定位：训诂传播 | AI赋能文献 | 新文科交叉</p>
</div>
""", unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.markdown("### 📚 功能导航")

    page = st.radio(
        "选择功能",
        ["🔍 智能训诂", "📖 语料库查询", "📊 统计信息", "💡 关于项目"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 📌 示例古语")
    st.markdown("点击下方示例快速体验：")

    examples = [
        "香囊佩胸前，祛湿又散寒",
        "晨起一杯姜枣茶，暖胃又驱寒",
        "苍术佩兰祛湿气，艾草温经通经络",
        "春夏养阳，秋冬养阴",
        "饭后百步走，活到九十九"
    ]

    for example in examples:
        if st.button(example, key=f"example_{example}"):
            st.session_state.xungu_input = example
            st.rerun()

    st.markdown("---")
    st.markdown("### ℹ️ 使用说明")
    st.markdown("""
    **训诂六维度：**
    1. **形训**：字形分析
    2. **音训**：字音分析
    3. **义训**：语义解释
    4. **文化溯源**：文化背景
    5. **草药关联**：瑶医草药
    6. **今译注释**：现代翻译
    """)

# 主内容区域
if page == "🔍 智能训诂":
    st.markdown("## 🔍 智能训诂分析")
    st.markdown("输入瑶医养生古语，AI将进行六维度专业训诂分析")

    # 输入区域
    col1, col2 = st.columns([3, 1])

    with col1:
        user_input = st.text_area(
            "请输入瑶医古语文本：",
            placeholder="例如：香囊佩胸前，祛湿又散寒",
            height=100,
            key="xungu_input"
        )

    with col2:
        st.write("")
        if st.button("开始训诂", type="primary", use_container_width=True):
            if user_input.strip():
                with st.spinner("正在进行训诂分析，请稍候..."):
                    try:
                        # 调用Agent进行训诂
                        agent = st.session_state.agent
                        response = agent.invoke({
                            "messages": [HumanMessage(content=f"请对以下瑶医古语进行六维度训诂分析：{user_input}")]
                        })

                        # 解析响应
                        result_text = response["messages"][-1].content

                        # 尝试解析JSON
                        try:
                            # 清理可能的markdown标记
                            result_text = result_text.strip()
                            if result_text.startswith("```json"):
                                result_text = result_text[7:]
                            if result_text.startswith("```"):
                                result_text = result_text[3:]
                            if result_text.endswith("```"):
                                result_text = result_text[:-3]
                            result_text = result_text.strip()

                            st.session_state.analysis_result = json.loads(result_text)
                        except:
                            st.session_state.analysis_result = {
                                "error": "解析失败",
                                "raw_content": result_text
                            }

                        # 添加到历史记录
                        st.session_state.history.append({
                            "input": user_input,
                            "result": st.session_state.analysis_result
                        })

                        st.success("训诂分析完成！")

                    except Exception as e:
                        st.error(f"分析失败：{str(e)}")
                        st.info("💡 提示：如果是网络错误，请检查网络连接后重试")
            else:
                st.warning("请输入古语文本")

    # 显示分析结果
    if st.session_state.analysis_result:
        st.markdown("---")
        st.markdown("## 📊 训诂分析结果")

        result = st.session_state.analysis_result

        if "error" in result:
            st.error(f"分析失败：{result['error']}")

            # 显示错误详情
            if "error_detail" in result:
                st.warning(f"错误详情：{result['error_detail']}")

            # 显示原始响应
            if "raw_content" in result:
                st.markdown("---")
                st.markdown("### 原始响应内容")
                st.text_area("原始内容", result['raw_content'], height=200)
        else:
            # 六维度展示
            dimensions = [
                ("形训", "字形分析与古字形考证"),
                ("音训", "字音分析与古音考证"),
                ("义训", "语义解释与词义演变"),
                ("文化溯源", "文化背景与历史传承"),
                ("草药关联", "瑶医草药与应用"),
                ("今译注释", "现代翻译与通俗解释")
            ]

            for i, (dim_key, dim_desc) in enumerate(dimensions):
                with st.expander(f"### {i+1}. {dim_key}", expanded=True):
                    st.markdown(f"<div class='dimension-title'>{dim_desc}</div>", unsafe_allow_html=True)
                    st.write(result.get(dim_key, "暂无内容"))

elif page == "📖 语料库查询":
    st.markdown("## 📖 语料库查询")

    # 加载语料库
    try:
        with open('assets/yaoyi_corpus.json', 'r', encoding='utf-8') as f:
            corpus_data = json.load(f)

        # 转换为数组格式（过滤掉metadata）
        corpus = []
        for key, value in corpus_data.items():
            if key not in ['version', 'description', 'created', 'total_count', 'corpus']:
                corpus.append({
                    '古语': key,
                    **value
                })

        # 搜索框
        search_query = st.text_input(
            "🔍 搜索古语",
            placeholder="输入关键词搜索..."
        )

        # 过滤选项
        col1, col2, col3 = st.columns(3)
        with col1:
            # 提取所有草药
            all_herbs_list = []
            for item in corpus:
                herbs = item.get('涉及草药', [])
                if herbs:
                    all_herbs_list.extend(herbs)

            filter_herb = st.multiselect(
                "筛选草药",
                sorted(list(set(all_herbs_list)))
            )
        with col2:
            filter_culture = st.multiselect(
                "筛选文化来源",
                sorted(list(set([item.get('文化来源', '') for item in corpus if item.get('文化来源')])))
            )
        with col3:
            filter_dimension = st.selectbox(
                "排序方式",
                ["默认", "按草药数量", "按文化来源"]
            )

        # 过滤和排序
        filtered_corpus = corpus
        if search_query:
            filtered_corpus = [
                item for item in filtered_corpus
                if search_query.lower() in item.get('古语', '').lower()
            ]
        if filter_herb:
            filtered_corpus = [
                item for item in filtered_corpus
                if any(herb in item.get('涉及草药', []) for herb in filter_herb)
            ]
        if filter_culture:
            filtered_corpus = [
                item for item in filtered_corpus
                if item.get('文化来源') in filter_culture
            ]
        if filter_dimension == "按草药数量":
            filtered_corpus = sorted(filtered_corpus, key=lambda x: len(x.get('涉及草药', [])), reverse=True)
        elif filter_dimension == "按文化来源":
            filtered_corpus = sorted(filtered_corpus, key=lambda x: x.get('文化来源', ''))

        # 显示结果
        st.markdown(f"### 搜索结果（共 {len(filtered_corpus)} 条）")

        for idx, item in enumerate(filtered_corpus, 1):
            with st.expander(f"### {idx}. {item.get('古语', '未知')}", expanded=False):
                st.write(f"**文化来源**：{item.get('文化来源', '未知')}")
                st.write(f"**涉及草药**：{', '.join(item.get('涉及草药', []))}")
                st.write(f"**训诂时间**：{item.get('训诂时间', '未知')}")

                # 显示六维度
                st.markdown("---")
                st.markdown("#### 训诂结果：")
                for dim_key in ["形训", "音训", "义训", "文化溯源", "草药关联", "今译注释"]:
                    if dim_key in item:
                        with st.expander(f"##### {dim_key}", expanded=False):
                            st.write(item[dim_key])

    except FileNotFoundError:
        st.warning("⚠️ 未找到语料库文件，请先创建 `assets/yaoyi_corpus.json`")
        st.info("💡 提示：运行一次训诂分析后，系统会自动创建语料库")
    except Exception as e:
        st.error(f"加载语料库失败：{str(e)}")

elif page == "📊 统计信息":
    st.markdown("## 📊 统计信息")

    try:
        with open('assets/yaoyi_corpus.json', 'r', encoding='utf-8') as f:
            corpus_data = json.load(f)

        # 转换为数组格式（过滤掉metadata）
        corpus = []
        for key, value in corpus_data.items():
            if key not in ['version', 'description', 'created', 'total_count', 'corpus']:
                corpus.append({
                    '古语': key,
                    **value
                })

        if len(corpus) == 0:
            st.warning("⚠️ 语料库为空，请先进行训诂分析")
        else:
            # 总体统计
            st.markdown("---")
            st.markdown("### 总体统计")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "总古语数量",
                    len(corpus),
                    delta_color="normal"
                )

            # 草药统计
            all_herbs = []
            for item in corpus:
                if '涉及草药' in item:
                    all_herbs.extend(item['涉及草药'])

            with col2:
                st.metric(
                    "涉及草药种类",
                    len(set(all_herbs)),
                    delta_color="normal"
                )

            # 文化来源统计
            all_cultures = list(set([item.get('文化来源', '') for item in corpus if item.get('文化来源')]))

            with col3:
                st.metric(
                    "文化来源",
                    len(all_cultures),
                    delta_color="normal"
                )

            # 详细列表
            if all_herbs:
                st.markdown("---")
                st.markdown("### 🌿 涉及的瑶医草药")
                st.write(", ".join(sorted(list(set(all_herbs)))))

            if all_cultures:
                st.markdown("---")
                st.markdown("### 🏔️ 文化来源地域")
                st.write(", ".join(all_cultures))

    except FileNotFoundError:
        st.warning("⚠️ 未找到语料库文件，请先创建 `assets/yaoyi_corpus.json`")
    except Exception as e:
        st.error(f"加载语料库失败：{str(e)}")

elif page == "💡 关于项目":
    st.markdown("## 💡 关于项目")

    st.markdown("""
    ### 项目简介
    本项目聚焦广西瑶族非遗瑶医养生文化，以"AI赋能古语训诂+数字化传承+文创商业化"为核心，构建"学术研究-技术开发-商业转化-文化反哺"的完整生态，是新文科背景下跨学科融合的创新实践项目。

    ### 核心创新
    1. **AI+训诂**：首次将AI技术深度融入瑶医古语训诂研究
    2. **六维度解读**：形训、音训、义训、文化溯源、草药关联、今译注释
    3. **语料库建设**：标准化整理100句瑶医养生古语
    4. **新文科融合**：汉语言文学+人工智能+非遗保护

    ### 指导教师
    - **程辉**：古汉语训诂与AI文科融合指导
    - **陈钰文**：非遗文化与实践指导
    - **宋原**：人工智能技术指导

    ### 项目目标
    - **短期目标**：完成AI辅助训诂模型开发与语料库搭建
    - **中期目标**：拓展至苗族、壮族等多民族文献整理
    - **长期目标**：打造"非遗数字化传承+AI学术服务"专业平台

    ### 联系方式
    - **项目负责人**：黄子恩西
    - **联系电话**：19978867358
    - **邮箱**：1746465583@qq.com

    ---
    **项目支持**：广西外国语学院 | 国创大创竞赛
    """)

# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🌿 瑶医古语AI智能训诂模型 | AI赋能瑶医养生古语数字化解读传承与文创创新实践</p>
    <p>广西外国语学院 | 新文科交叉融合 | 非遗文化传播与文创创新</p>
</div>
""", unsafe_allow_html=True)
