# 卡牌选择器界面控件

**URL**: https://act.mihoyo.com/ys/ugc/tutorial/detail/mh2teu0bmfbc

**爬取时间**: 2026-01-04 08:22:07

---

## 卡牌选择器界面控件

*卡牌选择器提供编辑简单的决策交互界面功能

支持对可决策内容进行编辑，包括决策时间、决策项的表现、决策的交互方式等

# **一、卡牌选择器**的功能

![](../images/卡牌选择器界面控件_mh2teu0bmfbc_一卡牌选择器的功能.png)

关卡运行中，可通过默认配置/节点图唤起<span style="color: blue; font-style: italic;">卡牌选择器</span>

支持玩家进行交互，并在超时/交互后向节点图发送*决策弹窗完成事件*

# **二、卡牌选择器的编**辑

![](../images/卡牌选择器界面控件_mh2teu0bmfbc_二卡牌选择器的编辑.png)

## **1.添加卡牌选择器**

* *在**界面控件组编辑窗口**，添加界面控件模板-卡牌选择器*
* 卡牌选择器默认为一个界面控件组

![](../images/卡牌选择器界面控件_mh2teu0bmfbc_1添加卡牌选择器.png)

## **2.界面配**置 - 卡牌选择器

是卡牌选择器的整体外显和使用规则配置处，支持玩家定义卡牌选择器的外显风格

### (1)可见性

![](../images/卡牌选择器界面控件_mh2teu0bmfbc_1可见性.png)


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">索引</span> | 用于唤起卡牌选择器节点的入参 |
| <span style="color: blue; font-style: italic;">初始可见</span> | 若不勾选，则界面控件激活后不可见  支持通过节点图-*修改界面控件组状态*调整该参数 |


### (2)变换

![](../images/卡牌选择器界面控件_mh2teu0bmfbc_2变换.png)


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">位置</span> | 支持手写输入界面控件位置  也支持通过编辑界面拖动该界面控件，进行调整 |
| <span style="color: blue; font-style: italic;">\大小</span> | 不支持配置 |
| <span style="color: blue; font-style: italic;">层级</span> | 数字越大显示层级越高 |


## **3.界面配**置 - 决策面板

### (1)页面设置

![](../images/卡牌选择器界面控件_mh2teu0bmfbc_1页面设置.png)

#### a.可见性

![](../images/卡牌选择器界面控件_mh2teu0bmfbc_a可见性.png)

#### b.卡牌选择器

![](../images/卡牌选择器界面控件_mh2teu0bmfbc_b卡牌选择器.png)


|  |  |  |
| --- | --- | --- |
| 配置参数 | | 说明 |
| <span style="color: blue; font-style: italic;">显示标题</span> | | 勾选则当前卡牌选择器有最上方标题，并且可编辑 |
| <span style="color: blue; font-style: italic;">标题文本</span> | | 支持编辑显示标题 |
| <span style="color: blue; font-style: italic;">界面布局</span> | 枚举两种样式供选择 | |
| 列表 |  |
| 网格 |  |


#### **c.显示已选择数量**

![](../images/卡牌选择器界面控件_mh2teu0bmfbc_c显示已选择数量.png)


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">显示已选择数量</span> | 是否在卡牌选择器界面上显示当前已经选择个数 |


#### **d.显示可重置次数**

![](../images/卡牌选择器界面控件_mh2teu0bmfbc_d显示可重置次数.png)


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">显示可重置次数</span> | 是否在卡牌选择器界面上显示选择项可重置的下限和上限个数 |


#### **e.时间显示**

![](../images/卡牌选择器界面控件_mh2teu0bmfbc_e时间显示.png)


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">显示剩余时间(s)</span> | 若勾选，则倒计时时间结束时，自动关闭卡牌选择器，无需手动关闭  若倒计时时间结束前，玩家已完成交互，则后续界面是否留存遵从<span style="color: blue; font-style: italic;">决策完成样式</span>和<span style="color: blue; font-style: italic;">决策完成样式停留时长</span> |
| <span style="color: blue; font-style: italic;">结束前预警时间(s)</span> | 倒计时剩余时间达到配置时间时，会在时间显示界面空间上，做红色闪烁提示表现 |


#### **f.其他设**置

![](../images/卡牌选择器界面控件_mh2teu0bmfbc_f其他设置.png)


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">单人游玩时暂停游戏</span> | 若勾选则当关卡为单人关卡时，进行选择的时候会暂停游戏 |
| <span style="color: blue; font-style: italic;">控件可收起</span> | 若勾选，则卡牌选择器支持主动缩起  可选择暂不处理，后续处理或直到超时 |
| <span style="color: blue; font-style: italic;">可放弃选择</span> | 若勾选，则卡牌选择器支持主动关闭，卡牌选择器会增加关闭界面控件并支持交互  若选择关闭，则触发节点图的 决策完成-主动关闭事件 |


### (2)选项配置

![](../images/卡牌选择器界面控件_mh2teu0bmfbc_2选项配置.png)

#### **a.已知卡牌设置**

![](../images/卡牌选择器界面控件_mh2teu0bmfbc_a已知卡牌设置.png)


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">显示卡牌图标</span> | 外显卡牌是否包含图标，若包含，则支持指定设置中配置其图标 |
| <span style="color: blue; font-style: italic;">显示卡牌标题</span> | 外显卡牌是否显示标题，若包含，则支持指定设置中配置其标题 |
| <span style="color: blue; font-style: italic;">显示卡牌描述</span> | 外显卡牌是否显示描述，若包含，则支持指定设置中配置其描述 |


#### **b.未知卡牌设置**

![](../images/卡牌选择器界面控件_mh2teu0bmfbc_b未知卡牌设置.png)


|  |  |  |
| --- | --- | --- |
| 配置参数 | 说明 | |
| <span style="color: blue; font-style: italic;">选择后展示结果</span> | 在决策完成后，是否将选定决策项播放动效，切换显示其实际返回值 | |
| <span style="color: blue; font-style: italic;">结果页关闭方式</span> | 倒计时关闭 | 需要额外配置**倒计时时长(s)** |
| 手动关闭 | 需要主动关闭弹窗作为结束 |
| <span style="color: blue; font-style: italic;">倒计时时长(s)</span> | 决策完成后，经过配置时间以后，卡牌选择器会主动关闭 | |


#### **c.卡牌库设置**

![](../images/卡牌选择器界面控件_mh2teu0bmfbc_c卡牌库设置.png)

通过详情编辑，配置卡牌显示

![](../images/卡牌选择器界面控件_mh2teu0bmfbc_c卡牌库设置_2.png)


|  |  |  |
| --- | --- | --- |
| 配置参数 | 说明 | |
| <span style="color: blue; font-style: italic;">卡牌序号</span> | 用于在节点图唤起卡牌选择器时，作为卡牌显示调用  从1开始按顺序递增，不可修改 | |
| <span style="color: blue; font-style: italic;">卡牌类型</span> | 已知卡牌 | 提供明确可配置图标 |
| 未知卡牌 | 仅提供问号图标，推荐搭配**选择后展示结果**及**倒计时关闭**一同使用 |
| <span style="color: blue; font-style: italic;">卡牌图标</span> | 综合设置中开启图标配置，才会有该配置 | |
| <span style="color: blue; font-style: italic;">卡牌标题</span> | 文本配置 | |
| <span style="color: blue; font-style: italic;">卡牌描述</span> | 文本配置 | |
| <span style="color: blue; font-style: italic;">标签颜色</span> | 文本颜色 | |
| <span style="color: blue; font-style: italic;">标签描述</span> | 仅创作者(奇匠)自己可见的记录性质文本 | |


# **三、通过节点图管理卡牌选择器**

* **唤起卡牌选择器**

![](../images/卡牌选择器界面控件_mh2teu0bmfbc_三通过节点图管理卡牌选择器.png)

* **关闭卡牌选择器**

![](../images/卡牌选择器界面控件_mh2teu0bmfbc_三通过节点图管理卡牌选择器_2.png)

* **卡牌选择器完成时**

![](../images/卡牌选择器界面控件_mh2teu0bmfbc_三通过节点图管理卡牌选择器_3.png)

* **随机卡牌选择器选择列表**

![](../images/卡牌选择器界面控件_mh2teu0bmfbc_三通过节点图管理卡牌选择器_4.png)
