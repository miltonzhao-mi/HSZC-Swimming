-- 北京红衫众成游泳俱乐部管理信息系统 数据库初始化脚本

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS beijingshanshan DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE beijingshanshan;

-- 创建管理员用户表（如果不存在）
CREATE TABLE IF NOT EXISTS users_role (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL COMMENT '角色名称',
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '角色代码',
    description TEXT COMMENT '描述',
    permissions JSON DEFAULT '[]' COMMENT '权限列表',
    is_system BOOLEAN DEFAULT FALSE COMMENT '系统角色',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色表';

-- 创建用户表
CREATE TABLE IF NOT EXISTS users_user (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE COMMENT '用户名',
    password VARCHAR(128) NOT NULL COMMENT '密码哈希',
    role_id BIGINT COMMENT '角色ID',
    phone VARCHAR(20) COMMENT '手机号',
    avatar VARCHAR(255) COMMENT '头像',
    user_type VARCHAR(20) DEFAULT 'member' COMMENT '用户类型',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_role (role_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 创建会员表
CREATE TABLE IF NOT EXISTS members_member (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNIQUE COMMENT '关联用户ID',
    surname VARCHAR(50) NOT NULL COMMENT '姓',
    given_name VARCHAR(50) NOT NULL COMMENT '名',
    nickname VARCHAR(100) COMMENT '昵称',
    id_card VARCHAR(18) NOT NULL UNIQUE COMMENT '身份证号',
    id_card_front VARCHAR(255) COMMENT '身份证正面',
    id_card_back VARCHAR(255) COMMENT '身份证背面',
    avatar VARCHAR(255) COMMENT '免冠照片',
    gender VARCHAR(10) NOT NULL COMMENT '性别',
    birth_date DATE NOT NULL COMMENT '出生日期',
    phone VARCHAR(20) NOT NULL COMMENT '联系电话',
    member_type VARCHAR(20) DEFAULT 'temp' COMMENT '会员类型',
    member_status VARCHAR(20) DEFAULT 'normal' COMMENT '会员状态',
    trial_start_date DATE COMMENT '考核开始日期',
    trial_end_date DATE COMMENT '考核结束日期',
    trial_extended BOOLEAN DEFAULT FALSE COMMENT '是否延期',
    level_points INT DEFAULT 0 COMMENT '活跃度积分',
    level_grade VARCHAR(50) COMMENT '等级',
    approved_by BIGINT COMMENT '审批人',
    approved_at DATETIME COMMENT '审批时间',
    approval_remark TEXT COMMENT '审批备注',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_id_card (id_card),
    INDEX idx_phone (phone),
    INDEX idx_member_type (member_type),
    INDEX idx_member_status (member_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='会员表';

-- 创建活跃度记录表
CREATE TABLE IF NOT EXISTS members_activity (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    member_id BIGINT NOT NULL COMMENT '会员ID',
    activity_type VARCHAR(20) NOT NULL COMMENT '活动类型',
    activity_date DATE NOT NULL COMMENT '活动日期',
    description VARCHAR(200) COMMENT '描述',
    points INT DEFAULT 1 COMMENT '积分',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_member (member_id),
    INDEX idx_activity_date (activity_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='活跃度记录表';

-- 创建会员等级表
CREATE TABLE IF NOT EXISTS members_level (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL COMMENT '等级名称',
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '等级代码',
    min_points INT NOT NULL COMMENT '最低积分',
    max_points INT COMMENT '最高积分',
    description TEXT COMMENT '描述',
    sort_order INT DEFAULT 0 COMMENT '排序'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='会员等级表';

-- 创建比赛表
CREATE TABLE IF NOT EXISTS competitions_competition (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL COMMENT '比赛名称',
    description TEXT COMMENT '描述',
    location VARCHAR(200) COMMENT '地点',
    start_date DATE NOT NULL COMMENT '开始日期',
    end_date DATE NOT NULL COMMENT '结束日期',
    sign_up_deadline DATETIME NOT NULL COMMENT '报名截止时间',
    status VARCHAR(20) DEFAULT 'preparing' COMMENT '状态',
    poster VARCHAR(255) COMMENT '海报',
    created_by BIGINT COMMENT '创建人',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_start_date (start_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='比赛表';

-- 创建参赛报名表
CREATE TABLE IF NOT EXISTS competitions_signup (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    competition_id BIGINT NOT NULL COMMENT '比赛ID',
    member_id BIGINT NOT NULL COMMENT '会员ID',
    event_item VARCHAR(50) NOT NULL COMMENT '参赛项目',
    distance VARCHAR(20) NOT NULL COMMENT '距离',
    signup_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '报名时间',
    register_by VARCHAR(20) DEFAULT 'pc' COMMENT '报名渠道',
    status VARCHAR(20) DEFAULT 'registered' COMMENT '状态',
    UNIQUE KEY uk_competition_member_event_distance (competition_id, member_id, event_item, distance),
    INDEX idx_competition (competition_id),
    INDEX idx_member (member_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='参赛报名表';

-- 创建比赛成绩表
CREATE TABLE IF NOT EXISTS competitions_score (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    signup_id BIGINT NOT NULL UNIQUE COMMENT '报名ID',
    score_time DECIMAL(8,2) NOT NULL COMMENT '比赛成绩(秒)',
    rank INT COMMENT '名次',
    points INT DEFAULT 0 COMMENT '积分',
    submit_by BIGINT COMMENT '提交人',
    submit_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
    remarks TEXT COMMENT '备注',
    INDEX idx_signup (signup_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='比赛成绩表';

-- 创建比赛成绩册表
CREATE TABLE IF NOT EXISTS competitions_score_file (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    competition_id BIGINT NOT NULL COMMENT '比赛ID',
    name VARCHAR(200) NOT NULL COMMENT '文件名称',
    file VARCHAR(255) NOT NULL COMMENT '文件路径',
    file_type VARCHAR(20) DEFAULT 'pdf' COMMENT '文件类型',
    uploaded_by BIGINT COMMENT '上传人',
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_competition (competition_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='成绩册表';

-- 创建比赛项目表
CREATE TABLE IF NOT EXISTS competitions_event_item (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE COMMENT '项目名称',
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '项目代码',
    distances JSON DEFAULT '[]' COMMENT '距离列表',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='比赛项目表';

-- 创建训练通知表
CREATE TABLE IF NOT EXISTS trainings_notice (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL COMMENT '标题',
    content TEXT COMMENT '内容',
    location VARCHAR(200) NOT NULL COMMENT '训练地点',
    train_date DATE NOT NULL COMMENT '训练日期',
    start_time TIME NOT NULL COMMENT '开始时间',
    end_time TIME NOT NULL COMMENT '结束时间',
    coach VARCHAR(100) NOT NULL COMMENT '教练',
    max_participants INT COMMENT '最大人数',
    signup_deadline DATETIME NOT NULL COMMENT '报名截止时间',
    notice_type VARCHAR(20) DEFAULT 'push' COMMENT '通知方式',
    status VARCHAR(20) DEFAULT 'published' COMMENT '状态',
    created_by BIGINT COMMENT '创建人',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_train_date (train_date),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='训练通知表';

-- 创建训练报名表
CREATE TABLE IF NOT EXISTS trainings_signup (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    notice_id BIGINT NOT NULL COMMENT '训练通知ID',
    member_id BIGINT NOT NULL COMMENT '会员ID',
    signup_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '报名时间',
    status VARCHAR(20) DEFAULT 'registered' COMMENT '状态',
    UNIQUE KEY uk_notice_member (notice_id, member_id),
    INDEX idx_notice (notice_id),
    INDEX idx_member (member_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='训练报名表';

-- 创建训练笔记表
CREATE TABLE IF NOT EXISTS trainings_note (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    member_id BIGINT NOT NULL COMMENT '会员ID',
    notice_id BIGINT COMMENT '关联训练通知ID',
    title VARCHAR(200) NOT NULL COMMENT '标题',
    content TEXT NOT NULL COMMENT '内容',
    visibility VARCHAR(20) DEFAULT 'public' COMMENT '可见性',
    like_count INT DEFAULT 0 COMMENT '点赞数',
    comment_count INT DEFAULT 0 COMMENT '评论数',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_member (member_id),
    INDEX idx_visibility (visibility)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='训练笔记表';

-- 创建消息表
CREATE TABLE IF NOT EXISTS messages_message (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL COMMENT '标题',
    content TEXT NOT NULL COMMENT '内容',
    message_type VARCHAR(20) NOT NULL COMMENT '消息类型',
    sender BIGINT COMMENT '发送人',
    is_published BOOLEAN DEFAULT FALSE COMMENT '是否发布',
    published_at DATETIME COMMENT '发布时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_message_type (message_type),
    INDEX idx_is_published (is_published)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='消息表';

-- 创建消息阅读记录表
CREATE TABLE IF NOT EXISTS messages_read (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    message_id BIGINT NOT NULL COMMENT '消息ID',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    is_read BOOLEAN DEFAULT FALSE COMMENT '已读',
    read_at DATETIME COMMENT '阅读时间',
    UNIQUE KEY uk_message_user (message_id, user_id),
    INDEX idx_user (user_id),
    INDEX idx_is_read (is_read)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='消息阅读记录表';

-- 创建笔记表
CREATE TABLE IF NOT EXISTS notes_note (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    member_id BIGINT NOT NULL COMMENT '会员ID',
    title VARCHAR(200) NOT NULL COMMENT '标题',
    content TEXT NOT NULL COMMENT '内容',
    visibility VARCHAR(20) DEFAULT 'public' COMMENT '可见性',
    like_count INT DEFAULT 0 COMMENT '点赞数',
    comment_count INT DEFAULT 0 COMMENT '评论数',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_member (member_id),
    INDEX idx_visibility (visibility)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='笔记表';

-- 创建笔记评论表
CREATE TABLE IF NOT EXISTS notes_note_comment (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    note_id BIGINT NOT NULL COMMENT '笔记ID',
    member_id BIGINT NOT NULL COMMENT '评论人ID',
    content TEXT NOT NULL COMMENT '评论内容',
    parent_id BIGINT COMMENT '父评论ID',
    is_deleted BOOLEAN DEFAULT FALSE COMMENT '已删除',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_note (note_id),
    INDEX idx_member (member_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='笔记评论表';

-- 创建笔记点赞表
CREATE TABLE IF NOT EXISTS notes_note_like (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    note_id BIGINT NOT NULL COMMENT '笔记ID',
    member_id BIGINT NOT NULL COMMENT '点赞人ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_note_member (note_id, member_id),
    INDEX idx_note (note_id),
    INDEX idx_member (member_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='笔记点赞表';

-- 创建操作日志表
CREATE TABLE IF NOT EXISTS users_operation_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT COMMENT '操作用户',
    action VARCHAR(20) NOT NULL COMMENT '操作类型',
    model_name VARCHAR(100) NOT NULL COMMENT '模型名称',
    object_id VARCHAR(50) COMMENT '对象ID',
    detail JSON COMMENT '详情',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    user_agent TEXT COMMENT 'User-Agent',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='操作日志表';

-- 插入初始角色数据
INSERT INTO users_role (name, code, description, permissions, is_system) VALUES
('全局管理员', 'global_admin', '系统全局管理员，拥有所有权限', '["*"]', TRUE),
('比赛管理员', 'competition_admin', '负责比赛管理', '["competition.*", "signup.*", "score.*"]', TRUE),
('训练管理员', 'training_admin', '负责训练管理', '["training.*", "notice.*"]', TRUE)
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- 插入初始管理员账号 (密码: admin123)
INSERT INTO users_user (username, password, role_id, user_type, is_active) VALUES
('admin', 'pbkdf2_sha256$870000$default$5e884898da28047d9156e01f4e6a0c7c', 1, 'global_admin', TRUE)
ON DUPLICATE KEY UPDATE username=VALUES(username);

-- 插入比赛项目初始数据
INSERT INTO competitions_event_item (name, code, distances, is_active) VALUES
('蝶泳', 'butterfly', '["50m", "100m", "200m"]', TRUE),
('仰泳', 'backstroke', '["50m", "100m", "200m"]', TRUE),
('蛙泳', 'breaststroke', '["50m", "100m", "200m", "1000m"]', TRUE),
('自由泳', 'freestyle', '["50m", "100m", "200m", "1000m", "2000m"]', TRUE),
('混合泳', 'medley', '["100m", "200m", "400m"]', TRUE)
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- 插入会员等级初始数据
INSERT INTO members_level (name, code, min_points, max_points, description, sort_order) VALUES
('初级会员', 'junior', 0, 99, '新注册会员', 1),
('活跃会员', 'active', 100, 299, '积极参与活动和比赛', 2),
('精英会员', 'elite', 300, 599, '经常参与比赛并获得好成绩', 3),
('荣誉会员', 'honor', 600, NULL, '为俱乐部做出重要贡献', 4)
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- 创建游泳运动员等级标准表
CREATE TABLE IF NOT EXISTS standards_swimming (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    gender VARCHAR(10) NOT NULL COMMENT '性别',
    pool_length INT NOT NULL COMMENT '泳池长度',
    stroke VARCHAR(20) NOT NULL COMMENT '泳姿',
    distance INT NOT NULL COMMENT '距离(米)',
    level VARCHAR(20) NOT NULL COMMENT '等级',
    qualifying_time DECIMAL(8,2) NOT NULL COMMENT '达标成绩(秒)',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    version VARCHAR(20) DEFAULT '2025' COMMENT '版本',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_gender_pool_stroke_distance_level (gender, pool_length, stroke, distance, level),
    INDEX idx_gender (gender),
    INDEX idx_pool_length (pool_length),
    INDEX idx_stroke (stroke),
    INDEX idx_distance (distance),
    INDEX idx_level (level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='游泳运动员等级标准';

-- 插入游泳运动员等级标准数据 (50米池男子)
INSERT INTO standards_swimming (gender, pool_length, stroke, distance, level, qualifying_time, version) VALUES
-- 男子自由泳
('male', 50, 'freestyle', 50, 'international', 21.89, '2025'),
('male', 50, 'freestyle', 50, 'national', 23.01, '2025'),
('male', 50, 'freestyle', 50, 'level_1', 24.04, '2025'),
('male', 50, 'freestyle', 50, 'level_2', 26.04, '2025'),
('male', 50, 'freestyle', 50, 'level_3', 28.04, '2025'),
('male', 50, 'freestyle', 100, 'international', 48.29, '2025'),
('male', 50, 'freestyle', 100, 'national', 50.74, '2025'),
('male', 50, 'freestyle', 100, 'level_1', 52.74, '2025'),
('male', 50, 'freestyle', 100, 'level_2', 55.74, '2025'),
('male', 50, 'freestyle', 100, 'level_3', 58.74, '2025'),
('male', 50, 'freestyle', 200, 'international', 105.71, '2025'),
('male', 50, 'freestyle', 200, 'national', 110.96, '2025'),
('male', 50, 'freestyle', 200, 'level_1', 115.61, '2025'),
('male', 50, 'freestyle', 200, 'level_2', 120.61, '2025'),
('male', 50, 'freestyle', 200, 'level_3', 125.61, '2025'),
('male', 50, 'freestyle', 400, 'international', 227.00, '2025'),
('male', 50, 'freestyle', 400, 'national', 238.35, '2025'),
('male', 50, 'freestyle', 400, 'level_1', 248.35, '2025'),
('male', 50, 'freestyle', 400, 'level_2', 258.35, '2025'),
('male', 50, 'freestyle', 400, 'level_3', 268.35, '2025'),
('male', 50, 'freestyle', 800, 'international', 470.91, '2025'),
('male', 50, 'freestyle', 800, 'national', 494.46, '2025'),
('male', 50, 'freestyle', 800, 'level_1', 514.46, '2025'),
('male', 50, 'freestyle', 800, 'level_2', 534.46, '2025'),
('male', 50, 'freestyle', 800, 'level_3', 554.46, '2025'),
('male', 50, 'freestyle', 1500, 'international', 884.72, '2025'),
('male', 50, 'freestyle', 1500, 'national', 929.05, '2025'),
('male', 50, 'freestyle', 1500, 'level_1', 954.05, '2025'),
('male', 50, 'freestyle', 1500, 'level_2', 989.05, '2025'),
('male', 50, 'freestyle', 1500, 'level_3', 1019.05, '2025'),
-- 男子仰泳
('male', 50, 'backstroke', 50, 'international', 24.92, '2025'),
('male', 50, 'backstroke', 50, 'national', 26.16, '2025'),
('male', 50, 'backstroke', 50, 'level_1', 27.41, '2025'),
('male', 50, 'backstroke', 50, 'level_2', 29.41, '2025'),
('male', 50, 'backstroke', 50, 'level_3', 31.41, '2025'),
('male', 50, 'backstroke', 100, 'international', 53.36, '2025'),
('male', 50, 'backstroke', 100, 'national', 56.03, '2025'),
('male', 50, 'backstroke', 100, 'level_1', 58.68, '2025'),
('male', 50, 'backstroke', 100, 'level_2', 61.68, '2025'),
('male', 50, 'backstroke', 100, 'level_3', 64.68, '2025'),
('male', 50, 'backstroke', 200, 'international', 114.92, '2025'),
('male', 50, 'backstroke', 200, 'national', 120.67, '2025'),
('male', 50, 'backstroke', 200, 'level_1', 126.02, '2025'),
('male', 50, 'backstroke', 200, 'level_2', 131.02, '2025'),
('male', 50, 'backstroke', 200, 'level_3', 136.02, '2025'),
-- 男子蛙泳
('male', 50, 'breaststroke', 50, 'international', 26.67, '2025'),
('male', 50, 'breaststroke', 50, 'national', 28.03, '2025'),
('male', 50, 'breaststroke', 50, 'level_1', 29.28, '2025'),
('male', 50, 'breaststroke', 50, 'level_2', 31.28, '2025'),
('male', 50, 'breaststroke', 50, 'level_3', 33.28, '2025'),
('male', 50, 'breaststroke', 100, 'international', 58.96, '2025'),
('male', 50, 'breaststroke', 100, 'national', 61.91, '2025'),
('male', 50, 'breaststroke', 100, 'level_1', 64.66, '2025'),
('male', 50, 'breaststroke', 100, 'level_2', 67.66, '2025'),
('male', 50, 'breaststroke', 100, 'level_3', 70.66, '2025'),
('male', 50, 'breaststroke', 200, 'international', 128.57, '2025'),
('male', 50, 'breaststroke', 200, 'national', 135.09, '2025'),
('male', 50, 'breaststroke', 200, 'level_1', 141.09, '2025'),
('male', 50, 'breaststroke', 200, 'level_2', 146.09, '2025'),
('male', 50, 'breaststroke', 200, 'level_3', 151.09, '2025'),
-- 男子蝶泳
('male', 50, 'butterfly', 50, 'international', 22.76, '2025'),
('male', 50, 'butterfly', 50, 'national', 23.92, '2025'),
('male', 50, 'butterfly', 50, 'level_1', 25.07, '2025'),
('male', 50, 'butterfly', 50, 'level_2', 27.07, '2025'),
('male', 50, 'butterfly', 50, 'level_3', 29.07, '2025'),
('male', 50, 'butterfly', 100, 'international', 50.74, '2025'),
('male', 50, 'butterfly', 100, 'national', 53.31, '2025'),
('male', 50, 'butterfly', 100, 'level_1', 55.81, '2025'),
('male', 50, 'butterfly', 100, 'level_2', 58.81, '2025'),
('male', 50, 'butterfly', 100, 'level_3', 61.81, '2025'),
('male', 50, 'butterfly', 200, 'international', 111.42, '2025'),
('male', 50, 'butterfly', 200, 'national', 117.00, '2025'),
('male', 50, 'butterfly', 200, 'level_1', 122.00, '2025'),
('male', 50, 'butterfly', 200, 'level_2', 127.00, '2025'),
('male', 50, 'butterfly', 200, 'level_3', 132.00, '2025'),
-- 男子混合泳
('male', 50, 'medley', 200, 'international', 115.55, '2025'),
('male', 50, 'medley', 200, 'national', 121.33, '2025'),
('male', 50, 'medley', 200, 'level_1', 126.83, '2025'),
('male', 50, 'medley', 200, 'level_2', 131.83, '2025'),
('male', 50, 'medley', 200, 'level_3', 136.83, '2025'),
('male', 50, 'medley', 400, 'international', 243.73, '2025'),
('male', 50, 'medley', 400, 'national', 255.92, '2025'),
('male', 50, 'medley', 400, 'level_1', 267.42, '2025'),
('male', 50, 'medley', 400, 'level_2', 277.42, '2025'),
('male', 50, 'medley', 400, 'level_3', 287.42, '2025')
ON DUPLICATE KEY UPDATE qualifying_time=VALUES(qualifying_time);

-- 插入游泳运动员等级标准数据 (50米池女子)
INSERT INTO standards_swimming (gender, pool_length, stroke, distance, level, qualifying_time, version) VALUES
-- 女子自由泳
('female', 50, 'freestyle', 50, 'international', 24.05, '2025'),
('female', 50, 'freestyle', 50, 'national', 25.25, '2025'),
('female', 50, 'freestyle', 50, 'level_1', 26.50, '2025'),
('female', 50, 'freestyle', 50, 'level_2', 28.50, '2025'),
('female', 50, 'freestyle', 50, 'level_3', 30.50, '2025'),
('female', 50, 'freestyle', 100, 'international', 52.21, '2025'),
('female', 50, 'freestyle', 100, 'national', 54.81, '2025'),
('female', 50, 'freestyle', 100, 'level_1', 57.31, '2025'),
('female', 50, 'freestyle', 100, 'level_2', 60.31, '2025'),
('female', 50, 'freestyle', 100, 'level_3', 63.31, '2025'),
('female', 50, 'freestyle', 200, 'international', 114.02, '2025'),
('female', 50, 'freestyle', 200, 'national', 119.82, '2025'),
('female', 50, 'freestyle', 200, 'level_1', 125.32, '2025'),
('female', 50, 'freestyle', 200, 'level_2', 130.32, '2025'),
('female', 50, 'freestyle', 200, 'level_3', 135.32, '2025'),
('female', 50, 'freestyle', 400, 'international', 236.83, '2025'),
('female', 50, 'freestyle', 400, 'national', 248.67, '2025'),
('female', 50, 'freestyle', 400, 'level_1', 260.07, '2025'),
('female', 50, 'freestyle', 400, 'level_2', 270.07, '2025'),
('female', 50, 'freestyle', 400, 'level_3', 280.07, '2025'),
('female', 50, 'freestyle', 800, 'international', 485.12, '2025'),
('female', 50, 'freestyle', 800, 'national', 509.37, '2025'),
('female', 50, 'freestyle', 800, 'level_1', 531.87, '2025'),
('female', 50, 'freestyle', 800, 'level_2', 551.87, '2025'),
('female', 50, 'freestyle', 800, 'level_3', 571.87, '2025'),
('female', 50, 'freestyle', 1500, 'international', 936.86, '2025'),
('female', 50, 'freestyle', 1500, 'national', 983.70, '2025'),
('female', 50, 'freestyle', 1500, 'level_1', 1018.70, '2025'),
('female', 50, 'freestyle', 1500, 'level_2', 1058.70, '2025'),
('female', 50, 'freestyle', 1500, 'level_3', 1098.70, '2025'),
-- 女子仰泳
('female', 50, 'backstroke', 50, 'international', 27.48, '2025'),
('female', 50, 'backstroke', 50, 'national', 28.85, '2025'),
('female', 50, 'backstroke', 50, 'level_1', 30.25, '2025'),
('female', 50, 'backstroke', 50, 'level_2', 32.25, '2025'),
('female', 50, 'backstroke', 50, 'level_3', 34.25, '2025'),
('female', 50, 'backstroke', 100, 'international', 58.21, '2025'),
('female', 50, 'backstroke', 100, 'national', 61.12, '2025'),
('female', 50, 'backstroke', 100, 'level_1', 64.02, '2025'),
('female', 50, 'backstroke', 100, 'level_2', 67.02, '2025'),
('female', 50, 'backstroke', 100, 'level_3', 70.02, '2025'),
('female', 50, 'backstroke', 200, 'international', 124.18, '2025'),
('female', 50, 'backstroke', 200, 'national', 130.49, '2025'),
('female', 50, 'backstroke', 200, 'level_1', 136.49, '2025'),
('female', 50, 'backstroke', 200, 'level_2', 141.49, '2025'),
('female', 50, 'backstroke', 200, 'level_3', 146.49, '2025'),
-- 女子蛙泳
('female', 50, 'breaststroke', 50, 'international', 29.88, '2025'),
('female', 50, 'breaststroke', 50, 'national', 31.38, '2025'),
('female', 50, 'breaststroke', 50, 'level_1', 32.88, '2025'),
('female', 50, 'breaststroke', 50, 'level_2', 34.88, '2025'),
('female', 50, 'breaststroke', 50, 'level_3', 36.88, '2025'),
('female', 50, 'breaststroke', 100, 'international', 65.15, '2025'),
('female', 50, 'breaststroke', 100, 'national', 68.41, '2025'),
('female', 50, 'breaststroke', 100, 'level_1', 71.41, '2025'),
('female', 50, 'breaststroke', 100, 'level_2', 74.41, '2025'),
('female', 50, 'breaststroke', 100, 'level_3', 77.41, '2025'),
('female', 50, 'breaststroke', 200, 'international', 140.46, '2025'),
('female', 50, 'breaststroke', 200, 'national', 147.48, '2025'),
('female', 50, 'breaststroke', 200, 'level_1', 154.48, '2025'),
('female', 50, 'breaststroke', 200, 'level_2', 159.48, '2025'),
('female', 50, 'breaststroke', 200, 'level_3', 164.48, '2025'),
-- 女子蝶泳
('female', 50, 'butterfly', 50, 'international', 25.49, '2025'),
('female', 50, 'butterfly', 50, 'national', 26.78, '2025'),
('female', 50, 'butterfly', 50, 'level_1', 28.03, '2025'),
('female', 50, 'butterfly', 50, 'level_2', 30.03, '2025'),
('female', 50, 'butterfly', 50, 'level_3', 32.03, '2025'),
('female', 50, 'butterfly', 100, 'international', 56.03, '2025'),
('female', 50, 'butterfly', 100, 'national', 58.83, '2025'),
('female', 50, 'butterfly', 100, 'level_1', 61.58, '2025'),
('female', 50, 'butterfly', 100, 'level_2', 64.58, '2025'),
('female', 50, 'butterfly', 100, 'level_3', 67.58, '2025'),
('female', 50, 'butterfly', 200, 'international', 121.87, '2025'),
('female', 50, 'butterfly', 200, 'national', 128.02, '2025'),
('female', 50, 'butterfly', 200, 'level_1', 134.02, '2025'),
('female', 50, 'butterfly', 200, 'level_2', 139.02, '2025'),
('female', 50, 'butterfly', 200, 'level_3', 144.02, '2025'),
-- 女子混合泳
('female', 50, 'medley', 200, 'international', 125.81, '2025'),
('female', 50, 'medley', 200, 'national', 132.10, '2025'),
('female', 50, 'medley', 200, 'level_1', 138.60, '2025'),
('female', 50, 'medley', 200, 'level_2', 143.60, '2025'),
('female', 50, 'medley', 200, 'level_3', 148.60, '2025'),
('female', 50, 'medley', 400, 'international', 262.52, '2025'),
('female', 50, 'medley', 400, 'national', 275.65, '2025'),
('female', 50, 'medley', 400, 'level_1', 288.65, '2025'),
('female', 50, 'medley', 400, 'level_2', 298.65, '2025'),
('female', 50, 'medley', 400, 'level_3', 308.65, '2025')
ON DUPLICATE KEY UPDATE qualifying_time=VALUES(qualifying_time);

-- 创建会员画像表
CREATE TABLE IF NOT EXISTS profiles_member_profile (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    member_id BIGINT NOT NULL UNIQUE COMMENT '会员ID',
    total_activities INT DEFAULT 0 COMMENT '累计活动次数',
    total_signups INT DEFAULT 0 COMMENT '累计报名次数',
    total_scores INT DEFAULT 0 COMMENT '累计有成绩次数',
    total_training INT DEFAULT 0 COMMENT '累计参训次数',
    total_points INT DEFAULT 0 COMMENT '累计积分',
    year_signups INT DEFAULT 0 COMMENT '年度报名',
    year_scores INT DEFAULT 0 COMMENT '年度有成绩',
    year_training INT DEFAULT 0 COMMENT '年度参训',
    year_points INT DEFAULT 0 COMMENT '年度积分',
    personal_records JSON COMMENT '个人最佳成绩',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_member (member_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='会员画像';

-- 创建成绩历史记录表
CREATE TABLE IF NOT EXISTS profiles_performance_record (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    member_id BIGINT NOT NULL COMMENT '会员ID',
    stroke VARCHAR(20) NOT NULL COMMENT '泳姿',
    distance INT NOT NULL COMMENT '距离(米)',
    score_time DECIMAL(8,2) NOT NULL COMMENT '成绩(秒)',
    rank INT COMMENT '名次',
    competition_name VARCHAR(200) NOT NULL COMMENT '比赛名称',
    competition_date DATE NOT NULL COMMENT '比赛日期',
    record_date DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '记录时间',
    INDEX idx_member_stroke_distance (member_id, stroke, distance),
    INDEX idx_competition_date (competition_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='成绩历史记录';
