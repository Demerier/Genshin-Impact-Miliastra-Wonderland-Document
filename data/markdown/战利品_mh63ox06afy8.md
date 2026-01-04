# 战利品

**URL**: https://act.mihoyo.com/ys/ugc/tutorial/detail/mh63ox06afy8

**爬取时间**: 2026-01-04 08:16:29

---

## 战利品


# 一、战利品组件的功能

战利品组件支持创作者(奇匠)配置一份固定的战利品集合模板数据，在组件的持有者被击倒时根据此份数据模板创建战利品

在设计上被推荐用于战利品相关的概念实现

战利品组件仅支持配置一份战利品模板数据

# 二、战利品组件的编辑

## 1.添加组件

![](../images/战利品_mh63ox06afy8_1添加组件.png)

(1)在实体或元件编辑界面中，打开组件编辑页签

(2)点击下方的“添加通用组件”，选择并点击“战利品”，成功添加

(3)点击“详细编辑”，展开编辑页

## 2.基础概念

![](../images/战利品_mh63ox06afy8_2基础概念.png)

### (1)基础设置

掉落表现以及掉落方式相关的配置

<span style="color: blue; font-style: italic;">销毁时掉落形态</span>：当组件的归属者被击倒时，掉落配置内的数据处理方式

<span style="color: blue; font-style: italic;">分离掉落</span>：掉落内容中的虚拟物品每一条转化成对应的掉落物进行掉落

<span style="color: blue; font-style: italic;">合并掉落</span>：掉落内容中的虚拟物品转化为一个掉落物进行掉落

<span style="color: blue; font-style: italic;">战利品掉落形式</span>：分为全员一份和每人一份

<span style="color: blue; font-style: italic;">全员一份</span>：所有玩家共享同一份掉落物，当一名玩家拾取时，其他玩家无法再次拾取

<span style="color: blue; font-style: italic;">每人一份</span>：每一个玩家的客户端会独立掉落一份该道具，玩家之间的拾取行为互不干预

<span style="color: blue; font-style: italic;">对应掉落物外形</span>：配置一个<span style="color: red; font-style: italic;">掉落物</span>元件，掉落物是一个有物理实体的元件，当虚拟道具被创建在场景上，会以关联掉落物的模型进行展示。此处仅当选择合并掉落时生效，如果选择分离掉落，则每一个掉落物会使用道具或货币模板自身配置的关联掉落物

### (2)掉落内容

掉落的虚拟道具数据配置，点击添加物品即可配置一个虚拟物品列表

<span style="color: blue; font-style: italic;">物品列表</span>：可以选取所有已定义的道具、货币模板及数量

![](../images/战利品_mh63ox06afy8_2掉落内容.png)

# 三、战利品拾取实例

![](../images/战利品_mh63ox06afy8_三战利品拾取实例.png)

# 四、节点图操作战利品组件

### 战利品组件相关执行节点

* 触发战利品掉落

![](../images/战利品_mh63ox06afy8_战利品组件相关执行节点.png)

* 设置战利品掉落内容

![](../images/战利品_mh63ox06afy8_战利品组件相关执行节点_2.png)
