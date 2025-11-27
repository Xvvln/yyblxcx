# 数据库设计

> 数据库：MySQL 8.0  
> 字符集：utf8mb4  
> 排序规则：utf8mb4_unicode_ci  
> 数据库名：health_db

---

## 连接信息

```
host: localhost
port: 3306
database: health_db
user: root
password: 1234
```

---

## ER 关系图

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│     users       │───┐   │    products     │       │    courses      │
│   (用户表)      │   │   │   (商品表)      │       │   (课程表)      │
└─────────────────┘   │   └─────────────────┘       └─────────────────┘
        │             │           │                         │
        │             │           │                         │
        ▼             │           ▼                         ▼
┌─────────────────┐   │   ┌─────────────────┐       ┌─────────────────┐
│health_screenings│   │   │  order_items    │       │user_course_     │
│ (健康筛查)      │   │   │  (订单明细)     │       │  collects       │
└─────────────────┘   │   └─────────────────┘       └─────────────────┘
        │             │           │
        ▼             │           ▼
┌─────────────────┐   │   ┌─────────────────┐       ┌─────────────────┐
│ sport_records   │   ├──►│    orders       │◄──────│    coupons      │
│ (运动记录)      │   │   │   (订单表)      │       │  (优惠券)       │
└─────────────────┘   │   └─────────────────┘       └─────────────────┘
        │             │
        ▼             │   ┌─────────────────┐       ┌─────────────────┐
┌─────────────────┐   ├──►│     carts       │       │  daily_tasks    │
│ food_records    │   │   │   (购物车)      │       │ (每日任务)      │
│ (饮食记录)      │   │   └─────────────────┘       └─────────────────┘
└─────────────────┘   │                                     │
        │             │   ┌─────────────────┐               ▼
        ▼             │   │     posts       │       ┌─────────────────┐
┌─────────────────┐   ├──►│  (社区动态)     │       │user_task_records│
│checkin_records  │   │   └─────────────────┘       │ (任务记录)      │
│ (打卡记录)      │   │           │                 └─────────────────┘
└─────────────────┘   │           ▼
                      │   ┌─────────────────┐       ┌─────────────────┐
                      │   │ post_comments   │       │   coin_records  │
                      │   │   (评论)        │       │  (积分记录)     │
                      │   └─────────────────┘       └─────────────────┘
                      │
                      │   ┌─────────────────┐       ┌─────────────────┐
                      └──►│  user_follows   │       │    admins       │
                          │  (关注关系)     │       │   (管理员)      │
                          └─────────────────┘       └─────────────────┘
```

---

## 数据表统计（共 38 张）

### 用户模块（3张）

| 表名 | 说明 |
|-----|------|
| users | 用户基础信息（含余额、积分、粉丝数） |
| user_health_profiles | 用户健康档案 |
| user_addresses | 收货地址 |

### 健康筛查模块（2张）

| 表名 | 说明 |
|-----|------|
| health_screenings | 健康筛查记录 |
| health_reminders | 健康提醒设置 |

### 运动模块（3张）

| 表名 | 说明 |
|-----|------|
| sport_records | 运动记录 |
| sport_goals | 运动目标 |
| courses | 运动/饮食课程 |

### 膳食模块（2张）

| 表名 | 说明 |
|-----|------|
| food_records | 饮食记录 |
| food_library | 食物库 |

### 商城模块（8张）

| 表名 | 说明 |
|-----|------|
| product_categories | 商品分类 |
| products | 商品 |
| product_reviews | 商品评价 |
| carts | 购物车 |
| coupons | 优惠券模板 |
| user_coupons | 用户优惠券 |
| orders | 订单 |
| order_items | 订单明细 |

### 社区模块（6张）

| 表名 | 说明 |
|-----|------|
| posts | 社区动态 |
| post_comments | 动态评论 |
| post_likes | 动态点赞 |
| topics | 话题 |
| user_follows | 关注关系 |
| user_course_collects | 课程收藏 |

### 私信模块（2张）

| 表名 | 说明 |
|-----|------|
| conversations | 会话列表 |
| messages | 私信消息 |

### 积分任务模块（4张）

| 表名 | 说明 |
|-----|------|
| coin_records | 积分变动记录 |
| checkin_records | 打卡记录 |
| daily_tasks | 每日任务配置 |
| user_task_records | 用户任务完成记录 |

### 会员模块（1张）

| 表名 | 说明 |
|-----|------|
| member_orders | 会员购买记录 |

### AI模块（1张）

| 表名 | 说明 |
|-----|------|
| ai_chat_records | AI对话记录 |

### 系统管理模块（6张）

| 表名 | 说明 |
|-----|------|
| admins | 管理员 |
| admin_logs | 管理员操作日志 |
| notifications | 系统通知 |
| banners | 轮播图 |
| system_configs | 系统配置 |
| files | 文件管理 |

---

## SQL 文件说明

| 文件 | 内容 |
|-----|------|
| 01-用户模块.sql | users, user_health_profiles, user_addresses |
| 02-健康筛查模块.sql | health_screenings, health_reminders |
| 03-运动模块.sql | sport_records, sport_goals |
| 04-饮食模块.sql | food_records, food_library |
| 05-课程模块.sql | courses, user_course_collects |
| 06-商城模块.sql | 商品、购物车、订单、优惠券相关表 |
| 07-社区模块.sql | 动态、评论、点赞、关注、私信相关表 |
| 08-积分任务模块.sql | 积分、打卡、任务相关表 |
| 09-系统管理模块.sql | 管理员、通知、轮播图、配置相关表 |
| **init-all.sql** | 完整初始化脚本（按依赖顺序） |

---

## 初始化命令

```bash
# 方式一：命令行
mysql -u root -p1234 < docs/数据库设计/init-all.sql

# 方式二：MySQL 客户端
mysql> source docs/数据库设计/init-all.sql;
```

**注意**：数据库已于 2025-11-27 初始化完成，无需重复执行。
