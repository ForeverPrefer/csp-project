# CSP 校园资源分享平台

<div align="center">

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.2.7-green?logo=django)
![Bootstrap](https://img.shields.io/badge/Bootstrap-3.x-purple?logo=bootstrap)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

**连接校园，共享优质资源**

</div>

---

## 📖 项目简介

**CSP (Campus Sharing Platform)** 是一个面向高校校园的在线资源分享平台，为师生提供学习资源的在线上传、分类浏览、全文搜索、下载和收藏管理功能。项目服务于**西华师范大学**，致力于打造高效、便捷的校园资源共享生态。

---

## ✨ 核心功能

| 功能模块 | 说明 |
|----------|------|
| 🔐 **手机号登录注册** | 支持手机号+密码注册登录，记住我功能，自定义用户模型 |
| 📤 **资源上传** | 支持文档、软件、教程、模板四大分类，最大 50MB |
| 📂 **资源分类浏览** | 按文档资料/软件工具/学习教程/模板资源分类查看 |
| 🔍 **全文搜索** | 实时搜索建议、搜索历史记录、搜索结果分页展示 |
| ⬇️ **资源下载** | 下载计数统计、下载历史追踪 |
| ⭐ **收藏管理** | 收藏/取消收藏、收藏夹管理 |
| 👤 **个人中心** | 我的资源、下载历史、收藏夹、账户设置、密码修改 |
| 📊 **精品推荐** | 基于下载量和收藏数的双重认证推荐算法 |
| 🛡️ **Django Admin** | 内置后台管理，轻松管理用户和资源 |

---

## 🛠️ 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **后端框架** | Django 5.2.7 | MTV 架构，ORM，模板引擎 |
| **语言** | Python 3.14 | 全栈业务逻辑 |
| **数据库** | SQLite3 | 轻量级本地存储，开箱即用 |
| **前端框架** | Bootstrap 3 + jQuery 3.2.1 | 响应式 UI，交互增强 |
| **模板引擎** | Django Templates | 服务端渲染 |
| **二维码** | qrcode + Pillow | 生成带 Logo 的二维码 |
| **部署** | PythonAnywhere | 生产环境，WhiteNoise 静态文件 |

---

## 📁 项目结构

```
My_CSP/
├── CSP/                    # Django 项目配置
│   ├── settings.py         # 配置（开发/生产双环境自动切换）
│   ├── urls.py             # 根路由表
│   ├── wsgi.py             # WSGI 部署入口
│   └── asgi.py             # ASGI 入口
├── home/                   # 🏠 首页模块（搜索+统计+推荐）
├── rsharing/               # 📂 资源中心（分类浏览/详情/下载/收藏）
├── upzy/                   # 📤 资源上传模块
├── flview/                 # 🔍 分类浏览（最新/热门/精品推荐）
├── register/               # 🔐 登录注册（自定义User模型）
├── self/                   # 👤 个人中心（我的资源/下载/收藏/设置）
├── about/                  # ℹ️ 关于我们
├── help/                   # ❓ 帮助中心
├── text/                   # 🛠 工具脚本（二维码生成）
├── static/                 # 静态资源（CSS/JS/图片/字体）
├── templates/              # 基础模板 base.html
├── media/                  # 用户上传文件存储
├── manage.py               # Django 管理入口
├── requirements.txt        # 依赖清单
└── db.sqlite3              # SQLite 数据库
```

---

## 🗄️ 数据模型

### CustomUser（自定义用户）
| 字段 | 类型 | 说明 |
|------|------|------|
| phone | CharField(11) | 手机号（替代 username 作为登录凭证） |
| email | EmailField | 邮箱（唯一） |
| display_name | CharField | 显示昵称 |
| real_name | CharField | 真实姓名 |

### Resource（资源）
| 字段 | 类型 | 说明 |
|------|------|------|
| resource_name | CharField(200) | 资源名称 |
| resource_type | CharField | 分类：文档资料/软件工具/学习教程/模板资源 |
| resource_file | FileField | 文件（按 年/月/日 自动分目录） |
| resource_desc | TextField | 资源描述 |
| uploader | FK → User | 上传者 |
| upload_time | DateTimeField | 上传时间 |
| download_count | IntegerField | 下载次数 |

### Favorite（收藏）
- 用户-资源多对多关系，联合唯一约束
- 支持 AJAX 异步收藏/取消

### DownloadHistory（下载历史）
- 记录用户下载行为，支持历史回溯

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- pip

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/ForeverPrefer/csp-project.git
cd csp-project

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. 安装依赖
pip install -r requirements.txt

# 5. 数据库迁移
python manage.py migrate

# 6. 创建管理员
python manage.py createsuperuser

# 7. 启动开发服务器
python manage.py runserver
```

访问 http://127.0.0.1:8000/ 即可使用。

管理后台：http://127.0.0.1:8000/admin/

---

## 🌐 部署

项目已配置 **开发/生产** 双环境自动切换（通过 `PYTHONANYWHERE_DOMAIN` 环境变量判断）：

| 配置项 | 开发环境 | 生产环境 |
|--------|----------|----------|
| DEBUG | ✅ True | ❌ False |
| 静态文件 | Django 默认 | WhiteNoise 压缩缓存 |
| HTTPS | ❌ | ✅ HSTS + Secure Cookie |
| 日志 | 控制台 | 文件日志 |

部署到 PythonAnywhere：

```bash
# 在 PythonAnywhere 控制台
git clone https://github.com/ForeverPrefer/csp-project.git
cd csp-project
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic
```

---

## 📝 依赖清单

```
asgiref==3.10.0
colorama==0.4.6
Django==5.2.7
pillow==12.0.0
qrcode==8.2
sqlparse==0.5.3
tzdata==2025.2
```

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

---

## 📧 联系方式

- **Email**: 3502449120@qq.com
- **电话**: 152-2813-4150
- **地址**: 南充市顺庆区西华师范大学

---

## 📄 许可证

本项目采用 MIT 许可证。

---

<div align="center">

**Made with ❤️ for West China Normal University**

⭐ 如果这个项目对你有帮助，请点亮 Star！

</div>
