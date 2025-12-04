-- =============================================
-- 迁移脚本：添加用户设置和反馈表
-- 执行方式：mysql -u root -p health_db < migrate_add_settings_feedback.sql
-- =============================================

USE health_db;

-- 用户设置表
CREATE TABLE IF NOT EXISTS user_settings (
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
CREATE TABLE IF NOT EXISTS user_feedbacks (
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

-- 给 users 表添加 total_checkin_days 字段（如果不存在）
ALTER TABLE users ADD COLUMN IF NOT EXISTS total_checkin_days INT UNSIGNED DEFAULT 0 COMMENT '累计签到天数' AFTER continuous_checkin_days;

SELECT '迁移完成！已创建 user_settings 和 user_feedbacks 表' AS message;

