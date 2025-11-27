-- =============================================
-- 积分与任务模块
-- 包含：points_records, gifts, gift_exchanges, daily_tasks, 
--       user_task_records, member_orders
-- =============================================

-- 积分记录表
CREATE TABLE points_records (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    
    points_type ENUM('sport', 'food') NOT NULL COMMENT '积分类型：运动币/膳食币',
    change_amount INT NOT NULL COMMENT '变动数量（正负）',
    balance INT UNSIGNED NOT NULL COMMENT '变动后余额',
    
    -- 来源
    source_type ENUM('checkin', 'continuous_bonus', 'task', 'exchange', 'expire', 'admin') 
        NOT NULL COMMENT '来源类型',
    source_id BIGINT UNSIGNED DEFAULT NULL COMMENT '来源ID',
    
    remark VARCHAR(200) DEFAULT NULL COMMENT '备注',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    INDEX idx_points_type (points_type),
    INDEX idx_created_at (created_at),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='积分记录表';

-- 积分商城礼品表
CREATE TABLE gifts (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '礼品名称',
    image VARCHAR(255) DEFAULT NULL COMMENT '礼品图片',
    description VARCHAR(500) DEFAULT NULL COMMENT '礼品描述',
    
    -- 兑换所需积分
    sport_coins_required INT UNSIGNED DEFAULT 0 COMMENT '所需运动币',
    food_coins_required INT UNSIGNED DEFAULT 0 COMMENT '所需膳食币',
    
    stock INT UNSIGNED DEFAULT 0 COMMENT '库存',
    exchange_count INT UNSIGNED DEFAULT 0 COMMENT '已兑换数量',
    
    sort_order INT DEFAULT 0 COMMENT '排序',
    status TINYINT DEFAULT 1 COMMENT '状态：0下架 1上架',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='积分商城礼品表';

-- 礼品兑换记录表
CREATE TABLE gift_exchanges (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    gift_id BIGINT UNSIGNED NOT NULL COMMENT '礼品ID',
    
    sport_coins_used INT UNSIGNED DEFAULT 0 COMMENT '消耗运动币',
    food_coins_used INT UNSIGNED DEFAULT 0 COMMENT '消耗膳食币',
    
    -- 收货信息
    receiver_name VARCHAR(50) DEFAULT NULL COMMENT '收货人',
    receiver_phone VARCHAR(20) DEFAULT NULL COMMENT '收货电话',
    receiver_address VARCHAR(255) DEFAULT NULL COMMENT '收货地址',
    
    status ENUM('pending', 'shipped', 'completed') DEFAULT 'pending' COMMENT '状态',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (gift_id) REFERENCES gifts(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='礼品兑换记录表';

-- 每日任务配置表
CREATE TABLE daily_tasks (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '任务名称',
    description VARCHAR(500) DEFAULT NULL COMMENT '任务描述',
    
    task_type ENUM('sport_checkin', 'food_checkin', 'sport_minutes', 'food_record', 'post', 'share') 
        NOT NULL COMMENT '任务类型',
    target_value INT DEFAULT 1 COMMENT '目标值（如运动30分钟，target_value=30）',
    
    -- 奖励
    reward_sport_coins INT UNSIGNED DEFAULT 0 COMMENT '奖励运动币',
    reward_food_coins INT UNSIGNED DEFAULT 0 COMMENT '奖励膳食币',
    
    -- 任务周期
    is_daily TINYINT DEFAULT 1 COMMENT '是否每日任务',
    
    sort_order INT DEFAULT 0 COMMENT '排序',
    status TINYINT DEFAULT 1 COMMENT '状态：0禁用 1启用',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='每日任务配置表';

-- 用户任务完成记录表
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
    INDEX idx_task_date (task_date),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES daily_tasks(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户任务完成记录表';

-- 会员购买记录表
CREATE TABLE member_orders (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    order_no VARCHAR(32) UNIQUE NOT NULL COMMENT '订单号',
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    
    member_type TINYINT NOT NULL COMMENT '会员类型：1月卡 2年卡 3终身',
    amount DECIMAL(10,2) NOT NULL COMMENT '支付金额',
    
    -- 支付信息
    pay_type ENUM('wechat', 'alipay', 'balance') DEFAULT NULL COMMENT '支付方式',
    pay_time DATETIME DEFAULT NULL COMMENT '支付时间',
    transaction_id VARCHAR(64) DEFAULT NULL COMMENT '第三方支付流水号',
    
    -- 会员有效期
    start_time DATETIME DEFAULT NULL COMMENT '开始时间',
    end_time DATETIME DEFAULT NULL COMMENT '结束时间（终身卡为NULL）',
    
    status ENUM('pending', 'paid', 'cancelled', 'refunded') DEFAULT 'pending' COMMENT '状态',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会员购买记录表';

