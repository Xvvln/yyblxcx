-- =============================================
-- 运动模块
-- 包含：sport_records, sport_checkins
-- =============================================

-- 运动记录表
CREATE TABLE sport_records (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    
    -- 运动类型
    sport_type ENUM('running', 'walking', 'cycling', 'rope_skipping', 'swimming', 'fitness', 'other') 
        NOT NULL COMMENT '运动类型',
    sport_name VARCHAR(50) DEFAULT NULL COMMENT '运动名称',
    
    -- 运动数据
    duration INT NOT NULL DEFAULT 0 COMMENT '运动时长(秒)',
    distance DECIMAL(10,2) DEFAULT NULL COMMENT '距离(米)',
    calories INT DEFAULT NULL COMMENT '消耗卡路里',
    steps INT DEFAULT NULL COMMENT '步数',
    avg_pace VARCHAR(20) DEFAULT NULL COMMENT '平均配速',
    avg_heart_rate INT DEFAULT NULL COMMENT '平均心率',
    
    -- GPS轨迹
    gps_track JSON DEFAULT NULL COMMENT 'GPS轨迹点',
    track_image VARCHAR(255) DEFAULT NULL COMMENT '轨迹截图',
    
    -- 运动照片
    images JSON DEFAULT NULL COMMENT '运动照片列表',
    
    -- 备注
    remark TEXT DEFAULT NULL COMMENT '运动备注',
    
    -- 获得的积分
    earned_coins INT DEFAULT 0 COMMENT '获得的运动币',
    
    start_time DATETIME NOT NULL COMMENT '开始时间',
    end_time DATETIME DEFAULT NULL COMMENT '结束时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    INDEX idx_sport_type (sport_type),
    INDEX idx_start_time (start_time),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='运动记录表';

-- 运动打卡表
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

