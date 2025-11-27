-- =============================================
-- 社区模块
-- 包含：posts, comments, likes, follows, messages, conversations
-- =============================================

-- 社区动态表
CREATE TABLE posts (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    
    content TEXT NOT NULL COMMENT '动态内容',
    images JSON DEFAULT NULL COMMENT '图片列表',
    
    -- 关联运动/饮食记录
    related_type ENUM('sport', 'food', 'none') DEFAULT 'none' COMMENT '关联类型',
    related_id BIGINT UNSIGNED DEFAULT NULL COMMENT '关联记录ID',
    
    -- 标签
    tags JSON DEFAULT NULL COMMENT '标签列表',
    
    -- 统计
    like_count INT UNSIGNED DEFAULT 0 COMMENT '点赞数',
    comment_count INT UNSIGNED DEFAULT 0 COMMENT '评论数',
    share_count INT UNSIGNED DEFAULT 0 COMMENT '分享数',
    view_count INT UNSIGNED DEFAULT 0 COMMENT '浏览数',
    
    -- 状态
    status TINYINT DEFAULT 1 COMMENT '状态：0删除 1正常 2审核中',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    INDEX idx_status (status),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='社区动态表';

-- 评论表
CREATE TABLE comments (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    post_id BIGINT UNSIGNED NOT NULL COMMENT '动态ID',
    user_id BIGINT UNSIGNED NOT NULL COMMENT '评论用户ID',
    
    content VARCHAR(500) NOT NULL COMMENT '评论内容',
    
    -- 回复
    parent_id BIGINT UNSIGNED DEFAULT NULL COMMENT '父评论ID',
    reply_user_id BIGINT UNSIGNED DEFAULT NULL COMMENT '回复的用户ID',
    
    like_count INT UNSIGNED DEFAULT 0 COMMENT '点赞数',
    status TINYINT DEFAULT 1 COMMENT '状态：0删除 1正常',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_post_id (post_id),
    INDEX idx_user_id (user_id),
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES comments(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='评论表';

-- 点赞表
CREATE TABLE likes (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    
    target_type ENUM('post', 'comment') NOT NULL COMMENT '点赞类型',
    target_id BIGINT UNSIGNED NOT NULL COMMENT '目标ID',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_user_target (user_id, target_type, target_id),
    INDEX idx_target (target_type, target_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='点赞表';

-- 关注关系表
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

-- 私聊消息表
CREATE TABLE messages (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    conversation_id VARCHAR(64) NOT NULL COMMENT '会话ID（由双方用户ID生成）',
    sender_id BIGINT UNSIGNED NOT NULL COMMENT '发送者ID',
    receiver_id BIGINT UNSIGNED NOT NULL COMMENT '接收者ID',
    
    content TEXT NOT NULL COMMENT '消息内容',
    msg_type ENUM('text', 'image', 'emoji') DEFAULT 'text' COMMENT '消息类型',
    
    is_read TINYINT DEFAULT 0 COMMENT '是否已读：0未读 1已读',
    read_time DATETIME DEFAULT NULL COMMENT '阅读时间',
    
    -- 软删除
    sender_deleted TINYINT DEFAULT 0 COMMENT '发送者是否删除',
    receiver_deleted TINYINT DEFAULT 0 COMMENT '接收者是否删除',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_conversation (conversation_id),
    INDEX idx_sender (sender_id),
    INDEX idx_receiver (receiver_id),
    INDEX idx_created_at (created_at),
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='私聊消息表';

-- 会话列表表
CREATE TABLE conversations (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    conversation_id VARCHAR(64) UNIQUE NOT NULL COMMENT '会话ID',
    user1_id BIGINT UNSIGNED NOT NULL COMMENT '用户1 ID（较小的ID）',
    user2_id BIGINT UNSIGNED NOT NULL COMMENT '用户2 ID（较大的ID）',
    
    last_message TEXT DEFAULT NULL COMMENT '最后一条消息',
    last_message_time DATETIME DEFAULT NULL COMMENT '最后消息时间',
    
    user1_unread INT UNSIGNED DEFAULT 0 COMMENT '用户1未读数',
    user2_unread INT UNSIGNED DEFAULT 0 COMMENT '用户2未读数',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_user1 (user1_id),
    INDEX idx_user2 (user2_id),
    INDEX idx_last_time (last_message_time),
    FOREIGN KEY (user1_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (user2_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会话列表表';

