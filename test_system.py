#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
千星奇域提示词工程系统测试脚本
"""

import json
import requests
from typing import Dict, Any

# API基础URL
BASE_URL = "http://localhost:8000"

class TestClient:
    """测试客户端"""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """发送请求"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        return self._request("GET", "/health")

    def create_knowledge(self, knowledge_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建知识"""
        return self._request("POST", "/api/v1/knowledge", json=knowledge_data)

    def get_knowledge(self, knowledge_id: str) -> Dict[str, Any]:
        """获取知识"""
        return self._request("GET", f"/api/v1/knowledge/{knowledge_id}")

    def list_knowledge(self, **params) -> Dict[str, Any]:
        """获取知识列表"""
        return self._request("GET", "/api/v1/knowledge", params=params)

    def search_knowledge(self, query: str, category: str = None, limit: int = 5) -> Dict[str, Any]:
        """搜索知识"""
        data = {"query": query}
        if category:
            data["category"] = category
        data["limit"] = limit
        return self._request("POST", "/api/v1/knowledge/search", json=data)

    def generate_prompt(self, user_question: str, **kwargs) -> Dict[str, Any]:
        """生成提示词"""
        data = {"user_question": user_question, **kwargs}
        return self._request("POST", "/api/v1/prompts/generate", json=data)

    def get_templates(self) -> Dict[str, Any]:
        """获取提示词模板"""
        return self._request("GET", "/api/v1/prompts/templates")

    def ai_chat(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """AI聊天"""
        data = {"prompt": prompt, **kwargs}
        return self._request("POST", "/api/v1/ai/chat", json=data)

    def ai_generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """AI生成"""
        data = {"prompt": prompt, **kwargs}
        return self._request("POST", "/api/v1/ai/generate", json=data)

def run_tests():
    """运行测试"""
    client = TestClient()
    
    print("=" * 50)
    print("千星奇域提示词工程系统测试")
    print("=" * 50)
    
    # 1. 健康检查
    print("\n1. 健康检查")
    try:
        result = client.health_check()
        print(f"   ✓ 成功: {result}")
    except Exception as e:
        print(f"   ✗ 失败: {e}")
        return
    
    # 2. 获取提示词模板
    print("\n2. 获取提示词模板")
    try:
        result = client.get_templates()
        print(f"   ✓ 成功: 找到 {len(result['data'])} 个模板")
        for template in result['data'][:3]:
            print(f"     - {template['name']}: {template['description']}")
    except Exception as e:
        print(f"   ✗ 失败: {e}")
    
    # 3. 创建测试知识
    print("\n3. 创建测试知识")
    test_knowledge = {
        "title": "技能系统",
        "category": "战斗系统",
        "content": "千星奇域技能系统允许创建多种类型的技能，包括瞬发技能、蓄力技能、普通技能、连段技能和瞄准技能。每个技能都可以配置技能动画、技能资源和技能效果。",
        "limitations": ["技能类型有限", "动画资源需要预先准备"],
        "tags": ["技能", "战斗", "能力"],
        "version": "1.0"
    }
    
    try:
        result = client.create_knowledge(test_knowledge)
        knowledge_id = result['data']['id']
        print(f"   ✓ 成功: 创建知识ID: {knowledge_id}")
    except Exception as e:
        print(f"   ✗ 失败: {e}")
        knowledge_id = None
    
    # 4. 搜索知识
    print("\n4. 搜索知识")
    try:
        result = client.search_knowledge("技能系统")
        print(f"   ✓ 成功: 找到 {len(result['data'])} 个相关知识")
        for item in result['data']:
            print(f"     - {item['title']} (分数: {item['score']:.2f})")
    except Exception as e:
        print(f"   ✗ 失败: {e}")
    
    # 5. 生成提示词
    print("\n5. 生成提示词")
    user_question = "如何在千星奇域中创建一个技能系统？"
    try:
        result = client.generate_prompt(
            user_question=user_question,
            role="game_designer",
            phase="design_planning",
            knowledge_categories=["战斗系统"]
        )
        prompt = result['data']['prompt']
        print(f"   ✓ 成功: 生成提示词")
        print(f"     提示词长度: {len(prompt)} 字符")
        print(f"     模板: {result['data']['template_used']}")
        print(f"     知识块数量: {len(result['data']['knowledge_chunks'])}")
        print(f"     提示词预览: {prompt[:200]}...")
    except Exception as e:
        print(f"   ✗ 失败: {e}")
    
    # 6. 列出知识
    print("\n6. 列出知识")
    try:
        result = client.list_knowledge(category="战斗系统")
        print(f"   ✓ 成功: 找到 {result['data']['total']} 个战斗系统相关知识")
    except Exception as e:
        print(f"   ✗ 失败: {e}")
    
    print("\n" + "=" * 50)
    print("测试完成！")
    print("=" * 50)

if __name__ == "__main__":
    run_tests()