-- =============================================
-- 课程模块
-- 包含：courses, user_course_collects
-- =============================================

-- 课程表
CREATE TABLE courses (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL COMMENT '课程标题',
    cover_image VARCHAR(255) DEFAULT NULL COMMENT '封面图',
    description TEXT DEFAULT NULL COMMENT '课程描述',
    
    course_type ENUM('sport', 'food') NOT NULL COMMENT '课程类型：运动/饮食',
    category VARCHAR(50) DEFAULT NULL COMMENT '分类（如：减脂、增肌、康复）',
    difficulty ENUM('easy', 'medium', 'hard') DEFAULT 'medium' COMMENT '难度',
    duration INT DEFAULT NULL COMMENT '时长(分钟)',
    
    -- 课程内容
    video_url VARCHAR(500) DEFAULT NULL COMMENT '视频链接',
    content TEXT DEFAULT NULL COMMENT '图文内容',
    steps JSON DEFAULT NULL COMMENT '步骤详情',
    
    -- 适用人群
    suitable_for JSON DEFAULT NULL COMMENT '适用人群标签',
    calories INT DEFAULT NULL COMMENT '预计消耗卡路里（运动课程）',
    
    -- 统计
    view_count INT UNSIGNED DEFAULT 0 COMMENT '观看数',
    like_count INT UNSIGNED DEFAULT 0 COMMENT '点赞数',
    collect_count INT UNSIGNED DEFAULT 0 COMMENT '收藏数',
    
    -- 权限
    is_member_only TINYINT DEFAULT 0 COMMENT '是否仅会员可看',
    
    sort_order INT DEFAULT 0 COMMENT '排序',
    status TINYINT DEFAULT 1 COMMENT '状态：0下架 1上架',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_course_type (course_type),
    INDEX idx_category (category),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='课程表';

-- 用户课程收藏表
CREATE TABLE user_course_collects (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    course_id BIGINT UNSIGNED NOT NULL COMMENT '课程ID',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_user_course (user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户课程收藏表';

