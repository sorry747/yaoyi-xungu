"""
瑶医古语AI智能训诂模型 - 测试脚本
"""
import json
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agents.agent import build_agent
from langchain_core.messages import HumanMessage

def test_agent():
    """测试Agent功能"""
    print("="*80)
    print("瑶医古语AI智能训诂模型 - 功能测试")
    print("="*80)

    # 初始化Agent
    print("\n[1/4] 正在初始化Agent...")
    try:
        agent = build_agent()
        print("✅ Agent初始化成功")
    except Exception as e:
        print(f"❌ Agent初始化失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    # 测试训诂功能
    print("\n[2/4] 测试训诂功能...")
    test_text = "香囊佩胸前，祛湿又散寒"
    print(f"测试文本: {test_text}")

    try:
        response = agent.invoke({
            "messages": [HumanMessage(content=f"请对以下瑶医古语进行六维度训诂分析：{test_text}")]
        })

        result_text = response["messages"][-1].content

        # 尝试解析JSON
        try:
            result_text = result_text.strip()
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()

            result = json.loads(result_text)
            print("✅ 训诂分析成功")
            print("\n结果:")
            print(json.dumps(result, ensure_ascii=False, indent=2))

            # 检查六维度是否完整
            required_fields = ["原文", "形训", "音训", "义训", "文化溯源", "草药关联", "今译注释"]
            missing_fields = [field for field in required_fields if field not in result]

            if missing_fields:
                print(f"\n⚠️  缺少字段: {', '.join(missing_fields)}")
            else:
                print("\n✅ 六维度完整")

        except json.JSONDecodeError as e:
            print(f"⚠️  JSON解析失败: {str(e)}")
            print(f"原始内容: {result_text}")
            return False

    except Exception as e:
        print(f"❌ 训诂分析失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    # 测试语料库查询功能
    print("\n[3/4] 测试语料库查询功能...")
    try:
        response = agent.invoke({
            "messages": [HumanMessage(content="查询语料库，关键词：香囊")]
        })

        result_text = response["messages"][-1].content
        result = json.loads(result_text)

        print("✅ 语料库查询成功")
        print(f"查询结果: {result}")

    except Exception as e:
        print(f"❌ 语料库查询失败: {str(e)}")

    # 测试统计功能
    print("\n[4/4] 测试统计功能...")
    try:
        response = agent.invoke({
            "messages": [HumanMessage(content="获取语料库统计信息")]
        })

        result_text = response["messages"][-1].content
        result = json.loads(result_text)

        print("✅ 统计信息获取成功")
        print(f"统计结果: {result}")

    except Exception as e:
        print(f"❌ 统计信息获取失败: {str(e)}")

    print("\n" + "="*80)
    print("✅ 测试完成！")
    print("="*80)
    print("\n下一步：运行可视化界面")
    print("命令: streamlit run app.py")

    return True

if __name__ == "__main__":
    success = test_agent()
    sys.exit(0 if success else 1)
