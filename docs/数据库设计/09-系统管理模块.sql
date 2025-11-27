-- =============================================
-- 系统管理模块
-- 包含：reminders, doctors, articles, admins, admin_logs
-- =============================================

-- 提醒设置表
CREATE TABLE reminders (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    
    reminder_type ENUM('sport', 'breakfast', 'lunch', 'dinner', 'water', 'medicine') 
        NOT NULL COMMENT '提醒类型',
    reminder_time TIME NOT NULL COMMENT '提醒时间',
    is_enabled TINYINT DEFAULT 1 COMMENT '是否启用',
    
    repeat_days VARCHAR(20) DEFAULT '1,2,3,4,5,6,7' COMMENT '重复日期（1-7代表周一到周日）',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='提醒设置表';

-- 医生表
CREATE TABLE doctors (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL COMMENT '医生姓名',
    avatar VARCHAR(255) DEFAULT NULL COMMENT '头像',
    title VARCHAR(50) DEFAULT NULL COMMENT '职称',
    hospital VARCHAR(100) DEFAULT NULL COMMENT '医院',
    department VARCHAR(50) DEFAULT NULL COMMENT '科室',
    specialty VARCHAR(200) DEFAULT NULL COMMENT '专长',
    introduction TEXT DEFAULT NULL COMMENT '简介',
    
    -- 坐诊信息
    schedule JSON DEFAULT NULL COMMENT '坐诊时间表',
    consultation_fee DECIMAL(10,2) DEFAULT NULL COMMENT '咨询费用',
    
    sort_order INT DEFAULT 0 COMMENT '排序',
    status TINYINT DEFAULT 1 COMMENT '状态：0禁用 1启用',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='医生表';

-- 健康科普文章表
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
    status TINYINT DEFAULT 1 COMMENT '状态：0下架 1上架',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_category (category),
    INDEX idx_status (status),
    FOREIGN KEY (author_id) REFERENCES doctors(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='健康科普文章表';

-- 管理员表
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
    
    status TINYINT DEFAULT 1 COMMENT '状态：0禁用 1正常',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='管理员表';

-- 操作日志表
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

