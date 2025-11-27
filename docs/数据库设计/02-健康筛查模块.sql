-- =============================================
-- 健康筛查模块
-- 包含：health_screenings
-- =============================================

CREATE TABLE health_screenings (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    
    -- 基础体征
    height DECIMAL(5,2) DEFAULT NULL COMMENT '身高(cm)',
    weight DECIMAL(5,2) DEFAULT NULL COMMENT '体重(kg)',
    bmi DECIMAL(4,2) DEFAULT NULL COMMENT 'BMI指数',
    heart_rate INT DEFAULT NULL COMMENT '心率(次/分)',
    blood_pressure_high INT DEFAULT NULL COMMENT '收缩压',
    blood_pressure_low INT DEFAULT NULL COMMENT '舒张压',
    body_temperature DECIMAL(3,1) DEFAULT NULL COMMENT '体温',
    blood_sugar DECIMAL(4,2) DEFAULT NULL COMMENT '血糖',
    
    -- 上传的图片
    face_image VARCHAR(255) DEFAULT NULL COMMENT '面部照片',
    body_image VARCHAR(255) DEFAULT NULL COMMENT '体态照片',
    
    -- 问卷数据
    questionnaire_data JSON DEFAULT NULL COMMENT '问卷答案JSON',
    
    -- AI分析结果
    risk_level ENUM('low', 'medium', 'high') DEFAULT 'low' COMMENT '风险等级',
    risk_tags JSON DEFAULT NULL COMMENT '风险标签',
    ai_suggestion TEXT DEFAULT NULL COMMENT 'AI生成的健康建议',
    diet_suggestion TEXT DEFAULT NULL COMMENT '膳食建议',
    exercise_suggestion TEXT DEFAULT NULL COMMENT '运动建议',
    lifestyle_suggestion TEXT DEFAULT NULL COMMENT '生活方式建议',
    
    -- 推荐商品
    recommended_products JSON DEFAULT NULL COMMENT '推荐商品ID列表',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    INDEX idx_risk_level (risk_level),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='健康筛查记录表';

