# 营养不良筛查与健康管理 - 后端 API

基于 FastAPI 的后端 API 服务。

## 技术栈

- Python 3.11+
- FastAPI (Web 框架)
- SQLAlchemy 2.0 (ORM，异步模式)
- MySQL 8.0 (数据库)
- Pydantic v2 (数据校验)
- JWT (认证)
- DashScope (AI 服务)

## 快速开始

### 1. 创建虚拟环境

```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

主要配置项：
- `DATABASE_URL`: 数据库连接地址
- `JWT_SECRET_KEY`: JWT 密钥
- `WECHAT_APPID`: 微信小程序 AppID（可选）
- `WECHAT_SECRET`: 微信小程序 Secret（可选）
- `DASHSCOPE_API_KEY`: 阿里云百炼 API Key（AI功能）

### 4. 启动服务

```bash
# 方式一：使用启动脚本
python run.py

# 方式二：直接使用 uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   │
│   ├── models/              # SQLAlchemy 模型 (14个文件)
│   │   ├── user.py          # 用户、健康档案、地址
│   │   ├── health.py        # 健康筛查、提醒
│   │   ├── sport.py         # 运动记录、目标
│   │   ├── food.py          # 饮食记录、食物库
│   │   ├── course.py        # 课程
│   │   ├── shop.py          # 商品、分类、评价
│   │   ├── cart.py          # 购物车
│   │   ├── order.py         # 订单
│   │   ├── coupon.py        # 优惠券
│   │   ├── community.py     # 社区动态
│   │   ├── message.py       # 私信
│   │   ├── points.py        # 积分、签到、任务
│   │   ├── member.py        # 会员订单
│   │   └── system.py        # 系统管理
│   │
│   ├── schemas/             # Pydantic 数据验证
│   │   ├── common.py        # 通用模型
│   │   ├── auth.py          # 认证
│   │   └── user.py          # 用户
│   │
│   ├── api/                 # API 路由
│   │   ├── v1/              # 小程序端 (24个模块)
│   │   └── admin/           # 管理后台 (7个模块)
│   │
│   ├── services/            # 业务逻辑
│   │   └── ai_service.py    # AI 服务
│   │
│   └── utils/               # 工具函数
│       ├── security.py      # JWT、密码加密
│       ├── response.py      # 统一响应
│       └── helpers.py       # 辅助函数
│
├── uploads/                 # 上传文件目录
├── requirements.txt         # Python 依赖
├── run.py                   # 启动脚本
├── .env.example             # 环境变量示例
└── README.md                # 本文件
```

## API 模块说明

### 小程序端 API (`/api/v1/`)

| 模块 | 前缀 | 接口数 | 说明 |
|-----|------|--------|------|
| auth | /auth | 2 | 微信登录、注册 |
| user | /user | 5 | 用户信息、健康档案 |
| health | /health | 3 | 健康筛查 |
| sport | /sport | 3 | 运动记录、打卡 |
| sport_goal | /sport-goal | 5 | 运动目标 |
| food | /food | 3 | 饮食记录、打卡 |
| food_library | /food-library | 3 | 食物库 |
| course | /course | 5 | 课程浏览、收藏 |
| shop | /shop | 4 | 商品浏览 |
| cart | /cart | 4 | 购物车 |
| order | /order | 7 | 订单管理 |
| coupon | /coupon | 3 | 优惠券 |
| community | /community | 14 | 社区动态 |
| message | /message | 4 | 私聊 |
| points | /points | 4 | 积分 |
| task | /task | 3 | 每日任务 |
| checkin | /checkin | 4 | 签到 |
| member | /member | 4 | 会员 |
| reminder | /reminder | 4 | 提醒设置 |
| address | /address | 5 | 收货地址 |
| doctor | /doctor, /article | 4 | 医生、文章 (Mock) |
| ai | /ai | 3 | AI 助手 |
| notification | /notification | 5 | 通知 |
| banner | /banner | 1 | 轮播图 |
| stats | /stats | 4 | 个人统计 |
| upload | /upload | 1 | 文件上传 |
| **合计** | | **103** | |

### 管理后台 API (`/api/admin/`)

| 模块 | 前缀 | 接口数 | 说明 |
|-----|------|--------|------|
| auth | /auth | 3 | 管理员登录、登出 |
| user | /user | 3 | 用户管理 |
| audit | /audit | 4 | 内容审核 |
| product | /product, /category | 8 | 商品管理 |
| order | /order | 4 | 订单管理 |
| stats | /stats | 4 | 数据统计 |
| setting | /setting | 6 | 系统设置 |
| **合计** | | **32** | |

## 测试账号

### 管理后台

| 账号 | 密码 | 角色 |
|------|------|------|
| admin | admin123 | 超级管理员 |

### 小程序端

通过微信登录，无需账号密码。

## 暂缓实现的功能

以下功能按文档要求暂缓实现，返回模拟数据：

| 功能 | 原因 | 当前处理 |
|------|------|----------|
| 微信/支付宝支付 | 需商户资质 | 直接返回支付成功 |
| GPS轨迹存储 | 后端逻辑复杂 | 前端mock，预留接口 |
| AI图像识别 | 需模型集成 | 预留接口结构 |
| 硬件数据接入 | 无设备 | 手动输入代替 |
| 面部/饮食识别 | 复杂AI | 预留接口返回mock |

## 统一响应格式

```json
// 成功
{
  "code": 200,
  "message": "success",
  "data": { ... }
}

// 分页
{
  "code": 200,
  "message": "success",
  "data": {
    "list": [...],
    "total": 100,
    "page": 1,
    "page_size": 20
  }
}

// 错误
{
  "code": 400,
  "message": "参数错误",
  "data": null
}
```

## 认证方式

### 小程序端

使用 JWT Token，请求头添加：

```
Authorization: Bearer {token}
```

### 管理后台

同样使用 JWT Token，但存储在 `admin_token` 中：

```
Authorization: Bearer {admin_token}
```

## 部署

### Docker 部署

```bash
# 构建镜像
docker build -t health-api .

# 运行容器
docker run -d -p 8000:8000 --env-file .env health-api
```

### 生产模式

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 开发指南

详见：[docs/13-后端开发文档.md](../docs/13-后端开发文档.md)
