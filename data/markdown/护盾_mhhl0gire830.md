# 护盾

**URL**: https://act.mihoyo.com/ys/ugc/tutorial/detail/mhhl0gire830

**爬取时间**: 2026-01-04 08:28:03

---

## 护盾


# 一、护盾的定义

护盾是一种额外的防护层，叠加在单位的基础生命值之上，其主要作用是吸收或抵挡即将到来的伤害

护盾可以添加在物件、角色、造物等实体上

护盾需要预先定义好模板才可以在单位上引用使用

# 二、护盾的编辑

在系统菜单中点击【护盾管理】，打开护盾管理工具。

![](../images/护盾_mhhl0gire830_二护盾的编辑.png)

点击【添加护盾】即可新建一个护盾模板

![](../images/护盾_mhhl0gire830_二护盾的编辑_2.png)

<span style="color: blue; font-style: italic;">护盾名称</span>：可自定义，用于创作者(奇匠)区分不同护盾模板

<span style="color: blue; font-style: italic;">配置ID</span>：该护盾的唯一标识，可用于节点图中使用

<span style="color: blue; font-style: italic;">可吸收元素伤害类型</span>：默认全部，代表所有类型伤害都会吸收。

<span style="color: blue; font-style: italic;">护盾值耗尽时移除</span>：默认开启。关闭时，即使护盾值耗尽，单位状态至少会保留1层

<span style="color: blue; font-style: italic;">显示UI</span>：护盾条会在实体的铭牌组件上显示

<span style="color: blue; font-style: italic;">UI颜色</span>：护盾条的颜色

<span style="color: blue; font-style: italic;">承伤比例</span>：受到伤害时，应用至该护盾上的伤害比例。

<span style="color: blue; font-style: italic;">覆写标签</span>：在使用节点添加单位状态的时候，如果在字典里传入的键和覆写标签一致，则按字典里的值覆写该承伤比例

<span style="color: blue; font-style: italic;">护盾值</span>：每层单位状态提供的护盾值

<span style="color: blue; font-style: italic;">忽略护盾强效</span>：添加护盾值时，是否忽略目标实体的【护盾强效调整率】属性

![](../images/护盾_mhhl0gire830_二护盾的编辑_3.png)

<span style="color: blue; font-style: italic;">无限吸收</span>：开启时将使吸收比例变为无限（即每次吸收伤害时只扣除1点护盾值）

<span style="color: blue; font-style: italic;">吸收比例</span>：每1点护盾值可吸收的伤害值

<span style="color: blue; font-style: italic;">结算优先级</span>：在多个护盾单位状态存在时，吸收伤害的优先级

<span style="color: blue; font-style: italic;">按层生效</span>：拥有多层单位状态时，生效的护盾值只取最早的一层。

<span style="color: blue; font-style: italic;">吸收溢出时伤害</span>：使护盾未阻挡的伤害归零

<span style="color: blue; font-style: italic;">攻击标签</span>：不配置时，代表护盾对所有攻击都生效。配置后，护盾仅对配置的攻击标签生效。

# 三、护盾的使用

护盾需要以单位状态效果方式添加，每个单位状态中只能有一个护盾效果

其中的护盾配置引用上述预先配置好的护盾模板

![](../images/护盾_mhhl0gire830_三护盾的使用.png)

# 四、护盾的结算模式

## 1.单个单位状态下护盾的计算流程

(1)将单位收到的伤害按照参数【承伤比例】分为【护盾承受部分】和【无视护盾部分】。

(2)【护盾承受部分】按照生效的【护盾值】和【吸收比例】决定能吸收多少伤害，若不能全部吸收，将有【溢出伤害】。

(3)上述步骤(1)、(2)中的【无视护盾部分】和【溢出伤害】，将加总作为最终要扣除的生命值（或由另一种护盾继续吸收、或按照配置归零）

## 2.护盾的结算模式

![](../images/护盾_mhhl0gire830_2护盾的结算模式.png)

关卡全局配置，共两种

<span style="color: blue; font-style: italic;">统一计算</span>：多种单位状态下的护盾，会按照结算优先级分别吸收伤害。

<span style="color: blue; font-style: italic;">独立计算</span>：伤害由每个单位状态下的护盾分别计算一次，吸收伤害量最多的一个护盾生效。

# 五、护盾相关节点图

【护盾受到攻击时】以下节点图都会收到该事件：

* 护盾所属单位状态节点图
* 所在实体节点图
* 玩家节点图（当受击者为角色时）

![](../images/护盾_mhhl0gire830_五护盾相关节点图.png)
