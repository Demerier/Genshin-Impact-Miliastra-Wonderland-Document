# 玩家

**URL**: https://act.mihoyo.com/ys/ugc/tutorial/detail/mhctmgi51lpo

**爬取时间**: 2026-01-04 08:05:17

---

## 玩家


# 一、玩家的概念

*玩家*一种特殊的抽象实体类型，用于描述游戏中“角色的从属概念”，如：

在提瓦特上，玩家队伍中可以编入多个角色。

在超限模式中，每个*玩家*只对应一个*角色*。

# 二、玩家的配置

玩家的具体配置通过玩家模板进行引用，模板配置入口如下：

![](../images/玩家_mhctmgi51lpo_二玩家的配置.png)

点击<span style="color: blue; font-style: italic;">新建模版</span>即可创建一个新的玩家模板

## 1.基础信息

![](../images/玩家_mhctmgi51lpo_1基础信息.png)

基础信息页签：可配置所有可用的玩家基础信息

<span style="color: blue; font-style: italic;">生效目标</span>：决定了该模板对哪些玩家生效

<span style="color: blue; font-style: italic;">等级</span>：覆写职业的初始等级

<span style="color: blue; font-style: italic;">出生点</span>：玩家可用的出生点列表，见预设点文档预设点

<span style="color: blue; font-style: italic;">初始职业</span>：该玩家模板的初始职业，职业定义见职业文档职业

<span style="color: blue; font-style: italic;">复苏</span>：玩家对应的复苏规则，见复苏规则文档复苏

<span style="color: blue; font-style: italic;">特殊被击倒损伤</span>：当角色因为溺水、摔伤等特殊原因被击倒时，扣除的生命的百分比

## 2.组件

![](../images/玩家_mhctmgi51lpo_2组件.png)

组件页签，可在此页签给玩家实体添加组件，或查看已添加的组件

玩家实体的可用组件概览

[自定义变量](自定义变量_mhso1b9wjica.md)

[全局计时器](全局计时器_mhawd6rl5kpy.md)

[单位状态](单位状态_mhd7nxrfa8im.md)

## 3.节点图

![](../images/玩家_mhctmgi51lpo_3节点图.png)

节点图配置页签，可在此页签给玩家实体添加节点图，或查看已添加的节点图

# 三、运行时特性

## **1.无物理实体**

玩家实体是一个纯逻辑实体

## **2.没有布设信息**

玩家实体并不会直接布设在场景上，因此没有布设信息

## **3.生命周期**

玩家实体的生命周期随关卡初始化创建，随关卡销毁而移除

当用户主动退出返回大厅时，玩家实体会被移除
