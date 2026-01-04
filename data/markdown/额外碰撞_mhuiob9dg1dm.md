# 额外碰撞

**URL**: https://act.mihoyo.com/ys/ugc/tutorial/detail/mhuiob9dg1dm

**爬取时间**: 2026-01-04 08:14:05

---

## 额外碰撞


# 一、额外碰撞组件的功能

碰撞阻挡，也称为碰撞检测，是指在游戏运行中为了模拟物理世界中的物体碰撞表现的功能。

除*原生碰撞*外，额外碰撞组件支持灵活配置需求的形状、大小和组合，作为实体运行时的生效碰撞范围，或者可攀爬范围。

额外碰撞组件可支持同时生效多个*额外碰撞*，他们的生效范围会进行叠加。

每个*额外碰撞*可支持同时生效多个碰撞范围，他们的生效范围也会进行叠加。

**原生碰撞**

原生碰撞是预制元件默认携带的碰撞。

可以通过配置“初始生效”，来设置“原生碰撞”是否开启

# 二、额外碰撞组件的编辑

## 1.添加组件

![](../images/额外碰撞_mhuiob9dg1dm_1添加组件.png)

(1)在实体或元件编辑界面中，打开组件编辑页签

(2)点击下方的“添加通用组件”，选择并点击“额外碰撞”，成功添加

 选中“额外碰撞组件”时，编辑中的实体会以蓝色显示“额外碰撞”组件当前生效的范围。

(3)点击“详细编辑”，展开编辑页

* **初始生效额外碰撞**

![](../images/额外碰撞_mhuiob9dg1dm_1添加组件_2.png)

![](../images/额外碰撞_mhuiob9dg1dm_1添加组件_3.png)


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">初始生效额外碰撞</span> | 当前配置生效的额外碰撞，对应“详细编辑”页内配置 |
| <span style="color: blue; font-style: italic;">额外碰撞结构列表</span> | 编辑实体所有额外碰撞枚举列表 |


* **原生碰撞**


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">原生碰撞生效</span> | 在基础属性页签中的“原生碰撞”支持配置生效与否 |
| <span style="color: blue;"></span><span style="color: blue; font-style: italic;">原生碰撞预览</span> | 若开启，则用蓝色点来显示原生碰撞范围 |


## 2.额外碰撞的编辑

![](../images/额外碰撞_mhuiob9dg1dm_2额外碰撞的编辑.png)

* 通过点击![](../images/额外碰撞_mhuiob9dg1dm_2额外碰撞的编辑_2.png)，添加“额外碰撞”。
* 新增的“额外碰撞”，默认配置初始生效。
* “序号:X”，X为“碰撞区序号”，作为节点输入项可以调整额外碰撞的参数

![](../images/额外碰撞_mhuiob9dg1dm_2额外碰撞的编辑_3.png)


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">初始生效</span> | 额外碰撞是否随实体创建一同激活生效 |
| <span style="color: blue; font-style: italic;">是否可攀爬</span> | 额外碰撞攀爬功能是否一同开启 |
| <span style="color: blue; font-style: italic;">\原生碰撞</span> | 提示原生碰撞是否生效 |
| <span style="color: blue; font-style: italic;">\原生碰撞预览 </span> | 开启可查看原生碰撞的范围 |


* 通过“添加额外碰撞”，可增加基础形状

![](../images/额外碰撞_mhuiob9dg1dm_2额外碰撞的编辑_4.png)


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">触发区形状</span> | 支持配置长方体、球体、胶囊体三种基础形状 |
| <span style="color: blue; font-style: italic;">中心</span> | 相对实体或元件中心的偏移 |
| <span style="color: blue; font-style: italic;">缩放倍率</span> | 支持配置形状在不同轴向上支持定义缩放 |
| <span style="color: blue; font-style: italic;">旋转</span> | 以中心位置为基准，在不同轴向上支持调整朝向 |


# 三、通过节点图管理额外碰撞

* 激活/关闭额外碰撞

通过选择实体、填入“额外碰撞序号”，调整该额外碰撞的生效与否。

若不生效，其可攀爬属性也不生效

![](../images/额外碰撞_mhuiob9dg1dm_三通过节点图管理额外碰撞.png)

* 激活/关闭额外碰撞可攀爬性

额外碰撞生效时，可以单独调整其可攀爬功能

![](../images/额外碰撞_mhuiob9dg1dm_三通过节点图管理额外碰撞_2.png)
