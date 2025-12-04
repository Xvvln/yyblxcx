"""
AI 健康助手服务 - 基于阿里云百炼平台（通义千问）

功能特性:
1. 基于用户健康档案的个性化回答
2. 上下文对话记忆管理
3. 专业健康领域知识
4. 营养不良筛查与健康管理专业助手
"""
from typing import Optional, List, Dict, Any
from datetime import date
from decimal import Decimal
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class AIHealthAssistant:
    """AI 健康助手 - 营养不良筛查与健康管理专家"""
    
    # 健康目标映射
    HEALTH_GOAL_MAP = {
        "lose_weight": "减脂瘦身",
        "gain_muscle": "增肌塑形",
        "keep_fit": "保持健康",
        "improve_sleep": "改善睡眠",
        "reduce_stress": "减压放松",
    }
    
    # BMI 分类
    BMI_CATEGORIES = [
        (18.5, "偏瘦", "建议适当增加营养摄入，注意蛋白质补充"),
        (24, "正常", "体重健康，继续保持良好的生活习惯"),
        (28, "偏胖", "建议控制饮食，增加运动量"),
        (float('inf'), "肥胖", "建议在专业指导下制定减重计划"),
    ]
    
    def __init__(self):
        self.api_key = settings.DASHSCOPE_API_KEY
        self.model = settings.DASHSCOPE_MODEL
        self._dashscope_initialized = False
    
    def _init_dashscope(self):
        """延迟初始化 dashscope"""
        if not self._dashscope_initialized and self.api_key:
            try:
                import dashscope
                dashscope.api_key = self.api_key
                self._dashscope_initialized = True
                logger.info("DashScope API 初始化成功")
            except Exception as e:
                logger.error(f"DashScope 初始化失败: {e}")
    
    def _calculate_bmi(self, height: Optional[Decimal], weight: Optional[Decimal]) -> tuple:
        """计算BMI及分类"""
        if not height or not weight or float(height) <= 0:
            return None, None, None
        
        height_m = float(height) / 100
        bmi = float(weight) / (height_m ** 2)
        
        for threshold, category, advice in self.BMI_CATEGORIES:
            if bmi < threshold:
                return round(bmi, 1), category, advice
        
        return round(bmi, 1), "肥胖", "建议在专业指导下制定减重计划"
    
    def _calculate_age(self, birthday: Optional[date]) -> Optional[int]:
        """计算年龄"""
        if not birthday:
            return None
        today = date.today()
        age = today.year - birthday.year
        if today.month < birthday.month or (today.month == birthday.month and today.day < birthday.day):
            age -= 1
        return age
    
    def _build_system_prompt(self, context: Optional[Dict[str, Any]]) -> str:
        """构建专业的系统提示词"""
        
        base_prompt = """# 角色设定
你是「营养健康助手」，一个专业的营养不良筛查与健康管理AI助手。你由资深营养师和健康管理专家团队设计，致力于为用户提供科学、个性化的健康建议。

## 核心能力
1. **营养评估**: 分析用户的饮食习惯，提供营养摄入建议
2. **体重管理**: 根据BMI和健康目标，制定合理的体重管理方案
3. **运动指导**: 提供适合用户身体状况的运动建议
4. **健康知识**: 普及营养学和健康管理知识
5. **疾病预防**: 针对慢性病提供饮食调理建议

## 回答原则
1. **个性化**: 结合用户的身体数据和健康档案给出针对性建议
2. **科学性**: 基于营养学和医学知识，不提供无依据的建议
3. **安全性**: 对于疑似疾病症状，建议用户及时就医
4. **友善性**: 语言亲切自然，像一位关心用户的健康顾问
5. **实用性**: 给出可操作的具体建议，而非空泛的理论

## 回答格式
- 使用清晰的结构，适当使用标题、列表
- 重要建议用醒目方式呈现
- 每次回复控制在合理长度，避免信息过载
- 适时追问以更好地了解用户需求

## 特别注意
- 你不是医生，不提供诊断和处方建议
- 遇到严重健康问题时，务必建议用户就医
- 尊重用户的饮食文化和个人偏好
- 考虑用户的实际执行能力
"""
        
        # 添加用户个性化信息
        if context:
            user_profile = "\n## 当前用户健康档案\n"
            
            # 基本信息
            basic_info = []
            if context.get("年龄"):
                basic_info.append(f"年龄: {context['年龄']}岁")
            if context.get("性别"):
                basic_info.append(f"性别: {context['性别']}")
            if context.get("身高"):
                basic_info.append(f"身高: {context['身高']}")
            if context.get("体重"):
                basic_info.append(f"体重: {context['体重']}")
            
            if basic_info:
                user_profile += "### 基本信息\n" + "\n".join(f"- {info}" for info in basic_info) + "\n"
            
            # BMI 信息
            if context.get("BMI"):
                user_profile += f"\n### 体重评估\n- BMI: {context['BMI']}"
                if context.get("BMI分类"):
                    user_profile += f" ({context['BMI分类']})"
                if context.get("BMI建议"):
                    user_profile += f"\n- 建议: {context['BMI建议']}"
                user_profile += "\n"
            
            # 健康目标
            if context.get("健康目标") and context["健康目标"] != "未知":
                user_profile += f"\n### 健康目标\n- {context['健康目标']}"
                if context.get("目标体重"):
                    user_profile += f"\n- 目标体重: {context['目标体重']}"
                user_profile += "\n"
            
            # 健康状况
            health_conditions = []
            if context.get("慢性病史") and context["慢性病史"] != "无":
                health_conditions.append(f"慢性病: {context['慢性病史']}")
            if context.get("过敏食物") and context["过敏食物"] != "无":
                health_conditions.append(f"食物过敏: {context['过敏食物']}")
            if context.get("伤病情况"):
                health_conditions.append(f"伤病: {context['伤病情况']}")
            
            if health_conditions:
                user_profile += "\n### 健康状况 (请特别注意)\n"
                user_profile += "\n".join(f"- ⚠️ {condition}" for condition in health_conditions) + "\n"
            
            # 饮食偏好
            if context.get("饮食习惯"):
                user_profile += f"\n### 饮食习惯\n- {context['饮食习惯']}\n"
            
            # 运动偏好
            if context.get("运动偏好"):
                user_profile += f"\n### 运动偏好\n- {context['运动偏好']}\n"
            if context.get("每日运动目标"):
                user_profile += f"- 每日运动目标: {context['每日运动目标']}\n"
            
            base_prompt += user_profile
            base_prompt += "\n请根据以上用户信息，提供个性化的健康建议。"
        
        return base_prompt
    
    async def chat(
        self, 
        user_message: str, 
        context: Optional[Dict[str, Any]] = None,
        history: Optional[List[Dict[str, str]]] = None
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
            logger.warning("AI API Key 未配置，使用模拟响应")
            return self._get_mock_response(user_message, context)
        
        self._init_dashscope()
        
        try:
            from dashscope import Generation
            
            # 构建系统提示词
            system_prompt = self._build_system_prompt(context)
            
            # 构建消息列表
            messages = [{"role": "system", "content": system_prompt}]
            
            # 添加历史对话（最多保留最近10轮）
            if history:
                # 过滤并限制历史记录
                recent_history = history[-20:]  # 最多20条消息（10轮对话）
                for msg in recent_history:
                    if msg.get("role") in ["user", "assistant"] and msg.get("content"):
                        messages.append({
                            "role": msg["role"],
                            "content": msg["content"]
                        })
            
            # 添加当前用户消息
            messages.append({"role": "user", "content": user_message})
            
            logger.info(f"调用千问API，消息数: {len(messages)}, 模型: {self.model}")
            
            # 调用千问 API
            response = Generation.call(
                model=self.model,
                messages=messages,
                result_format='message',
                max_tokens=1500,
                temperature=0.7,
                top_p=0.8,
            )
            
            if response.status_code == 200:
                reply = response.output.choices[0].message.content
                logger.info(f"AI响应成功，长度: {len(reply)}")
                return reply
            else:
                error_msg = f"AI服务异常 (code: {response.status_code}): {response.message}"
                logger.error(error_msg)
                # 降级到模拟响应
                return self._get_mock_response(user_message, context)
                
        except ImportError:
            logger.error("dashscope 模块未安装")
            return "AI服务暂不可用，请联系管理员。"
        except Exception as e:
            logger.error(f"AI服务调用失败: {str(e)}")
            # 降级到模拟响应
            return self._get_mock_response(user_message, context)
    
    def _get_mock_response(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """获取模拟响应（API不可用时的降级方案）"""
        
        # 个性化问候
        greeting = ""
        if context:
            if context.get("BMI分类") == "偏瘦":
                greeting = "根据您的BMI显示体重偏轻，"
            elif context.get("BMI分类") in ["偏胖", "肥胖"]:
                greeting = "根据您的BMI，体重管理是您的健康重点，"
        
        message_lower = message.lower()
        
        if "减肥" in message or "减重" in message or "瘦" in message:
            response = f"""{greeting}关于科学减重，我为您整理了以下建议：

**🍽️ 饮食调整**
- 控制每日热量摄入，建议减少300-500千卡
- 增加蛋白质摄入（鸡胸肉、鱼虾、豆腐）
- 多吃蔬菜，增加饱腹感
- 避免精制碳水和含糖饮料

**🏃 运动建议**
- 每周150分钟中等强度有氧运动
- 配合2-3次力量训练
- 日常增加步行，目标每天8000步

**⏰ 生活习惯**
- 保证7-8小时睡眠
- 细嚼慢咽，每餐20分钟以上
- 记录饮食，定期称重

💡 健康减重速度为每周0.5-1kg，切勿急于求成。"""
            return response

        elif "运动" in message or "锻炼" in message or "健身" in message:
            injury_note = ""
            if context and context.get("伤病情况"):
                injury_note = f"\n\n⚠️ **特别提醒**：您有 {context['伤病情况']}，运动时请注意保护，避免加重损伤。"
            
            return f"""为您推荐的运动方案：

**🔥 有氧运动**（每周3-5次）
- 快走/慢跑：30-45分钟
- 游泳：30分钟
- 骑行：45分钟

**💪 力量训练**（每周2-3次）
- 深蹲、俯卧撑、平板支撑
- 每个动作3组，每组12-15次
- 注意动作标准，避免受伤

**🧘 柔韧性训练**
- 运动前动态拉伸
- 运动后静态拉伸
- 可尝试瑜伽放松身心

**📝 注意事项**
- 循序渐进，不要突然增加强度
- 运动前热身10分钟
- 运动后补充水分和蛋白质{injury_note}"""

        elif "吃" in message or "饮食" in message or "营养" in message or "食物" in message:
            allergy_note = ""
            if context and context.get("过敏食物") and context["过敏食物"] != "无":
                allergy_note = f"\n\n⚠️ **过敏提醒**：您对 {context['过敏食物']} 过敏，请在饮食中注意避免。"
            
            return f"""健康饮食建议：

**🥗 每日营养搭配**
- 主食：全谷物为主（糙米、燕麦、全麦）
- 蛋白质：鱼虾、禽肉、蛋、豆制品
- 蔬菜：每天300-500克，种类丰富
- 水果：每天200-350克

**⏰ 进餐时间**
- 早餐：7:00-8:00（不要不吃！）
- 午餐：12:00-13:00
- 晚餐：18:00-19:00

**🚫 建议少吃**
- 油炸食品、膨化食品
- 含糖饮料、奶茶
- 加工肉制品
- 高盐腌制食品{allergy_note}"""

        elif "睡眠" in message or "失眠" in message or "睡不着" in message:
            return """改善睡眠的实用建议：

**🌙 睡前准备**
- 睡前1小时放下手机
- 温水泡脚15分钟
- 可以听轻音乐或冥想
- 卧室保持安静、黑暗、凉爽

**☕ 饮食调整**
- 午后避免咖啡和茶
- 晚餐不要太饱或太晚
- 睡前可喝温牛奶

**⏰ 作息规律**
- 固定时间入睡和起床
- 周末也保持规律
- 白天适当运动，但睡前3小时避免剧烈运动

**💡 如果持续失眠超过2周，建议就医检查。**"""

        elif "BMI" in message.upper() or "体重" in message:
            if context and context.get("BMI"):
                return f"""根据您的数据：

**📊 您的BMI分析**
- BMI值：{context.get('BMI', '未知')}
- 分类：{context.get('BMI分类', '未知')}
- 身高：{context.get('身高', '未知')}
- 体重：{context.get('体重', '未知')}

**💡 健康建议**
{context.get('BMI建议', '保持健康的生活方式')}

BMI只是健康评估的参考指标之一，还需要结合体脂率、腰围等综合判断。

需要我为您制定个性化的健康管理方案吗？"""
            else:
                return """BMI（身体质量指数）是评估体重是否健康的常用指标。

**📐 计算公式**
BMI = 体重(kg) ÷ 身高(m)²

**📊 分类标准**（中国标准）
- < 18.5：偏瘦
- 18.5-24：正常
- 24-28：超重
- ≥ 28：肥胖

请在「我的」页面完善身高体重信息，我可以为您计算并提供个性化建议。"""

        else:
            goal_tip = ""
            if context and context.get("健康目标") and context["健康目标"] != "未知":
                goal_tip = f"\n\n💡 我注意到您的健康目标是「{context['健康目标']}」，需要我为您提供相关建议吗？"
            
            return f"""您好！我是您的专属健康助手 🌟

我可以为您提供以下方面的专业建议：

**🍎 营养饮食**
- 每日营养搭配
- 食物热量查询
- 特殊人群饮食

**⚖️ 体重管理**
- BMI分析
- 减脂/增肌方案
- 健康体重计算

**🏃 运动健身**
- 运动计划制定
- 运动方式推荐
- 运动注意事项

**💊 健康生活**
- 睡眠改善
- 压力管理
- 慢性病饮食

请告诉我您想了解什么？{goal_tip}

⚠️ 温馨提示：我的建议仅供参考，如有严重健康问题请及时就医。"""


# 全局实例
ai_assistant = AIHealthAssistant()
