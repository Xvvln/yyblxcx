-- =============================================
-- 商城模块
-- 包含：product_categories, products, carts, orders, order_items, 
--       product_reviews, coupons, user_coupons
-- =============================================

-- 商品分类表
CREATE TABLE product_categories (
    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL COMMENT '分类名称',
    icon VARCHAR(255) DEFAULT NULL COMMENT '分类图标',
    sort_order INT DEFAULT 0 COMMENT '排序',
    status TINYINT DEFAULT 1 COMMENT '状态：0禁用 1启用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品分类表';

-- 商品表
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
    
    -- 商品详情
    description TEXT DEFAULT NULL COMMENT '商品描述',
    detail TEXT DEFAULT NULL COMMENT '商品详情(富文本)',
    
    -- 营养/适用信息
    nutrition_label JSON DEFAULT NULL COMMENT '营养标签',
    suitable_for JSON DEFAULT NULL COMMENT '适用人群',
    
    -- AI推荐标签
    ai_tags JSON DEFAULT NULL COMMENT 'AI推荐标签（如：增肌、减脂、补铁）',
    
    sort_order INT DEFAULT 0 COMMENT '排序',
    status TINYINT DEFAULT 1 COMMENT '状态：0下架 1上架',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_category_id (category_id),
    INDEX idx_status (status),
    INDEX idx_sales (sales),
    FOREIGN KEY (category_id) REFERENCES product_categories(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品表';

-- 购物车表
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

-- 优惠券模板表
CREATE TABLE coupons (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '优惠券名称',
    type ENUM('amount', 'percent') NOT NULL COMMENT '类型：amount满减 percent折扣',
    
    -- 优惠内容
    discount_amount DECIMAL(10,2) DEFAULT NULL COMMENT '减免金额（满减券）',
    discount_percent DECIMAL(4,2) DEFAULT NULL COMMENT '折扣比例（折扣券，如0.8表示8折）',
    min_amount DECIMAL(10,2) DEFAULT 0 COMMENT '最低消费金额',
    max_discount DECIMAL(10,2) DEFAULT NULL COMMENT '最高优惠金额（折扣券用）',
    
    -- 有效期
    start_time DATETIME NOT NULL COMMENT '开始时间',
    end_time DATETIME NOT NULL COMMENT '结束时间',
    
    -- 发放规则
    total_count INT UNSIGNED DEFAULT 0 COMMENT '发放总量（0表示不限）',
    received_count INT UNSIGNED DEFAULT 0 COMMENT '已领取数量',
    per_user_limit INT UNSIGNED DEFAULT 1 COMMENT '每人限领数量',
    
    -- 使用范围
    applicable_products JSON DEFAULT NULL COMMENT '适用商品ID（null表示全场通用）',
    applicable_categories JSON DEFAULT NULL COMMENT '适用分类ID',
    
    status TINYINT DEFAULT 1 COMMENT '状态：0禁用 1启用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='优惠券模板表';

-- 用户优惠券表
CREATE TABLE user_coupons (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    coupon_id BIGINT UNSIGNED NOT NULL COMMENT '优惠券ID',
    
    -- 来源
    source_type ENUM('receive', 'points_exchange', 'system', 'activity') NOT NULL COMMENT '来源类型',
    source_id BIGINT UNSIGNED DEFAULT NULL COMMENT '来源ID',
    
    -- 状态
    status ENUM('unused', 'used', 'expired') DEFAULT 'unused' COMMENT '状态',
    used_time DATETIME DEFAULT NULL COMMENT '使用时间',
    used_order_id BIGINT UNSIGNED DEFAULT NULL COMMENT '使用的订单ID',
    
    expire_time DATETIME NOT NULL COMMENT '过期时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_expire_time (expire_time),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (coupon_id) REFERENCES coupons(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户优惠券表';

-- 订单表
CREATE TABLE orders (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    order_no VARCHAR(32) UNIQUE NOT NULL COMMENT '订单号',
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    
    -- 金额
    total_amount DECIMAL(10,2) NOT NULL COMMENT '商品总金额',
    freight_amount DECIMAL(10,2) DEFAULT 0 COMMENT '运费',
    discount_amount DECIMAL(10,2) DEFAULT 0 COMMENT '优惠金额',
    pay_amount DECIMAL(10,2) NOT NULL COMMENT '实付金额',
    
    -- 支付信息
    pay_type ENUM('wechat', 'alipay', 'balance') DEFAULT NULL COMMENT '支付方式',
    pay_time DATETIME DEFAULT NULL COMMENT '支付时间',
    transaction_id VARCHAR(64) DEFAULT NULL COMMENT '第三方支付流水号',
    
    -- 收货信息
    receiver_name VARCHAR(50) NOT NULL COMMENT '收货人',
    receiver_phone VARCHAR(20) NOT NULL COMMENT '收货电话',
    receiver_address VARCHAR(255) NOT NULL COMMENT '收货地址',
    
    -- 订单状态
    status ENUM('pending', 'paid', 'shipped', 'completed', 'cancelled', 'refunding', 'refunded') 
        DEFAULT 'pending' COMMENT '订单状态',
    
    -- 物流信息
    express_company VARCHAR(50) DEFAULT NULL COMMENT '快递公司',
    express_no VARCHAR(50) DEFAULT NULL COMMENT '快递单号',
    ship_time DATETIME DEFAULT NULL COMMENT '发货时间',
    receive_time DATETIME DEFAULT NULL COMMENT '收货时间',
    
    -- 备注
    remark VARCHAR(500) DEFAULT NULL COMMENT '订单备注',
    
    -- 评价状态
    is_reviewed TINYINT DEFAULT 0 COMMENT '是否已评价：0未评价 1已评价',
    
    -- 使用的优惠券
    coupon_id BIGINT UNSIGNED DEFAULT NULL COMMENT '使用的优惠券ID',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    INDEX idx_order_no (order_no),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

-- 订单明细表
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

-- 商品评价表
CREATE TABLE product_reviews (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    order_id BIGINT UNSIGNED NOT NULL COMMENT '订单ID',
    order_item_id BIGINT UNSIGNED NOT NULL COMMENT '订单明细ID',
    product_id BIGINT UNSIGNED NOT NULL COMMENT '商品ID',
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    
    rating TINYINT NOT NULL DEFAULT 5 COMMENT '评分(1-5星)',
    content TEXT DEFAULT NULL COMMENT '评价内容',
    images JSON DEFAULT NULL COMMENT '评价图片',
    
    -- 商家回复
    reply_content TEXT DEFAULT NULL COMMENT '商家回复',
    reply_time DATETIME DEFAULT NULL COMMENT '回复时间',
    
    is_anonymous TINYINT DEFAULT 0 COMMENT '是否匿名评价',
    status TINYINT DEFAULT 1 COMMENT '状态：0隐藏 1显示',
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_product_id (product_id),
    INDEX idx_user_id (user_id),
    INDEX idx_order_id (order_id),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品评价表';

