# 选项卡

**URL**: https://act.mihoyo.com/ys/ugc/tutorial/detail/mh5jko05fzyw

**爬取时间**: 2026-01-04 08:11:16

---

## 选项卡


# 一、选项卡组件的功能

选项卡组件赋予玩家对动态物件和造物配置交互操作的功能

实体添加此组件后，支持同时配置、生效多个选项卡

每个选项卡支持通过本地过滤器判定对每个玩家是否显示

触发选项卡功能的实体类型为<span style="color: red; font-style: italic;">角色</span>

# 二、选项卡组件的编辑

## 1.添加组件

![](../images/选项卡_mh5jko05fzyw_1添加组件.png)

(1)在实体或元件编辑界面中，打开组件编辑页签(A)

(2)点击下方的“添加通用组件”，选择并点击“选项卡”，成功添加(B)、(C)

选中“选项卡”时，编辑中的实体会以蓝色范围显示选项卡触发区

(3)点击“详细编辑”，展开编辑页(D)

## 2.选项卡的编辑

![](../images/选项卡_mh5jko05fzyw_2选项卡的编辑.png)

### (1)选项卡基础信息


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">初始生效选项卡</span> | 下拉菜单提供选项卡枚举  通过修改后面的勾选框，可以修改生效情况，修改后生效状态会同步到选项卡编辑页内 |
| <span style="color: blue; font-style: italic;">\选项卡列表</span> | 枚举实体配置的所有选项卡 |

*可以通过点击来切换选项卡在编辑窗口的可见性状态，仅编辑时生效

![](../images/选项卡_mh5jko05fzyw_1选项卡基础信息_4.png)

点击“详细编辑”可进入选项卡列表和触发区域配置界面

### (2)选项卡列表

![](../images/选项卡_mh5jko05fzyw_2选项卡列表.png)

* 新增选项卡

![](../images/选项卡_mh5jko05fzyw_2选项卡列表_2.png)

点击添加选项卡，可新增选项卡

* 选项卡编辑

![](../images/选项卡_mh5jko05fzyw_2选项卡列表_3.png)

<span style="color: blue; font-style: italic;">选项序号	</span> *序号**X*，可用于节点图入参，调整选项卡的生效与否

<span style="color: blue; font-style: italic;">选项卡图标</span>	点击，可切换选项卡前面的图标。

![](../images/选项卡_mh5jko05fzyw_2选项卡列表_5.png)

<span style="color: blue; font-style: italic;">初始生效</span> 若开启，则该选项卡随实体创建立即生效。生效的选项卡可见，并可操作选中

<span style="color: blue; font-style: italic;">排序等级	</span>		控制选项卡的显示顺序，数字越大，显示越靠前

![](../images/选项卡_mh5jko05fzyw_2选项卡列表_6.png)

<span style="color: blue; font-style: italic;">本地过滤器</span>		分为布尔过滤器和整数过滤器两种。具体可见节点图

<span style="color: blue; font-style: italic;">过滤器节点图	</span>	可引用上述选择类型的过滤器节点图，用于判断选项卡是否达成显示条件

以下用布尔过滤器举例

![](../images/选项卡_mh5jko05fzyw_2选项卡列表_7.png)

![](../images/选项卡_mh5jko05fzyw_2选项卡列表_8.png)![](../images/选项卡_mh5jko05fzyw_2选项卡列表_9.png)

本地过滤器会在角色进入生效范围期间内，持续进行检测，若结果变化，立即更新显示。

对应本地过滤器节点图中的基础节点，进行说明

* 获取自身实体

输出参数为挂载选项卡组件的实体

* 获取目标实体

当自身角色在范围里，该节点输出参数为在选项卡生效范围内的自身角色实体

* 获取当前角色

输出参数为本地角色

* 举例说明

![](../images/选项卡_mh5jko05fzyw_2选项卡列表_10.png)

### (3)触发选项区域

![](../images/选项卡_mh5jko05fzyw_3触发选项区域.png)

* 添加触发区域

![](../images/选项卡_mh5jko05fzyw_3触发选项区域_2.png)

点击添加触发选项区域按键，可新增触发区域

* 触发区域

![](../images/选项卡_mh5jko05fzyw_3触发选项区域_3.png)


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">触发区形状 </span> | 支持长方体、球体、胶囊体，根据选择的不同形状会展开具体的大小配置参数 |
| <span style="color: blue; font-style: italic;">中心</span> | 相对实体/元件中心的偏移 |
| <span style="color: blue; font-style: italic;">旋转</span> | 以中心位置为基准，在不同轴向上支持调整朝向 |
| <span style="color: blue; font-style: italic;">缩放倍率</span> | 触发区配置形状在不同轴向上支持定义缩放 |


# 三、通过节点图管理选项卡

* 激活/关闭选项卡

通过输入选项卡序号，可控制选项卡的激活与否

![](../images/选项卡_mh5jko05fzyw_三通过节点图管理选项卡.png)

* 选项卡选中时

生效的选项卡被选中后，会向节点图发送事件

配置选项卡组件的实体节点图，会接受该事件

![](../images/选项卡_mh5jko05fzyw_三通过节点图管理选项卡_2.png)


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">事件源实体</span> | 挂载选项卡组件的实体 |
| <span style="color: blue; font-style: italic;">事件源GUID</span> | 挂载选项卡组件的实体，若无则输出0 |
| <span style="color: blue; font-style: italic;">选项卡序号</span> | 选项卡的序号 |
| <span style="color: blue; font-style: italic;">选择者实体</span> | 触发选项卡时的角色实体 |

**