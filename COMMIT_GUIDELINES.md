# Git提交规范

## 1. 提交信息格式

```
<类型>(<范围>): <描述>

[可选的正文]

[可选的页脚]
```

### 1.1 类型

必须是以下之一：

| 类型       | 描述                                                         |
|------------|--------------------------------------------------------------|
| feat       | 新功能、新特性                                               |
| fix        | 修复bug                                                      |
| docs       | 文档更新                                                     |
| style      | 代码风格更改（不影响功能）                                   |
| refactor   | 代码重构（既不是修复bug也不是添加新功能）                   |
| perf       | 性能优化                                                     |
| test       | 测试相关更改                                                 |
| build      | 构建系统或外部依赖项更改                                     |
| ci         | CI配置文件和脚本更改                                         |
| chore      | 其他不修改源代码或测试文件的更改                             |
| revert     | 回退之前的提交                                               |

### 1.2 范围

可选，用于说明提交影响的范围，例如：
- crawler
- parser
- downloader
- main
- docs
- config

### 1.3 描述

- 简短明了的描述，不超过50个字符
- 使用祈使句，动词开头
- 首字母小写
- 结尾不加标点符号

### 1.4 正文

- 详细描述提交的内容，说明更改的原因和影响
- 可以使用多行
- 每行不超过72个字符

### 1.5 页脚

- 用于关闭issue或添加重要说明
- 关闭issue示例：`Closes #123, #456`
- 重大更改示例：`BREAKING CHANGE: 更改了API接口`

## 2. 提交示例

### 2.1 新功能

```
feat(crawler): 添加断点续爬功能

实现了断点续爬功能，支持从上次中断的地方继续爬取

Closes #10
```

### 2.2 修复bug

```
fix(parser): 修复空图片链接匹配问题

解决了部分页面存在空图片链接的问题，改进了匹配逻辑

Closes #15
```

### 2.3 文档更新

```
docs: 更新README.md，添加使用说明

完善了项目的使用说明，包括安装步骤和配置方法
```

### 2.4 代码重构

```
refactor(downloader): 优化下载逻辑，提高效率

重构了下载器模块，使用异步下载提高效率
```

## 3. 分支管理策略

### 3.1 主要分支

- **master**：主分支，用于发布稳定版本
- **develop**：开发分支，用于集成各功能分支

### 3.2 辅助分支

- **feature/**：功能分支，用于开发新功能
- **bugfix/**：修复分支，用于修复bug
- **release/**：发布分支，用于准备发布版本
- **hotfix/**：热修复分支，用于紧急修复生产环境问题

### 3.3 分支命名规范

- `feature/功能名称`：例如 `feature/breakpoint-resume`
- `bugfix/问题描述`：例如 `bugfix/image-link-match`
- `release/版本号`：例如 `release/v1.0.0`
- `hotfix/问题描述`：例如 `hotfix/security-vulnerability`

### 3.4 分支创建与合并

1. **从develop分支创建feature分支**
   ```bash
   git checkout -b feature/new-feature develop
   ```

2. **完成功能开发后，合并到develop分支**
   ```bash
   git checkout develop
   git merge --no-ff feature/new-feature
   git branch -d feature/new-feature
   ```

3. **从develop分支创建release分支**
   ```bash
   git checkout -b release/v1.0.0 develop
   ```

4. **完成测试后，合并到master和develop分支**
   ```bash
   git checkout master
   git merge --no-ff release/v1.0.0
   git tag -a v1.0.0 -m "Version 1.0.0"
   git checkout develop
   git merge --no-ff release/v1.0.0
   git branch -d release/v1.0.0
   ```

5. **从master分支创建hotfix分支**
   ```bash
   git checkout -b hotfix/security-vulnerability master
   ```

6. **完成修复后，合并到master和develop分支**
   ```bash
   git checkout master
   git merge --no-ff hotfix/security-vulnerability
   git tag -a v1.0.1 -m "Version 1.0.1"
   git checkout develop
   git merge --no-ff hotfix/security-vulnerability
   git branch -d hotfix/security-vulnerability
   ```

## 4. 版本发布规范

### 4.1 版本号格式

遵循语义化版本控制（Semantic Versioning）：

```
MAJOR.MINOR.PATCH
```

- **MAJOR**：不兼容的API更改
- **MINOR**：向后兼容的新功能
- **PATCH**：向后兼容的bug修复

### 4.2 版本发布流程

1. 创建release分支
2. 更新版本号和CHANGELOG.md
3. 进行最终测试
4. 合并到master分支并打标签
5. 合并到develop分支
6. 删除release分支
7. 发布版本

## 5. CHANGELOG管理

### 5.1 CHANGELOG格式

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 新功能1
- 新功能2

### Changed
- 更改1
- 更改2

### Fixed
- 修复1
- 修复2

## [1.0.0] - 2026-01-01

### Added
- 初始版本
```

### 5.2 更新CHANGELOG的时机

- 在开发新功能或修复bug时，同步更新CHANGELOG.md
- 在创建release分支时，将Unreleased内容移动到对应版本

## 6. 代码审查规范

### 6.1 代码审查流程

1. 提交代码到功能分支
2. 创建Pull Request
3. 指定至少1名审查人员
4. 审查人员进行代码审查，提出修改意见
5. 作者根据意见修改代码
6. 审查通过后，合并到目标分支

### 6.2 代码审查重点

- 代码质量和可读性
- 功能正确性
- 性能影响
- 安全性
- 测试覆盖
- 代码规范

## 7. 最佳实践

1. **提交频率**：每个提交应该是一个完整的、可测试的更改
2. **提交大小**：每个提交应该专注于一个功能或修复
3. **提交信息**：清晰、准确地描述更改内容
4. **分支管理**：遵循分支命名规范，及时清理无用分支
5. **版本管理**：严格遵循语义化版本控制
6. **文档更新**：代码更改后及时更新相关文档
7. **代码审查**：所有代码更改都必须经过审查

## 8. 工具支持

### 8.1 提交信息验证

可以使用以下工具验证提交信息：
- [commitlint](https://commitlint.js.org/)
- [husky](https://typicode.github.io/husky/)

### 8.2 分支保护

在GitLab或GitHub上设置分支保护规则：
- 禁止直接推送到master和develop分支
- 要求Pull Request必须经过审查
- 要求通过CI测试

## 9. 违规处理

1. 提交信息不符合规范的，审查人员有权要求修改
2. 不遵循分支管理策略的，将被要求重新创建分支
3. 多次违规的，将进行团队内部沟通和培训

## 10. 修订历史

| 版本 | 日期       | 修订内容               | 修订人 |
|------|------------|------------------------|--------|
| 1.0  | 2026-01-04 | 初始版本               | 项目主管 |

---

**适用范围**：本规范适用于原神千星奇域官方文档爬取项目的所有Git操作。
**生效日期**：2026-01-04
