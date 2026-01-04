# 货币

**URL**: https://act.mihoyo.com/ys/ugc/tutorial/detail/mh2cr30yeak0

**爬取时间**: 2026-01-04 08:25:55

---

## 货币


# 一、货币的定义

货币是玩法中的一般等价物，用于标定虚拟道具的价值，以及在交易行为中作为交易能否成交的判据。货币可以被单位持有，并随交易或节点图逻辑增加或消耗

# 二、货币的编辑

通过【货币与背包】按钮进入编辑界面

![](../images/货币_mh2cr30yeak0_二货币的编辑.png)

进入货币页签，进行货币的详细编辑

![](../images/货币_mh2cr30yeak0_二货币的编辑_2.png)

<span style="color: blue; font-style: italic;">货币名称</span>：由创作者(奇匠)定义的货币的命名

<span style="color: blue; font-style: italic;">配置ID</span>：货币数据的唯一标识

**基础属性**

* *<span style="color: blue; font-style: italic;">图标</span>：游玩时货币的显示样式，可以点击图标在预制图标中选择一个*
* *<span style="color: blue; font-style: italic;">销毁时掉落形态</span>：当货币的持有者被击倒时，货币执行的逻辑*

<span style="color: blue; font-style: italic;">掉落</span>：转化为掉落物并创建在场景里

<span style="color: blue; font-style: italic;">销毁</span>：货币销毁

<span style="color: blue; font-style: italic;">保留</span>：仅针对角色生效，在角色复活后会保留之前持有的货币，对于角色以外的单位，等同于销毁

* *<span style="color: blue; font-style: italic;">战利品掉落形式</span>：货币掉落时，会转化为一个实体掉落在场景内*

<span style="color: blue; font-style: italic;">全员一份</span>：所有玩家共享同一份货币掉落物实体，当一名玩家拾取时，其他玩家无法再次拾取

<span style="color: blue; font-style: italic;">每人一份</span>：每一个玩家的本地会独立掉落一份货币对应的掉落物实体，玩家之间的拾取行为互不干预

* *<span style="color: blue; font-style: italic;">对应掉落物外形</span>：配置一个<span style="color: red; font-style: italic;">掉落物元件</span>，掉落物是一个有物理实体的元件，当虚拟道具被创建在场景上，会以关联掉落物的模型进行展示*
* *<span style="color: blue; font-style: italic;">显示优先级</span>：数字越大在背包中的显示越靠前*
