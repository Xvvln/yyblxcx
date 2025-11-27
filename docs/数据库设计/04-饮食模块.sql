-- =============================================
-- 饮食模块
-- 包含：food_records, food_checkins
-- =============================================

-- 饮食记录表
CREATE TABLE food_records (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    
    -- 餐次
    meal_type ENUM('breakfast', 'lunch', 'dinner', 'snack') NOT NULL COMMENT '餐次',
    meal_time DATETIME NOT NULL COMMENT '用餐时间',
    
    -- 食物信息
    food_name VARCHAR(100) DEFAULT NULL COMMENT '食物名称',
    food_image VARCHAR(255) DEFAULT NULL COMMENT '食物照片',
    
    -- 营养分析（AI识别或手动输入）
    calories INT DEFAULT NULL COMMENT '卡路里',
    protein DECIMAL(6,2) DEFAULT NULL COMMENT '蛋白质(g)',
    carbohydrate DECIMAL(6,2) DEFAULT NULL COMMENT '碳水化合物(g)',
    fat DECIMAL(6,2) DEFAULT NULL COMMENT '脂肪(g)',
    fiber DECIMAL(6,2) DEFAULT NULL COMMENT '膳食纤维(g)',
    
    -- AI分析
    ai_analysis TEXT DEFAULT NULL COMMENT 'AI营养分析',
    nutrition_score INT DEFAULT NULL COMMENT '营养评分(0-100)',
    
    -- 备注
    remark TEXT DEFAULT NULL COMMENT '备注',
    
    -- 获得的积分
    earned_coins INT DEFAULT 0 COMMENT '获得的膳食币',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    INDEX idx_meal_time (meal_time),
    INDEX idx_meal_type (meal_type),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='饮食记录表';

-- 饮食打卡表
CREATE TABLE food_checkins (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    checkin_date DATE NOT NULL COMMENT '打卡日期',
    
    -- 各餐打卡状态
    breakfast_done TINYINT DEFAULT 0 COMMENT '早餐已记录',
    lunch_done TINYINT DEFAULT 0 COMMENT '午餐已记录',
    dinner_done TINYINT DEFAULT 0 COMMENT '晚餐已记录',
    
    earned_coins INT DEFAULT 0 COMMENT '获得的膳食币',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_user_date (user_id, checkin_date),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='饮食打卡表';

