# 项目初始化待办清单

> 创建时间：2025-11-27  
> 状态说明：⬜ 待完成 | ✅ 已完成 | ⏸️ 暂缓

---

## 已完成

- ✅ 整理开发文档（docs/）
- ✅ 创建项目规则文件（.cursorrules、.editorconfig、.gitignore）
- ✅ 设计数据库（38张表）
- ✅ 初始化数据库（health_db）
- ✅ 配置 MCP 工具说明

---

## 待完成

### 一、小程序前端（uni-app + Vue 3）

#### 1.1 创建项目
```bash
# 方式一：CLI 创建（推荐）
npx degit dcloudio/uni-preset-vue#vite-ts miniprogram-frontend
cd miniprogram-frontend
npm install

# 方式二：HBuilderX 创建
# 文件 → 新建 → 项目 → uni-app → Vue3
```

#### 1.2 安装依赖
```bash
# UI 组件库（必须）
npm install wot-design-uni

# 状态管理（必须）
npm install pinia

# 工具库（推荐）
npm install dayjs
npm install lodash-es
```

#### 1.3 项目配置
- ⬜ 配置 `pages.json`（页面路由、tabBar）
- ⬜ 配置 `manifest.json`（小程序 AppID）
- ⬜ 创建 `src/utils/request.ts`（请求封装）
- ⬜ 创建 `src/stores/user.ts`（用户状态）
- ⬜ 创建 `src/stores/app.ts`（全局状态）
- ⬜ 配置环境变量（.env.development、.env.production）
- ⬜ 引入 Wot Design Uni 组件库
- ⬜ 创建占位图目录 `static/placeholder/`

#### 1.4 基础页面
- ⬜ 首页 `pages/index/index.vue`
- ⬜ 健康筛查 `pages/health/index.vue`
- ⬜ 社区 `pages/community/index.vue`
- ⬜ 商城 `pages/shop/index.vue`
- ⬜ 我的 `pages/user/index.vue`

---

### 二、后端（Python + FastAPI）

#### 2.1 创建项目
```bash
mkdir backend
cd backend
python -m venv venv

# Windows 激活
.\venv\Scripts\activate

# Mac/Linux 激活
source venv/bin/activate
```

#### 2.2 安装依赖
```bash
pip install fastapi uvicorn
pip install sqlalchemy aiomysql alembic
pip install pydantic pydantic-settings
pip install python-jose passlib bcrypt
pip install python-multipart
pip install redis
pip install dashscope
pip install httpx
```

#### 2.3 项目结构
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # 入口
│   ├── config.py            # 配置
│   ├── database.py          # 数据库连接
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py      # 认证
│   │       ├── users.py     # 用户
│   │       ├── health.py    # 健康筛查
│   │       ├── sport.py     # 运动
│   │       ├── food.py      # 膳食
│   │       ├── shop.py      # 商城
│   │       ├── community.py # 社区
│   │       └── ai.py        # AI助手
│   ├── models/              # 数据库模型
│   ├── schemas/             # Pydantic 模型
│   ├── services/            # 业务逻辑
│   └── utils/               # 工具函数
├── alembic/                 # 数据库迁移
├── .env                     # 环境变量
├── requirements.txt         # 依赖
└── README.md
```

#### 2.4 配置文件
- ⬜ 创建 `.env` 文件
- ⬜ 创建 `app/config.py`（读取环境变量）
- ⬜ 创建 `app/database.py`（数据库连接）
- ⬜ 初始化 Alembic（数据库迁移工具）
- ⬜ 创建 SQLAlchemy 模型（对应 38 张表）

#### 2.5 基础接口
- ⬜ 微信登录 `/api/v1/auth/wechat-login`
- ⬜ 用户信息 `/api/v1/users/me`
- ⬜ 文件上传 `/api/v1/upload`

---

### 三、Web 管理端（Vue 3 + Element Plus）

#### 3.1 创建项目
```bash
npm create vite@latest admin-web -- --template vue-ts
cd admin-web
npm install
```

#### 3.2 安装依赖
```bash
npm install element-plus @element-plus/icons-vue
npm install pinia
npm install vue-router
npm install axios
npm install dayjs
```

#### 3.3 项目配置
- ⬜ 配置路由 `src/router/index.ts`
- ⬜ 配置状态管理 `src/stores/`
- ⬜ 配置请求封装 `src/utils/request.ts`
- ⬜ 配置 Element Plus

#### 3.4 基础页面
- ⬜ 登录页
- ⬜ 首页/仪表盘
- ⬜ 用户管理
- ⬜ 商品管理
- ⬜ 订单管理
- ⬜ 内容审核
- ⬜ 系统设置

---

### 四、其他配置

#### 4.1 微信小程序
- ⬜ 注册微信小程序账号
- ⬜ 获取 AppID 和 AppSecret
- ⬜ 配置服务器域名（开发阶段可跳过）

#### 4.2 阿里云百炼
- ⬜ 注册阿里云账号
- ⬜ 开通百炼服务
- ⬜ 获取 API Key

#### 4.3 设计资源
- ⬜ 在 `design-references/` 放入 Keep App 截图
- ⬜ 创建占位图 `static/placeholder/default.png`

---

## 建议的开发顺序

```
1. 小程序前端基础框架 → 能跑起来、能看到页面
2. 后端基础框架 → 能启动、能连接数据库
3. 前后端联调 → 登录接口跑通
4. 按优先级开发功能模块（参考 docs/07-开发优先级.md）
   - P0: 用户登录、健康筛查、商城核心
   - P1: 运动记录、膳食管理、社区基础
   - P2: 积分系统、AI助手、课程
   - P3: 高级功能、优化
5. Web 管理端（可与前端并行开发）
```

---

## 快捷命令

```bash
# 启动后端
cd backend && .\venv\Scripts\activate && uvicorn app.main:app --reload

# 启动小程序
cd miniprogram-frontend && npm run dev:mp-weixin

# 启动管理端
cd admin-web && npm run dev

# 连接数据库
mysql -u root -p1234 health_db
```

---

## 注意事项

1. **禁止使用 Emoji** - 所有界面文案
2. **图标图片用占位符** - 等设计稿
3. **适老化功能默认关闭** - 实现但不启用
4. **暂缓功能做好预留** - GPS后端、支付后端、AI内核
5. **优先用 Wot Design Uni** - 组件库首选
6. **参考 Keep + App Store 风格** - 无设计稿时

