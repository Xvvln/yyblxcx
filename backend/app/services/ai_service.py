"""
AI 健康助手服务 - 基于阿里云百炼平台

TODO: 暂缓实现
原因: 需要配置百炼平台 API Key
当前: 返回模拟响应
后续: 对接百炼平台 API
"""
from typing import Optional
from app.config import settings


class AIHealthAssistant:
    """AI 健康助手"""
    
    def __init__(self):
        self.api_key = settings.DASHSCOPE_API_KEY
        self.model = settings.DASHSCOPE_MODEL
    
    async def chat(
        self, 
        user_message: str, 
        context: Optional[dict] = None,
        history: Optional[list] = None
    ) -> str:
        """
        与 AI 健康助手对话
        
        Args:
            user_message: 用户消息
            context: 用户健康档案等上下文
            history: 历史对话记录
            
        Returns:
            AI 回复内容
        """
        if not self.api_key:
            # API Key 未配置，返回模拟响应
            return self._get_mock_response(user_message)
        
        try:
            # TODO: 对接百炼平台 API
            # import dashscope
            # from dashscope import Generation
            # dashscope.api_key = self.api_key
            # 
            # system_prompt = self._build_system_prompt(context)
            # messages = [{"role": "system", "content": system_prompt}]
            # 
            # # 添加历史对话
            # if history:
            #     messages.extend(history)
            # 
            # # 添加当前消息
            # messages.append({"role": "user", "content": user_message})
            # 
            # response = Generation.call(
            #     model=self.model,
            #     messages=messages
            # )
            # if response.status_code == 200:
            #     return response.output.text
            # else:
            #     return f"AI服务异常: {response.message}"
            
            return self._get_mock_response(user_message)
            
        except Exception as e:
            return f"AI服务调用失败: {str(e)}"
    
    def _build_system_prompt(self, context: Optional[dict]) -> str:
        """构建系统提示词"""
        base_prompt = """你是一个专业的健康管理助手，具备营养学和运动科学知识。
请根据用户的问题提供专业、友善的健康建议。

注意事项：
1. 你的建议仅供参考，不能替代专业医疗诊断
2. 对于严重健康问题，建议用户及时就医
3. 回答要简洁明了，适合普通用户理解
"""
        if context:
            base_prompt += f"\n\n用户健康档案：\n{context}"
        
        return base_prompt
    
    def _get_mock_response(self, message: str) -> str:
        """获取模拟响应"""
        message_lower = message.lower()
        
        if "减肥" in message or "减重" in message:
            return """关于减重，我有以下建议：

1. 饮食控制：减少高热量、高油脂食物摄入，增加蔬菜和优质蛋白
2. 规律运动：每周至少150分钟中等强度有氧运动
3. 充足睡眠：保证每天7-8小时睡眠
4. 多喝水：每天喝足2000ml水

建议循序渐进，每周减重0.5-1kg为宜。如需个性化方案，建议咨询专业营养师。"""

        elif "运动" in message or "锻炼" in message:
            return """运动建议：

1. 有氧运动：快走、慢跑、游泳、骑车，每次30-45分钟
2. 力量训练：每周2-3次，注意动作规范
3. 柔韧性训练：运动前后做好拉伸

运动前要热身，运动后要拉伸。刚开始运动要循序渐进，避免受伤。"""

        elif "饮食" in message or "吃什么" in message:
            return """健康饮食建议：

1. 均衡搭配：主食、蛋白质、蔬菜、水果合理搭配
2. 少油少盐：烹饪少用油，控制盐的摄入
3. 规律进食：三餐规律，不要暴饮暴食
4. 多吃蔬果：每天蔬菜300-500g，水果200-350g

如有特殊饮食需求，建议咨询营养师制定个性化方案。"""

        elif "睡眠" in message or "失眠" in message:
            return """改善睡眠的建议：

1. 规律作息：固定时间入睡和起床
2. 睡前放松：避免剧烈运动和使用电子设备
3. 环境舒适：保持卧室安静、黑暗、温度适宜
4. 避免刺激：睡前避免咖啡因和酒精

如果长期失眠严重影响生活，建议就医检查。"""

        else:
            return """您好！我是您的健康助手。

我可以为您提供以下方面的建议：
- 饮食营养指导
- 运动锻炼建议
- 健康生活方式
- 体重管理建议

请告诉我您想了解什么？

注：我的建议仅供参考，如有严重健康问题请及时就医。"""


# 全局实例
ai_assistant = AIHealthAssistant()

