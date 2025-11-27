# 九、API 接口规范

## 9.1 基础信息

| 项目 | 说明 |
|-----|------|
| Base URL | `https://your-domain.com/api/v1` |
| 数据格式 | JSON |
| 认证方式 | JWT Token（Header: `Authorization: Bearer {token}`） |
| 字符编码 | UTF-8 |

## 9.2 响应格式

```json
// 成功响应
{
  "code": 200,
  "message": "success",
  "data": { ... }
}

// 错误响应
{
  "code": 400,
  "message": "参数错误",
  "data": null
}
```

## 9.3 状态码

| 状态码 | 说明 |
|-------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未登录或Token失效 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 9.4 核心接口列表

### 认证模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| POST | `/auth/login` | 微信登录 |
| POST | `/auth/register` | 完善用户信息 |

### 用户模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/user/profile` | 获取个人信息 |
| PUT | `/user/profile` | 更新个人信息 |
| POST | `/user/avatar` | 上传头像 |
| GET | `/user/health-profile` | 获取健康档案 |
| PUT | `/user/health-profile` | 更新健康档案 |

### 健康筛查模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| POST | `/health/screening` | 提交筛查数据 |
| GET | `/health/records` | 筛查记录列表 |
| GET | `/health/report/{id}` | 获取报告详情 |

### 运动模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| POST | `/sport/record` | 提交运动记录 |
| GET | `/sport/records` | 运动记录列表 |
| POST | `/sport/checkin` | 运动打卡 |

### 饮食模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| POST | `/food/record` | 提交饮食记录 |
| GET | `/food/records` | 饮食记录列表 |
| POST | `/food/checkin` | 饮食打卡 |

### 课程模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/course/list` | 课程列表 |
| GET | `/course/{id}` | 课程详情 |
| POST | `/course/{id}/collect` | 收藏课程 |
| DELETE | `/course/{id}/collect` | 取消收藏 |
| GET | `/course/my-collects` | 我的收藏 |

### 商城模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/shop/products` | 商品列表 |
| GET | `/shop/product/{id}` | 商品详情 |
| GET | `/shop/categories` | 商品分类 |
| GET | `/shop/product/{id}/reviews` | 商品评价列表 |

### 购物车模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/cart` | 购物车列表 |
| POST | `/cart` | 添加购物车 |
| PUT | `/cart/{id}` | 修改数量 |
| DELETE | `/cart/{id}` | 删除商品 |

### 订单模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| POST | `/order` | 创建订单 |
| GET | `/order/list` | 订单列表 |
| GET | `/order/{id}` | 订单详情 |
| POST | `/order/{id}/pay` | 发起支付 |
| POST | `/order/{id}/cancel` | 取消订单 |
| POST | `/order/{id}/confirm` | 确认收货 |
| POST | `/order/{id}/review` | 提交评价 |

### 优惠券模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/coupon/available` | 可领取优惠券 |
| POST | `/coupon/{id}/receive` | 领取优惠券 |
| GET | `/coupon/my-coupons` | 我的优惠券 |

### 社区模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/community/posts` | 动态列表 |
| GET | `/community/post/{id}` | 动态详情 |
| POST | `/community/post` | 发布动态 |
| DELETE | `/community/post/{id}` | 删除动态 |
| POST | `/community/post/{id}/like` | 点赞 |
| DELETE | `/community/post/{id}/like` | 取消点赞 |
| POST | `/community/post/{id}/comment` | 评论 |
| GET | `/community/post/{id}/comments` | 评论列表 |
| GET | `/community/following` | 关注列表 |
| GET | `/community/followers` | 粉丝列表 |
| POST | `/community/follow/{user_id}` | 关注用户 |
| DELETE | `/community/follow/{user_id}` | 取消关注 |

### 私聊模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/message/conversations` | 会话列表 |
| GET | `/message/history/{user_id}` | 聊天记录 |
| POST | `/message/send` | 发送消息 |
| POST | `/message/read/{conversation_id}` | 标记已读 |

### 积分模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/points/balance` | 积分余额 |
| GET | `/points/records` | 积分记录 |
| GET | `/points/gifts` | 可兑换礼品 |
| POST | `/points/exchange` | 兑换礼品 |

### 任务模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/task/daily` | 今日任务列表 |
| GET | `/task/progress` | 任务进度 |
| POST | `/task/{id}/claim` | 领取任务奖励 |

### 会员模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/member/info` | 会员信息 |
| GET | `/member/plans` | 会员套餐列表 |
| POST | `/member/purchase` | 购买会员 |
| GET | `/member/orders` | 会员购买记录 |

### 提醒模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/reminder/list` | 提醒设置列表 |
| POST | `/reminder` | 添加提醒 |
| PUT | `/reminder/{id}` | 修改提醒 |
| DELETE | `/reminder/{id}` | 删除提醒 |

### 地址模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/address/list` | 地址列表 |
| POST | `/address` | 添加地址 |
| PUT | `/address/{id}` | 修改地址 |
| DELETE | `/address/{id}` | 删除地址 |
| PUT | `/address/{id}/default` | 设为默认 |

### 远程医疗模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/doctor/list` | 医生列表 |
| GET | `/doctor/{id}` | 医生详情 |
| GET | `/article/list` | 科普文章列表 |
| GET | `/article/{id}` | 文章详情 |

### 上传模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| POST | `/upload/image` | 上传图片 |

---

## 9.5 Web管理端接口

> Base URL: `https://your-domain.com/api/admin/v1`

### 管理员认证

| 方法 | 路径 | 说明 |
|------|-----|------|
| POST | `/auth/login` | 管理员登录 |
| POST | `/auth/logout` | 退出登录 |
| GET | `/auth/info` | 获取当前管理员信息 |

### 用户管理

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/user/list` | 用户列表（分页） |
| GET | `/user/{id}` | 用户详情 |
| PUT | `/user/{id}/status` | 禁用/启用用户 |

### 内容审核

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/audit/posts` | 待审核动态列表 |
| PUT | `/audit/post/{id}` | 审核动态 |
| GET | `/audit/comments` | 待审核评论列表 |
| PUT | `/audit/comment/{id}` | 审核评论 |

### 商品管理

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/product/list` | 商品列表 |
| POST | `/product` | 添加商品 |
| PUT | `/product/{id}` | 编辑商品 |
| DELETE | `/product/{id}` | 删除商品 |
| GET | `/category/list` | 分类列表 |
| POST | `/category` | 添加分类 |

### 订单管理

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/order/list` | 订单列表 |
| GET | `/order/{id}` | 订单详情 |
| POST | `/order/{id}/ship` | 发货 |
| POST | `/order/{id}/refund` | 退款处理 |

### 数据统计

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/stats/overview` | 数据概览 |
| GET | `/stats/user` | 用户统计 |
| GET | `/stats/order` | 订单统计 |
| GET | `/stats/health` | 健康数据统计 |

### 系统设置

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/setting/points` | 积分规则配置 |
| PUT | `/setting/points` | 更新积分规则 |
| GET | `/setting/member` | 会员配置 |
| PUT | `/setting/member` | 更新会员配置 |
| GET | `/setting/system` | 系统配置列表 |
| PUT | `/setting/system` | 更新系统配置 |

---

## 9.6 补充接口（小程序端）

> 以下接口为实际开发中补充实现的接口

### 签到模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| POST | `/checkin` | 每日签到 |
| GET | `/checkin/status` | 签到状态 |
| GET | `/checkin/calendar` | 签到日历 |
| GET | `/checkin/stats` | 签到统计 |

### 运动目标模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/sport-goal` | 运动目标列表 |
| POST | `/sport-goal` | 创建运动目标 |
| PUT | `/sport-goal/{id}` | 更新运动目标 |
| DELETE | `/sport-goal/{id}` | 删除运动目标 |
| GET | `/sport-goal/stats` | 目标统计 |

### 食物库模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/food-library/search` | 搜索食物库 |
| GET | `/food-library/categories` | 食物分类 |
| GET | `/food-library/{id}` | 食物详情 |

### AI 助手模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| POST | `/ai/chat` | AI 对话 |
| GET | `/ai/history` | 对话历史 |
| DELETE | `/ai/history/{session_id}` | 删除对话 |

### 通知模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/notification/list` | 通知列表 |
| POST | `/notification/read` | 标记已读 |
| POST | `/notification/read-all` | 全部已读 |
| GET | `/notification/unread-count` | 未读数量 |
| DELETE | `/notification/{id}` | 删除通知 |

### 轮播图模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/banner/list` | 轮播图列表 |

### 个人统计模块

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/stats/overview` | 数据概览 |
| GET | `/stats/health` | 健康趋势 |
| GET | `/stats/sport` | 运动统计 |
| GET | `/stats/food` | 饮食统计 |

### 社区补充接口

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/community/post/{id}/comments` | 评论列表 |
| GET | `/community/topics` | 话题列表 |
| GET | `/community/topic/{id}` | 话题详情 |
| GET | `/community/ranking` | 排行榜 |

### 用户主页接口

| 方法 | 路径 | 说明 |
|------|-----|------|
| GET | `/user/{user_id}/profile` | 获取其他用户公开信息 |

**响应示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "nickname": "用户昵称",
    "avatar": "/uploads/avatars/xxx.jpg",
    "bio": "个人简介",
    "gender": 1,
    "user_level": 3,
    "follower_count": 100,
    "following_count": 50,
    "like_count": 500,
    "is_followed": false
  }
}
```

### 商品分类管理（管理后台补充）

| 方法 | 路径 | 说明 |
|------|-----|------|
| PUT | `/category/{id}` | 编辑分类 |
| DELETE | `/category/{id}` | 删除分类 |


