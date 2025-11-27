-- =============================================
-- 营养不良筛查与健康管理系统 - 数据库初始化脚本
-- 版本：v1.0
-- 共计 35 张表
-- 执行顺序按依赖关系排列
-- =============================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS health_db 
    DEFAULT CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

USE health_db;

-- =============================================
-- 1. 用户模块 (3张表)
-- =============================================

-- 用户表
CREATE TABLE users (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    openid VARCHAR(100) UNIQUE NOT NULL COMMENT '微信openid',
    union_id VARCHAR(100) DEFAULT NULL COMMENT '微信unionid',
    nickname VARCHAR(50) DEFAULT NULL COMMENT '昵称',
    avatar VARCHAR(255) DEFAULT NULL COMMENT '头像路径',
    phone VARCHAR(20) DEFAULT NULL COMMENT '手机号',
    gender TINYINT DEFAULT 0 COMMENT '性别：0未知 1男 2女',
    birthday DATE DEFAULT NULL COMMENT '生日',
    height DECIMAL(5,2) DEFAULT NULL COMMENT '身高(cm)',
    weight DECIMAL(5,2) DEFAULT NULL COMMENT '体重(kg)',
    member_level TINYINT DEFAULT 0 COMMENT '会员等级：0普通 1月卡 2年卡 3终身',
    member_expire_time DATETIME DEFAULT NULL COMMENT '会员到期时间',
    sport_coins INT UNSIGNED DEFAULT 0 COMMENT '运动币',
    food_coins INT UNSIGNED DEFAULT 0 COMMENT '膳食币',
    balance DECIMAL(10,2) DEFAULT 0 COMMENT '账户余额',
    user_level TINYINT DEFAULT 1 COMMENT '用户等级 1-10',
    follower_count INT UNSIGNED DEFAULT 0 COMMENT '粉丝数',
    following_count INT UNSIGNED DEFAULT 0 COMMENT '关注数',
    continuous_checkin_days INT UNSIGNED DEFAULT 0 COMMENT '连续打卡天数',
    last_checkin_date DATE DEFAULT NULL COMMENT '最后打卡日期',
    status TINYINT DEFAULT 1 COMMENT '状态：0禁用 1正常',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_openid (openid),
    INDEX idx_phone (phone),
    INDEX idx_member_level (member_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 用户健康档案表
CREATE TABLE user_health_profiles (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    health_goal VARCHAR(50) DEFAULT NULL COMMENT '健康目标',
    target_weight DECIMAL(5,2) DEFAULT NULL COMMENT '目标体重',
    preferred_sports JSON DEFAULT NULL COMMENT '偏好运动类型',
    daily_exercise_minutes INT DEFAULT 30 COMMENT '每日期望运动时长(分钟)',
    has_injury TINYINT DEFAULT 0 COMMENT '是否有伤病',
    injury_description TEXT DEFAULT NULL COMMENT '伤病描述',
    chronic_diseases JSON DEFAULT NULL COMMENT '慢性病',
    pushup_count INT DEFAULT NULL COMMENT '俯卧撑数量',
    squat_count INT DEFAULT NULL COMMENT '深蹲数量',
    crunch_count INT DEFAULT NULL COMMENT '卷腹数量',
    climb_stairs_tired TINYINT DEFAULT NULL COMMENT '爬5层楼是否疲劳',
    diet_habit VARCHAR(50) DEFAULT NULL COMMENT '饮食习惯',
    allergies JSON DEFAULT NULL COMMENT '过敏食物',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_id (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户健康档案表';

-- 用户收货地址表
CREATE TABLE user_addresses (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    receiver_name VARCHAR(50) NOT NULL COMMENT '收货人',
    receiver_phone VARCHAR(20) NOT NULL COMMENT '收货电话',
    province VARCHAR(50) NOT NULL COMMENT '省',
    city VARCHAR(50) NOT NULL COMMENT '市',
    district VARCHAR(50) NOT NULL COMMENT '区',
    detail VARCHAR(200) NOT NULL COMMENT '详细地址',
    is_default TINYINT DEFAULT 0 COMMENT '是否默认地址',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户收货地址表';

-- =============================================
-- 2. 健康筛查模块 (1张表)
-- =============================================

CREATE TABLE health_screenings (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    height DECIMAL(5,2) DEFAULT NULL COMMENT '身高(cm)',
    weight DECIMAL(5,2) DEFAULT NULL COMMENT '体重(kg)',
    bmi DECIMAL(4,2) DEFAULT NULL COMMENT 'BMI指数',
    heart_rate INT DEFAULT NULL COMMENT '心率(次/分)',
    blood_pressure_high INT DEFAULT NULL COMMENT '收缩压',
    blood_pressure_low INT DEFAULT NULL COMMENT '舒张压',
    body_temperature DECIMAL(3,1) DEFAULT NULL COMMENT '体温',
    blood_sugar DECIMAL(4,2) DEFAULT NULL COMMENT '血糖',
    face_image VARCHAR(255) DEFAULT NULL COMMENT '面部照片',
    body_image VARCHAR(255) DEFAULT NULL COMMENT '体态照片',
    questionnaire_data JSON DEFAULT NULL COMMENT '问卷答案JSON',
    risk_level ENUM('low', 'medium', 'high') DEFAULT 'low' COMMENT '风险等级',
    risk_tags JSON DEFAULT NULL COMMENT '风险标签',
    ai_suggestion TEXT DEFAULT NULL COMMENT 'AI生成的健康建议',
    diet_suggestion TEXT DEFAULT NULL COMMENT '膳食建议',
    exercise_suggestion TEXT DEFAULT NULL COMMENT '运动建议',
    lifestyle_suggestion TEXT DEFAULT NULL COMMENT '生活方式建议',
    recommended_products JSON DEFAULT NULL COMMENT '推荐商品ID列表',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    INDEX idx_risk_level (risk_level),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='健康筛查记录表';

-- =============================================
-- 3. 运动模块 (2张表)
-- =============================================

CREATE TABLE sport_records (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    sport_type ENUM('running', 'walking', 'cycling', 'rope_skipping', 'swimming', 'fitness', 'other') NOT NULL COMMENT '运动类型',
    sport_name VARCHAR(50) DEFAULT NULL COMMENT '运动名称',
    duration INT NOT NULL DEFAULT 0 COMMENT '运动时长(秒)',
    distance DECIMAL(10,2) DEFAULT NULL COMMENT '距离(米)',
    calories INT DEFAULT NULL COMMENT '消耗卡路里',
    steps INT DEFAULT NULL COMMENT '步数',
    avg_pace VARCHAR(20) DEFAULT NULL COMMENT '平均配速',
    avg_heart_rate INT DEFAULT NULL COMMENT '平均心率',
    gps_track JSON DEFAULT NULL COMMENT 'GPS轨迹点',
    track_image VARCHAR(255) DEFAULT NULL COMMENT '轨迹截图',
    images JSON DEFAULT NULL COMMENT '运动照片列表',
    remark TEXT DEFAULT NULL COMMENT '运动备注',
    earned_coins INT DEFAULT 0 COMMENT '获得的运动币',
    start_time DATETIME NOT NULL COMMENT '开始时间',
    end_time DATETIME DEFAULT NULL COMMENT '结束时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_sport_type (sport_type),
    INDEX idx_start_time (start_time),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='运动记录表';

CREATE TABLE sport_checkins (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    checkin_date DATE NOT NULL COMMENT '打卡日期',
    sport_record_id BIGINT UNSIGNED DEFAULT NULL COMMENT '关联的运动记录',
    earned_coins INT DEFAULT 0 COMMENT '获得的运动币',
    is_continuous_bonus TINYINT DEFAULT 0 COMMENT '是否连续打卡奖励',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_date (user_id, checkin_date),
    INDEX idx_checkin_date (checkin_date),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (sport_record_id) REFERENCES sport_records(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='运动打卡表';

-- =============================================
-- 4. 饮食模块 (2张表)
-- =============================================

CREATE TABLE food_records (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    meal_type ENUM('breakfast', 'lunch', 'dinner', 'snack') NOT NULL COMMENT '餐次',
    meal_time DATETIME NOT NULL COMMENT '用餐时间',
    food_name VARCHAR(100) DEFAULT NULL COMMENT '食物名称',
    food_image VARCHAR(255) DEFAULT NULL COMMENT '食物照片',
    calories INT DEFAULT NULL COMMENT '卡路里',
    protein DECIMAL(6,2) DEFAULT NULL COMMENT '蛋白质(g)',
    carbohydrate DECIMAL(6,2) DEFAULT NULL COMMENT '碳水化合物(g)',
    fat DECIMAL(6,2) DEFAULT NULL COMMENT '脂肪(g)',
    fiber DECIMAL(6,2) DEFAULT NULL COMMENT '膳食纤维(g)',
    ai_analysis TEXT DEFAULT NULL COMMENT 'AI营养分析',
    nutrition_score INT DEFAULT NULL COMMENT '营养评分(0-100)',
    remark TEXT DEFAULT NULL COMMENT '备注',
    earned_coins INT DEFAULT 0 COMMENT '获得的膳食币',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_meal_time (meal_time),
    INDEX idx_meal_type (meal_type),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='饮食记录表';

CREATE TABLE food_checkins (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    checkin_date DATE NOT NULL COMMENT '打卡日期',
    breakfast_done TINYINT DEFAULT 0 COMMENT '早餐已记录',
    lunch_done TINYINT DEFAULT 0 COMMENT '午餐已记录',
    dinner_done TINYINT DEFAULT 0 COMMENT '晚餐已记录',
    earned_coins INT DEFAULT 0 COMMENT '获得的膳食币',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_date (user_id, checkin_date),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='饮食打卡表';

-- =============================================
-- 5. 课程模块 (2张表)
-- =============================================

CREATE TABLE courses (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL COMMENT '课程标题',
    cover_image VARCHAR(255) DEFAULT NULL COMMENT '封面图',
    description TEXT DEFAULT NULL COMMENT '课程描述',
    course_type ENUM('sport', 'food') NOT NULL COMMENT '课程类型',
    category VARCHAR(50) DEFAULT NULL COMMENT '分类',
    difficulty ENUM('easy', 'medium', 'hard') DEFAULT 'medium' COMMENT '难度',
    duration INT DEFAULT NULL COMMENT '时长(分钟)',
    video_url VARCHAR(500) DEFAULT NULL COMMENT '视频链接',
    content TEXT DEFAULT NULL COMMENT '图文内容',
    steps JSON DEFAULT NULL COMMENT '步骤详情',
    suitable_for JSON DEFAULT NULL COMMENT '适用人群标签',
    calories INT DEFAULT NULL COMMENT '预计消耗卡路里',
    view_count INT UNSIGNED DEFAULT 0 COMMENT '观看数',
    like_count INT UNSIGNED DEFAULT 0 COMMENT '点赞数',
    collect_count INT UNSIGNED DEFAULT 0 COMMENT '收藏数',
    is_member_only TINYINT DEFAULT 0 COMMENT '是否仅会员可看',
    sort_order INT DEFAULT 0 COMMENT '排序',
    status TINYINT DEFAULT 1 COMMENT '状态：0下架 1上架',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_course_type (course_type),
    INDEX idx_category (category),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='课程表';

CREATE TABLE user_course_collects (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    course_id BIGINT UNSIGNED NOT NULL COMMENT '课程ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_course (user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户课程收藏表';

-- =============================================
-- 6. 商城模块 (8张表)
-- =============================================

CREATE TABLE product_categories (
    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL COMMENT '分类名称',
    icon VARCHAR(255) DEFAULT NULL COMMENT '分类图标',
    sort_order INT DEFAULT 0 COMMENT '排序',
    status TINYINT DEFAULT 1 COMMENT '状态：0禁用 1启用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品分类表';

CREATE TABLE products (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    category_id INT UNSIGNED NOT NULL COMMENT '分类ID',
    name VARCHAR(100) NOT NULL COMMENT '商品名称',
    subtitle VARCHAR(200) DEFAULT NULL COMMENT '副标题',
    main_image VARCHAR(255) NOT NULL COMMENT '主图',
    images JSON DEFAULT NULL COMMENT '商品图片列表',
    price DECIMAL(10,2) NOT NULL COMMENT '售价',
    original_price DECIMAL(10,2) DEFAULT NULL COMMENT '原价',
    stock INT UNSIGNED DEFAULT 0 COMMENT '库存',
    sales INT UNSIGNED DEFAULT 0 COMMENT '销量',
    description TEXT DEFAULT NULL COMMENT '商品描述',
    detail TEXT DEFAULT NULL COMMENT '商品详情(富文本)',
    nutrition_label JSON DEFAULT NULL COMMENT '营养标签',
    suitable_for JSON DEFAULT NULL COMMENT '适用人群',
    ai_tags JSON DEFAULT NULL COMMENT 'AI推荐标签',
    sort_order INT DEFAULT 0 COMMENT '排序',
    status TINYINT DEFAULT 1 COMMENT '状态：0下架 1上架',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category_id (category_id),
    INDEX idx_status (status),
    INDEX idx_sales (sales),
    FOREIGN KEY (category_id) REFERENCES product_categories(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品表';

CREATE TABLE carts (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    product_id BIGINT UNSIGNED NOT NULL COMMENT '商品ID',
    quantity INT UNSIGNED NOT NULL DEFAULT 1 COMMENT '数量',
    selected TINYINT DEFAULT 1 COMMENT '是否选中',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_product (user_id, product_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='购物车表';

CREATE TABLE coupons (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '优惠券名称',
    type ENUM('amount', 'percent') NOT NULL COMMENT '类型',
    discount_amount DECIMAL(10,2) DEFAULT NULL COMMENT '减免金额',
    discount_percent DECIMAL(4,2) DEFAULT NULL COMMENT '折扣比例',
    min_amount DECIMAL(10,2) DEFAULT 0 COMMENT '最低消费金额',
    max_discount DECIMAL(10,2) DEFAULT NULL COMMENT '最高优惠金额',
    start_time DATETIME NOT NULL COMMENT '开始时间',
    end_time DATETIME NOT NULL COMMENT '结束时间',
    total_count INT UNSIGNED DEFAULT 0 COMMENT '发放总量',
    received_count INT UNSIGNED DEFAULT 0 COMMENT '已领取数量',
    per_user_limit INT UNSIGNED DEFAULT 1 COMMENT '每人限领数量',
    applicable_products JSON DEFAULT NULL COMMENT '适用商品ID',
    applicable_categories JSON DEFAULT NULL COMMENT '适用分类ID',
    status TINYINT DEFAULT 1 COMMENT '状态：0禁用 1启用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='优惠券模板表';

CREATE TABLE user_coupons (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    coupon_id BIGINT UNSIGNED NOT NULL COMMENT '优惠券ID',
    source_type ENUM('receive', 'points_exchange', 'system', 'activity') NOT NULL COMMENT '来源类型',
    source_id BIGINT UNSIGNED DEFAULT NULL COMMENT '来源ID',
    status ENUM('unused', 'used', 'expired') DEFAULT 'unused' COMMENT '状态',
    used_time DATETIME DEFAULT NULL COMMENT '使用时间',
    used_order_id BIGINT UNSIGNED DEFAULT NULL COMMENT '使用的订单ID',
    expire_time DATETIME NOT NULL COMMENT '过期时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (coupon_id) REFERENCES coupons(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户优惠券表';

CREATE TABLE orders (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    order_no VARCHAR(32) UNIQUE NOT NULL COMMENT '订单号',
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    total_amount DECIMAL(10,2) NOT NULL COMMENT '商品总金额',
    freight_amount DECIMAL(10,2) DEFAULT 0 COMMENT '运费',
    discount_amount DECIMAL(10,2) DEFAULT 0 COMMENT '优惠金额',
    pay_amount DECIMAL(10,2) NOT NULL COMMENT '实付金额',
    pay_type ENUM('wechat', 'alipay', 'balance') DEFAULT NULL COMMENT '支付方式',
    pay_time DATETIME DEFAULT NULL COMMENT '支付时间',
    transaction_id VARCHAR(64) DEFAULT NULL COMMENT '第三方支付流水号',
    receiver_name VARCHAR(50) NOT NULL COMMENT '收货人',
    receiver_phone VARCHAR(20) NOT NULL COMMENT '收货电话',
    receiver_address VARCHAR(255) NOT NULL COMMENT '收货地址',
    status ENUM('pending', 'paid', 'shipped', 'completed', 'cancelled', 'refunding', 'refunded') DEFAULT 'pending' COMMENT '订单状态',
    express_company VARCHAR(50) DEFAULT NULL COMMENT '快递公司',
    express_no VARCHAR(50) DEFAULT NULL COMMENT '快递单号',
    ship_time DATETIME DEFAULT NULL COMMENT '发货时间',
    receive_time DATETIME DEFAULT NULL COMMENT '收货时间',
    remark VARCHAR(500) DEFAULT NULL COMMENT '订单备注',
    is_reviewed TINYINT DEFAULT 0 COMMENT '是否已评价',
    coupon_id BIGINT UNSIGNED DEFAULT NULL COMMENT '使用的优惠券ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_order_no (order_no),
    INDEX idx_status (status),
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

CREATE TABLE order_items (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    order_id BIGINT UNSIGNED NOT NULL COMMENT '订单ID',
    product_id BIGINT UNSIGNED NOT NULL COMMENT '商品ID',
    product_name VARCHAR(100) NOT NULL COMMENT '商品名称（快照）',
    product_image VARCHAR(255) NOT NULL COMMENT '商品图片（快照）',
    price DECIMAL(10,2) NOT NULL COMMENT '单价（快照）',
    quantity INT UNSIGNED NOT NULL COMMENT '数量',
    total_price DECIMAL(10,2) NOT NULL COMMENT '小计',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_order_id (order_id),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单明细表';

CREATE TABLE product_reviews (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    order_id BIGINT UNSIGNED NOT NULL COMMENT '订单ID',
    order_item_id BIGINT UNSIGNED NOT NULL COMMENT '订单明细ID',
    product_id BIGINT UNSIGNED NOT NULL COMMENT '商品ID',
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    rating TINYINT NOT NULL DEFAULT 5 COMMENT '评分(1-5星)',
    content TEXT DEFAULT NULL COMMENT '评价内容',
    images JSON DEFAULT NULL COMMENT '评价图片',
    reply_content TEXT DEFAULT NULL COMMENT '商家回复',
    reply_time DATETIME DEFAULT NULL COMMENT '回复时间',
    is_anonymous TINYINT DEFAULT 0 COMMENT '是否匿名评价',
    status TINYINT DEFAULT 1 COMMENT '状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_product_id (product_id),
    INDEX idx_user_id (user_id),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品评价表';

-- =============================================
-- 7. 社区模块 (6张表)
-- =============================================

CREATE TABLE posts (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    content TEXT NOT NULL COMMENT '动态内容',
    images JSON DEFAULT NULL COMMENT '图片列表',
    related_type ENUM('sport', 'food', 'none') DEFAULT 'none' COMMENT '关联类型',
    related_id BIGINT UNSIGNED DEFAULT NULL COMMENT '关联记录ID',
    tags JSON DEFAULT NULL COMMENT '标签列表',
    like_count INT UNSIGNED DEFAULT 0 COMMENT '点赞数',
    comment_count INT UNSIGNED DEFAULT 0 COMMENT '评论数',
    share_count INT UNSIGNED DEFAULT 0 COMMENT '分享数',
    view_count INT UNSIGNED DEFAULT 0 COMMENT '浏览数',
    status TINYINT DEFAULT 1 COMMENT '状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='社区动态表';

CREATE TABLE comments (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    post_id BIGINT UNSIGNED NOT NULL COMMENT '动态ID',
    user_id BIGINT UNSIGNED NOT NULL COMMENT '评论用户ID',
    content VARCHAR(500) NOT NULL COMMENT '评论内容',
    parent_id BIGINT UNSIGNED DEFAULT NULL COMMENT '父评论ID',
    reply_user_id BIGINT UNSIGNED DEFAULT NULL COMMENT '回复的用户ID',
    like_count INT UNSIGNED DEFAULT 0 COMMENT '点赞数',
    status TINYINT DEFAULT 1 COMMENT '状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_post_id (post_id),
    INDEX idx_user_id (user_id),
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES comments(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='评论表';

CREATE TABLE likes (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    target_type ENUM('post', 'comment') NOT NULL COMMENT '点赞类型',
    target_id BIGINT UNSIGNED NOT NULL COMMENT '目标ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_target (user_id, target_type, target_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='点赞表';

CREATE TABLE follows (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    follower_id BIGINT UNSIGNED NOT NULL COMMENT '关注者ID',
    following_id BIGINT UNSIGNED NOT NULL COMMENT '被关注者ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_follow (follower_id, following_id),
    INDEX idx_following (following_id),
    FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (following_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='关注关系表';

CREATE TABLE messages (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    conversation_id VARCHAR(64) NOT NULL COMMENT '会话ID',
    sender_id BIGINT UNSIGNED NOT NULL COMMENT '发送者ID',
    receiver_id BIGINT UNSIGNED NOT NULL COMMENT '接收者ID',
    content TEXT NOT NULL COMMENT '消息内容',
    msg_type ENUM('text', 'image', 'emoji') DEFAULT 'text' COMMENT '消息类型',
    is_read TINYINT DEFAULT 0 COMMENT '是否已读',
    read_time DATETIME DEFAULT NULL COMMENT '阅读时间',
    sender_deleted TINYINT DEFAULT 0 COMMENT '发送者是否删除',
    receiver_deleted TINYINT DEFAULT 0 COMMENT '接收者是否删除',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_conversation (conversation_id),
    INDEX idx_sender (sender_id),
    INDEX idx_receiver (receiver_id),
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='私聊消息表';

CREATE TABLE conversations (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    conversation_id VARCHAR(64) UNIQUE NOT NULL COMMENT '会话ID',
    user1_id BIGINT UNSIGNED NOT NULL COMMENT '用户1 ID',
    user2_id BIGINT UNSIGNED NOT NULL COMMENT '用户2 ID',
    last_message TEXT DEFAULT NULL COMMENT '最后一条消息',
    last_message_time DATETIME DEFAULT NULL COMMENT '最后消息时间',
    user1_unread INT UNSIGNED DEFAULT 0 COMMENT '用户1未读数',
    user2_unread INT UNSIGNED DEFAULT 0 COMMENT '用户2未读数',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user1 (user1_id),
    INDEX idx_user2 (user2_id),
    FOREIGN KEY (user1_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (user2_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会话列表表';

-- =============================================
-- 8. 积分与任务模块 (6张表)
-- =============================================

CREATE TABLE points_records (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    points_type ENUM('sport', 'food') NOT NULL COMMENT '积分类型',
    change_amount INT NOT NULL COMMENT '变动数量',
    balance INT UNSIGNED NOT NULL COMMENT '变动后余额',
    source_type ENUM('checkin', 'continuous_bonus', 'task', 'exchange', 'expire', 'admin') NOT NULL COMMENT '来源类型',
    source_id BIGINT UNSIGNED DEFAULT NULL COMMENT '来源ID',
    remark VARCHAR(200) DEFAULT NULL COMMENT '备注',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_points_type (points_type),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='积分记录表';

CREATE TABLE gifts (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '礼品名称',
    image VARCHAR(255) DEFAULT NULL COMMENT '礼品图片',
    description VARCHAR(500) DEFAULT NULL COMMENT '礼品描述',
    sport_coins_required INT UNSIGNED DEFAULT 0 COMMENT '所需运动币',
    food_coins_required INT UNSIGNED DEFAULT 0 COMMENT '所需膳食币',
    stock INT UNSIGNED DEFAULT 0 COMMENT '库存',
    exchange_count INT UNSIGNED DEFAULT 0 COMMENT '已兑换数量',
    sort_order INT DEFAULT 0 COMMENT '排序',
    status TINYINT DEFAULT 1 COMMENT '状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='积分商城礼品表';

CREATE TABLE gift_exchanges (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    gift_id BIGINT UNSIGNED NOT NULL COMMENT '礼品ID',
    sport_coins_used INT UNSIGNED DEFAULT 0 COMMENT '消耗运动币',
    food_coins_used INT UNSIGNED DEFAULT 0 COMMENT '消耗膳食币',
    receiver_name VARCHAR(50) DEFAULT NULL COMMENT '收货人',
    receiver_phone VARCHAR(20) DEFAULT NULL COMMENT '收货电话',
    receiver_address VARCHAR(255) DEFAULT NULL COMMENT '收货地址',
    status ENUM('pending', 'shipped', 'completed') DEFAULT 'pending' COMMENT '状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (gift_id) REFERENCES gifts(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='礼品兑换记录表';

CREATE TABLE daily_tasks (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '任务名称',
    description VARCHAR(500) DEFAULT NULL COMMENT '任务描述',
    task_type ENUM('sport_checkin', 'food_checkin', 'sport_minutes', 'food_record', 'post', 'share') NOT NULL COMMENT '任务类型',
    target_value INT DEFAULT 1 COMMENT '目标值',
    reward_sport_coins INT UNSIGNED DEFAULT 0 COMMENT '奖励运动币',
    reward_food_coins INT UNSIGNED DEFAULT 0 COMMENT '奖励膳食币',
    is_daily TINYINT DEFAULT 1 COMMENT '是否每日任务',
    sort_order INT DEFAULT 0 COMMENT '排序',
    status TINYINT DEFAULT 1 COMMENT '状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='每日任务配置表';

CREATE TABLE user_task_records (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    task_id BIGINT UNSIGNED NOT NULL COMMENT '任务ID',
    task_date DATE NOT NULL COMMENT '任务日期',
    current_value INT DEFAULT 0 COMMENT '当前完成值',
    is_completed TINYINT DEFAULT 0 COMMENT '是否完成',
    is_rewarded TINYINT DEFAULT 0 COMMENT '是否已领取奖励',
    completed_at DATETIME DEFAULT NULL COMMENT '完成时间',
    rewarded_at DATETIME DEFAULT NULL COMMENT '领取奖励时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_task_date (user_id, task_id, task_date),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES daily_tasks(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户任务完成记录表';

CREATE TABLE member_orders (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    order_no VARCHAR(32) UNIQUE NOT NULL COMMENT '订单号',
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    member_type TINYINT NOT NULL COMMENT '会员类型：1月卡 2年卡 3终身',
    amount DECIMAL(10,2) NOT NULL COMMENT '支付金额',
    pay_type ENUM('wechat', 'alipay', 'balance') DEFAULT NULL COMMENT '支付方式',
    pay_time DATETIME DEFAULT NULL COMMENT '支付时间',
    transaction_id VARCHAR(64) DEFAULT NULL COMMENT '第三方支付流水号',
    start_time DATETIME DEFAULT NULL COMMENT '开始时间',
    end_time DATETIME DEFAULT NULL COMMENT '结束时间',
    status ENUM('pending', 'paid', 'cancelled', 'refunded') DEFAULT 'pending' COMMENT '状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会员购买记录表';

-- =============================================
-- 9. 系统管理模块 (5张表)
-- =============================================

CREATE TABLE reminders (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    reminder_type ENUM('sport', 'breakfast', 'lunch', 'dinner', 'water', 'medicine') NOT NULL COMMENT '提醒类型',
    reminder_time TIME NOT NULL COMMENT '提醒时间',
    is_enabled TINYINT DEFAULT 1 COMMENT '是否启用',
    repeat_days VARCHAR(20) DEFAULT '1,2,3,4,5,6,7' COMMENT '重复日期',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='提醒设置表';

CREATE TABLE doctors (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL COMMENT '医生姓名',
    avatar VARCHAR(255) DEFAULT NULL COMMENT '头像',
    title VARCHAR(50) DEFAULT NULL COMMENT '职称',
    hospital VARCHAR(100) DEFAULT NULL COMMENT '医院',
    department VARCHAR(50) DEFAULT NULL COMMENT '科室',
    specialty VARCHAR(200) DEFAULT NULL COMMENT '专长',
    introduction TEXT DEFAULT NULL COMMENT '简介',
    schedule JSON DEFAULT NULL COMMENT '坐诊时间表',
    consultation_fee DECIMAL(10,2) DEFAULT NULL COMMENT '咨询费用',
    sort_order INT DEFAULT 0 COMMENT '排序',
    status TINYINT DEFAULT 1 COMMENT '状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='医生表';

CREATE TABLE articles (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL COMMENT '文章标题',
    cover_image VARCHAR(255) DEFAULT NULL COMMENT '封面图',
    summary VARCHAR(500) DEFAULT NULL COMMENT '摘要',
    content TEXT NOT NULL COMMENT '文章内容',
    author_id BIGINT UNSIGNED DEFAULT NULL COMMENT '作者（医生ID）',
    category VARCHAR(50) DEFAULT NULL COMMENT '分类',
    tags JSON DEFAULT NULL COMMENT '标签',
    view_count INT UNSIGNED DEFAULT 0 COMMENT '阅读数',
    like_count INT UNSIGNED DEFAULT 0 COMMENT '点赞数',
    sort_order INT DEFAULT 0 COMMENT '排序',
    status TINYINT DEFAULT 1 COMMENT '状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    FOREIGN KEY (author_id) REFERENCES doctors(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='健康科普文章表';

CREATE TABLE admins (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL COMMENT '用户名',
    password VARCHAR(255) NOT NULL COMMENT '密码（加密存储）',
    nickname VARCHAR(50) DEFAULT NULL COMMENT '昵称',
    avatar VARCHAR(255) DEFAULT NULL COMMENT '头像',
    role ENUM('super_admin', 'admin', 'operator', 'auditor') DEFAULT 'operator' COMMENT '角色',
    permissions JSON DEFAULT NULL COMMENT '权限列表',
    last_login_time DATETIME DEFAULT NULL COMMENT '最后登录时间',
    last_login_ip VARCHAR(50) DEFAULT NULL COMMENT '最后登录IP',
    status TINYINT DEFAULT 1 COMMENT '状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='管理员表';

CREATE TABLE admin_logs (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    admin_id BIGINT UNSIGNED NOT NULL COMMENT '管理员ID',
    module VARCHAR(50) NOT NULL COMMENT '操作模块',
    action VARCHAR(50) NOT NULL COMMENT '操作动作',
    target_type VARCHAR(50) DEFAULT NULL COMMENT '操作对象类型',
    target_id BIGINT UNSIGNED DEFAULT NULL COMMENT '操作对象ID',
    content TEXT DEFAULT NULL COMMENT '操作内容/备注',
    ip VARCHAR(50) DEFAULT NULL COMMENT 'IP地址',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_admin_id (admin_id),
    INDEX idx_created_at (created_at),
    FOREIGN KEY (admin_id) REFERENCES admins(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='操作日志表';

-- =============================================
-- 初始化完成
-- 共计 35 张表
-- =============================================

