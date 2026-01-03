# 版本标签管理指南

## 1. 概述

本项目采用语义化版本控制（Semantic Versioning）规范，用于统一版本号格式，便于版本管理和发布。

## 2. 语义化版本号格式

版本号格式：`vX.Y.Z`，其中：

- **X**：主版本号（Major）- 当你做了不兼容的API修改
- **Y**：次版本号（Minor）- 当你做了向下兼容的功能性新增
- **Z**：修订号（Patch）- 当你做了向下兼容的问题修正

## 3. 版本号递增规则

### 3.1 主版本号（X）

- 当你做了不兼容的API修改
- 当你升级了核心依赖库，导致现有代码无法正常工作
- 当你重构了核心模块，改变了模块间的依赖关系

### 3.2 次版本号（Y）

- 当你做了向下兼容的功能性新增
- 当你添加了新的API或功能
- 当你改进了现有功能，但保持API兼容

### 3.3 修订号（Z）

- 当你做了向下兼容的问题修正
- 当你修复了bug
- 当你做了性能优化
- 当你更新了文档或测试用例

## 4. 预发布版本

对于尚未稳定的版本，可以使用预发布版本号：

```
vX.Y.Z-prerelease
```

预发布版本标识符包括：

- alpha：内部测试版本
- beta：公开测试版本
- rc：候选发布版本

例如：
- v1.0.0-alpha.1
- v1.0.0-beta.2
- v1.0.0-rc.1

## 5. 版本发布流程

### 5.1 准备发布

1. 确保所有功能开发都已完成
2. 运行所有测试，确保测试通过
3. 更新CHANGELOG.md文件
4. 更新项目依赖版本

### 5.2 创建发布分支

1. 从develop分支创建发布分支，命名格式：`release/vX.Y.Z`
2. 在发布分支上进行最后的调整和测试
3. 修复发现的bug（但不添加新功能）

### 5.3 合并到main分支

1. 当发布分支准备就绪时，合并到main分支
2. 在main分支上创建版本标签：`vX.Y.Z`
3. 推送标签到远程仓库

### 5.4 合并到develop分支

1. 将发布分支合并到develop分支，确保develop分支包含所有发布内容
2. 删除发布分支

### 5.5 发布通知

1. 编写发布说明，包括：
   - 新增功能
   - 修复的bug
   - 不兼容的变更
   - 升级说明
2. 通知团队成员和相关 stakeholders

## 6. 版本标签创建

使用git命令创建版本标签：

```bash
# 创建带注释的标签
git tag -a v1.0.0 -m "Version 1.0.0 release"

# 推送标签到远程仓库
git push origin v1.0.0

# 推送所有标签到远程仓库
git push origin --tags
```

## 7. CHANGELOG.md 规范

### 7.1 格式

```markdown
# Changelog

## [Unreleased]
### Added
- 新增功能1
- 新增功能2

### Changed
- 修改功能1

### Fixed
- 修复bug1
- 修复bug2

## [1.0.0] - 2023-10-01
### Added
- 第一个稳定版本

[Unreleased]: https://github.com/username/repo/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/username/repo/releases/tag/v1.0.0
```

### 7.2 分类

- **Added**：新增的功能
- **Changed**：已有的功能变更
- **Deprecated**：即将移除的功能
- **Removed**：已移除的功能
- **Fixed**：修复的bug
- **Security**：与安全相关的修复

## 8. 版本发布示例

### 8.1 从develop分支创建发布分支

```bash
git checkout develop
git checkout -b release/v1.0.0
```

### 8.2 更新CHANGELOG.md

```markdown
## [1.0.0] - 2023-10-01
### Added
- 实现了网站爬取功能
- 添加了Markdown转换功能
- 实现了图片下载功能

### Fixed
- 修复了HTML解析错误
- 解决了图片链接处理问题
```

### 8.3 合并到main分支并创建标签

```bash
git checkout main
git merge --no-ff release/v1.0.0
git tag -a v1.0.0 -m "Version 1.0.0 release"
git push origin main
git push origin v1.0.0
```

### 8.4 合并到develop分支

```bash
git checkout develop
git merge --no-ff release/v1.0.0
git branch -d release/v1.0.0
```

## 9. 最佳实践

- 定期发布版本，保持版本号的递增
- 避免跳过版本号，保持版本号的连续性
- 详细记录每个版本的变更内容
- 发布前进行充分的测试
- 及时通知相关人员

## 10. 版本控制工具

- **git**：版本控制和标签管理
- **standard-version**：自动生成CHANGELOG和版本标签
- **GitHub/GitLab**：发布管理和通知
