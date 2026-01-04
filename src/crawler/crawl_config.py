#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
正式爬取配置
定义正式爬取的参数、页面列表和监控指标
"""

from typing import List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class CrawlConfig:
    """爬取配置类"""

    # 请求频率控制
    request_delay_min: float = 2.0
    request_delay_max: float = 3.0
    max_retries: int = 5
    timeout: int = 30

    # 页面加载配置
    wait_until: str = "networkidle"
    wait_timeout: int = 30000
    additional_wait: int = 1000

    # 并发控制
    max_concurrent: int = 1

    # 数据提取配置
    extract_title: bool = True
    extract_content: bool = True
    extract_links: bool = True
    extract_images: bool = True

    # 质量控制
    min_content_length: int = 100
    validate_links: bool = True

    # 存储配置
    save_markdown: bool = True
    save_html: bool = False
    markdown_dir: str = "data/markdown"
    html_dir: str = "data/html"
    images_dir: str = "data/images"

    # 日志配置
    log_level: str = "INFO"
    log_dir: str = "logs/crawl"

    # 增量更新配置
    enable_incremental: bool = True
    skip_existing: bool = False

    # 断点续传配置
    enable_resume: bool = True
    resume_file: str = "data/crawl_resume.json"


@dataclass
class CrawlPage:
    """爬取页面配置"""

    url: str
    name: str
    description: str
    category: str = "default"
    priority: int = 1

    # 预期指标
    expected_load_time: float = 10.0
    expected_content_length: int = 500

    # 提取字段
    extract_fields: List[str] = field(default_factory=lambda: ["title", "content", "links", "images"])


# 正式爬取页面列表
# 根据目标网站结构设计，包含所有144个教程页面
CRAWL_PAGES = [
    # 基础页面（优先级最高）
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh29wpicgvh0",
        name="读前须知",
        description="读前须知，包含重要声明和特殊符号说明",
        category="basic",
        priority=0
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhs2w008wf14",
        name="更新日志",
        description="更新日志，记录内容更新历史",
        category="basic",
        priority=0
    ),

    # 1. 界面介绍（13个页面）
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhz71urk21nq",
        name="界面介绍",
        description="界面介绍，介绍各种功能界面",
        category="interface",
        priority=1
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhn4bsi5lb58",
        name="整体界面",
        description="整体界面介绍页面，包含7张图片",
        category="interface",
        priority=1
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhwe1n94b1x6",
        name="地形编辑",
        description="地形编辑功能介绍",
        category="interface",
        priority=1
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhnffmieeqbg",
        name="实体摆放",
        description="实体摆放功能介绍",
        category="interface",
        priority=1
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhwp5h9d4h3e",
        name="元件库",
        description="元件库功能介绍",
        category="interface",
        priority=1
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhexhcr1qjh2",
        name="战斗预设",
        description="战斗预设功能介绍",
        category="interface",
        priority=1
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhn9vpia00qc",
        name="关卡设置",
        description="关卡设置功能介绍",
        category="interface",
        priority=1
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhie54ik9ovg",
        name="试玩",
        description="试玩功能介绍",
        category="interface",
        priority=1
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh9fj3rudd9q",
        name="多人试玩",
        description="多人试玩功能介绍",
        category="interface",
        priority=1
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mho777i0ga90",
        name="千星沙箱",
        description="千星沙箱功能介绍",
        category="interface",
        priority=1
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhxbd59urbfu",
        name="资产导入导出",
        description="资产导入导出功能介绍",
        category="interface",
        priority=1
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhq6wdimcd84",
        name="撤销与还原",
        description="撤销与还原功能介绍",
        category="interface",
        priority=1
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhf66q9jc4uq",
        name="奇域资产中心",
        description="奇域资产中心功能介绍",
        category="interface",
        priority=1
    ),

    # 2. 概念介绍（113个页面）
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhdtk89yhd6q",
        name="概念介绍",
        description="概念介绍，说明各种基础概念",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh2xoxrop0la",
        name="单位",
        description="单位概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhctmgi51lpo",
        name="玩家",
        description="玩家概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh796lr44x0e",
        name="复苏",
        description="复苏概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh3ecor1x5cm",
        name="角色",
        description="角色概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhufqo0c0tqw",
        name="造物",
        description="造物概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhlh4n9m4i56",
        name="物件",
        description="物件概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhciimiw86jg",
        name="本地投射物",
        description="本地投射物概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh3pgiraqkiu",
        name="关卡",
        description="关卡概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhjx2miruaos",
        name="功能",
        description="功能概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh3oxo0ojgxk",
        name="基础信息",
        description="基础信息概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhuqbn9yn5bu",
        name="变换原生碰撞可见性和创建设置",
        description="变换原生碰撞可见性和创建设置概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhrutdio6904",
        name="模型",
        description="模型概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhe1ixri46ta",
        name="阵营",
        description="阵营概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhzldmiwdgu4",
        name="单位标签",
        description="单位标签概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhqmrlr6h58e",
        name="实体布设组",
        description="实体布设组概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhlb1vivioys",
        name="负载优化",
        description="负载优化概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh6fj30p2cmo",
        name="数据复制粘贴",
        description="数据复制粘贴概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhtwkur42see",
        name="特化配置",
        description="特化配置概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhvyqz9xwu0q",
        name="基础战斗属性",
        description="基础战斗属性概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhw9ut96q96y",
        name="仇恨配置",
        description="仇恨配置概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhvg40rc5w9i",
        name="受击盒设置",
        description="受击盒设置概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mha42r0cwx74",
        name="战斗设置",
        description="战斗设置概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh0ucw9e76f6",
        name="能力单元",
        description="能力单元概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh3rgo0c16c8",
        name="常规设置",
        description="常规设置概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhei6orvcbkm",
        name="通用组件",
        description="通用组件概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh5jko05fzyw",
        name="选项卡",
        description="选项卡概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhnmcmipncrg",
        name="基础运动器",
        description="基础运动器概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh8w69rzuc3i",
        name="碰撞触发器",
        description="碰撞触发器概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhso1b9wjica",
        name="自定义变量",
        description="自定义变量概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhaqt9rgqv4u",
        name="投射运动器",
        description="投射运动器概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhstl890y7xe",
        name="角色扰动装置",
        description="角色扰动装置概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhawd6rl5kpy",
        name="全局计时器",
        description="全局计时器概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh6rh59iil2i",
        name="单位状态",
        description="单位状态概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhufb90zbnts",
        name="定时器",
        description="定时器概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh2pir0hat1s",
        name="命中检测",
        description="命中检测概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhuiob9dg1dm",
        name="额外碰撞",
        description="额外碰撞概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhuts59m9gju",
        name="跟随运动器",
        description="跟随运动器概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh4ppo02m1o8",
        name="特效播放",
        description="特效播放概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhmshmimtegs",
        name="自定义挂接点",
        description="自定义挂接点概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhn95di01j84",
        name="碰撞触发源",
        description="碰撞触发源概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhwiv89yra02",
        name="音效播放器",
        description="音效播放器概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh5n160t2b6w",
        name="铭牌",
        description="铭牌概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhwtz297kp6a",
        name="文本气泡",
        description="文本气泡概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh5y5001vqd4",
        name="背包组件",
        description="背包组件概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh63ox06afy8",
        name="战利品",
        description="战利品概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mho6gviqhsqs",
        name="商店组件",
        description="商店组件概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhfc0lr1tcke",
        name="扫描标签",
        description="扫描标签概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh0pppib5eyc",
        name="小地图标识",
        description="小地图标识概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhgkan9wgil6",
        name="光源",
        description="光源概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhjwjrr5n73i",
        name="节点图",
        description="节点图概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhk23ora1wom",
        name="基础概念",
        description="基础概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhb3ho0k5l2w",
        name="节点图编辑指引",
        description="节点图编辑指引说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhmzm3rltetq",
        name="资产",
        description="资产概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhe1030vx380",
        name="特效",
        description="特效概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhw3s1ig4g0k",
        name="预设状态",
        description="预设状态概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh57xz9afh7e",
        name="技能动画",
        description="技能动画概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhnapxrumtzy",
        name="界面控件",
        description="界面控件概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhwkfsitckrw",
        name="交互按钮界面控件",
        description="交互按钮界面控件概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhjja1ipq9ck",
        name="道具展示界面控件",
        description="道具展示界面控件概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhnltrr3g966",
        name="文本框界面控件",
        description="文本框界面控件概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhen7r0djxkg",
        name="弹窗界面控件",
        description="弹窗界面控件概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhwpzpixrad0",
        name="进度条界面控件",
        description="进度条界面控件概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhnrdor7uyra",
        name="计时器界面控件",
        description="计时器界面控件概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhesro0hyn5k",
        name="计分板界面控件",
        description="计分板界面控件概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh2teu0bmfbc",
        name="卡牌选择器界面控件",
        description="卡牌选择器界面控件概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mheybl0mdcqo",
        name="高级概念",
        description="高级概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhewyi0fjfvs",
        name="界面控件组管理",
        description="界面控件组管理概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhozt0r74ng6",
        name="界面布局",
        description="界面布局概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhg1700h8bug",
        name="界面控件组",
        description="界面控件组概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhfua005zpeg",
        name="主镜头",
        description="主镜头概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhjsw9rluwou",
        name="外围系统",
        description="外围系统概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mho2rt9ir6ay",
        name="排行榜",
        description="排行榜概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhf45sisuup8",
        name="竞技段位",
        description="竞技段位概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh65jrr2yj3i",
        name="成就",
        description="成就概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhx1du08nhwo",
        name="关卡结算",
        description="关卡结算概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhjdhpi4sd10",
        name="奇域礼盒",
        description="奇域礼盒概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mht8l59439d6",
        name="资源系统",
        description="资源系统概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhbgx0rspbqu",
        name="道具",
        description="道具概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhkl2yin0cxo",
        name="装备",
        description="装备概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh2cr30yeak0",
        name="货币",
        description="货币概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhogfq9bf86q",
        name="背包",
        description="背包概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhkfj1iilnck",
        name="掉落物",
        description="掉落物概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhi9s7isvp50",
        name="商店",
        description="商店概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mho81frl33im",
        name="技能",
        description="技能概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh6ate95agb6",
        name="技能资源",
        description="技能资源概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhodlcrpht3q",
        name="职业",
        description="职业概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhfvn30ctm9c",
        name="预设点",
        description="预设点概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhhl0gire830",
        name="护盾",
        description="护盾概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh333vim2h44",
        name="路径",
        description="路径概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhd7nxrfa8im",
        name="单位状态",
        description="单位状态概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhh5zgirw9cc",
        name="其它概念",
        description="其它概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhzcw29qjjma",
        name="局内存档",
        description="局内存档概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhk59aiqtwyk",
        name="多语言文本",
        description="多语言文本概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhaneb9qnvay",
        name="文字聊天",
        description="文字聊天概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhq9b601kh9k",
        name="背景音乐",
        description="背景音乐概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhdznsie9up8",
        name="环境配置",
        description="环境配置概念说明",
        category="concept",
        priority=2
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhzhzb9rw0uy",
        name="元件组",
        description="元件组概念说明",
        category="concept",
        priority=2
    ),

    # 3. 节点介绍（13个页面）
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhsok60iqlxk",
        name="节点介绍",
        description="节点介绍，介绍各种节点",
        category="node",
        priority=3
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhuto3r800b2",
        name="服务器节点",
        description="服务器节点介绍",
        category="node",
        priority=3
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhw66orrrfkm",
        name="执行节点",
        description="执行节点介绍",
        category="node",
        priority=3
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhn7ko01v3yw",
        name="事件节点",
        description="事件节点介绍",
        category="node",
        priority=3
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhe8yn9bysd6",
        name="流程控制节点",
        description="流程控制节点介绍",
        category="node",
        priority=3
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhwbqlrw655q",
        name="查询节点",
        description="查询节点介绍",
        category="node",
        priority=3
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhnd4l069tk0",
        name="运算节点",
        description="运算节点介绍",
        category="node",
        priority=3
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhlv230i3opc",
        name="客户端节点",
        description="客户端节点介绍",
        category="node",
        priority=3
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mholjx05ji8w",
        name="查询节点",
        description="查询节点介绍",
        category="node",
        priority=3
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhfmxw9fn6n6",
        name="运算节点",
        description="运算节点介绍",
        category="node",
        priority=3
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh6obvipqv1g",
        name="执行节点",
        description="执行节点介绍",
        category="node",
        priority=3
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhxppurzujfq",
        name="流程控制节点",
        description="流程控制节点介绍",
        category="node",
        priority=3
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhor3u09y7u0",
        name="其它节点",
        description="其它节点介绍",
        category="node",
        priority=3
    ),

    # 4. 辅助功能（2个页面）
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhoyplr76zr2",
        name="辅助功能",
        description="辅助功能介绍",
        category="auxiliary",
        priority=4
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mho2hirgodxi",
        name="负载计算功能",
        description="负载计算功能介绍",
        category="auxiliary",
        priority=4
    ),

    # 5. 附录（17个页面）
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhsumxr9cf3y",
        name="附录",
        description="附录，包含补充内容",
        category="appendix",
        priority=5
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhrvqvioautg",
        name="能力单元效果",
        description="能力单元效果说明",
        category="appendix",
        priority=5
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhyg4i0inazs",
        name="造物行为模式图鉴",
        description="造物行为模式图鉴说明",
        category="appendix",
        priority=5
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhpsmb91keka",
        name="造物行为模式的未入战行为",
        description="造物行为模式的未入战行为说明",
        category="appendix",
        priority=5
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhzys1ic5eok",
        name="造物技能说明",
        description="造物技能说明",
        category="appendix",
        priority=5
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhou93r2pxv2",
        name="单位状态效果池",
        description="单位状态效果池说明",
        category="appendix",
        priority=5
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhk7nlregm9q",
        name="节点图高级特性",
        description="节点图高级特性说明",
        category="appendix",
        priority=5
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhkirfrna1fy",
        name="泛型引脚",
        description="泛型引脚说明",
        category="appendix",
        priority=5
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhtshailzs7w",
        name="节点图变量",
        description="节点图变量说明",
        category="appendix",
        priority=5
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhty17iqeht0",
        name="复合节点",
        description="复合节点说明",
        category="appendix",
        priority=5
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhu951iz7wz8",
        name="节点图日志",
        description="节点图日志说明",
        category="appendix",
        priority=5
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhrnuz9izfne",
        name="客户端节点图日志",
        description="客户端节点图日志说明",
        category="appendix",
        priority=5
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhip8yit341o",
        name="复合节点图日志",
        description="复合节点图日志说明",
        category="appendix",
        priority=5
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhlaj0r9bldi",
        name="信号",
        description="信号说明",
        category="appendix",
        priority=5
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhubgk9yy8gy",
        name="字典",
        description="字典说明",
        category="appendix",
        priority=5
    ),
    CrawlPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh3fmi0t99ns",
        name="结构体",
        description="结构体说明",
        category="appendix",
        priority=5
    ),
]


# 页面解析规则
PARSING_RULES = {
    "content_selectors": [
        ".doc-view",
        ".content",
        "main",
        "article",
        ".article",
        ".post",
        ".page-content",
        ".entry-content",
        ".main-content",
        "#content",
        ".container",
        ".wrapper"
    ],

    "title_selectors": [
        "title",
        "h1",
        ".title",
        ".page-title",
        "#title"
    ],

    "image_selectors": [
        "img[data-src]",
        "img[src]"
    ],

    "link_selectors": [
        "a[href]"
    ],

    "list_selectors": [
        "ul",
        "ol",
        ".prosemirror-list-new"
    ],

    "table_selectors": [
        "table",
        ".table"
    ]
}


# 数据提取字段定义
EXTRACTION_FIELDS = {
    "title": {
        "required": True,
        "type": "str",
        "description": "页面标题"
    },
    "content": {
        "required": True,
        "type": "str",
        "description": "页面主要内容（Markdown格式）"
    },
    "links": {
        "required": False,
        "type": "list",
        "description": "页面中的链接列表"
    },
    "images": {
        "required": False,
        "type": "list",
        "description": "页面中的图片URL列表"
    },
    "load_time": {
        "required": True,
        "type": "float",
        "description": "页面加载时间（秒）"
    },
    "status_code": {
        "required": True,
        "type": "int",
        "description": "HTTP响应状态码"
    },
    "content_length": {
        "required": True,
        "type": "int",
        "description": "提取的内容长度"
    },
    "image_count": {
        "required": False,
        "type": "int",
        "description": "提取的图片数量"
    },
    "link_count": {
        "required": False,
        "type": "int",
        "description": "提取的链接数量"
    }
}


# 监控指标定义
MONITORING_METRICS = {
    "success_rate": {
        "description": "成功爬取的页面比例",
        "formula": "successful_pages / total_pages * 100"
    },
    "average_load_time": {
        "description": "平均页面加载时间",
        "formula": "sum(load_time) / total_pages"
    },
    "average_content_length": {
        "description": "平均内容长度",
        "formula": "sum(content_length) / total_pages"
    },
    "total_images_downloaded": {
        "description": "下载的图片总数",
        "formula": "sum(image_count)"
    },
    "total_links_extracted": {
        "description": "提取的链接总数",
        "formula": "sum(link_count)"
    },
    "retry_count": {
        "description": "重试次数",
        "formula": "sum(retries)"
    },
    "error_count": {
        "description": "错误次数",
        "formula": "sum(errors)"
    }
}


# 正式爬取配置实例
CRAWL_CONFIG = CrawlConfig(
    request_delay_min=2.0,
    request_delay_max=3.0,
    max_retries=5,
    timeout=30,
    wait_until="networkidle",
    wait_timeout=30000,
    additional_wait=1000,
    max_concurrent=1,
    extract_title=True,
    extract_content=True,
    extract_links=True,
    extract_images=True,
    min_content_length=100,
    validate_links=True,
    save_markdown=True,
    save_html=False,
    markdown_dir="data/markdown",
    html_dir="data/html",
    images_dir="data/images",
    log_level="INFO",
    log_dir="logs/crawl",
    enable_incremental=True,
    skip_existing=False,
    enable_resume=True,
    resume_file="data/crawl_resume.json"
)
