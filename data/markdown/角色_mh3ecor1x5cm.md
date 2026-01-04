# 角色

**URL**: https://act.mihoyo.com/ys/ugc/tutorial/detail/mh3ecor1x5cm

**爬取时间**: 2026-01-04 08:05:47

---

## 角色

*区别于*玩家实体*，*角色实体*指代的是游戏过程中玩家实际控制的走跑爬飞单位，有物理实体

# 一、角色模板

在超限模式中，玩家和角色是一一对应的，因此角色的<span style="color: blue; font-style: italic;">模板配置</span>作为<span style="color: blue; font-style: italic;">玩家模板</span>的一部分存在，入口在玩家模板的角色编辑页签下：

![](../images/角色_mh3ecor1x5cm_一角色模板.png)

页签概述：

：基础信息页签，角色这里对比其它实体仅有音效相关信息

：特化配置页签，角色这里对比其它实体仅有战斗设置相关参数

：通用组件页签，可在此页签给角色实体添加组件，或查看已添加的组件

：节点图配置页签，可在此页签给角色实体添加节点图，或查看已添加的节点图

# 二、角色实体的可用组件概览

[碰撞触发器](碰撞触发器_mh8w69rzuc3i.md)

[自定义变量](自定义变量_mhso1b9wjica.md)

[全局计时器](全局计时器_mhawd6rl5kpy.md)

[单位状态](单位状态_mhd7nxrfa8im.md)

[特效播放](特效播放_mh4ppo02m1o8.md)

[自定义挂接点](自定义挂接点_mhmshmimtegs.md)

[碰撞触发源](碰撞触发源_mhn95di01j84.md)

[音效播放器](音效播放器_mhwiv89yra02.md)

[背包组件](背包组件_mh5y5001vqd4.md)

[战利品](战利品_mh63ox06afy8.md)

[铭牌](铭牌_mh5n160t2b6w.md)

[文本气泡](文本气泡_mhwtz297kp6a.md)

[扫描标签](扫描标签_mhfc0lr1tcke.md)

[小地图标识](小地图标识_mh0pppib5eyc.md)

此外还有仅角色可以添加的装备栏组件

详情可见装备

# 三、运行时特性

* *角色在游戏过程中，会根据模板配置动态进行初始化，因此角色实体不具有对应的<span style="color: red; font-style: italic;">GUID</span>*
* *特殊的，当角色生命值归零时，角色实体上的节点图可以收到角色的<span style="color: red; font-style: italic;">实体销毁时事件</span>以及<span style="color: red; font-style: italic;">实体移除/销毁时事件</span>，而物件销毁时，事件会被推送到关卡实体上*
* 在联机游玩过程中，如果玩家主动返回大厅，则关卡会收到角色的移除事件
