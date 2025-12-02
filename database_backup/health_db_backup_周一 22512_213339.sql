-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: health_db
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin_logs`
--

DROP TABLE IF EXISTS `admin_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin_logs` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `admin_id` bigint unsigned NOT NULL COMMENT '管理员ID',
  `action` varchar(100) NOT NULL COMMENT '操作类型',
  `target_type` varchar(50) DEFAULT NULL COMMENT '操作对象类型',
  `target_id` bigint unsigned DEFAULT NULL COMMENT '操作对象ID',
  `content` text COMMENT '操作内容',
  `ip` varchar(50) DEFAULT NULL COMMENT 'IP地址',
  `user_agent` varchar(255) DEFAULT NULL COMMENT 'User Agent',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_admin_id` (`admin_id`),
  KEY `idx_action` (`action`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `admin_logs_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admins` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='管理员操作日志表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_logs`
--

LOCK TABLES `admin_logs` WRITE;
/*!40000 ALTER TABLE `admin_logs` DISABLE KEYS */;
INSERT INTO `admin_logs` VALUES (1,1,'login','admin',1,'管理员登录系统','192.168.1.100','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0','2025-11-27 11:49:54'),(2,1,'create','product',1,'创建商品：乳清蛋白粉','192.168.1.100','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0','2025-11-27 11:49:54'),(3,1,'update','product',2,'更新商品价格：维生素D3','192.168.1.100','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0','2025-11-27 11:49:54'),(4,1,'create','coupon',1,'创建优惠券：新人专享','192.168.1.100','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0','2025-11-27 11:49:54'),(5,2,'login','admin',2,'管理员登录系统','192.168.1.101','Mozilla/5.0 (Macintosh; Intel Mac OS X) Chrome/119.0','2025-11-27 11:49:54'),(6,2,'review','post',3,'审核通过帖子','192.168.1.101','Mozilla/5.0 (Macintosh; Intel Mac OS X) Chrome/119.0','2025-11-27 11:49:54'),(7,1,'delete','post_comment',5,'删除违规评论','192.168.1.100','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0','2025-11-27 11:49:54'),(8,1,'update','user',4,'修改用户会员等级','192.168.1.100','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0','2025-11-27 11:49:54'),(9,1,'create','banner',1,'创建首页轮播图','192.168.1.100','Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0','2025-11-27 11:49:54'),(10,2,'update','system_config',1,'更新系统配置','192.168.1.101','Mozilla/5.0 (Macintosh; Intel Mac OS X) Chrome/119.0','2025-11-27 11:49:54'),(11,1,'export','order',NULL,'导出订单数据','192.168.1.100','Mozilla/5.0 Chrome/119.0','2025-11-27 12:03:12'),(12,1,'update','banner',1,'更新首页轮播图','192.168.1.100','Mozilla/5.0 Chrome/119.0','2025-11-27 12:03:12'),(13,2,'create','coupon',7,'创建满200减30优惠券','192.168.1.101','Mozilla/5.0 Chrome/119.0','2025-11-27 12:03:12'),(14,1,'update','product',13,'更新商品库存','192.168.1.100','Mozilla/5.0 Chrome/119.0','2025-11-27 12:03:12'),(15,2,'delete','post',5,'删除违规帖子','192.168.1.101','Mozilla/5.0 Chrome/119.0','2025-11-27 12:03:12'),(16,1,'update','user',3,'修改用户信息','192.168.1.100','Mozilla/5.0 Chrome/119.0','2025-11-27 12:03:12'),(17,1,'create','course',11,'创建新课程：全身燃脂20分钟','192.168.1.100','Mozilla/5.0 Chrome/119.0','2025-11-27 12:03:12'),(18,2,'update','system_config',NULL,'更新系统配置','192.168.1.101','Mozilla/5.0 Chrome/119.0','2025-11-27 12:03:12'),(19,1,'export','user',NULL,'导出用户数据','192.168.1.100','Mozilla/5.0 Chrome/119.0','2025-11-27 12:03:12'),(20,1,'logout','admin',1,'管理员退出登录','192.168.1.100','Mozilla/5.0 Chrome/119.0','2025-11-27 12:03:12'),(21,1,'login','admin',1,'管理员登录','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0','2025-11-27 15:47:08');
/*!40000 ALTER TABLE `admin_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `password` varchar(255) NOT NULL COMMENT '密码(加密)',
  `nickname` varchar(50) DEFAULT NULL COMMENT '昵称',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像',
  `role` enum('super_admin','admin','operator') DEFAULT 'operator' COMMENT '角色',
  `permissions` json DEFAULT NULL COMMENT '权限列表',
  `last_login_time` datetime DEFAULT NULL COMMENT '最后登录时间',
  `last_login_ip` varchar(50) DEFAULT NULL COMMENT '最后登录IP',
  `status` tinyint DEFAULT '1' COMMENT '状态：0禁用 1正常',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `idx_username` (`username`),
  KEY `idx_role` (`role`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='管理员表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES (1,'admin','$2b$12$gXoEWoNUyZjuJz5Na8txROIkHnocC.AKXWdUUnGCnvWDAqT9n7iKS','超级管理员',NULL,'super_admin',NULL,'2025-11-27 15:47:08',NULL,1,'2025-11-27 11:46:10','2025-11-27 15:47:08'),(2,'manager','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.K7HdB8aQGjH3Hy','运营管理员',NULL,'admin',NULL,NULL,NULL,1,'2025-11-27 11:46:10','2025-11-27 11:46:10');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ai_chat_records`
--

DROP TABLE IF EXISTS `ai_chat_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ai_chat_records` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `session_id` varchar(50) NOT NULL COMMENT '会话ID',
  `role` enum('user','assistant') NOT NULL COMMENT '角色',
  `content` text NOT NULL COMMENT '内容',
  `tokens_used` int DEFAULT '0' COMMENT 'token消耗',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_session_id` (`session_id`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `ai_chat_records_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='AI对话记录表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ai_chat_records`
--

LOCK TABLES `ai_chat_records` WRITE;
/*!40000 ALTER TABLE `ai_chat_records` DISABLE KEYS */;
INSERT INTO `ai_chat_records` VALUES (1,1,'session_001','user','我想减肥，应该怎么吃？',0,'2024-11-25 10:00:00'),(2,1,'session_001','assistant','减肥饮食建议：1. 控制总热量摄入，每天减少300-500大卡；2. 增加蛋白质摄入，每餐保证有优质蛋白；3. 减少精制碳水，选择全谷物；4. 多吃蔬菜，增加饱腹感；5. 避免含糖饮料和零食。',0,'2024-11-25 10:00:05'),(3,1,'session_001','user','有什么推荐的早餐吗？',0,'2024-11-25 10:01:00'),(4,1,'session_001','assistant','推荐健康早餐：1. 全麦面包+鸡蛋+牛奶；2. 燕麦粥+坚果+水果；3. 鸡胸肉沙拉+全麦吐司；4. 豆浆+杂粮包+蔬菜。热量控制在300-400大卡左右。',0,'2024-11-25 10:01:05'),(5,2,'session_002','user','瑜伽适合什么时间练？',0,'2024-11-24 08:00:00'),(6,2,'session_002','assistant','瑜伽最佳练习时间：1. 早晨6-8点，唤醒身体，提升精气神；2. 傍晚5-7点，缓解一天疲劳；3. 睡前9-10点，放松身心助眠。建议空腹或饭后2小时练习。',0,'2024-11-24 08:00:05'),(7,3,'session_003','user','高血压能做什么运动？',0,'2024-11-23 15:00:00'),(8,3,'session_003','assistant','高血压患者运动建议：1. 散步、太极等低强度有氧运动最佳；2. 避免憋气、剧烈运动；3. 运动前后监测血压；4. 每次30分钟，每周5次；5. 血压过高(>180/110)时暂停运动。建议在医生指导下进行。',0,'2024-11-23 15:00:05'),(9,4,'session_004','user','怎么防止减肥反弹？',0,'2024-11-22 20:00:00'),(10,4,'session_004','assistant','防止减肥反弹的方法：1. 不要过度节食，保证基础代谢；2. 坚持运动，增加肌肉量；3. 慢慢恢复正常饮食，不要突然暴食；4. 保持良好作息；5. 定期监测体重，及时调整。减肥是长期过程，不要急于求成。',0,'2024-11-22 20:00:05'),(11,5,'session_005','user','新手健身应该注意什么？',0,'2024-11-21 19:00:00'),(12,5,'session_005','assistant','新手健身注意事项：1. 从低强度开始，循序渐进；2. 学习正确动作，避免受伤；3. 运动前热身，运动后拉伸；4. 保证充足休息和睡眠；5. 注意补充蛋白质和水分；6. 不要攀比，按自己节奏来。建议请教练指导初期训练。',0,'2024-11-21 19:00:05'),(13,1,'session_006','user','我最近总是失眠，有什么改善方法吗？',0,'2024-11-24 22:00:00'),(14,1,'session_006','assistant','改善失眠的建议：1. 保持规律作息，每天同一时间睡觉起床；2. 睡前1小时避免使用电子设备；3. 睡前可以做放松瑜伽或冥想；4. 避免下午3点后摄入咖啡因；5. 保持卧室安静、黑暗、凉爽。如果持续失眠超过2周，建议就医。',0,'2024-11-24 22:00:08'),(15,2,'session_007','user','我想增肌，饮食上有什么建议？',0,'2024-11-23 19:00:00'),(16,2,'session_007','assistant','增肌饮食建议：1. 每日蛋白质摄入1.6-2.2g/kg体重；2. 优质蛋白来源：鸡胸肉、鸡蛋、牛肉、鱼类、豆制品；3. 训练后30分钟内补充蛋白质；4. 保证充足碳水化合物作为能量来源；5. 适量摄入健康脂肪；6. 少食多餐，每3-4小时进食一次。',0,'2024-11-23 19:00:10'),(17,3,'session_008','user','老年人如何预防骨质疏松？',0,'2024-11-22 09:00:00'),(18,3,'session_008','assistant','预防骨质疏松的方法：1. 每天保证1000-1200mg钙摄入，如牛奶、豆制品；2. 补充维生素D，每天晒太阳15-30分钟；3. 适量负重运动如散步、太极；4. 戒烟限酒；5. 定期骨密度检查；6. 防止跌倒，注意居家安全。建议在医生指导下补充钙片和维生素D。',0,'2024-11-22 09:00:12'),(19,4,'session_009','user','运动后肌肉酸痛怎么缓解？',0,'2024-11-21 21:00:00'),(20,4,'session_009','assistant','缓解运动后肌肉酸痛：1. 运动后充分拉伸5-10分钟；2. 冷热交替淋浴或泡澡；3. 适量补充蛋白质帮助肌肉恢复；4. 轻度活动如散步促进血液循环；5. 充足睡眠让身体恢复；6. 按摩或使用泡沫轴放松肌肉。一般延迟性肌肉酸痛2-3天会自然缓解。',0,'2024-11-21 21:00:08'),(21,19,'0b1a3973','user','如何制定健康的减肥计划？',0,'2025-11-27 20:05:35'),(22,19,'0b1a3973','assistant','关于减重，我有以下建议：\n\n1. 饮食控制：减少高热量、高油脂食物摄入，增加蔬菜和优质蛋白\n2. 规律运动：每周至少150分钟中等强度有氧运动\n3. 充足睡眠：保证每天7-8小时睡眠\n4. 多喝水：每天喝足2000ml水\n\n建议循序渐进，每周减重0.5-1kg为宜。如需个性化方案，建议咨询专业营养师。',0,'2025-11-27 20:05:35');
/*!40000 ALTER TABLE `ai_chat_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `banners`
--

DROP TABLE IF EXISTS `banners`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `banners` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL COMMENT '标题',
  `image_url` varchar(255) NOT NULL COMMENT '图片地址',
  `link_type` varchar(50) DEFAULT NULL COMMENT '链接类型：page/product/post/url',
  `link_value` varchar(255) DEFAULT NULL COMMENT '链接值',
  `position` varchar(50) DEFAULT 'home' COMMENT '展示位置：home/mall/community',
  `sort_order` int DEFAULT '0' COMMENT '排序',
  `is_active` tinyint DEFAULT '1' COMMENT '是否启用',
  `start_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_position` (`position`),
  KEY `idx_is_active` (`is_active`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='轮播图表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `banners`
--

LOCK TABLES `banners` WRITE;
/*!40000 ALTER TABLE `banners` DISABLE KEYS */;
INSERT INTO `banners` VALUES (1,'双十一健康好物节','','page','/pages/shop/index','home',100,1,'2024-11-01 00:00:00','2024-11-30 23:59:59','2025-11-27 11:46:06'),(2,'新人专享优惠','','page','/pages/coupon/index','home',99,1,'2024-01-01 00:00:00','2025-12-31 23:59:59','2025-11-27 11:46:06'),(3,'每日运动打卡','','page','/pages/sport/index','home',98,1,'2024-01-01 00:00:00','2025-12-31 23:59:59','2025-11-27 11:46:06'),(4,'健康筛查入口','','page','/pages/health/index','home',97,1,'2024-01-01 00:00:00','2025-12-31 23:59:59','2025-11-27 11:46:06'),(5,'会员专属福利','','page','/pages/member/index','home',96,1,'2024-01-01 00:00:00','2025-12-31 23:59:59','2025-11-27 11:46:06'),(6,'双12健康狂欢节','/placeholder/banner_1212.jpg','page','/pages/activity/1212','home',6,1,'2024-12-01 00:00:00','2024-12-15 23:59:59','2025-11-27 12:02:11'),(7,'冬季养生专场','/placeholder/banner_winter.jpg','page','/pages/topic/winter','home',7,1,'2024-11-01 00:00:00','2025-02-28 23:59:59','2025-11-27 12:02:11'),(8,'新品上市 蛋白棒','/placeholder/banner_protein.jpg','product','17','home',8,1,'2024-11-20 00:00:00','2024-12-20 23:59:59','2025-11-27 12:02:11'),(9,'会员专享8折','/placeholder/banner_member.jpg','page','/pages/member/index','home',9,1,'2024-11-01 00:00:00','2024-12-31 23:59:59','2025-11-27 12:02:11'),(10,'健身课程免费体验','/placeholder/banner_course.jpg','course','/pages/course/list','course',1,1,'2024-11-01 00:00:00','2024-12-31 23:59:59','2025-11-27 12:02:11');
/*!40000 ALTER TABLE `banners` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carts`
--

DROP TABLE IF EXISTS `carts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carts` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `product_id` bigint unsigned NOT NULL COMMENT '商品ID',
  `spec_id` varchar(50) DEFAULT NULL COMMENT '规格ID',
  `quantity` int NOT NULL DEFAULT '1' COMMENT '数量',
  `is_selected` tinyint DEFAULT '1' COMMENT '是否选中',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `carts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `carts_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='购物车表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carts`
--

LOCK TABLES `carts` WRITE;
/*!40000 ALTER TABLE `carts` DISABLE KEYS */;
INSERT INTO `carts` VALUES (1,1,8,NULL,2,1,'2025-11-27 11:44:38','2025-11-27 11:44:38'),(2,1,11,'2',1,1,'2025-11-27 11:44:38','2025-11-27 11:44:38'),(3,2,3,'1',1,1,'2025-11-27 11:44:38','2025-11-27 11:44:38'),(4,2,9,NULL,1,0,'2025-11-27 11:44:38','2025-11-27 11:44:38'),(5,3,4,NULL,2,1,'2025-11-27 11:44:38','2025-11-27 11:44:38'),(6,4,12,'1',1,1,'2025-11-27 11:44:38','2025-11-27 11:44:38'),(7,5,1,'1',1,1,'2025-11-27 11:44:38','2025-11-27 11:44:38'),(8,5,10,'L',1,1,'2025-11-27 11:44:38','2025-11-27 11:44:38'),(9,1,13,'2kg',1,1,'2025-11-27 12:01:36','2025-11-27 12:01:36'),(10,1,14,'100片',2,1,'2025-11-27 12:01:36','2025-11-27 12:01:36'),(11,2,15,'90粒',1,1,'2025-11-27 12:01:36','2025-11-27 12:01:36'),(12,2,16,'12瓶',1,0,'2025-11-27 12:01:36','2025-11-27 12:01:36'),(13,3,17,'巧克力',2,1,'2025-11-27 12:01:36','2025-11-27 12:01:36'),(14,4,18,'20支',1,1,'2025-11-27 12:01:36','2025-11-27 12:01:36'),(15,4,19,'500g',1,1,'2025-11-27 12:01:36','2025-11-27 12:01:36'),(16,5,20,'60片',1,1,'2025-11-27 12:01:36','2025-11-27 12:01:36'),(17,16,1,NULL,2,1,'2025-11-27 16:50:41','2025-11-27 16:59:15'),(18,17,1,NULL,1,1,'2025-11-27 18:31:42','2025-11-27 18:31:42'),(19,18,1,NULL,1,1,'2025-11-27 19:47:30','2025-11-27 19:47:30'),(20,21,13,NULL,1,1,'2025-11-27 20:23:00','2025-11-27 20:23:00');
/*!40000 ALTER TABLE `carts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `checkin_records`
--

DROP TABLE IF EXISTS `checkin_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `checkin_records` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `checkin_date` date NOT NULL COMMENT '打卡日期',
  `sport_coins_earned` int DEFAULT '0' COMMENT '获得运动币',
  `food_coins_earned` int DEFAULT '0' COMMENT '获得膳食币',
  `is_continuous` tinyint DEFAULT '0' COMMENT '是否连续打卡',
  `continuous_days` int DEFAULT '1' COMMENT '连续天数',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_date` (`user_id`,`checkin_date`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_checkin_date` (`checkin_date`),
  CONSTRAINT `checkin_records_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='打卡记录表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `checkin_records`
--

LOCK TABLES `checkin_records` WRITE;
/*!40000 ALTER TABLE `checkin_records` DISABLE KEYS */;
INSERT INTO `checkin_records` VALUES (1,1,'2024-11-25',25,15,1,15,'2025-11-27 11:44:49'),(2,1,'2024-11-24',25,15,1,14,'2025-11-27 11:44:49'),(3,1,'2024-11-23',25,15,1,13,'2025-11-27 11:44:49'),(4,2,'2024-11-25',20,15,1,7,'2025-11-27 11:44:49'),(5,2,'2024-11-24',20,15,1,6,'2025-11-27 11:44:49'),(6,3,'2024-11-25',25,25,1,120,'2025-11-27 11:44:49'),(7,4,'2024-11-25',10,10,1,3,'2025-11-27 11:44:49'),(8,5,'2024-11-25',5,5,0,1,'2025-11-27 11:44:49'),(22,1,'2024-11-16',10,5,1,12,'2025-11-27 11:52:54'),(23,1,'2024-11-17',10,5,1,13,'2025-11-27 11:52:54'),(24,1,'2024-11-18',10,5,1,14,'2025-11-27 11:52:54'),(25,2,'2024-11-16',10,5,1,6,'2025-11-27 11:52:54'),(26,2,'2024-11-17',10,5,1,7,'2025-11-27 11:52:54'),(27,3,'2024-11-16',10,5,1,118,'2025-11-27 11:52:54'),(28,3,'2024-11-17',10,5,1,119,'2025-11-27 11:52:54'),(29,4,'2024-11-20',10,5,0,1,'2025-11-27 11:52:54'),(30,5,'2024-11-20',10,5,1,2,'2025-11-27 11:52:54'),(31,1,'2024-11-19',15,10,1,15,'2025-11-27 11:52:54'),(32,2,'2024-11-18',15,10,1,8,'2025-11-27 11:52:54'),(33,3,'2024-11-18',15,10,1,120,'2025-11-27 11:52:54'),(34,15,'2025-11-27',5,5,0,1,'2025-11-27 16:36:47'),(35,16,'2025-11-27',5,5,0,1,'2025-11-27 16:50:23'),(36,17,'2025-11-27',5,5,0,1,'2025-11-27 18:32:08');
/*!40000 ALTER TABLE `checkin_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coin_records`
--

DROP TABLE IF EXISTS `coin_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coin_records` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `coin_type` enum('sport','food') NOT NULL COMMENT '币种类型',
  `amount` int NOT NULL COMMENT '变动数量(正为获得，负为消耗)',
  `balance` int NOT NULL COMMENT '变动后余额',
  `source` varchar(50) NOT NULL COMMENT '来源：checkin/sport/food/exchange/shop',
  `source_id` bigint unsigned DEFAULT NULL COMMENT '来源ID',
  `description` varchar(200) DEFAULT NULL COMMENT '描述',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_coin_type` (`coin_type`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `coin_records_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='积分记录表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coin_records`
--

LOCK TABLES `coin_records` WRITE;
/*!40000 ALTER TABLE `coin_records` DISABLE KEYS */;
INSERT INTO `coin_records` VALUES (1,1,'sport',25,1280,'checkin',NULL,'连续打卡15天','2025-11-27 11:44:53'),(2,1,'sport',3,1255,'sport_record',NULL,'运动35分钟获得','2025-11-27 11:44:53'),(3,1,'food',9,860,'food_record',NULL,'记录3餐获得','2025-11-27 11:44:53'),(4,2,'sport',20,560,'checkin',NULL,'连续打卡7天','2025-11-27 11:44:53'),(5,2,'food',9,420,'food_record',NULL,'记录3餐获得','2025-11-27 11:44:53'),(6,3,'sport',25,3200,'checkin',NULL,'连续打卡120天','2025-11-27 11:44:53'),(7,3,'food',6,2800,'food_record',NULL,'记录2餐获得','2025-11-27 11:44:53'),(8,4,'sport',10,180,'checkin',NULL,'连续打卡3天','2025-11-27 11:44:53'),(9,4,'sport',2,170,'sport_record',NULL,'运动25分钟获得','2025-11-27 11:44:53'),(10,5,'sport',5,60,'checkin',NULL,'首次打卡','2025-11-27 11:44:53'),(11,5,'sport',4,55,'sport_record',NULL,'运动45分钟获得','2025-11-27 11:44:53'),(12,1,'sport',20,1300,'checkin',NULL,'运动打卡奖励','2025-11-27 11:52:48'),(13,1,'food',15,875,'checkin',NULL,'饮食打卡奖励','2025-11-27 11:52:48'),(14,2,'sport',20,580,'checkin',NULL,'运动打卡奖励','2025-11-27 11:52:48'),(15,2,'food',10,430,'food_record',NULL,'饮食记录奖励','2025-11-27 11:52:48'),(16,3,'sport',50,3250,'goal',1,'完成运动目标奖励','2025-11-27 11:52:48'),(17,3,'food',30,2830,'task',NULL,'完成饮食任务奖励','2025-11-27 11:52:48'),(18,4,'sport',-50,130,'exchange',5,'兑换优惠券','2025-11-27 11:52:48'),(19,4,'food',20,170,'post',14,'分享帖子奖励','2025-11-27 11:52:48'),(20,5,'sport',30,90,'task',NULL,'完成新手任务','2025-11-27 11:52:48'),(21,5,'food',15,55,'food_record',NULL,'首次记录饮食','2025-11-27 11:52:48'),(22,1,'sport',-100,1200,'order',1,'商城兑换','2025-11-27 11:52:48'),(23,2,'sport',-30,550,'lottery',NULL,'兑换抽奖券','2025-11-27 11:52:48'),(24,3,'food',-200,2630,'member',3,'会员续费折扣','2025-11-27 11:52:48'),(25,15,'sport',5,5,'daily_checkin',NULL,'连续签到第1天','2025-11-27 16:36:47'),(26,15,'food',5,5,'daily_checkin',NULL,'连续签到第1天','2025-11-27 16:36:47'),(27,16,'sport',5,5,'daily_checkin',NULL,'连续签到第1天','2025-11-27 16:50:23'),(28,16,'food',5,5,'daily_checkin',NULL,'连续签到第1天','2025-11-27 16:50:23'),(29,17,'sport',5,5,'daily_checkin',NULL,'连续签到第1天','2025-11-27 18:32:08'),(30,17,'food',5,5,'daily_checkin',NULL,'连续签到第1天','2025-11-27 18:32:08');
/*!40000 ALTER TABLE `coin_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `conversations`
--

DROP TABLE IF EXISTS `conversations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conversations` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_a_id` bigint unsigned NOT NULL COMMENT '用户A',
  `user_b_id` bigint unsigned NOT NULL COMMENT '用户B',
  `last_message_id` bigint unsigned DEFAULT NULL COMMENT '最后一条消息ID',
  `last_message_time` datetime DEFAULT NULL COMMENT '最后消息时间',
  `user_a_unread` int DEFAULT '0' COMMENT '用户A未读数',
  `user_b_unread` int DEFAULT '0' COMMENT '用户B未读数',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_users` (`user_a_id`,`user_b_id`),
  KEY `idx_user_a` (`user_a_id`),
  KEY `idx_user_b` (`user_b_id`),
  KEY `idx_last_time` (`last_message_time`),
  CONSTRAINT `conversations_ibfk_1` FOREIGN KEY (`user_a_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `conversations_ibfk_2` FOREIGN KEY (`user_b_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='会话表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conversations`
--

LOCK TABLES `conversations` WRITE;
/*!40000 ALTER TABLE `conversations` DISABLE KEYS */;
INSERT INTO `conversations` VALUES (1,1,2,NULL,'2024-11-25 10:30:00',0,1,'2025-11-27 11:45:11','2025-11-27 11:45:11'),(2,1,3,NULL,'2024-11-24 20:00:00',0,0,'2025-11-27 11:45:11','2025-11-27 11:45:11'),(3,2,4,NULL,'2024-11-23 15:00:00',1,0,'2025-11-27 11:45:11','2025-11-27 11:45:11'),(4,1,4,NULL,'2024-11-24 15:30:00',0,1,'2025-11-27 11:58:08','2025-11-27 11:58:08'),(5,2,5,NULL,'2024-11-23 20:15:00',1,0,'2025-11-27 11:58:08','2025-11-27 11:58:08'),(6,3,4,NULL,'2024-11-22 16:45:00',0,0,'2025-11-27 11:58:08','2025-11-27 11:58:08'),(7,1,5,NULL,'2024-11-25 10:00:00',0,2,'2025-11-27 11:58:08','2025-11-27 11:58:08');
/*!40000 ALTER TABLE `conversations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coupons`
--

DROP TABLE IF EXISTS `coupons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coupons` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '优惠券名称',
  `type` enum('fixed','percent') NOT NULL COMMENT '类型：fixed固定金额 percent折扣',
  `value` decimal(10,2) NOT NULL COMMENT '优惠值(金额或折扣率)',
  `min_amount` decimal(10,2) DEFAULT '0.00' COMMENT '最低消费金额',
  `max_discount` decimal(10,2) DEFAULT NULL COMMENT '最大优惠金额(折扣券)',
  `total_count` int NOT NULL COMMENT '发放总量',
  `used_count` int DEFAULT '0' COMMENT '已使用数量',
  `start_time` datetime NOT NULL COMMENT '生效时间',
  `end_time` datetime NOT NULL COMMENT '失效时间',
  `applicable_products` json DEFAULT NULL COMMENT '适用商品ID(null为全场)',
  `applicable_categories` json DEFAULT NULL COMMENT '适用分类ID',
  `is_active` tinyint DEFAULT '1' COMMENT '是否启用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_is_active` (`is_active`),
  KEY `idx_end_time` (`end_time`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='优惠券表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coupons`
--

LOCK TABLES `coupons` WRITE;
/*!40000 ALTER TABLE `coupons` DISABLE KEYS */;
INSERT INTO `coupons` VALUES (1,'新人专享券','fixed',20.00,99.00,NULL,1000,156,'2024-01-01 00:00:00','2025-12-31 23:59:59',NULL,NULL,1,'2025-11-27 11:42:28'),(2,'满199减30','fixed',30.00,199.00,NULL,500,89,'2024-01-01 00:00:00','2025-12-31 23:59:59',NULL,NULL,1,'2025-11-27 11:42:28'),(3,'满299减50','fixed',50.00,299.00,NULL,300,45,'2024-01-01 00:00:00','2025-12-31 23:59:59',NULL,NULL,1,'2025-11-27 11:42:28'),(4,'会员专享9折','percent',10.00,100.00,50.00,200,34,'2024-01-01 00:00:00','2025-12-31 23:59:59',NULL,NULL,1,'2025-11-27 11:42:28'),(5,'营养品专享券','fixed',25.00,150.00,NULL,400,78,'2024-01-01 00:00:00','2025-12-31 23:59:59',NULL,'[1]',1,'2025-11-27 11:42:28'),(6,'限时特惠8折','percent',20.00,200.00,100.00,100,23,'2024-11-01 00:00:00','2025-01-31 23:59:59',NULL,NULL,1,'2025-11-27 11:42:28'),(7,'满200减30','fixed',30.00,200.00,NULL,1000,320,'2024-11-01 00:00:00','2024-12-31 23:59:59',NULL,NULL,1,'2025-11-27 12:01:40'),(8,'8折优惠券','percent',80.00,100.00,50.00,500,180,'2024-11-01 00:00:00','2024-12-31 23:59:59',NULL,NULL,1,'2025-11-27 12:01:40'),(9,'满100减15','fixed',15.00,100.00,NULL,2000,890,'2024-11-01 00:00:00','2024-12-31 23:59:59',NULL,NULL,1,'2025-11-27 12:01:40'),(10,'新品9折券','percent',90.00,50.00,30.00,300,45,'2024-11-20 00:00:00','2024-12-20 23:59:59',NULL,'[1, 2]',1,'2025-11-27 12:01:40');
/*!40000 ALTER TABLE `coupons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL COMMENT '课程标题',
  `subtitle` varchar(200) DEFAULT NULL COMMENT '副标题',
  `cover_image` varchar(255) DEFAULT NULL COMMENT '封面图',
  `video_url` varchar(255) DEFAULT NULL COMMENT '视频地址',
  `duration` int DEFAULT '0' COMMENT '时长(秒)',
  `difficulty` enum('beginner','intermediate','advanced') DEFAULT 'beginner' COMMENT '难度',
  `sport_type` varchar(50) DEFAULT NULL COMMENT '运动类型',
  `calories` int DEFAULT '0' COMMENT '预计消耗卡路里',
  `equipment` json DEFAULT NULL COMMENT '所需器材',
  `description` text COMMENT '课程介绍',
  `coach_name` varchar(50) DEFAULT NULL COMMENT '教练名称',
  `coach_avatar` varchar(255) DEFAULT NULL COMMENT '教练头像',
  `play_count` int DEFAULT '0' COMMENT '播放次数',
  `collect_count` int DEFAULT '0' COMMENT '收藏次数',
  `is_free` tinyint DEFAULT '1' COMMENT '是否免费',
  `is_recommend` tinyint DEFAULT '0' COMMENT '是否推荐',
  `sort_order` int DEFAULT '0' COMMENT '排序',
  `status` tinyint DEFAULT '1' COMMENT '状态：0下架 1上架',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_sport_type` (`sport_type`),
  KEY `idx_difficulty` (`difficulty`),
  KEY `idx_is_recommend` (`is_recommend`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='运动课程表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES (1,'零基础燃脂HIIT','20分钟高效燃脂 适合新手',NULL,NULL,20,'beginner','hiit',200,'[\"瑜伽垫\"]','专为零基础设计的高强度间歇训练，通过短时间高效运动快速燃烧脂肪。','陈教练',NULL,125680,8956,1,1,100,1,'2025-11-27 11:42:23','2025-11-27 11:42:23'),(2,'马甲线养成计划','30天打造完美腹肌',NULL,NULL,25,'intermediate','strength',180,'[\"瑜伽垫\"]','针对腹部核心的系统训练，每天25分钟，30天见效。','李教练',NULL,89560,6234,0,1,99,1,'2025-11-27 11:42:23','2025-11-27 11:42:23'),(3,'晨间瑜伽唤醒','开启活力一天',NULL,NULL,15,'beginner','yoga',80,'[\"瑜伽垫\"]','温和的晨间瑜伽练习，唤醒身体，提升一天的精气神。','王教练',NULL,156780,12345,1,1,98,1,'2025-11-27 11:42:23','2025-11-27 11:42:23'),(4,'户外跑步指南','科学跑步 避免损伤',NULL,NULL,30,'beginner','running',300,'[]','学习正确的跑步姿势和呼吸方法，让跑步更高效更安全。','张教练',NULL,78900,5678,1,0,97,1,'2025-11-27 11:42:23','2025-11-27 11:42:23'),(5,'全身力量训练','打造完美身材',NULL,NULL,45,'intermediate','strength',350,'[\"哑铃\", \"瑜伽垫\"]','全面的力量训练课程，覆盖全身各大肌群，塑造健美身材。','刘教练',NULL,67890,4567,0,1,96,1,'2025-11-27 11:42:23','2025-11-27 11:42:23'),(6,'办公室拉伸','缓解久坐疲劳',NULL,NULL,10,'beginner','yoga',50,'[]','专为久坐办公人群设计，利用碎片时间缓解颈肩腰背疲劳。','王教练',NULL,234560,18900,1,1,95,1,'2025-11-27 11:42:23','2025-11-27 11:42:23'),(7,'跳绳燃脂','简单高效的有氧运动',NULL,NULL,20,'intermediate','rope_jumping',280,'[\"跳绳\"]','跳绳是最高效的燃脂运动之一，20分钟相当于慢跑40分钟。','陈教练',NULL,56780,3456,1,0,94,1,'2025-11-27 11:42:23','2025-11-27 11:42:23'),(8,'睡前放松瑜伽','改善睡眠质量',NULL,NULL,15,'beginner','yoga',40,'[\"瑜伽垫\"]','舒缓的睡前瑜伽，帮助身心放松，提升睡眠质量。','王教练',NULL,189000,15678,1,1,93,1,'2025-11-27 11:42:23','2025-11-27 11:42:23'),(9,'高级HIIT挑战','极限燃脂训练',NULL,NULL,30,'advanced','hiit',400,'[\"瑜伽垫\"]','高难度的HIIT挑战，适合有一定基础的健身者挑战自我。','李教练',NULL,34560,2345,0,0,92,1,'2025-11-27 11:42:23','2025-11-27 11:42:23'),(10,'游泳入门教程','零基础学游泳',NULL,NULL,40,'beginner','swimming',350,'[]','从零开始学习蛙泳，专业教练详细讲解每个动作要领。','张教练',NULL,45670,3890,1,0,91,1,'2025-11-27 11:42:23','2025-11-27 11:42:23'),(11,'全身燃脂20分钟','适合忙碌人群的快速燃脂训练',NULL,NULL,20,'intermediate','hiit',200,'[]','无需器械，随时随地进行的高效燃脂训练','张教练',NULL,2580,180,1,1,1,1,'2025-11-27 11:59:42','2025-11-27 11:59:42'),(12,'睡前放松瑜伽','帮助缓解疲劳改善睡眠',NULL,NULL,15,'beginner','yoga',60,'[\"瑜伽垫\"]','通过温和的体式帮助身心放松，改善睡眠质量','李老师',NULL,3200,280,1,1,2,1,'2025-11-27 11:59:42','2025-11-27 11:59:42'),(13,'核心力量训练','针对腹部和核心肌群',NULL,NULL,25,'advanced','strength',180,'[\"瑜伽垫\"]','专项核心训练，打造马甲线','王教练',NULL,1890,150,0,0,3,1,'2025-11-27 11:59:42','2025-11-27 11:59:42'),(14,'办公室颈椎保健操','久坐族必备',NULL,NULL,10,'beginner','stretch',30,'[]','办公室随时可做，缓解颈椎酸痛','赵老师',NULL,5600,420,1,1,4,1,'2025-11-27 11:59:42','2025-11-27 11:59:42'),(15,'晨间活力瑜伽','唤醒身体开启新一天',NULL,NULL,20,'beginner','yoga',80,'[\"瑜伽垫\"]','晨间练习，让你一整天精力充沛','李老师',NULL,2100,190,1,0,5,1,'2025-11-27 11:59:42','2025-11-27 11:59:42'),(16,'腿部塑形训练','打造纤细美腿',NULL,NULL,30,'intermediate','strength',220,'[\"哑铃\"]','针对腿部肌群的塑形训练','张教练',NULL,1650,130,0,0,6,1,'2025-11-27 11:59:42','2025-11-27 11:59:42'),(17,'太极拳入门教程','24式太极拳教学',NULL,NULL,45,'beginner','taichi',150,'[]','跟随大师学习正宗24式太极拳','陈大师',NULL,890,85,1,0,7,1,'2025-11-27 11:59:42','2025-11-27 11:59:42'),(18,'高强度间歇训练','短时间高效燃脂',NULL,NULL,25,'advanced','hiit',350,'[]','适合有运动基础者的高强度训练','王教练',NULL,1200,95,0,1,8,1,'2025-11-27 11:59:42','2025-11-27 11:59:42'),(19,'孕期瑜伽','安全温和的孕期运动',NULL,NULL,30,'beginner','yoga',90,'[\"瑜伽垫\", \"瑜伽砖\"]','专为孕妈设计的安全瑜伽课程','周老师',NULL,680,65,0,0,9,1,'2025-11-27 11:59:42','2025-11-27 11:59:42'),(20,'肩背放松拉伸','缓解肩背紧张',NULL,NULL,15,'beginner','stretch',40,'[]','简单有效的肩背放松动作','赵老师',NULL,3800,340,1,1,10,1,'2025-11-27 11:59:42','2025-11-27 11:59:42');
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `daily_tasks`
--

DROP TABLE IF EXISTS `daily_tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `daily_tasks` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '任务名称',
  `description` varchar(200) DEFAULT NULL COMMENT '任务描述',
  `task_type` varchar(50) NOT NULL COMMENT '任务类型：sport/food/checkin/share',
  `target_value` int DEFAULT '1' COMMENT '目标值',
  `reward_coin_type` enum('sport','food') NOT NULL COMMENT '奖励币种',
  `reward_amount` int NOT NULL COMMENT '奖励数量',
  `is_active` tinyint DEFAULT '1' COMMENT '是否启用',
  `sort_order` int DEFAULT '0' COMMENT '排序',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_task_type` (`task_type`),
  KEY `idx_is_active` (`is_active`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='每日任务配置表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `daily_tasks`
--

LOCK TABLES `daily_tasks` WRITE;
/*!40000 ALTER TABLE `daily_tasks` DISABLE KEYS */;
INSERT INTO `daily_tasks` VALUES (1,'每日打卡','完成每日打卡签到','checkin',1,'sport',5,1,100,'2025-11-27 11:44:58'),(2,'运动30分钟','完成30分钟以上运动','sport_duration',30,'sport',10,1,99,'2025-11-27 11:44:58'),(3,'记录3餐','记录今日三餐饮食','food_record',3,'food',10,1,98,'2025-11-27 11:44:58'),(4,'消耗200卡','运动消耗200大卡以上','calories_burn',200,'sport',15,1,97,'2025-11-27 11:44:58'),(5,'喝水8杯','记录8杯水的饮水量','water_intake',8,'food',5,1,96,'2025-11-27 11:44:58'),(6,'早睡早起','在23:00前入睡，7:00前起床','sleep_schedule',1,'sport',10,1,95,'2025-11-27 11:44:58'),(7,'分享动态','发布一条社区动态','post_share',1,'food',5,1,94,'2025-11-27 11:44:58'),(8,'完成课程','完成一节运动课程','course_complete',1,'sport',10,1,93,'2025-11-27 11:44:58'),(9,'浏览商城','浏览商城3个商品','browse',3,'food',5,1,9,'2025-11-27 12:03:06'),(10,'邀请好友','邀请1位好友注册','invite',1,'sport',50,1,10,'2025-11-27 12:03:06'),(11,'完成健康筛查','完成1次健康筛查','screening',1,'sport',30,1,11,'2025-11-27 12:03:06'),(12,'观看课程','观看1节运动课程','course',1,'sport',15,1,12,'2025-11-27 12:03:06');
/*!40000 ALTER TABLE `daily_tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `files`
--

DROP TABLE IF EXISTS `files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `files` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned DEFAULT NULL COMMENT '上传用户ID',
  `file_name` varchar(255) NOT NULL COMMENT '原文件名',
  `file_path` varchar(255) NOT NULL COMMENT '存储路径',
  `file_type` varchar(50) DEFAULT NULL COMMENT '文件类型',
  `file_size` int DEFAULT '0' COMMENT '文件大小(字节)',
  `mime_type` varchar(100) DEFAULT NULL COMMENT 'MIME类型',
  `module` varchar(50) DEFAULT NULL COMMENT '所属模块',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_module` (`module`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='文件管理表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `files`
--

LOCK TABLES `files` WRITE;
/*!40000 ALTER TABLE `files` DISABLE KEYS */;
INSERT INTO `files` VALUES (1,1,'avatar_1.jpg','/uploads/avatars/avatar_1.jpg','image',102400,'image/jpeg','avatar','2025-11-27 11:49:47'),(2,2,'avatar_2.jpg','/uploads/avatars/avatar_2.jpg','image',98304,'image/jpeg','avatar','2025-11-27 11:49:47'),(3,3,'avatar_3.jpg','/uploads/avatars/avatar_3.jpg','image',115200,'image/jpeg','avatar','2025-11-27 11:49:47'),(4,1,'post_1_1.jpg','/uploads/posts/post_1_1.jpg','image',204800,'image/jpeg','community','2025-11-27 11:49:47'),(5,1,'post_1_2.jpg','/uploads/posts/post_1_2.jpg','image',180224,'image/jpeg','community','2025-11-27 11:49:47'),(6,2,'post_2_1.jpg','/uploads/posts/post_2_1.jpg','image',163840,'image/jpeg','community','2025-11-27 11:49:47'),(7,1,'food_1.jpg','/uploads/food/food_1.jpg','image',143360,'image/jpeg','food','2025-11-27 11:49:47'),(8,1,'food_2.jpg','/uploads/food/food_2.jpg','image',122880,'image/jpeg','food','2025-11-27 11:49:47'),(9,NULL,'product_1.jpg','/uploads/products/product_1.jpg','image',307200,'image/jpeg','product','2025-11-27 11:49:47'),(10,NULL,'product_2.jpg','/uploads/products/product_2.jpg','image',286720,'image/jpeg','product','2025-11-27 11:49:47'),(11,NULL,'banner_1.jpg','/uploads/banners/banner_1.jpg','image',512000,'image/jpeg','banner','2025-11-27 11:49:47'),(12,NULL,'course_1.jpg','/uploads/courses/course_1.jpg','image',409600,'image/jpeg','course','2025-11-27 11:49:47');
/*!40000 ALTER TABLE `files` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `food_library`
--

DROP TABLE IF EXISTS `food_library`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `food_library` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '食物名称',
  `category` varchar(50) DEFAULT NULL COMMENT '分类',
  `image` varchar(255) DEFAULT NULL COMMENT '图片',
  `calories_per_100g` int DEFAULT '0' COMMENT '每100g卡路里',
  `protein_per_100g` decimal(6,2) DEFAULT '0.00' COMMENT '每100g蛋白质',
  `carbs_per_100g` decimal(6,2) DEFAULT '0.00' COMMENT '每100g碳水',
  `fat_per_100g` decimal(6,2) DEFAULT '0.00' COMMENT '每100g脂肪',
  `fiber_per_100g` decimal(6,2) DEFAULT '0.00' COMMENT '每100g纤维',
  `gi_value` int DEFAULT NULL COMMENT 'GI值(升糖指数)',
  `suitable_for` json DEFAULT NULL COMMENT '适合人群',
  `not_suitable_for` json DEFAULT NULL COMMENT '不适合人群',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_name` (`name`),
  KEY `idx_category` (`category`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='食物库';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `food_library`
--

LOCK TABLES `food_library` WRITE;
/*!40000 ALTER TABLE `food_library` DISABLE KEYS */;
INSERT INTO `food_library` VALUES (1,'鸡胸肉','肉类',NULL,165,31.00,0.00,3.60,0.00,0,'[\"增肌\", \"减脂\"]',NULL,'2025-11-27 11:47:02'),(2,'牛肉','肉类',NULL,250,26.00,0.00,15.00,0.00,0,'[\"增肌\"]',NULL,'2025-11-27 11:47:02'),(3,'三文鱼','水产',NULL,208,20.00,0.00,13.00,0.00,0,'[\"健脑\", \"护心\"]','[\"痛风\"]','2025-11-27 11:47:02'),(4,'鸡蛋','蛋类',NULL,155,13.00,1.10,11.00,0.00,0,'[\"增肌\", \"补充蛋白\"]','[\"高胆固醇\"]','2025-11-27 11:47:02'),(5,'牛奶','乳制品',NULL,42,3.40,5.00,1.00,0.00,30,'[\"补钙\", \"增肌\"]','[\"乳糖不耐\"]','2025-11-27 11:47:02'),(6,'糙米饭','主食',NULL,111,2.60,23.00,0.90,1.80,50,'[\"减脂\", \"控糖\"]',NULL,'2025-11-27 11:47:02'),(7,'全麦面包','主食',NULL,247,13.00,41.00,3.40,7.00,55,'[\"健康主食\"]','[\"麸质过敏\"]','2025-11-27 11:47:02'),(8,'燕麦','主食',NULL,389,17.00,66.00,7.00,11.00,55,'[\"降血糖\", \"减脂\"]',NULL,'2025-11-27 11:47:02'),(9,'西兰花','蔬菜',NULL,34,2.80,7.00,0.40,2.60,10,'[\"减脂\", \"抗氧化\"]',NULL,'2025-11-27 11:47:02'),(10,'菠菜','蔬菜',NULL,23,2.90,3.60,0.40,2.20,15,'[\"补铁\", \"护眼\"]','[\"肾结石\"]','2025-11-27 11:47:02'),(11,'番茄','蔬菜',NULL,18,0.90,3.90,0.20,1.20,15,'[\"减脂\", \"抗氧化\"]',NULL,'2025-11-27 11:47:02'),(12,'苹果','水果',NULL,52,0.30,14.00,0.20,2.40,36,'[\"减脂\", \"润肠\"]',NULL,'2025-11-27 11:47:02'),(13,'香蕉','水果',NULL,89,1.10,23.00,0.30,2.60,51,'[\"运动补能\", \"补钾\"]','[\"糖尿病\"]','2025-11-27 11:47:02'),(14,'牛油果','水果',NULL,160,2.00,9.00,15.00,7.00,15,'[\"护心\", \"减脂\"]',NULL,'2025-11-27 11:47:02'),(15,'杏仁','坚果',NULL,579,21.00,22.00,50.00,12.00,15,'[\"补脑\", \"护心\"]',NULL,'2025-11-27 11:47:02'),(16,'核桃','坚果',NULL,654,15.00,14.00,65.00,7.00,15,'[\"补脑\", \"抗衰老\"]',NULL,'2025-11-27 11:47:02'),(17,'豆腐','豆制品',NULL,76,8.00,1.90,4.80,0.40,15,'[\"补钙\", \"低脂\"]','[\"痛风\"]','2025-11-27 11:47:02'),(18,'酸奶','乳制品',NULL,61,3.50,4.70,3.30,0.00,33,'[\"肠道健康\", \"补钙\"]','[\"乳糖不耐\"]','2025-11-27 11:47:02'),(19,'苹果','fruit',NULL,52,0.30,13.80,0.20,2.40,36,'[\"减肥\", \"糖尿病\"]','[]','2025-11-27 11:59:13'),(20,'香蕉','fruit',NULL,89,1.10,22.80,0.30,2.60,51,'[\"运动前\", \"增肌\"]','[\"糖尿病\"]','2025-11-27 11:59:13'),(21,'橙子','fruit',NULL,47,0.90,11.80,0.10,2.40,43,'[\"减肥\", \"补充维C\"]','[]','2025-11-27 11:59:13'),(22,'菠菜','vegetable',NULL,23,2.90,3.60,0.40,2.20,15,'[\"减肥\", \"补铁\"]','[\"结石患者\"]','2025-11-27 11:59:13'),(23,'胡萝卜','vegetable',NULL,41,0.90,9.60,0.20,2.80,71,'[\"护眼\", \"儿童\"]','[]','2025-11-27 11:59:13'),(24,'猪肉（瘦）','meat',NULL,143,20.30,0.00,6.20,0.00,0,'[\"增肌\", \"补充蛋白\"]','[\"高血脂\"]','2025-11-27 11:59:13'),(25,'牛肉（瘦）','meat',NULL,106,20.20,0.00,2.30,0.00,0,'[\"增肌\", \"减肥\"]','[\"痛风\"]','2025-11-27 11:59:13'),(26,'三文鱼','seafood',NULL,208,20.40,0.00,13.40,0.00,0,'[\"护心\", \"补脑\"]','[\"海鲜过敏\"]','2025-11-27 11:59:13'),(27,'虾仁','seafood',NULL,99,20.30,0.50,1.60,0.00,0,'[\"减肥\", \"增肌\"]','[\"海鲜过敏\", \"痛风\"]','2025-11-27 11:59:13'),(28,'豆腐','bean',NULL,81,8.10,4.20,4.20,0.40,15,'[\"素食\", \"减肥\"]','[\"痛风\"]','2025-11-27 11:59:13'),(29,'牛奶','dairy',NULL,42,3.40,4.80,1.50,0.00,27,'[\"补钙\", \"儿童\"]','[\"乳糖不耐\"]','2025-11-27 11:59:13'),(30,'酸奶','dairy',NULL,72,3.50,9.30,2.50,0.00,36,'[\"肠道健康\", \"减肥\"]','[\"乳糖不耐\"]','2025-11-27 11:59:13'),(31,'白米饭','grain',NULL,116,2.60,25.90,0.30,0.30,83,'[\"日常主食\"]','[\"糖尿病\", \"减肥\"]','2025-11-27 11:59:13'),(32,'面条','grain',NULL,138,4.50,28.20,0.50,0.80,81,'[\"日常主食\"]','[\"糖尿病\"]','2025-11-27 11:59:13'),(33,'馒头','grain',NULL,223,7.00,47.00,1.10,1.30,88,'[\"日常主食\"]','[\"糖尿病\", \"减肥\"]','2025-11-27 11:59:13'),(34,'核桃','nut',NULL,654,14.90,13.70,65.20,6.70,15,'[\"补脑\", \"孕妇\"]','[\"减肥\"]','2025-11-27 11:59:13'),(35,'杏仁','nut',NULL,578,21.20,21.70,49.40,12.20,15,'[\"护心\", \"补充维E\"]','[\"减肥\"]','2025-11-27 11:59:13'),(36,'花生','nut',NULL,567,25.80,16.10,49.20,8.50,14,'[\"补充蛋白\", \"增肌\"]','[\"减肥\", \"花生过敏\"]','2025-11-27 11:59:13');
/*!40000 ALTER TABLE `food_library` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `food_records`
--

DROP TABLE IF EXISTS `food_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `food_records` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `meal_type` enum('breakfast','lunch','dinner','snack') NOT NULL COMMENT '餐次',
  `record_date` date NOT NULL COMMENT '记录日期',
  `food_name` varchar(100) NOT NULL COMMENT '食物名称',
  `food_image` varchar(255) DEFAULT NULL COMMENT '食物图片',
  `amount` decimal(8,2) DEFAULT NULL COMMENT '食用量(克)',
  `calories` int DEFAULT '0' COMMENT '卡路里',
  `protein` decimal(6,2) DEFAULT '0.00' COMMENT '蛋白质(g)',
  `carbs` decimal(6,2) DEFAULT '0.00' COMMENT '碳水(g)',
  `fat` decimal(6,2) DEFAULT '0.00' COMMENT '脂肪(g)',
  `fiber` decimal(6,2) DEFAULT '0.00' COMMENT '纤维(g)',
  `is_ai_recognized` tinyint DEFAULT '0' COMMENT '是否AI识别',
  `ai_confidence` decimal(3,2) DEFAULT NULL COMMENT 'AI识别置信度',
  `coins_earned` int DEFAULT '0' COMMENT '获得膳食币',
  `notes` text COMMENT '备注',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_record_date` (`record_date`),
  KEY `idx_meal_type` (`meal_type`),
  CONSTRAINT `food_records_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='膳食记录表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `food_records`
--

LOCK TABLES `food_records` WRITE;
/*!40000 ALTER TABLE `food_records` DISABLE KEYS */;
INSERT INTO `food_records` VALUES (1,1,'breakfast','2024-11-25','全麦面包+鸡蛋+牛奶',NULL,350.00,420,25.00,45.00,12.00,5.00,0,NULL,3,'营养早餐','2025-11-27 11:43:51'),(2,1,'lunch','2024-11-25','鸡胸肉沙拉',NULL,400.00,380,40.00,15.00,8.00,6.00,0,NULL,3,'减脂餐','2025-11-27 11:43:51'),(3,1,'dinner','2024-11-25','清蒸鱼+糙米饭+西兰花',NULL,500.00,520,35.00,55.00,10.00,8.00,0,NULL,3,'晚餐清淡','2025-11-27 11:43:51'),(4,2,'breakfast','2024-11-25','牛油果鸡蛋三明治',NULL,280.00,380,18.00,30.00,20.00,4.00,0,NULL,3,'高蛋白早餐','2025-11-27 11:43:51'),(5,2,'lunch','2024-11-25','轻食沙拉',NULL,350.00,320,15.00,25.00,12.00,8.00,0,NULL,3,NULL,'2025-11-27 11:43:51'),(6,2,'snack','2024-11-25','混合坚果',NULL,30.00,180,5.00,6.00,15.00,2.00,0,NULL,3,'下午茶','2025-11-27 11:43:51'),(7,3,'breakfast','2024-11-25','燕麦粥+水果',NULL,300.00,280,8.00,50.00,5.00,6.00,0,NULL,3,'养胃早餐','2025-11-27 11:43:51'),(8,3,'lunch','2024-11-25','蔬菜汤面',NULL,400.00,380,12.00,60.00,8.00,5.00,0,NULL,3,'清淡饮食','2025-11-27 11:43:51'),(9,4,'breakfast','2024-11-25','代餐奶昔',NULL,200.00,180,15.00,20.00,3.00,5.00,0,NULL,3,'减脂期代餐','2025-11-27 11:43:51'),(10,4,'lunch','2024-11-25','鸡胸肉便当',NULL,350.00,350,35.00,30.00,8.00,4.00,0,NULL,3,'自己做的','2025-11-27 11:43:51'),(11,5,'breakfast','2024-11-25','包子+豆浆',NULL,300.00,420,15.00,65.00,10.00,3.00,0,NULL,3,NULL,'2025-11-27 11:43:51'),(12,5,'lunch','2024-11-25','牛肉面',NULL,500.00,650,30.00,80.00,18.00,3.00,0,NULL,3,'外卖','2025-11-27 11:43:51'),(13,1,'breakfast','2024-11-20','全麦面包',NULL,100.00,180,8.00,32.00,2.00,4.00,0,NULL,5,'早餐主食','2025-11-27 11:55:39'),(14,1,'breakfast','2024-11-20','煎蛋',NULL,50.00,90,6.00,1.00,7.00,0.00,0,NULL,5,'早餐蛋白','2025-11-27 11:55:39'),(15,1,'breakfast','2024-11-20','牛奶',NULL,250.00,120,6.00,10.00,6.00,0.00,0,NULL,5,'早餐饮品','2025-11-27 11:55:39'),(16,2,'breakfast','2024-11-20','燕麦粥',NULL,200.00,150,5.00,27.00,3.00,4.00,1,NULL,8,'','2025-11-27 11:55:39'),(17,2,'breakfast','2024-11-20','蓝莓',NULL,80.00,40,1.00,10.00,0.00,2.00,1,NULL,5,'配燕麦','2025-11-27 11:55:39'),(18,3,'breakfast','2024-11-20','豆浆',NULL,300.00,80,7.00,5.00,3.00,1.00,0,NULL,5,'自制无糖','2025-11-27 11:55:39'),(19,3,'breakfast','2024-11-20','杂粮馒头',NULL,100.00,200,6.00,42.00,1.00,3.00,0,NULL,5,'','2025-11-27 11:55:39'),(20,4,'lunch','2024-11-20','水煮鸡胸肉',NULL,150.00,165,31.00,0.00,3.60,0.00,0,NULL,8,'减脂午餐','2025-11-27 11:55:39'),(21,4,'lunch','2024-11-20','西兰花',NULL,150.00,34,3.00,7.00,0.40,3.00,0,NULL,5,'','2025-11-27 11:55:39'),(22,4,'lunch','2024-11-20','糙米饭',NULL,150.00,180,4.00,38.00,1.00,2.00,0,NULL,5,'','2025-11-27 11:55:39'),(23,5,'lunch','2024-11-20','番茄炒蛋',NULL,200.00,150,8.00,8.00,10.00,1.00,1,NULL,8,'','2025-11-27 11:55:39'),(24,5,'lunch','2024-11-20','米饭',NULL,200.00,230,4.00,50.00,0.50,1.00,0,NULL,5,'','2025-11-27 11:55:39'),(25,1,'dinner','2024-11-20','清蒸鲈鱼',NULL,200.00,180,25.00,0.00,8.00,0.00,0,NULL,10,'晚餐','2025-11-27 11:55:39'),(26,1,'dinner','2024-11-20','炒青菜',NULL,150.00,60,2.00,5.00,4.00,2.00,0,NULL,5,'','2025-11-27 11:55:39'),(27,2,'dinner','2024-11-20','三文鱼沙拉',NULL,250.00,280,22.00,8.00,18.00,3.00,1,NULL,10,'低碳晚餐','2025-11-27 11:55:39'),(28,3,'dinner','2024-11-20','小米粥',NULL,300.00,90,2.00,19.00,1.00,1.00,0,NULL,5,'养胃晚餐','2025-11-27 11:55:39');
/*!40000 ALTER TABLE `food_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `health_reminders`
--

DROP TABLE IF EXISTS `health_reminders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `health_reminders` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `reminder_type` varchar(50) NOT NULL COMMENT '提醒类型：water/meal/sport/medicine',
  `reminder_time` time NOT NULL COMMENT '提醒时间',
  `content` varchar(200) DEFAULT NULL COMMENT '提醒内容',
  `repeat_days` json DEFAULT NULL COMMENT '重复日期(1-7代表周一到周日)',
  `is_enabled` tinyint DEFAULT '1' COMMENT '是否启用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_reminder_type` (`reminder_type`),
  CONSTRAINT `health_reminders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='健康提醒表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `health_reminders`
--

LOCK TABLES `health_reminders` WRITE;
/*!40000 ALTER TABLE `health_reminders` DISABLE KEYS */;
INSERT INTO `health_reminders` VALUES (1,1,'drink','09:00:00','该喝水啦，保持水分摄入','[1, 2, 3, 4, 5, 6, 7]',1,'2025-11-27 11:45:35','2025-11-27 11:45:35'),(2,1,'drink','14:00:00','下午了，记得补充水分','[1, 2, 3, 4, 5, 6, 7]',1,'2025-11-27 11:45:35','2025-11-27 11:45:35'),(3,1,'exercise','18:00:00','下班了，该运动啦','[1, 2, 3, 4, 5]',1,'2025-11-27 11:45:35','2025-11-27 11:45:35'),(4,2,'meal','07:30:00','早餐时间到，记得吃早餐','[1, 2, 3, 4, 5, 6, 7]',1,'2025-11-27 11:45:35','2025-11-27 11:45:35'),(5,2,'exercise','07:00:00','晨间瑜伽时间','[1, 2, 3, 4, 5, 6, 7]',1,'2025-11-27 11:45:35','2025-11-27 11:45:35'),(6,3,'drink','08:00:00','早起一杯温水','[1, 2, 3, 4, 5, 6, 7]',1,'2025-11-27 11:45:35','2025-11-27 11:45:35'),(7,3,'exercise','06:30:00','晨练时间到','[1, 2, 3, 4, 5, 6, 7]',1,'2025-11-27 11:45:35','2025-11-27 11:45:35'),(8,4,'meal','12:00:00','午餐时间，控制热量摄入','[1, 2, 3, 4, 5]',1,'2025-11-27 11:45:35','2025-11-27 11:45:35'),(9,4,'sleep','22:30:00','准备休息，早睡早起','[1, 2, 3, 4, 5, 6, 7]',1,'2025-11-27 11:45:35','2025-11-27 11:45:35'),(10,1,'medicine','08:00:00','记得服用每日维生素D和钙片',NULL,1,'2025-11-27 11:58:07','2025-11-27 11:58:07'),(11,1,'exercise','06:30:00','该去晨跑啦，今日目标5公里','[1, 3, 5]',1,'2025-11-27 11:58:07','2025-11-27 11:58:07'),(12,1,'water','10:00:00','记得补充水分，保持每天8杯水',NULL,1,'2025-11-27 11:58:07','2025-11-27 11:58:07'),(13,2,'exercise','06:00:00','该做晨间瑜伽了',NULL,1,'2025-11-27 11:58:07','2025-11-27 11:58:07'),(14,2,'meal','07:30:00','别忘了吃早餐哦',NULL,1,'2025-11-27 11:58:07','2025-11-27 11:58:07'),(15,3,'medicine','07:00:00','按时服用降压药',NULL,1,'2025-11-27 11:58:07','2025-11-27 11:58:07'),(16,3,'checkup','08:00:00','记得测量血压并记录',NULL,1,'2025-11-27 11:58:07','2025-11-27 11:58:07'),(17,3,'exercise','06:00:00','去公园散步吧',NULL,1,'2025-11-27 11:58:07','2025-11-27 11:58:07'),(18,4,'meal','12:00:00','注意控制今日热量摄入',NULL,1,'2025-11-27 11:58:07','2025-11-27 11:58:07'),(19,4,'exercise','19:00:00','该去健身了，今日目标消耗300大卡','[1, 2, 3, 4, 5]',1,'2025-11-27 11:58:07','2025-11-27 11:58:07'),(20,5,'water','09:00:00','新手运动后记得多喝水',NULL,1,'2025-11-27 11:58:07','2025-11-27 11:58:07'),(21,5,'exercise','18:00:00','按照新手计划进行今日训练','[2, 4, 6]',1,'2025-11-27 11:58:07','2025-11-27 11:58:07');
/*!40000 ALTER TABLE `health_reminders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `health_screenings`
--

DROP TABLE IF EXISTS `health_screenings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `health_screenings` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `height` decimal(5,2) DEFAULT NULL COMMENT '身高(cm)',
  `weight` decimal(5,2) DEFAULT NULL COMMENT '体重(kg)',
  `bmi` decimal(4,2) DEFAULT NULL COMMENT 'BMI指数',
  `heart_rate` int DEFAULT NULL COMMENT '心率(次/分)',
  `blood_pressure_high` int DEFAULT NULL COMMENT '收缩压',
  `blood_pressure_low` int DEFAULT NULL COMMENT '舒张压',
  `body_temperature` decimal(3,1) DEFAULT NULL COMMENT '体温',
  `blood_sugar` decimal(4,2) DEFAULT NULL COMMENT '血糖',
  `face_image` varchar(255) DEFAULT NULL COMMENT '面部照片',
  `body_image` varchar(255) DEFAULT NULL COMMENT '体态照片',
  `questionnaire_data` json DEFAULT NULL COMMENT '问卷答案JSON',
  `risk_level` enum('low','medium','high') DEFAULT 'low' COMMENT '风险等级',
  `risk_tags` json DEFAULT NULL COMMENT '风险标签',
  `ai_suggestion` text COMMENT 'AI生成的健康建议',
  `diet_suggestion` text COMMENT '膳食建议',
  `exercise_suggestion` text COMMENT '运动建议',
  `lifestyle_suggestion` text COMMENT '生活方式建议',
  `recommended_products` json DEFAULT NULL COMMENT '推荐商品ID列表',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_created_at` (`created_at`),
  KEY `idx_risk_level` (`risk_level`),
  CONSTRAINT `health_screenings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='健康筛查记录表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `health_screenings`
--

LOCK TABLES `health_screenings` WRITE;
/*!40000 ALTER TABLE `health_screenings` DISABLE KEYS */;
INSERT INTO `health_screenings` VALUES (1,1,175.00,70.00,22.86,72,118,78,36.5,5.20,NULL,NULL,NULL,'low','[]','您的各项指标都在正常范围内，继续保持良好的生活习惯。','建议保持高蛋白饮食，适当控制碳水摄入。','建议每周进行3-4次力量训练，配合有氧运动。','保持规律作息，每天睡眠7-8小时。',NULL,'2024-11-20 10:00:00'),(2,2,165.00,55.00,20.20,68,110,72,36.4,4.80,NULL,NULL,NULL,'low','[]','身体状况良好，BMI在正常范围内。','注意补充蛋白质和钙质，预防骨质疏松。','建议增加柔韧性训练，每周2-3次瑜伽。','注意防晒，保持好心情。',NULL,'2024-11-18 14:30:00'),(3,3,172.00,68.00,22.99,75,135,88,36.6,5.80,NULL,NULL,NULL,'medium','[\"血压偏高\"]','血压略微偏高，建议密切关注，必要时就医。','建议低盐低脂饮食，多吃蔬菜水果。','建议以散步、太极等低强度运动为主。','避免情绪激动，保持心态平和。',NULL,'2024-11-15 09:00:00'),(4,4,160.00,52.00,20.31,65,105,68,36.3,4.50,NULL,NULL,NULL,'low','[]','各项指标正常，减重效果显著，继续保持。','注意营养均衡，不要过度节食。','建议有氧和力量训练结合，防止肌肉流失。','保持好心情，减重是马拉松不是短跑。',NULL,'2024-11-22 16:00:00'),(5,5,178.00,80.00,25.25,78,125,82,36.5,5.50,NULL,NULL,NULL,'medium','[\"体重偏高\"]','BMI略微超标，建议通过运动和饮食调整。','建议控制总热量摄入，减少高油高糖食物。','建议每周至少150分钟中等强度有氧运动。','循序渐进，不要急于求成。',NULL,'2024-11-10 11:00:00'),(6,1,175.00,68.00,22.20,68,118,75,36.5,5.20,NULL,NULL,NULL,'low','[]','根据您的体检数据分析，各项指标均在正常范围内，建议继续保持当前的生活方式。','建议每日摄入蛋白质80-100g，控制碳水化合物摄入，多吃蔬菜水果。','建议每周进行3-5次中等强度有氧运动，每次30-45分钟。','保持规律作息，每天睡眠7-8小时，避免熬夜。','[1, 2, 4]','2025-11-27 11:57:36'),(7,2,162.00,52.00,19.80,62,110,70,36.3,4.80,NULL,NULL,NULL,'low','[\"体重偏轻\"]','您的BMI略低于正常范围，建议适当增加营养摄入。','建议增加蛋白质和碳水化合物摄入，每日热量增加200-300大卡。','建议进行力量训练，帮助增加肌肉量。','保持规律饮食，不要跳过任何一餐。','[1, 5, 9]','2025-11-27 11:57:36'),(8,3,168.00,72.00,25.50,75,135,88,36.6,6.50,NULL,NULL,NULL,'medium','[\"血压偏高\", \"血糖偏高\"]','您的血压和血糖指标略高于正常值，建议减少盐分摄入，每天进行30分钟以上的有氧运动。','减少盐分摄入，控制每日钠摄入量在2000mg以下，多吃富含钾的食物。','建议每天进行30分钟以上低强度有氧运动，如散步、太极。','戒烟限酒，保持心情舒畅，定期监测血压血糖。','[2, 3, 6]','2025-11-27 11:57:36'),(9,4,165.00,70.00,25.70,72,122,80,36.4,5.50,NULL,NULL,NULL,'medium','[\"超重\"]','您当前处于超重边缘，建议控制每日热量摄入，增加有氧运动频率。','控制每日热量摄入在1500-1800大卡，减少精制碳水和油脂。','建议每周进行5次有氧运动，每次45分钟以上。','避免久坐，每小时起身活动5分钟。','[5, 7, 10]','2025-11-27 11:57:36'),(10,5,178.00,75.00,23.70,70,120,78,36.5,5.30,NULL,NULL,NULL,'low','[]','您的身体状况良好，建议继续保持规律的运动习惯。','保持均衡饮食，注意蛋白质摄入。','继续保持当前运动频率，可以尝试增加运动强度。','保持良好的生活习惯，充足睡眠。','[1, 4]','2025-11-27 11:57:36'),(11,1,175.00,67.00,21.90,66,116,73,36.4,5.10,NULL,NULL,NULL,'low','[]','相比上次筛查，您的体重有所下降，各项指标更加理想。','继续保持当前饮食习惯，可适当增加优质蛋白。','可以尝试增加运动强度或时长。','继续保持良好作息。','[1, 2]','2025-11-27 11:57:36'),(12,3,168.00,70.00,24.80,72,130,85,36.5,6.20,NULL,NULL,NULL,'medium','[\"血压偏高\", \"血糖偏高\"]','您的血压和血糖指标较上次有所改善，说明生活方式调整效果明显，请继续保持。','继续低盐低糖饮食，增加膳食纤维摄入。','保持每日运动习惯，可适当增加运动时间。','继续保持良好心态，规律作息。','[2, 3, 6]','2025-11-27 11:57:36'),(13,13,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 1, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-11-27 16:30:32'),(14,14,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 1, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-11-27 16:33:18'),(15,15,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 1, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-11-27 16:36:24'),(16,16,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 1, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-11-27 16:43:04'),(17,17,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 1, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-11-27 18:26:39'),(18,18,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 1, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-11-27 19:46:44'),(19,19,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 1, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-11-27 20:03:34'),(20,20,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 1, \"birthday\": \"1996-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-11-27 20:13:39'),(21,21,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 1, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-11-27 20:20:49'),(22,22,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 2, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-11-27 20:28:50'),(23,23,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 1, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-11-27 20:45:27'),(24,24,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 1, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-11-28 13:21:19'),(25,25,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 1, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-11-28 13:28:47'),(26,26,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 1, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-11-28 13:39:21'),(27,27,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 1, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-11-28 13:46:51'),(28,28,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 0, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-11-28 13:47:46'),(29,29,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 1, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-11-28 13:51:22'),(30,30,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 1, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-11-28 13:56:59'),(31,31,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 1, \"birthday\": \"1997-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-11-28 14:11:53'),(32,32,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 0, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-11-28 14:23:10'),(33,33,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 1, \"birthday\": \"1995-03-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-12-01 10:56:53'),(34,34,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 0, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-12-01 11:00:54'),(35,35,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 0, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-12-01 11:08:51'),(36,36,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 0, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-12-01 11:14:47'),(37,37,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 0, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-12-01 11:22:51'),(38,38,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 0, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-12-01 11:26:43'),(39,39,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 0, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-12-01 11:29:00'),(40,40,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 0, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-12-01 11:31:01'),(41,41,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 0, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-12-01 11:33:43'),(42,42,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 0, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-12-01 11:43:04'),(43,43,170.00,60.00,20.76,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{\"gender\": 0, \"birthday\": \"1995-01-01\"}','low','[]','根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。','建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。','建议每天保持30分钟以上中等强度运动，如快走、慢跑等。','建议早睡早起，保证充足睡眠，避免久坐，定期体检。',NULL,'2025-12-01 11:44:36');
/*!40000 ALTER TABLE `health_screenings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member_orders`
--

DROP TABLE IF EXISTS `member_orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member_orders` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `order_no` varchar(32) NOT NULL COMMENT '订单号',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `member_type` enum('month','year','lifetime') NOT NULL COMMENT '会员类型',
  `original_price` decimal(10,2) NOT NULL COMMENT '原价',
  `pay_amount` decimal(10,2) NOT NULL COMMENT '实付金额',
  `pay_type` enum('wechat','alipay') DEFAULT NULL COMMENT '支付方式',
  `status` enum('pending','paid','cancelled') DEFAULT 'pending' COMMENT '状态',
  `pay_time` datetime DEFAULT NULL COMMENT '支付时间',
  `expire_time` datetime DEFAULT NULL COMMENT '到期时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_no` (`order_no`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_order_no` (`order_no`),
  KEY `idx_status` (`status`),
  CONSTRAINT `member_orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='会员订单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member_orders`
--

LOCK TABLES `member_orders` WRITE;
/*!40000 ALTER TABLE `member_orders` DISABLE KEYS */;
INSERT INTO `member_orders` VALUES (1,'M20241101001',1,'year',360.00,168.00,'wechat','paid','2024-11-01 10:00:00','2025-10-31 23:59:59','2024-11-01 09:55:00'),(2,'M20241015001',2,'month',30.00,19.90,'wechat','paid','2024-10-15 14:30:00','2024-11-14 23:59:59','2024-10-15 14:25:00'),(3,'M20241001001',3,'lifetime',999.00,399.00,'alipay','paid','2024-10-01 08:00:00','2099-12-31 23:59:59','2024-10-01 07:55:00'),(4,'MEM2024110100001',1,'year',268.00,198.00,'wechat','paid','2024-01-01 10:00:00','2025-01-01 23:59:59','2025-11-27 11:58:43'),(5,'MEM2024100100002',2,'month',29.00,29.00,'alipay','paid','2024-10-01 15:30:00','2024-11-01 23:59:59','2025-11-27 11:58:43'),(6,'MEM2024110100003',2,'month',29.00,29.00,'wechat','paid','2024-11-01 09:00:00','2024-12-01 23:59:59','2025-11-27 11:58:43'),(7,'MEM2023060100004',3,'lifetime',998.00,998.00,'wechat','paid','2023-06-01 12:00:00','2099-12-31 23:59:59','2025-11-27 11:58:43'),(8,'MEM2024111500005',4,'month',29.00,29.00,'alipay','paid','2024-11-15 18:00:00','2024-12-15 23:59:59','2025-11-27 11:58:43');
/*!40000 ALTER TABLE `member_orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `conversation_id` bigint unsigned NOT NULL COMMENT '会话ID',
  `sender_id` bigint unsigned NOT NULL COMMENT '发送者ID',
  `receiver_id` bigint unsigned NOT NULL COMMENT '接收者ID',
  `content` text NOT NULL COMMENT '消息内容',
  `msg_type` enum('text','image','voice') DEFAULT 'text' COMMENT '消息类型',
  `is_read` tinyint DEFAULT '0' COMMENT '是否已读',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_conversation` (`conversation_id`),
  KEY `idx_sender` (`sender_id`),
  KEY `idx_receiver` (`receiver_id`),
  CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`conversation_id`) REFERENCES `conversations` (`id`) ON DELETE CASCADE,
  CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `messages_ibfk_3` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='私信消息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (1,1,1,2,'你好，看到你的减脂打卡了，很励志！','text',1,'2025-11-27 11:45:16'),(2,1,2,1,'谢谢！一起加油！','text',1,'2025-11-27 11:45:16'),(3,1,1,2,'请问你平时都做什么运动？','text',1,'2025-11-27 11:45:16'),(4,1,2,1,'主要是HIIT和跳绳，效果很好','text',0,'2025-11-27 11:45:16'),(5,2,1,3,'王老师，请问高血压适合做什么运动？','text',1,'2025-11-27 11:45:16'),(6,2,3,1,'建议以散步、太极等低强度运动为主，避免剧烈运动。','text',1,'2025-11-27 11:45:16'),(7,3,2,4,'看到你减重20斤了，太厉害了！','text',1,'2025-11-27 11:45:16'),(8,3,4,2,'主要是坚持，一开始很难，后来就习惯了','text',1,'2025-11-27 11:45:16'),(9,3,2,4,'能分享一下你的食谱吗？','text',0,'2025-11-27 11:45:16'),(22,4,1,4,'你好，看到你的减肥帖子了，效果真好！','text',1,'2025-11-27 11:58:15'),(23,4,4,1,'谢谢！主要是坚持运动和控制饮食','text',1,'2025-11-27 11:58:15'),(24,4,1,4,'能分享一下具体的饮食计划吗？','text',0,'2025-11-27 11:58:15'),(25,5,2,5,'新手健身有什么建议吗？','text',1,'2025-11-27 11:58:15'),(26,5,5,2,'我也是新手，一起加油吧！','text',0,'2025-11-27 11:58:15'),(27,6,3,4,'太极拳对减肥也有帮助的','text',1,'2025-11-27 11:58:15'),(28,6,4,3,'是吗？怎么练呢？','text',1,'2025-11-27 11:58:15'),(29,6,3,4,'可以先从24式太极拳开始，我可以教你','text',1,'2025-11-27 11:58:15'),(30,7,1,5,'加油！坚持就是胜利','text',1,'2025-11-27 11:58:15'),(31,7,5,1,'谢谢前辈鼓励！','text',1,'2025-11-27 11:58:15'),(32,7,1,5,'有问题随时问我','text',0,'2025-11-27 11:58:15'),(33,7,1,5,'我之前也是新手过来的','text',0,'2025-11-27 11:58:15');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `type` varchar(50) NOT NULL COMMENT '通知类型：system/like/comment/follow/order',
  `title` varchar(100) NOT NULL COMMENT '标题',
  `content` text COMMENT '内容',
  `related_id` bigint unsigned DEFAULT NULL COMMENT '关联ID',
  `related_type` varchar(50) DEFAULT NULL COMMENT '关联类型',
  `is_read` tinyint DEFAULT '0' COMMENT '是否已读',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_type` (`type`),
  KEY `idx_is_read` (`is_read`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='通知表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
INSERT INTO `notifications` VALUES (1,1,'order','订单发货通知','您的订单 20241125001002 已发货，请注意查收',2,'order',0,'2025-11-27 11:47:09'),(2,1,'points','积分到账通知','恭喜您获得25运动币，连续打卡15天',NULL,NULL,1,'2025-11-27 11:47:09'),(3,2,'social','新粉丝通知','用户健康达人小明关注了您',1,'user',1,'2025-11-27 11:47:09'),(4,3,'social','评论通知','用户健康达人小明评论了您的动态',3,'post',0,'2025-11-27 11:47:09'),(5,4,'social','点赞通知','您的动态获得了新的点赞',5,'post',0,'2025-11-27 11:47:09'),(6,5,'system','系统通知','欢迎加入健康管理平台，开始您的健康之旅！',NULL,NULL,1,'2025-11-27 11:47:09'),(7,1,'order','订单发货通知','您的订单ORD2024112700006已发货，请注意查收',6,'order',1,'2025-11-27 11:52:22'),(8,2,'order','订单发货通知','您的订单ORD2024112700007已发货，请注意查收',7,'order',1,'2025-11-27 11:52:22'),(9,3,'order','订单发货通知','您的订单ORD2024112700008已发货，请注意查收',8,'order',0,'2025-11-27 11:52:22'),(10,1,'coupon','优惠券到账','恭喜您获得30元优惠券一张，有效期7天',1,'coupon',1,'2025-11-27 11:52:22'),(11,2,'coupon','优惠券到账','恭喜您获得满减优惠券一张，有效期7天',2,'coupon',0,'2025-11-27 11:52:22'),(12,4,'member','会员即将到期','您的会员将于3天后到期，续费享优惠',NULL,NULL,0,'2025-11-27 11:52:22'),(13,1,'like','收到点赞','有人赞了你的帖子\"今天完成了5公里跑步\"',1,'post',0,'2025-11-27 11:52:22'),(14,2,'comment','收到评论','有人评论了你的帖子\"分享一套适合办公室做的颈椎瑜伽\"',2,'post',0,'2025-11-27 11:52:22'),(15,3,'follow','新粉丝通知','用户\"健康达人小明\"关注了你',1,'user',1,'2025-11-27 11:52:22'),(16,5,'system','系统公告','双十二活动即将开始，敬请期待',NULL,NULL,0,'2025-11-27 11:52:22'),(17,1,'health','健康提醒','距离上次健康筛查已过30天，建议进行新一轮筛查',NULL,NULL,0,'2025-11-27 11:52:22'),(18,2,'task','任务完成提醒','恭喜完成今日打卡任务，获得20运动币',NULL,NULL,1,'2025-11-27 11:52:22'),(19,3,'points','积分变动','消费获得50膳食币',NULL,NULL,1,'2025-11-27 11:52:22'),(20,4,'order','订单完成','您的订单已完成，欢迎评价',4,'order',0,'2025-11-27 11:52:22');
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_items` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `order_id` bigint unsigned NOT NULL COMMENT '订单ID',
  `product_id` bigint unsigned NOT NULL COMMENT '商品ID',
  `product_name` varchar(100) NOT NULL COMMENT '商品名称(快照)',
  `product_image` varchar(255) DEFAULT NULL COMMENT '商品图片(快照)',
  `spec_name` varchar(100) DEFAULT NULL COMMENT '规格名称',
  `price` decimal(10,2) NOT NULL COMMENT '单价',
  `quantity` int NOT NULL COMMENT '数量',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_order_id` (`order_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='订单商品表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_items`
--

LOCK TABLES `order_items` WRITE;
/*!40000 ALTER TABLE `order_items` DISABLE KEYS */;
INSERT INTO `order_items` VALUES (1,1,1,'乳清蛋白粉 巧克力味',NULL,'1kg装',238.00,1,'2025-11-27 11:44:20'),(2,2,3,'复合维生素片',NULL,'60片装',108.00,1,'2025-11-27 11:44:20'),(3,2,5,'益生菌粉',NULL,'30袋装',148.00,1,'2025-11-27 11:44:20'),(4,3,6,'代餐奶昔 草莓味',NULL,'15袋装',118.00,1,'2025-11-27 11:44:20'),(5,4,2,'分离乳清蛋白 原味',NULL,'1kg装',328.00,1,'2025-11-27 11:44:20'),(6,5,6,'代餐奶昔 草莓味',NULL,'15袋装',118.00,1,'2025-11-27 11:44:20'),(7,6,1,'乳清蛋白粉 巧克力味 2.27kg',NULL,'巧克力味',268.00,1,'2025-11-27 11:51:06'),(8,6,4,'益生菌胶囊 60粒',NULL,'60粒装',128.00,1,'2025-11-27 11:51:06'),(9,7,2,'维生素D3软胶囊 90粒',NULL,'90粒装',89.00,2,'2025-11-27 11:51:06'),(10,7,6,'钙镁片 120片',NULL,'120片装',78.00,1,'2025-11-27 11:51:06'),(11,8,5,'代餐奶昔 香草味 750g',NULL,'香草味',168.00,1,'2025-11-27 11:51:06'),(12,9,7,'燕麦代餐粉 500g',NULL,'500g装',99.00,1,'2025-11-27 11:51:06'),(13,10,1,'乳清蛋白粉 巧克力味 2.27kg',NULL,'巧克力味',268.00,1,'2025-11-27 11:51:06'),(14,10,3,'深海鱼油软胶囊 120粒',NULL,'120粒装',168.00,1,'2025-11-27 11:51:06'),(15,11,9,'胶原蛋白肽饮品 30支',NULL,'30支装',298.00,1,'2025-11-27 11:51:06'),(16,11,10,'复合维生素B族 100片',NULL,'100片装',68.00,2,'2025-11-27 11:51:06'),(17,11,4,'益生菌胶囊 60粒',NULL,'60粒装',128.00,1,'2025-11-27 11:51:06'),(18,12,8,'蓝莓护眼软糖 60粒',NULL,'60粒装',78.00,2,'2025-11-27 11:51:06'),(19,13,1,'乳清蛋白粉 巧克力味 2.27kg',NULL,'巧克力味',268.00,1,'2025-11-27 11:51:06'),(20,14,1,'乳清蛋白粉 巧克力味',NULL,NULL,258.00,1,'2025-11-27 20:46:06');
/*!40000 ALTER TABLE `order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `order_no` varchar(32) NOT NULL COMMENT '订单号',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `total_amount` decimal(10,2) NOT NULL COMMENT '订单总额',
  `pay_amount` decimal(10,2) NOT NULL COMMENT '实付金额',
  `discount_amount` decimal(10,2) DEFAULT '0.00' COMMENT '优惠金额',
  `freight_amount` decimal(10,2) DEFAULT '0.00' COMMENT '运费',
  `coupon_id` bigint unsigned DEFAULT NULL COMMENT '使用的优惠券ID',
  `pay_type` enum('wechat','alipay','balance','coins') DEFAULT NULL COMMENT '支付方式',
  `status` enum('pending','paid','shipped','received','completed','cancelled','refunding','refunded') DEFAULT 'pending' COMMENT '订单状态',
  `receiver_name` varchar(50) NOT NULL COMMENT '收货人',
  `receiver_phone` varchar(20) NOT NULL COMMENT '收货电话',
  `receiver_address` varchar(300) NOT NULL COMMENT '收货地址',
  `remark` text COMMENT '订单备注',
  `pay_time` datetime DEFAULT NULL COMMENT '支付时间',
  `ship_time` datetime DEFAULT NULL COMMENT '发货时间',
  `receive_time` datetime DEFAULT NULL COMMENT '收货时间',
  `tracking_company` varchar(50) DEFAULT NULL COMMENT '物流公司',
  `tracking_no` varchar(50) DEFAULT NULL COMMENT '物流单号',
  `is_reviewed` tinyint DEFAULT '0' COMMENT '是否已评价',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_no` (`order_no`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_order_no` (`order_no`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='订单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,'20241125001001',1,258.00,238.00,20.00,0.00,NULL,'wechat','completed','张明','13800138001','北京市北京市朝阳区望京街道望京SOHO T1 1501',NULL,'2024-11-20 10:30:00','2024-11-21 09:00:00',NULL,'顺丰速运','SF1234567890',1,'2024-11-20 10:00:00','2025-11-27 11:44:17'),(2,'20241125001002',1,296.00,266.00,30.00,0.00,NULL,'wechat','shipped','张明','13800138001','北京市北京市朝阳区望京街道望京SOHO T1 1501',NULL,'2024-11-22 15:00:00','2024-11-23 10:00:00',NULL,'京东快递','JD9876543210',0,'2024-11-22 14:30:00','2025-11-27 11:44:17'),(3,'20241125001003',2,168.00,148.00,20.00,0.00,NULL,'alipay','completed','李红','13800138002','上海市上海市浦东新区陆家嘴金融中心88号',NULL,'2024-11-18 11:00:00','2024-11-19 08:00:00',NULL,'圆通快递','YT1122334455',1,'2024-11-18 10:30:00','2025-11-27 11:44:17'),(4,'20241125001004',3,398.00,328.00,70.00,0.00,NULL,'wechat','paid','王强','13800138003','广东省广州市天河区珠江新城华夏路30号',NULL,'2024-11-24 16:00:00',NULL,NULL,NULL,NULL,0,'2024-11-24 15:30:00','2025-11-27 11:44:17'),(5,'20241125001005',4,138.00,118.00,20.00,0.00,NULL,'wechat','pending','李娜','13800138004','浙江省杭州市西湖区西溪湿地北门18号',NULL,NULL,NULL,NULL,NULL,NULL,0,'2024-11-25 09:00:00','2025-11-27 11:44:17'),(6,'ORD2024112700006',1,368.00,338.00,30.00,0.00,1,'wechat','completed','张明','13800138001','北京市朝阳区建国路88号1号楼502室','','2024-11-20 14:30:00','2024-11-21 09:00:00','2024-11-24 15:00:00','顺丰快递','SF1234567890',1,'2025-11-27 11:51:01','2025-11-27 11:51:01'),(7,'ORD2024112700007',2,256.00,256.00,0.00,0.00,NULL,'alipay','completed','李红','13900139002','上海市浦东新区世纪大道100号3号楼1801室','','2024-11-18 16:20:00','2024-11-19 10:00:00','2024-11-22 11:00:00','中通快递','ZT9876543210',1,'2025-11-27 11:51:01','2025-11-27 11:51:01'),(8,'ORD2024112700008',3,189.00,169.00,20.00,0.00,2,'wechat','shipped','王伟','13700137003','广州市天河区体育西路123号天河城2层','请尽快发货','2024-11-24 09:15:00','2024-11-25 08:30:00',NULL,'京东物流','JD2024112508001',0,'2025-11-27 11:51:01','2025-11-27 11:51:01'),(9,'ORD2024112700009',4,99.00,99.00,0.00,0.00,NULL,'wechat','paid','李丽','13600136004','深圳市南山区科技园南区科苑路15号','','2024-11-25 20:00:00',NULL,NULL,NULL,NULL,0,'2025-11-27 11:51:01','2025-11-27 11:51:01'),(10,'ORD2024112700010',5,458.00,408.00,50.00,0.00,3,NULL,'pending','张强','13500135005','杭州市西湖区文三路388号钱江新城','',NULL,NULL,NULL,NULL,NULL,0,'2025-11-27 11:51:01','2025-11-27 11:51:01'),(11,'ORD2024112700011',1,528.00,528.00,0.00,0.00,NULL,'wechat','completed','张明','13800138001','北京市朝阳区建国路88号1号楼502室','','2024-11-15 11:00:00','2024-11-16 09:00:00','2024-11-19 14:00:00','顺丰快递','SF1122334455',1,'2025-11-27 11:51:01','2025-11-27 11:51:01'),(12,'ORD2024112700012',2,178.00,168.00,10.00,0.00,NULL,NULL,'cancelled','李红','13900139002','上海市浦东新区世纪大道100号3号楼1801室','买错了',NULL,NULL,NULL,NULL,NULL,0,'2025-11-27 11:51:01','2025-11-27 11:51:01'),(13,'ORD2024112700013',3,299.00,269.00,30.00,0.00,4,'alipay','refunded','王伟','13700137003','广州市天河区体育西路123号天河城2层','','2024-11-10 15:30:00','2024-11-11 09:00:00',NULL,'申通快递','ST5566778899',0,'2025-11-27 11:51:01','2025-11-27 11:51:01'),(14,'20251127204605663913',23,258.00,258.00,0.00,0.00,NULL,'wechat','paid','1','12312312321','上海市上海市浦东新区12','','2025-11-27 20:52:08',NULL,NULL,NULL,NULL,0,'2025-11-27 20:46:06','2025-11-27 20:52:08');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post_comments`
--

DROP TABLE IF EXISTS `post_comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `post_comments` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `post_id` bigint unsigned NOT NULL COMMENT '动态ID',
  `user_id` bigint unsigned NOT NULL COMMENT '评论者ID',
  `parent_id` bigint unsigned DEFAULT NULL COMMENT '父评论ID(回复)',
  `reply_to_user_id` bigint unsigned DEFAULT NULL COMMENT '被回复用户ID',
  `content` text NOT NULL COMMENT '评论内容',
  `like_count` int DEFAULT '0' COMMENT '点赞数',
  `status` tinyint DEFAULT '1' COMMENT '状态：0删除 1正常',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_post_id` (`post_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_parent_id` (`parent_id`),
  CONSTRAINT `post_comments_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE,
  CONSTRAINT `post_comments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='动态评论表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post_comments`
--

LOCK TABLES `post_comments` WRITE;
/*!40000 ALTER TABLE `post_comments` DISABLE KEYS */;
INSERT INTO `post_comments` VALUES (1,1,2,NULL,NULL,'太厉害了！我也要坚持跑步',12,1,'2025-11-27 11:43:16'),(2,1,3,NULL,NULL,'配速很稳啊，加油！',8,1,'2025-11-27 11:43:16'),(3,1,4,1,2,'一起加油！',3,1,'2025-11-27 11:43:16'),(4,2,1,NULL,NULL,'看起来很好吃，求详细食谱！',15,1,'2025-11-27 11:43:16'),(5,2,5,NULL,NULL,'牛油果是真的贵啊',6,1,'2025-11-27 11:43:16'),(6,3,1,NULL,NULL,'收藏了，明天就试试！',23,1,'2025-11-27 11:43:16'),(7,3,2,NULL,NULL,'这个动作我总是做不标准',11,1,'2025-11-27 11:43:16'),(8,3,4,2,2,'注意腰部要贴紧地面',8,1,'2025-11-27 11:43:16'),(9,4,3,NULL,NULL,'HIIT确实燃脂效果好',9,1,'2025-11-27 11:43:16'),(10,5,1,NULL,NULL,'太励志了！怎么做到的？',34,1,'2025-11-27 11:43:16'),(11,5,2,NULL,NULL,'羡慕！我也要加油',18,1,'2025-11-27 11:43:16'),(12,5,3,NULL,NULL,'减重20斤很不容易了，恭喜！',27,1,'2025-11-27 11:43:16'),(28,11,2,NULL,NULL,'厉害了！配速提升很明显，继续加油！',8,1,'2025-11-27 11:51:58'),(29,11,3,NULL,NULL,'跑步真的是最好的有氧运动',5,1,'2025-11-27 11:51:58'),(30,11,4,13,2,'谢谢鼓励！',2,1,'2025-11-27 11:51:58'),(31,12,1,NULL,NULL,'这套动作我也在练，确实很有效',12,1,'2025-11-27 11:51:58'),(32,12,5,NULL,NULL,'保存了，上班族太需要了',9,1,'2025-11-27 11:51:58'),(33,13,1,NULL,NULL,'王老师的身体素质真好，向您学习！',15,1,'2025-11-27 11:51:58'),(34,13,4,NULL,NULL,'太极拳我也在学，请问有什么要点吗？',7,1,'2025-11-27 11:51:58'),(35,14,1,NULL,NULL,'减肥30天瘦10斤，你太厉害了！',22,1,'2025-11-27 11:51:58'),(36,14,2,NULL,NULL,'求分享具体的饮食计划！',18,1,'2025-11-27 11:51:58'),(37,14,3,NULL,NULL,'坚持就是胜利，加油！',10,1,'2025-11-27 11:51:58'),(38,15,2,NULL,NULL,'新手能有这个意识很好，加油！',6,1,'2025-11-27 11:51:58'),(39,16,3,NULL,NULL,'看起来好健康，食谱分享一下呗',9,1,'2025-11-27 11:51:58'),(40,17,1,NULL,NULL,'产后妈妈辛苦了，这些动作很有用',11,1,'2025-11-27 11:51:58'),(41,18,1,NULL,NULL,'控糖100天效果这么好，太棒了！',28,1,'2025-11-27 11:51:58'),(42,18,2,NULL,NULL,'血糖降这么多，真是太了不起了',19,1,'2025-11-27 11:51:58');
/*!40000 ALTER TABLE `post_comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post_likes`
--

DROP TABLE IF EXISTS `post_likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `post_likes` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `post_id` bigint unsigned NOT NULL COMMENT '动态ID',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_post_user` (`post_id`,`user_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `post_likes_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE,
  CONSTRAINT `post_likes_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='动态点赞表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post_likes`
--

LOCK TABLES `post_likes` WRITE;
/*!40000 ALTER TABLE `post_likes` DISABLE KEYS */;
INSERT INTO `post_likes` VALUES (1,1,2,'2025-11-27 11:43:23'),(2,1,3,'2025-11-27 11:43:23'),(3,1,4,'2025-11-27 11:43:23'),(4,1,5,'2025-11-27 11:43:23'),(5,2,1,'2025-11-27 11:43:23'),(6,2,3,'2025-11-27 11:43:23'),(7,2,4,'2025-11-27 11:43:23'),(8,3,1,'2025-11-27 11:43:23'),(9,3,2,'2025-11-27 11:43:23'),(10,3,4,'2025-11-27 11:43:23'),(11,3,5,'2025-11-27 11:43:23'),(12,4,2,'2025-11-27 11:43:23'),(13,4,3,'2025-11-27 11:43:23'),(14,5,1,'2025-11-27 11:43:23'),(15,5,2,'2025-11-27 11:43:23'),(16,5,3,'2025-11-27 11:43:23'),(17,5,4,'2025-11-27 11:43:23'),(18,5,5,'2025-11-27 11:43:23'),(59,11,1,'2025-11-27 11:51:59'),(60,11,3,'2025-11-27 11:51:59'),(61,11,4,'2025-11-27 11:51:59'),(62,11,5,'2025-11-27 11:51:59'),(63,12,1,'2025-11-27 11:51:59'),(64,12,3,'2025-11-27 11:51:59'),(65,12,4,'2025-11-27 11:51:59'),(66,12,5,'2025-11-27 11:51:59'),(67,13,1,'2025-11-27 11:51:59'),(68,13,2,'2025-11-27 11:51:59'),(69,13,4,'2025-11-27 11:51:59'),(70,13,5,'2025-11-27 11:51:59'),(71,14,1,'2025-11-27 11:51:59'),(72,14,2,'2025-11-27 11:51:59'),(73,14,3,'2025-11-27 11:51:59'),(74,14,5,'2025-11-27 11:51:59'),(75,15,1,'2025-11-27 11:51:59'),(76,15,2,'2025-11-27 11:51:59'),(77,15,3,'2025-11-27 11:51:59'),(78,15,4,'2025-11-27 11:51:59'),(79,16,2,'2025-11-27 11:51:59'),(80,16,3,'2025-11-27 11:51:59'),(81,16,4,'2025-11-27 11:51:59'),(82,16,5,'2025-11-27 11:51:59'),(83,17,1,'2025-11-27 11:51:59'),(84,17,3,'2025-11-27 11:51:59'),(85,17,4,'2025-11-27 11:51:59'),(86,17,5,'2025-11-27 11:51:59'),(87,18,1,'2025-11-27 11:51:59'),(88,18,2,'2025-11-27 11:51:59'),(89,18,4,'2025-11-27 11:51:59'),(90,18,5,'2025-11-27 11:51:59'),(91,19,1,'2025-11-27 11:51:59'),(92,19,2,'2025-11-27 11:51:59'),(93,19,3,'2025-11-27 11:51:59'),(94,19,5,'2025-11-27 11:51:59'),(95,20,1,'2025-11-27 11:51:59'),(96,20,2,'2025-11-27 11:51:59'),(97,20,3,'2025-11-27 11:51:59'),(98,20,4,'2025-11-27 11:51:59');
/*!40000 ALTER TABLE `post_likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `posts`
--

DROP TABLE IF EXISTS `posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `posts` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '作者ID',
  `content` text NOT NULL COMMENT '内容',
  `images` json DEFAULT NULL COMMENT '图片JSON数组',
  `video_url` varchar(255) DEFAULT NULL COMMENT '视频URL',
  `topic_id` bigint unsigned DEFAULT NULL COMMENT '话题ID',
  `location` varchar(100) DEFAULT NULL COMMENT '位置',
  `view_count` int DEFAULT '0' COMMENT '浏览数',
  `like_count` int DEFAULT '0' COMMENT '点赞数',
  `comment_count` int DEFAULT '0' COMMENT '评论数',
  `share_count` int DEFAULT '0' COMMENT '分享数',
  `is_top` tinyint DEFAULT '0' COMMENT '是否置顶',
  `is_essence` tinyint DEFAULT '0' COMMENT '是否精华',
  `status` tinyint DEFAULT '1' COMMENT '状态：0删除 1正常 2审核中',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_topic_id` (`topic_id`),
  KEY `idx_created_at` (`created_at`),
  KEY `idx_status` (`status`),
  CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='动态/帖子表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `posts`
--

LOCK TABLES `posts` WRITE;
/*!40000 ALTER TABLE `posts` DISABLE KEYS */;
INSERT INTO `posts` VALUES (1,1,'坚持跑步第30天！今天完成了5公里，配速5分30秒，感觉越来越轻松了。给自己一个大大的赞！运动真的会上瘾，接下来挑战10公里！','[]',NULL,2,'北京·朝阳公园',2356,189,45,12,0,1,1,'2024-11-25 07:30:00','2025-11-27 11:42:56'),(2,2,'今天的早餐：牛油果鸡蛋三明治+无糖豆浆。高蛋白低碳水，减脂期也能吃得美味又营养！食谱分享给大家～','[]',NULL,3,'上海·家里',1890,156,38,8,0,0,1,'2024-11-25 08:00:00','2025-11-27 11:42:56'),(3,3,'分享一个超有效的腹部训练动作：死虫式。每天3组，每组15次，坚持一个月腹肌就出来了！动作要点：腰部紧贴地面，不要塌腰。','[]',NULL,5,'广州·健身房',3457,267,89,34,1,1,1,'2024-11-24 19:00:00','2025-11-27 20:31:28'),(4,1,'第一次尝试HIIT训练，20分钟下来汗流浃背！燃脂效果真的比跑步强太多了，推荐大家试试。','[]',NULL,1,'北京·家里',1234,98,23,5,0,0,1,'2024-11-24 18:30:00','2025-11-27 11:42:56'),(5,4,'减重20斤达成！从82斤到62斤，用了4个月时间。分享我的经验：控制饮食+有氧运动+力量训练缺一不可。','[]',NULL,1,'杭州',5678,456,123,67,1,1,1,'2024-11-23 20:00:00','2025-11-27 11:42:56'),(6,2,'今天的瑜伽打卡～睡前15分钟拉伸，整个人都放松了。最近睡眠质量明显提升，推荐失眠的朋友试试。','[]',NULL,4,'上海·家里',890,78,15,3,0,0,1,'2024-11-23 22:00:00','2025-11-27 11:42:56'),(7,5,'健身小白入门打卡Day1！今天学习了深蹲的正确姿势，教练说我的动作还不错，继续加油！','[]',NULL,5,'南京·健身房',567,45,12,2,0,0,1,'2024-11-22 19:30:00','2025-11-27 11:42:56'),(8,3,'今天去医院做了体检，各项指标都正常！坚持运动一年，血压血糖都达标了，健康就是最大的财富。','[]',NULL,6,'广州·医院',2345,189,56,23,0,1,1,'2024-11-21 15:00:00','2025-11-27 11:42:56'),(9,1,'入手了新的智能手环，可以实时监测心率，运动数据一目了然。推荐给想要科学健身的朋友们！','[]',NULL,7,'北京',1567,123,34,11,0,0,1,'2024-11-20 12:00:00','2025-11-27 11:42:56'),(10,4,'早起打卡Day50！每天6点起床，慢跑30分钟，感觉整个人精神状态都不一样了。早起真的会改变人生！','[]',NULL,8,'杭州·西湖',3890,312,78,45,0,1,1,'2024-11-19 06:30:00','2025-11-27 11:42:56'),(11,1,'今天完成了5公里跑步，配速5分30秒，感觉状态越来越好了！坚持就是胜利，大家一起加油！','[]',NULL,1,NULL,321,45,12,3,0,0,1,'2025-11-27 11:51:50','2025-11-27 20:03:59'),(12,2,'分享一套适合办公室做的颈椎瑜伽，每天10分钟，告别颈椎酸痛~','[]',NULL,2,NULL,560,68,23,7,0,1,1,'2025-11-27 11:51:50','2025-11-27 11:51:50'),(13,3,'老年人运动要注意循序渐进，我每天早上6点去公园太极拳，已经坚持3年了，身体棒棒的！','[]',NULL,3,NULL,891,92,31,11,1,1,1,'2025-11-27 11:51:50','2025-11-27 20:03:46'),(14,4,'减肥第30天打卡！体重从75kg降到70kg，分享我的饮食和运动计划，希望对大家有帮助！','[]',NULL,4,NULL,1200,156,48,18,1,1,1,'2025-11-27 11:51:50','2025-11-27 11:51:50'),(15,5,'新手健身第一周，动作还不太标准，但是能感觉到身体在变化，继续努力！','[]',NULL,5,NULL,180,28,9,1,0,0,1,'2025-11-27 11:51:50','2025-11-27 11:51:50'),(16,1,'今天做了一顿营养均衡的晚餐：鸡胸肉配西兰花，全麦饭，营养又美味！','[]',NULL,6,NULL,420,52,18,4,0,0,1,'2025-11-27 11:51:50','2025-11-27 11:51:50'),(17,2,'产后恢复瑜伽心得分享，这几个动作对骨盆恢复特别有帮助~','[]',NULL,7,NULL,650,78,26,8,0,1,1,'2025-11-27 11:51:50','2025-11-27 11:51:50'),(18,3,'控糖第100天，血糖从8.5降到了6.2，感谢家人的支持和自己的坚持！','[]',NULL,8,NULL,1850,203,65,25,1,1,1,'2025-11-27 11:51:50','2025-11-27 11:51:50'),(19,4,'今天去健身房做了HIIT，累得够呛但是超级爽！燃脂效果真的好！','[]',NULL,1,NULL,280,35,11,2,0,0,1,'2025-11-27 11:51:50','2025-11-27 11:51:50'),(20,5,'瑜伽冥想真的可以帮助睡眠，之前失眠严重，现在每晚睡前冥想15分钟，睡得特别好','[]',NULL,2,NULL,510,63,21,6,0,0,1,'2025-11-27 11:51:50','2025-11-27 11:51:50');
/*!40000 ALTER TABLE `posts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_categories`
--

DROP TABLE IF EXISTS `product_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_categories` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL COMMENT '分类名称',
  `parent_id` bigint unsigned DEFAULT NULL COMMENT '父分类ID',
  `icon` varchar(255) DEFAULT NULL COMMENT '分类图标',
  `sort_order` int DEFAULT '0' COMMENT '排序',
  `is_active` tinyint DEFAULT '1' COMMENT '是否启用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_parent_id` (`parent_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='商品分类表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_categories`
--

LOCK TABLES `product_categories` WRITE;
/*!40000 ALTER TABLE `product_categories` DISABLE KEYS */;
INSERT INTO `product_categories` VALUES (1,'营养补充',NULL,NULL,1,1,'2025-11-27 11:41:35'),(2,'健康食品',NULL,NULL,2,1,'2025-11-27 11:41:35'),(3,'运动装备',NULL,NULL,3,1,'2025-11-27 11:41:35'),(4,'健康器械',NULL,NULL,4,1,'2025-11-27 11:41:35'),(5,'蛋白粉',1,NULL,1,1,'2025-11-27 11:41:35'),(6,'维生素',1,NULL,2,1,'2025-11-27 11:41:35'),(7,'益生菌',1,NULL,3,1,'2025-11-27 11:41:35'),(8,'代餐食品',2,NULL,1,1,'2025-11-27 11:41:35'),(9,'坚果零食',2,NULL,2,1,'2025-11-27 11:41:35'),(10,'运动服饰',3,NULL,1,1,'2025-11-27 11:41:35'),(11,'运动配件',3,NULL,2,1,'2025-11-27 11:41:35'),(12,'智能设备',4,NULL,1,1,'2025-11-27 11:41:35'),(13,'康复器材',4,NULL,2,1,'2025-11-27 11:41:35'),(14,'增肌系列',1,NULL,1,1,'2025-11-27 12:03:24'),(15,'减脂系列',1,NULL,2,1,'2025-11-27 12:03:24'),(16,'综合维生素',2,NULL,1,1,'2025-11-27 12:03:24'),(17,'单一维生素',2,NULL,2,1,'2025-11-27 12:03:24'),(18,'深海鱼油',3,NULL,1,1,'2025-11-27 12:03:24'),(19,'磷虾油',3,NULL,2,1,'2025-11-27 12:03:24');
/*!40000 ALTER TABLE `product_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_collects`
--

DROP TABLE IF EXISTS `product_collects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_collects` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_product` (`user_id`,`product_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_product_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='商品收藏表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_collects`
--

LOCK TABLES `product_collects` WRITE;
/*!40000 ALTER TABLE `product_collects` DISABLE KEYS */;
/*!40000 ALTER TABLE `product_collects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_reviews`
--

DROP TABLE IF EXISTS `product_reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_reviews` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `product_id` bigint unsigned NOT NULL COMMENT '商品ID',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `order_id` bigint unsigned NOT NULL COMMENT '订单ID',
  `rating` tinyint NOT NULL COMMENT '评分 1-5',
  `content` text COMMENT '评价内容',
  `images` json DEFAULT NULL COMMENT '评价图片',
  `is_anonymous` tinyint DEFAULT '0' COMMENT '是否匿名',
  `reply_content` text COMMENT '商家回复',
  `reply_time` datetime DEFAULT NULL COMMENT '回复时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `status` tinyint DEFAULT '1' COMMENT '状态: 0隐藏 1显示',
  PRIMARY KEY (`id`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_user_id` (`user_id`),
  CONSTRAINT `product_reviews_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE,
  CONSTRAINT `product_reviews_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='商品评价表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_reviews`
--

LOCK TABLES `product_reviews` WRITE;
/*!40000 ALTER TABLE `product_reviews` DISABLE KEYS */;
INSERT INTO `product_reviews` VALUES (1,1,1,1,5,'蛋白粉口感很好，巧克力味很浓，溶解性也不错，健身必备！','[]',0,NULL,NULL,'2025-11-27 11:44:36',1),(2,6,2,3,4,'代餐奶昔味道还可以，饱腹感强，适合减脂期。','[]',0,NULL,NULL,'2025-11-27 11:44:36',1),(3,3,1,2,5,'每天一片，感觉精神好多了，性价比很高。','[]',0,NULL,NULL,'2025-11-27 11:44:36',1),(4,1,2,1,5,'蛋白粉口感很好，溶解性强，喝起来不腻，健身必备！','[]',0,NULL,NULL,'2025-11-27 11:50:28',1),(5,2,3,2,4,'维生素D效果不错，吃了一段时间感觉精神好多了','[]',0,NULL,NULL,'2025-11-27 11:50:28',1),(6,3,1,3,5,'深海鱼油胶囊很大颗，没有腥味，值得购买','[]',1,NULL,NULL,'2025-11-27 11:50:28',1),(7,4,4,4,5,'益生菌效果明显，肠道舒服多了','[]',0,NULL,NULL,'2025-11-27 11:50:28',1),(8,5,2,5,4,'代餐奶昔味道还行，饱腹感强，减肥期间很需要','[]',0,NULL,NULL,'2025-11-27 11:50:28',1),(9,6,1,1,5,'钙镁片很好，老人家吃着也方便','[]',0,NULL,NULL,'2025-11-27 11:50:28',1),(10,7,3,2,4,'燕麦代餐粉冲泡方便，早餐吃很合适','[]',0,NULL,NULL,'2025-11-27 11:50:28',1),(11,8,5,3,5,'护眼软糖孩子很喜欢吃，不用担心挑食','[]',0,NULL,NULL,'2025-11-27 11:50:28',1),(12,1,4,4,4,'第二次购买了，确实不错','[]',0,NULL,NULL,'2025-11-27 11:50:28',1),(13,2,5,5,5,'家人都在吃，补充维生素D很重要','[]',1,NULL,NULL,'2025-11-27 11:50:28',1);
/*!40000 ALTER TABLE `product_reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `category_id` bigint unsigned DEFAULT NULL COMMENT '分类ID',
  `name` varchar(100) NOT NULL COMMENT '商品名称',
  `subtitle` varchar(200) DEFAULT NULL COMMENT '副标题',
  `images` json DEFAULT NULL COMMENT '商品图片JSON数组',
  `description` text COMMENT '商品描述',
  `original_price` decimal(10,2) NOT NULL COMMENT '原价',
  `current_price` decimal(10,2) NOT NULL COMMENT '现价',
  `member_price` decimal(10,2) DEFAULT NULL COMMENT '会员价',
  `stock` int DEFAULT '0' COMMENT '库存',
  `sales_count` int DEFAULT '0' COMMENT '销量',
  `suitable_tags` json DEFAULT NULL COMMENT '适用标签(如低糖、高蛋白)',
  `health_tags` json DEFAULT NULL COMMENT '健康标签',
  `specs` json DEFAULT NULL COMMENT '规格选项JSON',
  `is_recommend` tinyint DEFAULT '0' COMMENT '是否推荐',
  `is_on_sale` tinyint DEFAULT '1' COMMENT '是否上架',
  `sort_order` int DEFAULT '0' COMMENT '排序',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_category_id` (`category_id`),
  KEY `idx_is_on_sale` (`is_on_sale`),
  KEY `idx_is_recommend` (`is_recommend`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `product_categories` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='商品表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,5,'乳清蛋白粉 巧克力味','增肌必备 优质蛋白 易吸收','[\"/static/placeholder/product.png\"]','采用优质乳清蛋白，每份含25g蛋白质，支持肌肉生长和恢复。适合健身人群日常补充。',298.00,258.00,238.00,499,2356,'[\"健身人群\", \"增肌需求\"]','[\"高蛋白\", \"低脂肪\"]','[{\"name\": \"规格\", \"values\": [\"1kg装\", \"2kg装\"]}]',1,1,100,'2025-11-27 11:42:00','2025-11-27 20:52:47'),(2,5,'分离乳清蛋白 原味','高纯度蛋白 零添加糖','[\"/static/placeholder/product.png\"]','90%以上蛋白含量，无添加糖，适合对营养有高要求的健身爱好者。',398.00,358.00,328.00,300,1289,'[\"专业健身\", \"比赛备战\"]','[\"超高蛋白\", \"零糖\"]','[{\"name\": \"规格\", \"values\": [\"1kg装\"]}]',1,1,99,'2025-11-27 11:42:00','2025-11-27 20:52:47'),(3,6,'复合维生素片','每日一片 营养全面','[\"/static/placeholder/product.png\"]','含20种维生素和矿物质，满足日常营养需求，提升免疫力。',168.00,128.00,108.00,800,5678,'[\"上班族\", \"学生\", \"老年人\"]','[\"增强免疫\", \"补充营养\"]','[{\"name\": \"规格\", \"values\": [\"60片装\", \"120片装\"]}]',1,1,98,'2025-11-27 11:42:00','2025-11-27 20:52:47'),(4,6,'维生素D3软胶囊','阳光维生素 强健骨骼','[\"/static/placeholder/product.png\"]','每粒含2000IU维生素D3，促进钙吸收，维护骨骼健康。',98.00,78.00,68.00,600,3456,'[\"缺乏日照人群\", \"老年人\"]','[\"补钙\", \"骨骼健康\"]','[{\"name\": \"规格\", \"values\": [\"90粒装\"]}]',0,1,97,'2025-11-27 11:42:00','2025-11-27 20:52:47'),(5,7,'益生菌粉','肠道健康 增强免疫','[\"/static/placeholder/product.png\"]','含100亿活性益生菌，改善肠道环境，提升消化功能。',198.00,168.00,148.00,400,2890,'[\"消化不良\", \"免疫力低\"]','[\"调节肠道\", \"促进消化\"]','[{\"name\": \"规格\", \"values\": [\"30袋装\"]}]',1,1,96,'2025-11-27 11:42:00','2025-11-27 20:52:47'),(6,8,'代餐奶昔 草莓味','低卡饱腹 营养均衡','[\"/static/placeholder/product.png\"]','每份仅180大卡，含丰富膳食纤维和蛋白质，代替正餐轻松控制热量。',168.00,138.00,118.00,350,4567,'[\"减重人群\", \"控制饮食\"]','[\"低卡路里\", \"高饱腹\"]','[{\"name\": \"规格\", \"values\": [\"15袋装\", \"30袋装\"]}]',1,1,95,'2025-11-27 11:42:00','2025-11-27 20:52:47'),(7,8,'燕麦代餐粉','天然谷物 营养早餐','[\"/static/placeholder/product.png\"]','精选澳洲燕麦，富含β-葡聚糖，帮助控制血糖和胆固醇。',88.00,68.00,58.00,500,3234,'[\"早餐替代\", \"三高人群\"]','[\"降血糖\", \"高纤维\"]','[{\"name\": \"规格\", \"values\": [\"500g装\"]}]',0,1,94,'2025-11-27 11:42:00','2025-11-27 20:52:47'),(8,9,'混合坚果 每日坚果','7种坚果 科学配比','[\"/static/placeholder/product.png\"]','每天一包，补充优质脂肪酸和维生素E，健康零食首选。',128.00,98.00,88.00,600,6789,'[\"办公零食\", \"健康加餐\"]','[\"补脑\", \"抗氧化\"]','[{\"name\": \"规格\", \"values\": [\"30包装\"]}]',1,1,93,'2025-11-27 11:42:00','2025-11-27 20:52:47'),(9,10,'速干运动T恤','透气速干 舒适运动','[\"/static/placeholder/product.png\"]','采用高科技速干面料，快速排汗，保持运动时干爽舒适。',168.00,128.00,108.00,200,1234,'[\"跑步\", \"健身\", \"户外\"]','[\"速干\", \"透气\"]','[{\"name\": \"尺码\", \"values\": [\"S码\", \"M码\", \"L码\", \"XL码\"]}]',0,1,92,'2025-11-27 11:42:00','2025-11-27 20:52:47'),(10,11,'运动护膝','专业防护 减少损伤','[\"/static/placeholder/product.png\"]','采用高弹力材质，稳定膝关节，适合跑步、篮球等运动。',98.00,78.00,68.00,300,2345,'[\"跑步\", \"球类运动\"]','[\"保护关节\", \"防止损伤\"]','[{\"name\": \"规格\", \"values\": [\"单只装\", \"一对装\"]}]',0,1,91,'2025-11-27 11:42:00','2025-11-27 20:52:47'),(11,12,'智能体脂秤','精准测量 数据同步','[\"/static/placeholder/product.png\"]','测量14项身体数据，蓝牙连接APP，追踪身体变化趋势。',298.00,198.00,168.00,150,3456,'[\"减重人群\", \"健身爱好者\"]','[\"精准测量\", \"数据追踪\"]','[{\"name\": \"颜色\", \"values\": [\"白色\", \"黑色\"]}]',1,1,90,'2025-11-27 11:42:00','2025-11-27 20:52:47'),(12,12,'智能手环','心率监测 运动追踪','[\"/static/placeholder/product.png\"]','24小时心率监测，运动数据实时同步，支持多种运动模式。',399.00,299.00,259.00,100,1890,'[\"运动监测\", \"健康管理\"]','[\"心率监测\", \"睡眠分析\"]','[{\"name\": \"颜色\", \"values\": [\"黑色\", \"蓝色\"]}]',1,1,89,'2025-11-27 11:42:00','2025-11-27 20:52:47'),(13,1,'增肌蛋白粉 香草味 2kg','促进肌肉生长，运动后必备','[\"/static/placeholder/product.png\"]','高品质乳清蛋白，助力增肌',358.00,298.00,268.00,200,580,'[\"健身人群\", \"增肌\"]','[\"蛋白质补充\"]','[{\"name\": \"规格\", \"values\": [\"1kg\", \"2kg\"]}]',1,1,1,'2025-11-27 12:00:12','2025-11-27 20:52:47'),(14,2,'维生素C泡腾片 100片','增强免疫力，美白养颜','[\"/static/placeholder/product.png\"]','每日一片，补充维C',58.00,45.00,39.00,500,1200,'[\"全人群\"]','[\"免疫力\", \"美白\"]','[{\"name\": \"规格\", \"values\": [\"50片\", \"100片\"]}]',1,1,2,'2025-11-27 12:00:12','2025-11-27 20:52:47'),(15,3,'鳕鱼油软胶囊 90粒','DHA+EPA，健脑护眼','[\"/static/placeholder/product.png\"]','深海鳕鱼提取，品质保证',198.00,158.00,138.00,150,320,'[\"学生\", \"上班族\"]','[\"护眼\", \"健脑\"]','[{\"name\": \"规格\", \"values\": [\"60粒\", \"90粒\"]}]',0,1,3,'2025-11-27 12:00:12','2025-11-27 20:52:47'),(16,4,'乳酸菌饮品 12瓶装','调理肠胃，增强消化','[\"/static/placeholder/product.png\"]','活性乳酸菌，肠道好帮手',88.00,68.00,58.00,300,890,'[\"全人群\"]','[\"肠道健康\"]','[{\"name\": \"规格\", \"values\": [\"6瓶\", \"12瓶\"]}]',1,1,4,'2025-11-27 12:00:12','2025-11-27 20:52:47'),(17,5,'代餐蛋白棒 10支装','低卡高蛋白，代餐好选择','[\"/static/placeholder/product.png\"]','便携代餐，健康美味',158.00,128.00,108.00,250,450,'[\"减肥人群\", \"上班族\"]','[\"代餐\", \"蛋白质\"]','[{\"name\": \"口味\", \"values\": [\"巧克力\", \"花生\"]}]',0,1,5,'2025-11-27 12:00:12','2025-11-27 20:52:47'),(18,6,'葡萄糖酸钙口服液 20支','液体钙更易吸收','[\"/static/placeholder/product.png\"]','适合全家补钙',78.00,58.00,48.00,400,560,'[\"老人\", \"儿童\"]','[\"补钙\"]','[{\"name\": \"规格\", \"values\": [\"10支\", \"20支\"]}]',1,1,6,'2025-11-27 12:00:12','2025-11-27 20:52:47'),(19,7,'红豆薏米代餐粉 500g','祛湿消肿，健康代餐','[\"/static/placeholder/product.png\"]','天然食材，健康美味',89.00,69.00,59.00,280,720,'[\"减肥人群\", \"湿气重\"]','[\"祛湿\", \"代餐\"]','[{\"name\": \"规格\", \"values\": [\"250g\", \"500g\"]}]',1,1,7,'2025-11-27 12:00:12','2025-11-27 20:52:47'),(20,8,'叶黄素护眼片 60片','缓解眼疲劳，保护视力','[\"/static/placeholder/product.png\"]','电脑族必备护眼产品',148.00,118.00,98.00,180,380,'[\"学生\", \"上班族\"]','[\"护眼\"]','[{\"name\": \"规格\", \"values\": [\"30片\", \"60片\"]}]',0,1,8,'2025-11-27 12:00:12','2025-11-27 20:52:47');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sport_goals`
--

DROP TABLE IF EXISTS `sport_goals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sport_goals` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `goal_type` varchar(50) NOT NULL COMMENT '目标类型：daily_steps/weekly_distance等',
  `target_value` int NOT NULL COMMENT '目标值',
  `current_value` int DEFAULT '0' COMMENT '当前进度',
  `unit` varchar(20) DEFAULT NULL COMMENT '单位',
  `start_date` date NOT NULL COMMENT '开始日期',
  `end_date` date NOT NULL COMMENT '结束日期',
  `status` enum('active','completed','failed') DEFAULT 'active' COMMENT '状态',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  CONSTRAINT `sport_goals_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='运动目标表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sport_goals`
--

LOCK TABLES `sport_goals` WRITE;
/*!40000 ALTER TABLE `sport_goals` DISABLE KEYS */;
INSERT INTO `sport_goals` VALUES (1,1,'duration',150,120,'分钟','2024-11-18','2024-11-24','active','2025-11-27 11:49:42','2025-11-27 11:49:42'),(2,1,'calories',2000,1850,'大卡','2024-11-18','2024-11-24','active','2025-11-27 11:49:42','2025-11-27 11:49:42'),(3,1,'distance',30000,25000,'米','2024-11-18','2024-11-24','active','2025-11-27 11:49:42','2025-11-27 11:49:42'),(4,2,'duration',120,90,'分钟','2024-11-18','2024-11-24','active','2025-11-27 11:49:42','2025-11-27 11:49:42'),(5,2,'sessions',5,4,'次','2024-11-18','2024-11-24','active','2025-11-27 11:49:42','2025-11-27 11:49:42'),(6,3,'duration',60,60,'分钟','2024-11-25','2024-11-25','completed','2025-11-27 11:49:42','2025-11-27 11:49:42'),(7,3,'steps',8000,8500,'步','2024-11-25','2024-11-25','completed','2025-11-27 11:49:42','2025-11-27 11:49:42'),(8,4,'calories',300,280,'大卡','2024-11-25','2024-11-25','active','2025-11-27 11:49:42','2025-11-27 11:49:42'),(9,5,'duration',45,45,'分钟','2024-11-25','2024-11-25','completed','2025-11-27 11:49:42','2025-11-27 11:49:42');
/*!40000 ALTER TABLE `sport_goals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sport_records`
--

DROP TABLE IF EXISTS `sport_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sport_records` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `sport_type` varchar(50) NOT NULL COMMENT '运动类型：running/cycling/walking/fitness等',
  `sport_name` varchar(50) DEFAULT NULL COMMENT '运动名称',
  `duration` int NOT NULL COMMENT '运动时长(秒)',
  `distance` decimal(10,2) DEFAULT NULL COMMENT '运动距离(米)',
  `calories` int DEFAULT '0' COMMENT '消耗卡路里',
  `avg_pace` decimal(5,2) DEFAULT NULL COMMENT '平均配速(分/公里)',
  `avg_heart_rate` int DEFAULT NULL COMMENT '平均心率',
  `max_heart_rate` int DEFAULT NULL COMMENT '最大心率',
  `elevation_gain` decimal(8,2) DEFAULT NULL COMMENT '累计爬升(米)',
  `gps_track` json DEFAULT NULL COMMENT 'GPS轨迹JSON数组',
  `weather` varchar(20) DEFAULT NULL COMMENT '天气',
  `feeling` tinyint DEFAULT '3' COMMENT '运动感受1-5',
  `notes` text COMMENT '备注',
  `course_id` bigint unsigned DEFAULT NULL COMMENT '课程ID(如果是跟练)',
  `coins_earned` int DEFAULT '0' COMMENT '获得运动币',
  `start_time` datetime NOT NULL COMMENT '开始时间',
  `end_time` datetime NOT NULL COMMENT '结束时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_sport_type` (`sport_type`),
  KEY `idx_start_time` (`start_time`),
  CONSTRAINT `sport_records_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='运动记录表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sport_records`
--

LOCK TABLES `sport_records` WRITE;
/*!40000 ALTER TABLE `sport_records` DISABLE KEYS */;
INSERT INTO `sport_records` VALUES (1,1,'running','晨跑',35,5000.00,320,7.00,145,168,NULL,NULL,'晴',4,'今天状态不错，配速很稳',NULL,3,'2024-11-25 06:30:00','2024-11-25 07:05:00','2025-11-27 11:43:36'),(2,1,'strength','力量训练',60,NULL,280,NULL,125,150,NULL,NULL,'室内',4,'练了胸和三头',NULL,6,'2024-11-24 18:00:00','2024-11-24 19:00:00','2025-11-27 11:43:36'),(3,1,'running','夜跑',40,6000.00,385,6.67,150,172,NULL,NULL,'多云',5,'突破个人最好成绩',NULL,4,'2024-11-23 20:00:00','2024-11-23 20:40:00','2025-11-27 11:43:36'),(4,2,'yoga','晨间瑜伽',30,NULL,90,NULL,95,110,NULL,NULL,'室内',5,'感觉身体很舒展',NULL,3,'2024-11-25 07:00:00','2024-11-25 07:30:00','2025-11-27 11:43:36'),(5,2,'cycling','骑行',45,15000.00,350,NULL,135,155,NULL,NULL,'晴',4,'沿江骑行，风景很好',NULL,4,'2024-11-24 16:00:00','2024-11-24 16:45:00','2025-11-27 11:43:36'),(6,3,'walking','散步',60,5000.00,180,12.00,100,115,NULL,NULL,'晴',4,'和老伴一起散步',NULL,6,'2024-11-25 06:00:00','2024-11-25 07:00:00','2025-11-27 11:43:36'),(7,4,'hiit','HIIT燃脂',25,NULL,280,NULL,155,178,NULL,NULL,'室内',4,'跟着课程练的',NULL,2,'2024-11-25 19:00:00','2024-11-25 19:25:00','2025-11-27 11:43:36'),(8,4,'rope_jumping','跳绳',20,NULL,220,NULL,150,170,NULL,NULL,'室内',3,'跳了2000个',NULL,2,'2024-11-24 19:30:00','2024-11-24 19:50:00','2025-11-27 11:43:36'),(9,5,'strength','新手力量训练',45,NULL,200,NULL,120,145,NULL,NULL,'室内',3,'第一次练器械，有点累',NULL,4,'2024-11-25 18:00:00','2024-11-25 18:45:00','2025-11-27 11:43:36'),(10,1,'running','户外跑步',35,5.20,320,6.73,142,168,NULL,NULL,'sunny',4,'早晨跑步',NULL,15,'2024-11-20 07:00:00','2024-11-20 07:35:00','2025-11-27 11:55:27'),(11,1,'cycling','骑行',45,12.00,280,NULL,128,152,NULL,NULL,'cloudy',4,'下班骑行',NULL,12,'2024-11-21 18:00:00','2024-11-21 18:45:00','2025-11-27 11:55:27'),(12,2,'yoga','瑜伽',60,NULL,180,NULL,95,110,NULL,NULL,'indoor',5,'晨间瑜伽',NULL,20,'2024-11-20 06:30:00','2024-11-20 07:30:00','2025-11-27 11:55:27'),(13,2,'swimming','游泳',40,1.00,350,NULL,135,158,NULL,NULL,'indoor',4,'游泳健身',NULL,18,'2024-11-22 19:00:00','2024-11-22 19:40:00','2025-11-27 11:55:27'),(14,3,'walking','散步',60,5.00,200,12.00,85,100,NULL,NULL,'sunny',5,'公园散步',NULL,10,'2024-11-20 06:00:00','2024-11-20 07:00:00','2025-11-27 11:55:27'),(15,3,'tai_chi','太极拳',45,NULL,120,NULL,75,88,NULL,NULL,'sunny',5,'太极拳练习',NULL,15,'2024-11-21 06:00:00','2024-11-21 06:45:00','2025-11-27 11:55:27'),(16,4,'hiit','HIIT训练',25,NULL,300,NULL,155,180,NULL,NULL,'indoor',3,'HIIT训练',NULL,20,'2024-11-23 20:00:00','2024-11-23 20:25:00','2025-11-27 11:55:27'),(17,4,'strength','力量训练',50,NULL,250,NULL,120,145,NULL,NULL,'indoor',4,'力量训练',NULL,18,'2024-11-24 19:00:00','2024-11-24 19:50:00','2025-11-27 11:55:27'),(18,5,'running','跑步',20,2.50,180,8.00,138,162,NULL,NULL,'cloudy',3,'新手跑步',NULL,8,'2024-11-24 07:30:00','2024-11-24 07:50:00','2025-11-27 11:55:27'),(19,5,'yoga','睡前瑜伽',30,NULL,90,NULL,88,105,NULL,NULL,'indoor',5,'睡前瑜伽',NULL,10,'2024-11-25 21:00:00','2024-11-25 21:30:00','2025-11-27 11:55:27'),(20,1,'strength','健身房力量',60,NULL,320,NULL,125,150,NULL,NULL,'indoor',4,'健身房力量训练',NULL,22,'2024-11-22 19:00:00','2024-11-22 20:00:00','2025-11-27 11:55:27'),(21,2,'pilates','普拉提',45,NULL,160,NULL,100,118,NULL,NULL,'indoor',5,'普拉提课程',NULL,15,'2024-11-23 10:00:00','2024-11-23 10:45:00','2025-11-27 11:55:27');
/*!40000 ALTER TABLE `sport_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_configs`
--

DROP TABLE IF EXISTS `system_configs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_configs` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `config_key` varchar(100) NOT NULL COMMENT '配置键',
  `config_value` text COMMENT '配置值',
  `description` varchar(200) DEFAULT NULL COMMENT '描述',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `config_key` (`config_key`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='系统配置表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_configs`
--

LOCK TABLES `system_configs` WRITE;
/*!40000 ALTER TABLE `system_configs` DISABLE KEYS */;
INSERT INTO `system_configs` VALUES (1,'checkin_base_reward','5','打卡基础奖励积分','2025-11-27 11:46:27','2025-11-27 11:46:27'),(2,'checkin_continuous_multiplier','1','连续打卡奖励倍数','2025-11-27 11:46:27','2025-11-27 11:46:27'),(3,'checkin_max_multiplier','5','连续打卡最大倍数','2025-11-27 11:46:27','2025-11-27 11:46:27'),(4,'sport_coin_per_minute','0.1','每分钟运动获得运动币','2025-11-27 11:46:27','2025-11-27 11:46:27'),(5,'food_coin_per_record','3','每条饮食记录获得膳食币','2025-11-27 11:46:27','2025-11-27 11:46:27'),(6,'member_month_price','19.90','月卡会员价格','2025-11-27 11:46:27','2025-11-27 11:46:27'),(7,'member_year_price','168.00','年卡会员价格','2025-11-27 11:46:27','2025-11-27 11:46:27'),(8,'member_lifetime_price','399.00','终身会员价格','2025-11-27 11:46:27','2025-11-27 11:46:27'),(9,'points_to_rmb_rate','10','积分兑换比例（10积分=1元）','2025-11-27 11:46:27','2025-11-27 11:46:27'),(10,'order_auto_cancel_minutes','30','未支付订单自动取消时间（分钟）','2025-11-27 11:46:27','2025-11-27 11:46:27'),(11,'order_auto_confirm_days','7','发货后自动确认收货天数','2025-11-27 11:46:27','2025-11-27 11:46:27');
/*!40000 ALTER TABLE `system_configs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topics`
--

DROP TABLE IF EXISTS `topics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `topics` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL COMMENT '话题名称',
  `description` varchar(200) DEFAULT NULL COMMENT '话题描述',
  `cover_image` varchar(255) DEFAULT NULL COMMENT '封面图',
  `post_count` int DEFAULT '0' COMMENT '帖子数量',
  `participant_count` int DEFAULT '0' COMMENT '参与人数',
  `is_hot` tinyint DEFAULT '0' COMMENT '是否热门',
  `sort_order` int DEFAULT '0' COMMENT '排序',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_name` (`name`),
  KEY `idx_is_hot` (`is_hot`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='话题表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topics`
--

LOCK TABLES `topics` WRITE;
/*!40000 ALTER TABLE `topics` DISABLE KEYS */;
INSERT INTO `topics` VALUES (1,'减脂打卡','记录你的减脂之旅，一起见证蜕变',NULL,2356,8900,1,100,'2025-11-27 11:43:10'),(2,'跑步爱好者','跑步让生活更美好',NULL,1890,6780,1,99,'2025-11-27 11:43:10'),(3,'健康饮食','分享健康美味的食谱',NULL,3456,12340,1,98,'2025-11-27 11:43:10'),(4,'瑜伽时光','瑜伽让身心放松',NULL,1234,4560,1,97,'2025-11-27 11:43:10'),(5,'力量训练','增肌塑形交流区',NULL,890,3450,0,96,'2025-11-27 11:43:10'),(6,'健身问答','有问必答，互帮互助',NULL,567,2340,0,95,'2025-11-27 11:43:10'),(7,'运动装备','分享好用的运动装备',NULL,456,1890,0,94,'2025-11-27 11:43:10'),(8,'早起打卡','早起的鸟儿有虫吃',NULL,2890,9870,1,93,'2025-11-27 11:43:10'),(9,'营养早餐','分享你的营养早餐',NULL,128,560,1,1,'2025-11-27 12:00:32'),(10,'健身打卡','每日健身记录',NULL,356,890,1,2,'2025-11-27 12:00:32'),(11,'控糖日记','控糖心得分享',NULL,89,320,0,3,'2025-11-27 12:00:32'),(12,'素食生活','素食爱好者交流',NULL,67,280,0,4,'2025-11-27 12:00:32'),(13,'跑步圈','跑步爱好者聚集地',NULL,234,670,1,5,'2025-11-27 12:00:32'),(14,'产后恢复','产后妈妈交流',NULL,78,240,0,6,'2025-11-27 12:00:32'),(15,'中老年养生','适合中老年的养生方法',NULL,156,480,1,7,'2025-11-27 12:00:32'),(16,'睡眠改善','改善睡眠质量',NULL,98,360,0,8,'2025-11-27 12:00:32');
/*!40000 ALTER TABLE `topics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_addresses`
--

DROP TABLE IF EXISTS `user_addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_addresses` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `receiver_name` varchar(50) NOT NULL COMMENT '收货人',
  `receiver_phone` varchar(20) NOT NULL COMMENT '收货电话',
  `province` varchar(50) NOT NULL COMMENT '省',
  `city` varchar(50) NOT NULL COMMENT '市',
  `district` varchar(50) NOT NULL COMMENT '区',
  `detail` varchar(200) NOT NULL COMMENT '详细地址',
  `is_default` tinyint DEFAULT '0' COMMENT '是否默认地址',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  CONSTRAINT `user_addresses_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户收货地址表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_addresses`
--

LOCK TABLES `user_addresses` WRITE;
/*!40000 ALTER TABLE `user_addresses` DISABLE KEYS */;
INSERT INTO `user_addresses` VALUES (1,1,'张明','13800138001','北京市','北京市','朝阳区','望京街道望京SOHO T1 1501',1,'2025-11-27 11:41:28','2025-11-27 11:41:28'),(2,1,'张明','13800138001','北京市','北京市','海淀区','中关村大街1号',0,'2025-11-27 11:41:28','2025-11-27 11:41:28'),(3,2,'李红','13800138002','上海市','上海市','浦东新区','陆家嘴金融中心88号',1,'2025-11-27 11:41:28','2025-11-27 11:41:28'),(4,3,'王强','13800138003','广东省','广州市','天河区','珠江新城华夏路30号',1,'2025-11-27 11:41:28','2025-11-27 11:41:28'),(5,4,'李娜','13800138004','浙江省','杭州市','西湖区','西溪湿地北门18号',1,'2025-11-27 11:41:28','2025-11-27 11:41:28'),(6,5,'张伟','13800138005','江苏省','南京市','鼓楼区','新街口商圈金鹰国际',1,'2025-11-27 11:41:28','2025-11-27 11:41:28'),(7,1,'张明','13800138001','北京市','北京市','海淀区','中关村科技园区1号楼101室',0,'2025-11-27 12:00:51','2025-11-27 12:00:51'),(8,2,'李红','13900139002','上海市','上海市','静安区','南京西路1000号2501室',0,'2025-11-27 12:00:51','2025-11-27 12:00:51'),(9,3,'王伟','13700137003','广东省','深圳市','福田区','华强北商业中心3楼',0,'2025-11-27 12:00:51','2025-11-27 12:00:51'),(10,4,'李丽','13600136004','浙江省','杭州市','滨江区','网易科技园B座8楼',0,'2025-11-27 12:00:51','2025-11-27 12:00:51'),(11,5,'张强','13500135005','江苏省','南京市','鼓楼区','新街口广场A区12号',0,'2025-11-27 12:00:51','2025-11-27 12:00:51'),(12,22,'1','12312312323','广东省','深圳市','南山区','123',1,'2025-11-27 20:29:20','2025-11-27 20:29:28'),(13,23,'1','12312312321','上海市','上海市','浦东新区','12',1,'2025-11-27 20:46:03','2025-11-27 20:46:03');
/*!40000 ALTER TABLE `user_addresses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_coupons`
--

DROP TABLE IF EXISTS `user_coupons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_coupons` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `coupon_id` bigint unsigned NOT NULL COMMENT '优惠券ID',
  `status` enum('unused','used','expired') DEFAULT 'unused' COMMENT '状态',
  `used_time` datetime DEFAULT NULL COMMENT '使用时间',
  `order_id` bigint unsigned DEFAULT NULL COMMENT '使用的订单ID',
  `received_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '领取时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_coupon_id` (`coupon_id`),
  KEY `idx_status` (`status`),
  CONSTRAINT `user_coupons_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `user_coupons_ibfk_2` FOREIGN KEY (`coupon_id`) REFERENCES `coupons` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户优惠券表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_coupons`
--

LOCK TABLES `user_coupons` WRITE;
/*!40000 ALTER TABLE `user_coupons` DISABLE KEYS */;
INSERT INTO `user_coupons` VALUES (1,1,1,'used',NULL,NULL,'2024-11-15 10:00:00'),(2,1,2,'unused',NULL,NULL,'2024-11-20 10:00:00'),(3,1,4,'unused',NULL,NULL,'2024-11-22 10:00:00'),(4,2,1,'used',NULL,NULL,'2024-11-10 10:00:00'),(5,2,3,'unused',NULL,NULL,'2024-11-18 10:00:00'),(6,3,2,'unused',NULL,NULL,'2024-11-15 10:00:00'),(7,3,4,'unused',NULL,NULL,'2024-11-20 10:00:00'),(8,4,1,'used',NULL,NULL,'2024-11-20 10:00:00'),(9,4,5,'unused',NULL,NULL,'2024-11-22 10:00:00'),(10,5,1,'unused',NULL,NULL,'2024-11-24 10:00:00'),(11,1,7,'unused',NULL,NULL,'2025-11-27 12:01:43'),(12,1,8,'unused',NULL,NULL,'2025-11-27 12:01:43'),(13,2,7,'used','2024-11-18 16:20:00',7,'2025-11-27 12:01:43'),(14,2,9,'unused',NULL,NULL,'2025-11-27 12:01:43'),(15,3,7,'unused',NULL,NULL,'2025-11-27 12:01:43'),(16,3,10,'unused',NULL,NULL,'2025-11-27 12:01:43'),(17,4,8,'expired',NULL,NULL,'2025-11-27 12:01:43'),(18,5,7,'unused',NULL,NULL,'2025-11-27 12:01:43'),(19,5,9,'unused',NULL,NULL,'2025-11-27 12:01:43');
/*!40000 ALTER TABLE `user_coupons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_course_collects`
--

DROP TABLE IF EXISTS `user_course_collects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_course_collects` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `course_id` bigint unsigned NOT NULL COMMENT '课程ID',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_course` (`user_id`,`course_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `user_course_collects_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `user_course_collects_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户收藏课程表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_course_collects`
--

LOCK TABLES `user_course_collects` WRITE;
/*!40000 ALTER TABLE `user_course_collects` DISABLE KEYS */;
INSERT INTO `user_course_collects` VALUES (1,1,1,'2025-11-27 11:45:09'),(2,1,2,'2025-11-27 11:45:09'),(3,1,5,'2025-11-27 11:45:09'),(4,2,3,'2025-11-27 11:45:09'),(5,2,6,'2025-11-27 11:45:09'),(6,2,8,'2025-11-27 11:45:09'),(7,3,3,'2025-11-27 11:45:09'),(8,3,6,'2025-11-27 11:45:09'),(9,4,1,'2025-11-27 11:45:09'),(10,4,6,'2025-11-27 11:45:09'),(11,4,7,'2025-11-27 11:45:09'),(12,5,1,'2025-11-27 11:45:09'),(13,5,4,'2025-11-27 11:45:09'),(14,5,5,'2025-11-27 11:45:09'),(15,1,11,'2025-11-27 11:59:44'),(16,1,12,'2025-11-27 11:59:44'),(17,1,13,'2025-11-27 11:59:44'),(18,2,12,'2025-11-27 11:59:44'),(19,2,15,'2025-11-27 11:59:44'),(20,2,19,'2025-11-27 11:59:44'),(21,3,14,'2025-11-27 11:59:44'),(22,3,17,'2025-11-27 11:59:44'),(23,3,20,'2025-11-27 11:59:44'),(24,4,11,'2025-11-27 11:59:44'),(25,4,13,'2025-11-27 11:59:44'),(26,4,16,'2025-11-27 11:59:44'),(27,4,18,'2025-11-27 11:59:44'),(28,5,11,'2025-11-27 11:59:44'),(29,5,12,'2025-11-27 11:59:44'),(30,5,14,'2025-11-27 11:59:44'),(31,5,15,'2025-11-27 11:59:44');
/*!40000 ALTER TABLE `user_course_collects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_follows`
--

DROP TABLE IF EXISTS `user_follows`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_follows` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '关注者ID',
  `follow_user_id` bigint unsigned NOT NULL COMMENT '被关注者ID',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_follow` (`user_id`,`follow_user_id`),
  KEY `follow_user_id` (`follow_user_id`),
  CONSTRAINT `user_follows_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `user_follows_ibfk_2` FOREIGN KEY (`follow_user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户关注表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_follows`
--

LOCK TABLES `user_follows` WRITE;
/*!40000 ALTER TABLE `user_follows` DISABLE KEYS */;
INSERT INTO `user_follows` VALUES (1,1,2,'2025-11-27 11:43:24'),(2,1,3,'2025-11-27 11:43:24'),(3,1,4,'2025-11-27 11:43:24'),(4,2,1,'2025-11-27 11:43:24'),(5,2,3,'2025-11-27 11:43:24'),(6,2,5,'2025-11-27 11:43:24'),(7,3,1,'2025-11-27 11:43:24'),(8,3,2,'2025-11-27 11:43:24'),(9,4,1,'2025-11-27 11:43:24'),(10,4,2,'2025-11-27 11:43:24'),(11,4,3,'2025-11-27 11:43:24'),(12,4,5,'2025-11-27 11:43:24'),(13,5,1,'2025-11-27 11:43:24'),(14,5,3,'2025-11-27 11:43:24');
/*!40000 ALTER TABLE `user_follows` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_health_profiles`
--

DROP TABLE IF EXISTS `user_health_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_health_profiles` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `health_goal` varchar(50) DEFAULT NULL COMMENT '健康目标',
  `target_weight` decimal(5,2) DEFAULT NULL COMMENT '目标体重',
  `preferred_sports` json DEFAULT NULL COMMENT '偏好运动类型',
  `daily_exercise_minutes` int DEFAULT '30' COMMENT '每日期望运动时长(分钟)',
  `has_injury` tinyint DEFAULT '0' COMMENT '是否有伤病',
  `injury_description` text COMMENT '伤病描述',
  `chronic_diseases` json DEFAULT NULL COMMENT '慢性病',
  `pushup_count` int DEFAULT NULL COMMENT '俯卧撑数量',
  `squat_count` int DEFAULT NULL COMMENT '深蹲数量',
  `crunch_count` int DEFAULT NULL COMMENT '卷腹数量',
  `climb_stairs_tired` tinyint DEFAULT NULL COMMENT '爬5层楼是否疲劳',
  `diet_habit` varchar(50) DEFAULT NULL COMMENT '饮食习惯',
  `allergies` json DEFAULT NULL COMMENT '过敏食物',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_id` (`user_id`),
  CONSTRAINT `user_health_profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户健康档案表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_health_profiles`
--

LOCK TABLES `user_health_profiles` WRITE;
/*!40000 ALTER TABLE `user_health_profiles` DISABLE KEYS */;
INSERT INTO `user_health_profiles` VALUES (1,1,'增肌减脂',68.00,'[\"running\", \"strength\", \"swimming\"]',60,0,NULL,NULL,NULL,NULL,NULL,NULL,'均衡饮食',NULL,'2025-11-27 11:41:23','2025-11-27 11:41:23'),(2,2,'保持体重',55.00,'[\"yoga\", \"dancing\", \"cycling\"]',45,0,NULL,NULL,NULL,NULL,NULL,NULL,'素食为主','[\"海鲜\"]','2025-11-27 11:41:23','2025-11-27 11:41:23'),(3,3,'健康养生',65.00,'[\"walking\", \"tai_chi\"]',30,0,NULL,'[\"高血压\"]',NULL,NULL,NULL,NULL,'低盐饮食',NULL,'2025-11-27 11:41:23','2025-11-27 11:41:23'),(4,4,'减重塑形',48.00,'[\"hiit\", \"rope_jumping\", \"running\"]',60,0,NULL,NULL,NULL,NULL,NULL,NULL,'低碳饮食','[\"牛奶\"]','2025-11-27 11:41:23','2025-11-27 11:41:23'),(5,5,'增强体质',75.00,'[\"strength\", \"running\"]',45,1,NULL,NULL,NULL,NULL,NULL,NULL,'高蛋白',NULL,'2025-11-27 11:41:23','2025-11-27 11:41:23');
/*!40000 ALTER TABLE `user_health_profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_task_records`
--

DROP TABLE IF EXISTS `user_task_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_task_records` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `task_id` bigint unsigned NOT NULL COMMENT '任务ID',
  `task_date` date NOT NULL COMMENT '任务日期',
  `current_value` int DEFAULT '0' COMMENT '当前进度',
  `is_completed` tinyint DEFAULT '0' COMMENT '是否完成',
  `is_claimed` tinyint(1) DEFAULT '0' COMMENT '是否已领取奖励',
  `is_rewarded` tinyint DEFAULT '0' COMMENT '是否已领取奖励',
  `completed_at` datetime DEFAULT NULL COMMENT '完成时间',
  `claimed_at` datetime DEFAULT NULL COMMENT '领取奖励时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_task_date` (`user_id`,`task_id`,`task_date`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_task_date` (`task_date`),
  KEY `task_id` (`task_id`),
  CONSTRAINT `user_task_records_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `user_task_records_ibfk_2` FOREIGN KEY (`task_id`) REFERENCES `daily_tasks` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户任务记录表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_task_records`
--

LOCK TABLES `user_task_records` WRITE;
/*!40000 ALTER TABLE `user_task_records` DISABLE KEYS */;
INSERT INTO `user_task_records` VALUES (1,1,1,'2024-11-25',1,1,0,1,'2024-11-25 07:00:00',NULL,'2025-11-27 11:45:29','2025-11-27 11:45:29'),(2,1,2,'2024-11-25',35,1,0,1,'2024-11-25 07:35:00',NULL,'2025-11-27 11:45:29','2025-11-27 11:45:29'),(3,1,3,'2024-11-25',3,1,0,0,'2024-11-25 19:00:00',NULL,'2025-11-27 11:45:29','2025-11-27 11:45:29'),(4,1,4,'2024-11-25',320,1,0,1,'2024-11-25 07:35:00',NULL,'2025-11-27 11:45:29','2025-11-27 11:45:29'),(5,2,1,'2024-11-25',1,1,0,1,'2024-11-25 07:30:00',NULL,'2025-11-27 11:45:29','2025-11-27 11:45:29'),(6,2,2,'2024-11-25',30,1,0,0,'2024-11-25 08:00:00',NULL,'2025-11-27 11:45:29','2025-11-27 11:45:29'),(7,2,3,'2024-11-25',2,0,0,0,NULL,NULL,'2025-11-27 11:45:29','2025-11-27 11:45:29'),(8,3,1,'2024-11-25',1,1,0,1,'2024-11-25 06:00:00',NULL,'2025-11-27 11:45:29','2025-11-27 11:45:29'),(9,3,2,'2024-11-25',60,1,0,1,'2024-11-25 07:00:00',NULL,'2025-11-27 11:45:29','2025-11-27 11:45:29'),(10,4,1,'2024-11-25',1,1,0,1,'2024-11-25 19:00:00',NULL,'2025-11-27 11:45:29','2025-11-27 11:45:29'),(11,4,2,'2024-11-25',25,0,0,0,NULL,NULL,'2025-11-27 11:45:29','2025-11-27 11:45:29'),(12,1,1,'2024-11-20',1,1,0,1,'2024-11-20 07:30:00',NULL,'2025-11-27 11:58:40','2025-11-27 11:58:40'),(13,1,2,'2024-11-20',3,1,0,1,'2024-11-20 18:30:00',NULL,'2025-11-27 11:58:40','2025-11-27 11:58:40'),(14,1,3,'2024-11-20',35,1,0,1,'2024-11-20 07:35:00',NULL,'2025-11-27 11:58:40','2025-11-27 11:58:40'),(15,2,1,'2024-11-20',1,1,0,1,'2024-11-20 08:00:00',NULL,'2025-11-27 11:58:40','2025-11-27 11:58:40'),(16,2,2,'2024-11-20',3,1,0,1,'2024-11-20 19:00:00',NULL,'2025-11-27 11:58:40','2025-11-27 11:58:40'),(17,2,4,'2024-11-20',60,1,0,1,'2024-11-20 07:30:00',NULL,'2025-11-27 11:58:40','2025-11-27 11:58:40'),(18,3,1,'2024-11-20',1,1,0,1,'2024-11-20 06:30:00',NULL,'2025-11-27 11:58:40','2025-11-27 11:58:40'),(19,3,5,'2024-11-20',1,1,0,1,'2024-11-20 09:00:00',NULL,'2025-11-27 11:58:40','2025-11-27 11:58:40'),(20,4,1,'2024-11-24',1,1,0,1,'2024-11-24 10:00:00',NULL,'2025-11-27 11:58:40','2025-11-27 11:58:40'),(21,4,3,'2024-11-24',25,0,0,0,NULL,NULL,'2025-11-27 11:58:40','2025-11-27 11:58:40'),(22,5,1,'2024-11-24',1,1,0,1,'2024-11-24 09:00:00',NULL,'2025-11-27 11:58:40','2025-11-27 11:58:40'),(23,5,6,'2024-11-24',1,1,0,1,'2024-11-24 12:00:00',NULL,'2025-11-27 11:58:40','2025-11-27 11:58:40'),(24,1,1,'2024-11-21',1,1,0,1,'2024-11-21 07:00:00',NULL,'2025-11-27 11:58:40','2025-11-27 11:58:40'),(25,1,7,'2024-11-21',1,1,0,1,'2024-11-21 20:00:00',NULL,'2025-11-27 11:58:40','2025-11-27 11:58:40'),(26,2,1,'2024-11-21',1,1,0,1,'2024-11-21 07:30:00',NULL,'2025-11-27 11:58:40','2025-11-27 11:58:40');
/*!40000 ALTER TABLE `user_task_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `openid` varchar(100) NOT NULL COMMENT '微信openid',
  `union_id` varchar(100) DEFAULT NULL COMMENT '微信unionid',
  `nickname` varchar(50) DEFAULT NULL COMMENT '昵称',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像路径',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `gender` tinyint DEFAULT '0' COMMENT '性别：0未知 1男 2女',
  `birthday` date DEFAULT NULL COMMENT '生日',
  `height` decimal(5,2) DEFAULT NULL COMMENT '身高(cm)',
  `weight` decimal(5,2) DEFAULT NULL COMMENT '体重(kg)',
  `member_level` tinyint DEFAULT '0' COMMENT '会员等级：0普通 1月卡 2年卡 3终身',
  `member_expire_time` datetime DEFAULT NULL COMMENT '会员到期时间',
  `sport_coins` int unsigned DEFAULT '0' COMMENT '运动币',
  `food_coins` int unsigned DEFAULT '0' COMMENT '膳食币',
  `balance` decimal(10,2) DEFAULT '0.00' COMMENT '账户余额',
  `user_level` tinyint DEFAULT '1' COMMENT '用户等级 1-10',
  `follower_count` int unsigned DEFAULT '0' COMMENT '粉丝数',
  `following_count` int unsigned DEFAULT '0' COMMENT '关注数',
  `continuous_checkin_days` int unsigned DEFAULT '0' COMMENT '连续打卡天数',
  `total_checkin_days` int unsigned DEFAULT '0' COMMENT '累计签到天数',
  `last_checkin_date` date DEFAULT NULL COMMENT '最后打卡日期',
  `status` tinyint DEFAULT '1' COMMENT '状态：0禁用 1正常',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `openid` (`openid`),
  KEY `idx_openid` (`openid`),
  KEY `idx_phone` (`phone`),
  KEY `idx_member_level` (`member_level`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'dev_test001',NULL,'健康达人小明',NULL,'13800138001',1,'1995-06-15',175.00,70.00,2,'2025-12-31 23:59:59',1280,860,199.00,5,128,56,15,0,NULL,1,'2025-11-27 11:41:14','2025-11-27 20:03:51'),(2,'dev_test002',NULL,'运动爱好者小红',NULL,'13800138002',2,'1998-03-22',165.00,55.00,1,'2025-06-30 23:59:59',560,420,50.00,3,86,42,7,0,NULL,1,'2025-11-27 11:41:14','2025-11-27 11:41:14'),(3,'dev_test003',NULL,'养生专家老王',NULL,'13800138003',1,'1980-11-08',172.00,68.00,3,'2099-12-31 23:59:59',3200,2800,500.00,8,1256,89,120,0,NULL,1,'2025-11-27 11:41:14','2025-11-27 11:41:14'),(4,'dev_test004',NULL,'减肥达人小李',NULL,'13800138004',2,'2000-01-18',160.00,52.00,0,NULL,180,150,0.00,2,45,23,3,0,NULL,1,'2025-11-27 11:41:14','2025-11-27 11:41:14'),(5,'dev_test005',NULL,'健身新手小张',NULL,'13800138005',1,'1992-07-25',178.00,80.00,0,NULL,60,40,0.00,1,12,8,1,0,NULL,1,'2025-11-27 11:41:14','2025-11-27 11:41:14'),(6,'dev_0b36dyFa1bFrJK09wlHa1u9eAu26dyF4',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-27 16:13:33','2025-11-27 16:13:33'),(7,'dev_12',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-27 16:16:13','2025-11-27 16:16:13'),(8,'dev_0e3KxyFa1R6tJK0CqvFa1mhkQQ1KxyFP',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-27 16:19:01','2025-11-27 16:19:01'),(9,'dev_0f3O4Skl2jfoJg4iXvol2IfV7E3O4Skq',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-27 16:22:52','2025-11-27 16:22:52'),(10,'dev_123',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-27 16:23:08','2025-11-27 16:23:08'),(11,'dev_0b3GIJ0w3EoD463jMo2w3So89z2GIJ0f',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-27 16:26:54','2025-11-27 16:26:54'),(12,'dev_0e3jUh1w39sb5632Js2w3DGPJA3jUh11',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-27 16:28:23','2025-11-27 16:28:23'),(13,'dev_0c35ooGa1kzhKK0F8qGa1nDzVo25ooGR',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-27 16:30:27','2025-11-27 16:30:27'),(14,'dev_0e3b0xml2Ok4Lg4pJQml2bWqxd2b0xmP',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-27 16:33:13','2025-11-27 16:33:13'),(15,'dev_0b3kTdHa1jb8LK0vAYGa1c5o1v3kTdHC',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,5,5,0.00,1,0,0,1,1,'2025-11-27',1,'2025-11-27 16:36:19','2025-11-27 16:36:47'),(16,'dev_0b3r68Ga1MK1KK0n8lIa1bs7pB2r68GZ',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,5,5,0.00,1,0,0,1,1,'2025-11-27',1,'2025-11-27 16:42:59','2025-11-27 16:50:23'),(17,'dev_1764239147359',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,5,5,0.00,1,0,0,1,1,'2025-11-27',1,'2025-11-27 18:26:10','2025-11-27 18:32:08'),(18,'dev_0c31sNkl2AmjJg4rVtml2qPkk321sNku',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-27 19:46:37','2025-11-27 19:46:37'),(19,'dev_0e3PCDll2DG7Kg4TNKnl2qYQ4l1PCDlK',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-27 20:03:28','2025-11-27 20:03:51'),(20,'dev_0b38rKml2wilLg4ixQkl2POLRu08rKmk',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-27 20:13:34','2025-11-27 20:13:34'),(21,'dev_0c3khNFa1fSCJK0pQnHa1bMfoa0khNFA',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-27 20:20:41','2025-11-27 20:20:41'),(22,'dev_0a3jaFll2XK7Kg409vll28RTBJ0jaFlN',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-27 20:28:44','2025-11-27 20:28:44'),(23,'dev_0e3abGll2zV8Kg45USml2Jgsqc2abGln',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-27 20:45:21','2025-11-27 20:45:21'),(24,'dev_0a3bpfGa1HmRJK0uCgHa1AKSHe2bpfGy',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-28 13:21:14','2025-11-28 13:21:14'),(25,'dev_0f3kmk0w392W363tKa2w3z3o9u1kmk0w',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-28 13:28:41','2025-11-28 13:28:41'),(26,'dev_0a3khrFa1eNyJK0qh3Ga1fucZi4khrFU',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-28 13:37:58','2025-11-28 13:37:58'),(27,'dev_0f3IUZFa1Tg7KK0rhTFa1FGsU21IUZFY',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-28 13:46:47','2025-11-28 13:46:47'),(28,'dev_0f3Y0hGa1SCXJK0IrxFa1F6IGS0Y0hGN',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-28 13:47:38','2025-11-28 13:47:38'),(29,'dev_0c3MJl0w3vq2463Brv3w3Zby7d1MJl09',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-28 13:51:17','2025-11-28 13:51:17'),(30,'dev_0f3rJLkl2lZBJg4GlZml22Plg90rJLkz',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-28 13:56:54','2025-11-28 13:56:54'),(31,'dev_0e3er1Ga1PSdKK094uFa1902Ck0er1GB',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-28 14:11:47','2025-11-28 14:11:47'),(32,'dev_0a34MV0w33zy4633Ep3w3lGF8E34MV0E',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-11-28 14:23:06','2025-11-28 14:23:06'),(33,'dev_0f3dp3Ha1T48KK0TkuJa1TWkUe0dp3HW',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-12-01 10:56:48','2025-12-01 10:56:48'),(34,'dev_0a3HHZkl25ElKg4om9ol2VGY2K1HHZkn',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-12-01 11:00:48','2025-12-01 11:00:48'),(35,'dev_0b3wxA0w3lVR563V312w3EZJCk0wxA0a',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-12-01 11:08:48','2025-12-01 11:08:48'),(36,'dev_0c32v4Ha1LR9KK0B7aHa16zQyO12v4H5',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-12-01 11:14:44','2025-12-01 11:14:44'),(37,'dev_0a3pNYFa1umfLK08BfHa1bg4Jb3pNYFI',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-12-01 11:22:48','2025-12-01 11:22:48'),(38,'dev_0e3Zw30w3Y8l563fZ01w3Z2lHe2Zw30R',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-12-01 11:26:40','2025-12-01 11:26:40'),(39,'dev_0e3kIFml2SMPJg4oOrml2AY27k4kIFm7',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-12-01 11:28:57','2025-12-01 11:28:57'),(40,'dev_0a3XPFml2kDPJg4Uzgll2JOBb22XPFmG',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-12-01 11:30:58','2025-12-01 11:30:58'),(41,'dev_0a3smrFa1dmIKK0Tv8Ja1i5kM33smrFV',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-12-01 11:33:41','2025-12-01 11:33:41'),(42,'dev_0f3bwKIa1JurHK0St6Ha1HSG3F0bwKIf',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-12-01 11:43:02','2025-12-01 11:43:02'),(43,'dev_0a3dwRll2dzzJg4CzHml2HNTwl2dwRl9',NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,0,NULL,0,0,0.00,1,0,0,0,0,NULL,1,'2025-12-01 11:44:33','2025-12-01 11:44:33');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'health_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-01 21:33:39
