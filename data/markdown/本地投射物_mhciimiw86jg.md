# 本地投射物

**URL**: https://act.mihoyo.com/ys/ugc/tutorial/detail/mhciimiw86jg

**爬取时间**: 2026-01-04 08:06:25

---

## 本地投射物


# 一、本地投射物的定义

本地投射物是由本地计算和呈现投射物效果以及命中表现效果的实体

# 二、本地投射物的特点

本地投射物需要在编辑时预先定义，才能被技能节点图引用创建。技能相关可参考[技能](技能_mho81frl33im.md)

本地投射物实体运行时，依赖*投射运动器*决定其运行时的规则，依赖*命中检测*决定其碰撞触发的判定规则和效果。

本地投射物实体运行时，遵循“生命周期”的配置

# **三、本地投射物的编**辑

## 1.新建本地投射物

进入战斗预设页签后，可以选择本地投射物页签，按需管理页签，并在页签内新建对应的本地投射物

![](../images/本地投射物_mhciimiw86jg_1新建本地投射物.png)

点击<span style="color: blue; font-style: italic;">确认创建</span>即可新建一个本地投射物

![](../images/本地投射物_mhciimiw86jg_1新建本地投射物_2.png)

## 2.命名与索引

![](../images/本地投射物_mhciimiw86jg_2命名与索引.png)

每个预定义的本地投射物<span style="color: blue; font-style: italic;">命名</span>需要全局唯一，并且会自动生成全局唯一的<span style="color: blue; font-style: italic;">元件</span><span style="color: blue; font-style: italic;">ID</span>。

## **3.基础属**性

第一栏为基础属性栏

![](../images/本地投射物_mhciimiw86jg_3基础属性.png)

### (1)基础设置

本地投射物运行时采用的模型配置，可选模型皆来自于预先提供的投射物模型库。

支持调节xyz轴缩放，切换模型后，缩放数值会保留

![](../images/本地投射物_mhciimiw86jg_1基础设置.png)

### **(2)战斗参数**

![](../images/本地投射物_mhciimiw86jg_2战斗参数.png)

![](../images/本地投射物_mhciimiw86jg_2战斗参数_2.png)


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">属性设置</span> | 提供2个枚举项，*继承自创建者*和*独立设置*，不同选项选择后下方对应的参数不同  默认为继承自创建者  继承自创建者：生命值、攻击力、防御力，和创建者相同  独立设置：按需配置生命值、攻击力、防御力  不同选项选择后下方对应的参数不同 |
| <span style="color: blue; font-style: italic;">后续是否受创建者影响</span> | 若开启，则创建者受到的部分单位状态会同步给投射物  仅有影响生命值、攻击力、防御力的单位状态会同步 |


### **(3)生命周期设**置

![](../images/本地投射物_mhciimiw86jg_3生命周期设置.png)


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">永久持续</span> | 若不开启，需要填写具体的<span style="color: blue; font-style: italic;">持续时长</span> |
| <span style="color: blue; font-style: italic;">持续时长</span> | 无其他影响因素条件下，该本地投射物从开始运行到销毁的最长时间 |
| <span style="color: blue; font-style: italic;">X/Z轴销毁距离</span> | 除*能力单元*外，优先级最高的本地投射物运行时销毁判定条件  本地投射物运行时超过最大销毁距离，会自行销毁 |
| <span style="color: blue; font-style: italic;">Y轴销毁距离</span> |


### **(4)生命周期结束时行为设**置

本地投射物生命周期结束时，会依照配置顺序从上到下执行配置的能力单元。

此处引用的能力单元来自于该本地投射物能力单元内的编辑。

![](../images/本地投射物_mhciimiw86jg_4生命周期结束时行为设置.png)

## **4.通用组件**

第二栏为通用组件栏

![](../images/本地投射物_mhciimiw86jg_4通用组件.png)

![](../images/本地投射物_mhciimiw86jg_4通用组件_2.png)

### **(1)特效播放**组件

详情可见[特效播放](特效播放_mh4ppo02m1o8.md)

### **(2)投射运动**器组件

详情可见[投射运动器](投射运动器_mhaqt9rgqv4u.md)

### **(3)命中检**测组件

详情可见[命中检测](命中检测_mh2pir0hat1s.md)

## 5.能力单元

第三栏为能力单元栏

![](../images/本地投射物_mhciimiw86jg_5能力单元.png)

本地投射物可引用能力单元，需要进行预定义编辑，详情可见[能力单元](能力单元_mh0ucw9e76f6.md)

![](../images/本地投射物_mhciimiw86jg_5能力单元_2.png)

通过“详细编辑”可以对能力单元进行调整

在<span style="color: red; font-style: italic;">命中检测组件</span>中，可引用预定义的能力单元，在命中检测生效后执行
