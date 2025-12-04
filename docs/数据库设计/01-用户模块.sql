-- =============================================
-- 用户模块
-- 包含：users, user_health_profiles, user_addresses
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
    
    -- 身体基础数据
    height DECIMAL(5,2) DEFAULT NULL COMMENT '身高(cm)',
    weight DECIMAL(5,2) DEFAULT NULL COMMENT '体重(kg)',
    
    -- 会员信息
    member_level TINYINT DEFAULT 0 COMMENT '会员等级：0普通 1月卡 2年卡 3终身',
    member_expire_time DATETIME DEFAULT NULL COMMENT '会员到期时间',
    
    -- 积分与余额
    sport_coins INT UNSIGNED DEFAULT 0 COMMENT '运动币',
    food_coins INT UNSIGNED DEFAULT 0 COMMENT '膳食币',
    balance DECIMAL(10,2) DEFAULT 0 COMMENT '账户余额（用于余额支付）',
    user_level TINYINT DEFAULT 1 COMMENT '用户等级 1-10',
    
    -- 社交统计
    follower_count INT UNSIGNED DEFAULT 0 COMMENT '粉丝数',
    following_count INT UNSIGNED DEFAULT 0 COMMENT '关注数',
    
    -- 连续打卡
    continuous_checkin_days INT UNSIGNED DEFAULT 0 COMMENT '连续打卡天数',
    last_checkin_date DATE DEFAULT NULL COMMENT '最后打卡日期',
    
    -- 状态
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
    
    -- 健康目标
    health_goal VARCHAR(50) DEFAULT NULL COMMENT '健康目标：减脂/增肌/保持健康/康复训练',
    target_weight DECIMAL(5,2) DEFAULT NULL COMMENT '目标体重',
    
    -- 运动偏好
    preferred_sports JSON DEFAULT NULL COMMENT '偏好运动类型',
    daily_exercise_minutes INT DEFAULT 30 COMMENT '每日期望运动时长(分钟)',
    
    -- 身体状况
    has_injury TINYINT DEFAULT 0 COMMENT '是否有伤病',
    injury_description TEXT DEFAULT NULL COMMENT '伤病描述',
    chronic_diseases JSON DEFAULT NULL COMMENT '慢性病',
    
    -- 体能测试
    pushup_count INT DEFAULT NULL COMMENT '俯卧撑数量',
    squat_count INT DEFAULT NULL COMMENT '深蹲数量',
    crunch_count INT DEFAULT NULL COMMENT '卷腹数量',
    climb_stairs_tired TINYINT DEFAULT NULL COMMENT '爬5层楼是否疲劳：0否 1是',
    
    -- 饮食习惯
    diet_habit VARCHAR(50) DEFAULT NULL COMMENT '饮食习惯：正常/素食/低碳/生酮',
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

-- 用户设置表
CREATE TABLE user_settings (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    
    -- 隐私设置
    share_health_data TINYINT DEFAULT 0 COMMENT '向医生展示健康数据：0否 1是',
    public_profile TINYINT DEFAULT 1 COMMENT '允许陌生人查看动态：0否 1是',
    personalized TINYINT DEFAULT 1 COMMENT '个性化推荐：0否 1是',
    
    -- 通用设置
    elderly_mode TINYINT DEFAULT 0 COMMENT '长辈模式：0否 1是',
    notification_enabled TINYINT DEFAULT 1 COMMENT '消息通知：0否 1是',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_user_id (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户设置表';

-- 用户反馈表
CREATE TABLE user_feedbacks (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    
    content TEXT NOT NULL COMMENT '反馈内容',
    images JSON DEFAULT NULL COMMENT '反馈图片',
    contact VARCHAR(100) DEFAULT NULL COMMENT '联系方式',
    
    status TINYINT DEFAULT 0 COMMENT '状态：0待处理 1已处理 2已回复',
    reply TEXT DEFAULT NULL COMMENT '回复内容',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户反馈表';

