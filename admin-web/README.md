# 营养不良筛查与健康管理 - Web 管理后台

基于 Vue 3 + Element Plus 的管理后台。

## 技术栈

- Vue 3 (前端框架)
- TypeScript (类型安全)
- Vite (构建工具)
- Element Plus (UI 组件库)
- Pinia (状态管理)
- Vue Router (路由)
- Axios (HTTP 请求)
- Tailwind CSS (原子化 CSS)
- ECharts (图表)

## 快速开始

### 1. 安装依赖

```bash
cd admin-web
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:3000

### 3. 生产构建

```bash
npm run build
```

输出目录：`dist/`

## 项目结构

```
admin-web/
├── src/
│   ├── api/                    # API 接口封装
│   │   ├── request.ts          # Axios 封装
│   │   ├── auth.ts             # 认证接口
│   │   ├── user.ts             # 用户管理
│   │   ├── audit.ts            # 内容审核
│   │   ├── product.ts          # 商品管理
│   │   ├── order.ts            # 订单管理
│   │   ├── stats.ts            # 统计数据
│   │   ├── setting.ts          # 系统设置
│   │   └── index.ts            # 统一导出
│   │
│   ├── layout/                 # 布局组件
│   │   └── MainLayout.vue      # 主布局
│   │
│   ├── router/                 # 路由配置
│   │   └── index.ts            # 路由定义
│   │
│   ├── store/                  # 状态管理
│   │   ├── index.ts            # Pinia 实例
│   │   └── admin.ts            # 管理员状态
│   │
│   ├── views/                  # 页面组件
│   │   ├── Login.vue           # 登录页
│   │   ├── Dashboard.vue       # 仪表盘
│   │   ├── UserList.vue        # 用户管理
│   │   ├── ContentAudit.vue    # 内容审核
│   │   ├── ProductList.vue     # 商品管理
│   │   ├── OrderList.vue       # 订单管理
│   │   └── Settings.vue        # 系统设置
│   │
│   ├── App.vue                 # 根组件
│   ├── main.ts                 # 入口文件
│   └── style.css               # 全局样式
│
├── public/                     # 静态资源
├── index.html                  # HTML 入口
├── package.json                # 项目配置
├── vite.config.ts              # Vite 配置
├── tailwind.config.js          # Tailwind 配置
└── tsconfig.json               # TypeScript 配置
```

## 功能模块

| 页面 | 路由 | 功能 |
|------|------|------|
| 登录 | /login | 管理员登录 |
| 仪表盘 | /dashboard | 数据概览、图表、待办事项 |
| 用户管理 | /users | 用户列表、详情、禁用/启用 |
| 内容审核 | /content | 动态/评论审核、通过/拒绝 |
| 商品管理 | /products | 商品CRUD、分类管理、上下架 |
| 订单管理 | /orders | 订单列表、发货、退款 |
| 系统设置 | /settings | 积分规则、会员配置、订单配置 |

## API 对接

所有 API 已对接后端 `/api/admin/` 接口：

| 模块 | 接口数 | 状态 |
|------|--------|------|
| 认证 | 3 | ✅ |
| 用户管理 | 3 | ✅ |
| 内容审核 | 4 | ✅ |
| 商品管理 | 8 | ✅ |
| 订单管理 | 4 | ✅ |
| 数据统计 | 4 | ✅ |
| 系统设置 | 6 | ✅ |

## 测试账号

| 账号 | 密码 | 角色 |
|------|------|------|
| admin | admin123 | 超级管理员 |

## 设计规范

### 颜色系统（苹果风格）

```css
--apple-blue: #0071e3;      /* 主色调 */
--apple-dark: #1d1d1f;      /* 深色文字 */
--apple-gray: #f5f5f7;      /* 背景灰 */
--apple-text-gray: #86868b; /* 次要文字 */
--apple-border: #d2d2d7;    /* 边框色 */
```

### 禁止使用紫色

根据项目规范，禁止使用紫色（包括 #667eea、#764ba2 等紫色渐变）。

## 注意事项

1. **确保后端已启动**：默认连接 `http://localhost:8000/api/admin`
2. **Token 存储**：使用 localStorage 存储 `admin_token`
3. **路由守卫**：未登录自动跳转登录页

## 开发指南

详见：[docs/14-管理后台开发文档.md](../docs/14-管理后台开发文档.md)


















