# 关卡结算

**URL**: https://act.mihoyo.com/ys/ugc/tutorial/detail/mhx1du08nhwo

**爬取时间**: 2026-01-04 08:24:46

---

## 关卡结算


# 一、关卡结算的定义

<span style="color: blue; font-style: italic;">关卡结算</span>是由节点图触发的行为，触发结算后整个关卡将会结束，关卡结算结果将会被传递到<span style="color: red; font-style: italic;">外围系统</span>来更新<span style="color: red; font-style: italic;">排行榜</span>、<span style="color: red; font-style: italic;">竞技段位</span>相关的数据

# 二、关卡结算状态

关卡结算状态需要在游玩过程中动态修改，在调用结算关卡节点后，会按各玩家当前的结算状态进行结算

关卡结算状态是每个玩家的属性，由两个字段构成

<span style="color: blue; font-style: italic;">逃跑合法性</span>：当逃跑合法性为“否”时，玩家的结算状态都为“逃跑状态”

<span style="color: blue; font-style: italic;">结算状态</span>：仅当逃跑合法性为“是”，该字段才有意义，有“胜利”，“失败”，“未定”三种状态，作为加<span style="color: red; font-style: italic;">段位分</span>的判据

<span style="color: blue; font-style: italic;">胜利</span>：以该状态结算关卡时，获得对应计分模板的胜利分数

![](../images/关卡结算_mhx1du08nhwo_二关卡结算状态.png)

*失败*：以该状态结算关卡时，获得对应计分模板的失败分数

![](../images/关卡结算_mhx1du08nhwo_二关卡结算状态_2.png)

*未定*：玩家默认处于的状态，以该状态结算关卡时，获得对应计分模板的未定分数

![](../images/关卡结算_mhx1du08nhwo_二关卡结算状态_3.png)

# 三、关卡结算表现

关卡结算表现决定了对局会以何种形式进行结算，仅在对局内进行展示，并不会影响到外围系统

从系统菜单点击【关卡设置】，可进入关卡设置界面

![](../images/关卡结算_mhx1du08nhwo_三关卡结算表现.png)

在关卡设置界面的结算页签，即可进行关卡结算相关的设置

![](../images/关卡结算_mhx1du08nhwo_三关卡结算表现_2.png)

<span style="color: blue; font-style: italic;">结算界面类型</span>：决定了关卡结算时的界面显示样式，分为阵营结算和个人结算两种

<span style="color: blue; font-style: italic;">阵营结算</span>：以阵营为单位进行结算

![](../images/关卡结算_mhx1du08nhwo_三关卡结算表现_3.png)

<span style="color: blue; font-style: italic;">个人结算</span>：以个人为单位进行结算

![](../images/关卡结算_mhx1du08nhwo_三关卡结算表现_4.png)

<span style="color: blue; font-style: italic;">启用游戏内排名</span>：启用后，将可以使用排名设置节点，对结算阶段个人/阵营的展示顺序进行编辑

<span style="color: blue; font-style: italic;">排名数值比较顺序</span>：决定了排名数值映射到实际显示顺序的规则，分为由小到大和由大到小两种

<span style="color: blue; font-style: italic;">由小到大</span>：排名数值小的显示在上方

<span style="color: blue; font-style: italic;">由大到小</span>：排名数值大的显示在上方

# 四、以节点图管理关卡结算

* 结算关卡

![](../images/关卡结算_mhx1du08nhwo_四以节点图管理关卡结算.png)

* 设置玩家结算排名数值

![](../images/关卡结算_mhx1du08nhwo_四以节点图管理关卡结算_2.png)

* 设置阵营结算排名数值

![](../images/关卡结算_mhx1du08nhwo_四以节点图管理关卡结算_3.png)

* 设置玩家结算成功状态

![](../images/关卡结算_mhx1du08nhwo_四以节点图管理关卡结算_4.png)

* 设置阵营结算成功状态

![](../images/关卡结算_mhx1du08nhwo_四以节点图管理关卡结算_5.png)
