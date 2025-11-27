# 设计参考图

本文件夹用于存放 UI/UX 设计参考图片。

## 参考来源

主要参考 **Keep App** 的设计风格，包括：

- 首页布局
- 运动记录页面
- 打卡流程
- 社区动态页
- 个人中心
- 商城页面
- 等等...

## 文件命名规范

```
{页面名称}_{功能描述}_{序号}.{png|jpg}

示例：
- home_main_01.png
- sport_running_01.png
- sport_running_02.png
- community_feed_01.png
- shop_product_detail_01.png
- user_profile_01.png
```

## 使用说明

1. 将 Keep App 截图放入本文件夹
2. 按照命名规范重命名
3. 开发时参考对应页面的截图进行布局设计

## 参考图清单

请在下方记录已添加的参考图：

| 文件名 | 对应页面 | 参考要点 |
|-------|---------|---------|
| `auth_privacy_01.jpg` | 登录 / 注册 | 手机号登录页上的「隐私政策」弹窗布局、按钮层级、蒙层样式 |
| `auth_login_01.jpg` | 登录 / 注册 | 手机号登录表单、验证码按钮、第三方登录入口的整体排版 |
| `onboarding_welcome_01.jpg` | 新手引导 | 欢迎页插画、单一主按钮（开始问卷）的居中布局和留白比例 |
| `onboarding_identity_01.jpg` | 新手引导 | 「你的身份是？」多卡片选择样式，整屏列表 + 底部主按钮布局 |
| `onboarding_basic_gender_01.jpg` | 基础信息 | 基础信息列表 + 性别选择弹窗（底部弹出、左右两卡片）的样式 |
| `onboarding_basic_birthday_01.jpg` | 基础信息 | 生日选择器（日期滚轮）与上方表单项联动的交互和层级关系 |
| `onboarding_basic_height_01.jpg` | 基础信息 | 身高滑尺控件样式（刻度、当前值放大显示、确认按钮） |
| `onboarding_basic_weight_01.jpg` | 基础信息 | 体重滑尺 + BMI 结果区域整体排版、文本层级和颜色 |
| `onboarding_generating_plan_01.jpg` | 方案生成 | 纯色背景进度页，中央百分比 + 下方步骤列表的动效感布局 |
| `onboarding_plan_member_01.jpg` | 会员推荐 | 方案生成完成后叠加的会员推荐弹层（大图 + 会员卡 + CTA 按钮） |
| `community_feed_01.jpg` | 社区首页 | 顶部 Tab、搜索框、故事圆形入口、动态 Feed 卡片布局和底部 TabBar |
| `sport_running_01.jpg` | 运动记录 | 跑步首页：顶部模式切换、地图区域、底部大 GO 按钮及状态提示 |
| `shop_home_01.jpg` | 商城首页 | 商城多级分类 Tab、商品宫格卡片、Banner 区域以及底部导航风格 |
| `user_profile_01.jpg` | 我的首页 | 个人中心：头像区、会员卡片、功能网格入口、数据概览模块的排版 |
| `user_settings_01.jpg` | 设置 | 设置列表：分组标题、单元格样式、行内说明文字和右侧箭头布局 |
| `coach_schedule_01.jpg` | 训练计划 | 训练/教练页：目标卡片、训练日程（日历）、下方快捷入口的整体结构 |
| `community_video_01.jpg` | 社区详情 | 单条视频动态详情页：视频区域、标题标签、互动按钮、评论和底部操作 |
| `community_publish_01.jpg` | 发布动态 | 发布图文/视频动态页：封面图、标题输入、多行正文和底部发布按钮样式 |

> 说明：如果在 **Wot Design Uni / uni-ui** 等组件库中找不到完全匹配的组件（例如：滑尺、环形进度圈、特殊布局的弹窗等），  
> 则需要在项目中 **自行实现自定义组件**，但应尽量复用现有组件的交互细节与配色，保持整体风格一致。


