# 小地图标识

**URL**: https://act.mihoyo.com/ys/ugc/tutorial/detail/mh0pppib5eyc

**爬取时间**: 2026-01-04 08:17:51

---

## 小地图标识


# 一、小地图标识组件的功能

<span style="color: blue; font-style: italic;">小地图标识组件</span>，支持实体通过图标/范围等可视化标识显示在**预制小地图界面控件**中

小地图标识组件需要挂载于实体，支持<span style="color: red; font-style: italic;">玩家</span>、<span style="color: red; font-style: italic;">物件</span>、*造物*使用

小地图标识可以通过默认配置激活/关闭，也可以通过*节点图*控制指定小地图标识的激活/关闭

# **二、**小地图标识组件**的编**辑

## **1.添加组**件

![](../images/小地图标识_mh0pppib5eyc_1添加组件.png)

(1)在实体或元件编辑界面中，打开组件编辑页签

(2)点击下方的“添加组件”，选择并点击“小地图标识”，成功添加

(3)点击“详细编辑”，展开编辑页

## **2.**小地图标识**组**件的基础信息

![](../images/小地图标识_mh0pppib5eyc_2小地图标识组件的基础信息.png)


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">初始生效</span> | 下拉菜单提供小地图标识枚举  通过修改后面的勾选框，可以修改生效情况，修改后生效状态会同步到小地图标识详细编辑页内 |
| <span style="color: blue; font-style: italic;">\小地图标识列表</span> | 枚举实体配置的所有小地图标识 |


## 3. **添加小地图标识**

点击详细编辑可进入小地图标识的编辑

![](../images/小地图标识_mh0pppib5eyc_3添加小地图标识.png)

* 通过点击![](../images/小地图标识_mh0pppib5eyc_3添加小地图标识_2.png)，添加小地图标识。

添加的小地图标识**初始生效**默认开启。

* *<span style="color: blue; font-style: italic;">标记X</span>，X为**序号**，作为节点输入项可以调整小地图标识的初始生效参数。*

## 4. 小地图标识的参数说明

### (1)显示设置

![](../images/小地图标识_mh0pppib5eyc_1显示设置.png)


|  |  |  |
| --- | --- | --- |
| 配置参数 | 说明 | |
| <span style="color: blue; font-style: italic;">初始所有玩家可见</span> | 若开启，则小地图标识生效时，满足条件的所有玩家都可以在其小地图界面控件上看到该标识 | |
| <span style="color: blue; font-style: italic;">跟随物体可见性</span> | 若开启，则实体隐藏时，小地图标识一同隐藏 | |
| <span style="color: blue; font-style: italic;">显示优先级</span> | 在同一位置的小地图标识，造成堆叠后，优先级更高的会覆盖优先级低的。数字越大，优先级越高 | |


### (2)标记样式

![](../images/小地图标识_mh0pppib5eyc_2标记样式.png)


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">选择类型</span> | 分为图标、范围、标记点、玩家标记、造物头像几种，不同类型会带有不同的配置参数 |
| <span style="color: blue; font-style: italic;">显示高低差</span> | 开启后，高低差超过10m的实体会在小地图内额外标记 |


### (3)选择类型的分类

* 图标

![](../images/小地图标识_mh0pppib5eyc_3选择类型的分类.png)


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">选择图标</span> | 提供多种可供选择的图标 |
| <span style="color: blue; font-style: italic;">底图</span> | 提供无、圆形 |
| <span style="color: blue; font-style: italic;">底图外框颜色</span> | 图标底色支持选择，包括指定颜色和逻辑颜色。  逻辑颜色包括  【敌友关系】敌方红色、友方绿色、自身蓝色  【跟随自身阵营】根据自身当前的阵营颜色  【跟随所有者阵营】跟随当前实体的所有者阵营颜色 |
| <span style="color: blue; font-style: italic;">是否可点击</span> | 开启后，展开地图，点击标识点，会显示配置信息 |
| <span style="color: blue; font-style: italic;">文本内容</span> | 支持配置点击后的右侧显示文本 |


* 范围

![](../images/小地图标识_mh0pppib5eyc_3选择类型的分类_6.png)


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">范围样式</span> | 支持范围边缘显示为实线、虚线 |
| <span style="color: blue; font-style: italic;">颜色</span> | 图标底色支持选择，包括指定颜色和逻辑颜色。  逻辑颜色包括  【敌友关系】敌方红色、友方绿色、自身蓝色  【跟随自身阵营】根据自身当前的阵营颜色  【跟随所有者阵营】跟随当前实体的所有者阵营颜色 |
| <span style="color: blue; font-style: italic;">范围大小(m）</span> | 根据配置的尺寸，在小地图界面控件中，按比例显示 |


* 标记点

![](../images/小地图标识_mh0pppib5eyc_3选择类型的分类_9.png)


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">样式预览</span> | 展示点的样式，不可修改，且点在大地图中不可点击 |
| <span style="color: blue; font-style: italic;">颜色</span> | 图标底色支持选择，包括指定颜色和逻辑颜色。  逻辑颜色包括  【敌友关系】敌方红色、友方绿色、自身蓝色  【跟随自身阵营】根据自身当前的阵营颜色  【跟随所有者阵营】跟随当前实体的所有者阵营颜色 |


* 玩家标记

![](../images/小地图标识_mh0pppib5eyc_3选择类型的分类_11.png)


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">样式预览</span> | 预览图标为创作者(奇匠)的当前头像，实际生效的图标需要通过节点传入，且玩家标记在大地图中不可点击 |
| <span style="color: blue; font-style: italic;">底图外框颜色</span> | 图标底色支持选择，包括指定颜色和逻辑颜色。  逻辑颜色包括  【敌友关系】敌方红色、友方绿色、自身蓝色  【跟随自身阵营】根据自身当前的阵营颜色  【跟随所有者阵营】跟随当前实体的所有者阵营颜色 |


* 造物头像

![](../images/小地图标识_mh0pppib5eyc_3选择类型的分类_13.png)


|  |  |
| --- | --- |
| <span style="color: blue; font-style: italic;">头像预览</span> | 仅造物可以设置此项，仅提供预览，不可编辑 |
| <span style="color: blue; font-style: italic;">底图外框颜色</span> | 图标底色支持选择，包括指定颜色和逻辑颜色。  逻辑颜色包括  【敌友关系】敌方红色、友方绿色、自身蓝色  【跟随自身阵营】根据自身当前的阵营颜色 |
| <span style="color: blue; font-style: italic;">是否可点击</span> | 开启后，展开地图，点击标识点，会显示配置信息 |
| **标记名称** | 标记的名称 |
| <span style="color: blue; font-style: italic;">文本内容</span> | 支持配置点击后的右侧显示文本 |


# **三、通过节点图管理**小地图标识

* **修改小地图标识生效状态**

通过节点输入的小地图标识序号列表，批量修改目标实体的小地图标识生效状态。

![](../images/小地图标识_mh0pppib5eyc_三通过节点图管理小地图标识.png)

* **修改可见小地图标识的玩家列表**

![](../images/小地图标识_mh0pppib5eyc_三通过节点图管理小地图标识_2.png)

* **修改小地图标识的玩家标记**

![](../images/小地图标识_mh0pppib5eyc_三通过节点图管理小地图标识_3.png)

* **修改小地图缩放**

![](../images/小地图标识_mh0pppib5eyc_三通过节点图管理小地图标识_4.png)

* **修改追踪小地图标识的玩家列表**

![](../images/小地图标识_mh0pppib5eyc_三通过节点图管理小地图标识_5.png)

* **查询指定小地图标识信息**

![](../images/小地图标识_mh0pppib5eyc_三通过节点图管理小地图标识_6.png)

* **获取实体的小地图标识状态**

![](../images/小地图标识_mh0pppib5eyc_三通过节点图管理小地图标识_7.png)
