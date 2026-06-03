# 北京红衫众成游泳俱乐部管理信息系统

基于 Docker 的部署说明

## 系统要求

- Docker 20.10+
- Docker Compose 2.0+
- 最低配置：1核CPU / 2GB内存 / 40GB硬盘

## 快速部署

### 1. 克隆项目

```bash
git clone https://github.com/miltonzhao-mi/HSZC-Swimming.git
cd HSZC-Swimming
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，修改密码和域名
```

### 3. 启动服务

```bash
docker-compose up -d
```

### 4. 初始化数据库（首次运行）

```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

## 服务访问

| 服务 | 地址 | 说明 |
|------|------|------|
| 前台 | http://localhost | Vue3 管理后台 |
| 后台 API | http://localhost:8000 | Django REST API |
| API 文档 | http://localhost:8000/api/docs/ | Swagger API 文档 |
| 数据库 | localhost:3306 | MySQL 8.0 |

## 初始账号

- 用户名: admin
- 密码: admin123
- API 文档: http://localhost:8000/api/docs/

## 常用命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 重新构建
docker-compose up -d --build

# 进入后端容器
docker-compose exec backend bash

# 执行 Django 命令
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic
```

## 数据持久化

- `mysql_data` - MySQL 数据卷
- `redis_data` - Redis 数据卷
- `media_data` - 上传文件数据卷

## 生产环境部署

### 1. 服务器配置

```bash
# 安装 Docker
curl -fsSL https://get.docker.com | sh

# 安装 Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### 2. Nginx 反向代理（可选）

如果需要 HTTPS 和域名访问，在服务器前端再部署一个 Nginx：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. HTTPS 配置（使用 Let's Encrypt）

```bash
# 安装 certbot
apt install certbot python3-certbot-nginx

# 获取证书
certbot --nginx -d your-domain.com
```

### 4. 定时备份

```bash
# 备份数据库
docker-compose exec db mysqldump -u root -p$DB_ROOT_PASSWORD beijingshanshan > backup_$(date +%Y%m%d).sql

# 备份文件
tar -czf media_backup_$(date +%Y%m%d).tar.gz hszc-swimming-api/media/
```

## 目录结构

```
HSZC-Swimming/
├── docker-compose.yml     # Docker Compose 配置
├── .env                   # 环境变量（需创建）
├── init.sql              # 数据库初始化脚本
├── hszc-swimming-api/    # Django 后端
│   ├── Dockerfile
│   └── ...
└── hszc-swimming-web/    # Vue 前端
    ├── Dockerfile
    ├── nginx.conf
    └── ...
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Vite + Naive UI |
| 后端 | Django 5 + Django REST Framework |
| 数据库 | MySQL 8.0 |
| 缓存 | Redis 7 |
| 反向代理 | Nginx |
| 容器化 | Docker + Docker Compose |
