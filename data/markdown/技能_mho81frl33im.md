# 技能

**URL**: https://act.mihoyo.com/ys/ugc/tutorial/detail/mho81frl33im

**爬取时间**: 2026-01-04 08:27:04

---

## 技能


# 一、技能的定义

*技能*是一种通过接收游玩时的用户输入，让角色执行某一段预设行为的封装。在经典模式中，角色的普通攻击，元素战技，元素爆发等都是一个技能。

技能主要实现三个基本功能：

* *<span style="color: red; font-style: italic;">角色动画</span>的调用：在技能编辑时，创作者(奇匠)可以定义技能释放后的角色动画演出效果*
* *触发**客户端节点图**：通过编辑技能动画<span style="color: red; font-style: italic;">节点图事件轨道</span>上的事件，可以在动画的特定阶段触发指定的客户端节点图*
* *配置<span style="color: red; font-style: italic;">技能状态</span>：在动画播放的过程中，可以指定特定的时间窗口附加持续性的逻辑，比如播放循环动画等等*

# 二、技能的编辑

## 1.编辑入口

技能编辑的入口位于战斗预设页签的技能页签下

![](../images/技能_mho81frl33im_1编辑入口.png)

点击【新建技能】

![](../images/技能_mho81frl33im_1编辑入口_3.png)

并在弹出的窗口中选择【确认创建】即可完成新技能的添加

## 2.技能参数

一个技能的参数配置如下图：

![](../images/技能_mho81frl33im_2技能参数.png)

<span style="color: blue; font-style: italic;">配置ID</span>：技能的唯一标识，在节点图修改对应的技能配置时，引用该ID

<span style="color: blue; font-style: italic;">技能类型</span>：目前分为五种

<span style="color: blue; font-style: italic;">瞬发技能</span>：无法编辑动画，在接受输入的瞬间立即触发逻辑

<span style="color: blue; font-style: italic;">长按技能</span>：可以提供循环动画类型的技能，玩家长按对应的输入即可进入循环动画

<span style="color: blue; font-style: italic;">普通技能</span>：基础的技能类型

<span style="color: blue; font-style: italic;">连段技能</span>：可以配置一连串的连续动作，并在接受特定时点的输入后，在动作之间进行跳转

<span style="color: blue; font-style: italic;">瞄准技能</span>：提供成套的瞄准动作，并在施放技能时使角色进入瞄准状态

### (1)基础设置

![](../images/技能_mho81frl33im_1基础设置.png)

<span style="color: blue; font-style: italic;">启用运动坠崖保护</span>：勾选时，角色释放该技能产生位移时不会触发坠崖

<span style="color: blue; font-style: italic;">是否可以在空中释放</span>：在角色处于跳跃，下落，滑翔等空中状态时能否使用该技能

<span style="color: blue; font-style: italic;">技能备注</span>：可以在编辑时描述该技能的大致作用

### (2)数值配置

![](../images/技能_mho81frl33im_2数值配置.png)

<span style="color: blue; font-style: italic;">是否有冷却时间</span>：开启时可以配置技能冷却时间

<span style="color: blue; font-style: italic;">冷却时间(s)</span>：当该技能释放后需要多久才能够再次释放

<span style="color: blue; font-style: italic;">是否有次数限制</span>：开启时可以配置技能使用次数

<span style="color: blue; font-style: italic;">使用次数</span>：技能添加时的默认可使用次数，当使用次数归0时，技能无法使用，每经过一个冷却时间，可以恢复一次使用次数，最大恢复到默认配置的次数，就不会再增加

<span style="color: blue; font-style: italic;">是否有消耗</span>：开启时可以配置消耗类型和消耗量

<span style="color: blue; font-style: italic;">消耗类型</span>：释放该技能需要消耗的*技能资源*类型，具体查看技能资源

<span style="color: blue; font-style: italic;">消耗量</span>：释放该技能需要消耗的技能资源值

<span style="color: blue; font-style: italic;">索敌范围</span>：该技能释放时，会在多大的范围内寻找释放目标，并且在本地节点图内，可以通过查询节点获取到本次技能释放的目标单位，索敌范围目前提供了两种类型

<span style="color: blue; font-style: italic;">圆柱体</span>：使用<span style="color: blue; font-style: italic;">半径</span>和<span style="color: blue; font-style: italic;">高度</span>进行描述

![](../images/技能_mho81frl33im_2数值配置_2.png)

<span style="color: blue; font-style: italic;">扇形</span>：可以视为是圆柱的升级版本，除了<span style="color: blue; font-style: italic;">半径</span>和<span style="color: blue; font-style: italic;">高度</span>外，还可以配置筛选的<span style="color: blue; font-style: italic;">角度</span>，以及<span style="color: blue; font-style: italic;">旋转</span>

![](../images/技能_mho81frl33im_2数值配置_3.png)

### (3)生命周期管理

![](../images/技能_mho81frl33im_3生命周期管理.png)

<span style="color: blue; font-style: italic;">达到次数上限是否销毁技能</span>：开启时可以配置次数上限

<span style="color: blue; font-style: italic;">次数上限</span>：该技能在整个生命周期内可以使用的次数，当技能被使用达到最大次数时，技能会被自动移除

### (4)连段配置

对于连段技能类型的专有配置：

![](../images/技能_mho81frl33im_4连段配置.png)

<span style="color: blue; font-style: italic;">是否开启蓄力分支</span>：开启后可在动画编辑处定义连段转入蓄力动作相关逻辑

<span style="color: blue; font-style: italic;">蓄力公共前摇</span>：开启后，连段动画与蓄力动画将共用同一个前摇动画槽位，以及槽位内的所有配置。关闭后，运行时该槽位的动画将不会播放

### (5)瞄准配置

对于瞄准技能类型的专有配置：

![](../images/技能_mho81frl33im_5瞄准配置.png)

<span style="color: blue; font-style: italic;">瞄准进入方式</span>：分为长按和点按切换两种

<span style="color: blue; font-style: italic;">长按</span>：长按技能进入瞄准状态，松开后退出

<span style="color: blue; font-style: italic;">点按切换</span>：点按技能进入瞄准状态，再次点击退出

<span style="color: blue; font-style: italic;">瞄准中是否可移动</span>：在瞄准模式下角色是否可以进行位移

<span style="color: blue; font-style: italic;">瞄准发射动画时长</span>：切换为自定义后，可修改瞄准技能的发射动画播放时长(该功能在游戏运行时生效，预览时不生效)

# 三、技能的动画编辑

![](../images/技能_mho81frl33im_三技能的动画编辑.png)

在定义完了技能的释放条件和释放逻辑后，即可点击动画编辑，来继续编辑技能释放后的具体逻辑，不同的技能类型，配置方式也会有所区别：

## 1.普通技能

普通技能是最通用的技能类型，配置方式也最为常规，因此先以普通技能为例介绍动画编辑的大致配置方法

![](../images/技能_mho81frl33im_1普通技能.png)

界面如上图，以时间轴的形式来进行配置，分为动作轴和逻辑轴。在技能释放时，从前往后按时间依次触发动作轴上的动画，以及逻辑轴上的事件，依次来实现整个技能的具体效果。

### (1)添加动作

首先我们需要添加对应的<span style="color: red; font-style: italic;">动作</span>，入口在上图“A”所示位置，点击可选择目前可用的<span style="color: red; font-style: italic;">角色动画</span>

![](../images/技能_mho81frl33im_1添加动作.png)

动画是整个*技能轨道*的尺度，事件轴的总长度等于所有动画的时长之和，在对应的动画时点添加事件，即可让表现和逻辑匹配

### (2)编辑事件轨道

事件轨道在上图"B"所示位置

*事件轨道*分为四种类型：

<span style="color: blue; font-style: italic;">开始事件轨道</span>：在技能开始释放时立即触发的时点

<span style="color: blue; font-style: italic;">结束事件轨道</span>：在技能的动作全部播放完成后触发的时点

<span style="color: blue; font-style: italic;">节点图事件轨道</span>：可以根据动作进度进行打点并添加事件的轨道，在该轨道下可选择具体的动画进度位置，并添加一个*技能节点图*，如下图。当动画进行到配置的进度处时，技能节点图会被触发

![](../images/技能_mho81frl33im_2编辑事件轨道.png)

<span style="color: blue; font-style: italic;">状态轨道</span>：用于定义非触发类型的表现，如持续播放特效等，如下图，并且可以自由配置该状态的开始时点和结束时点

![](../images/技能_mho81frl33im_2编辑事件轨道_2.png)

## 2.瞬发技能

![](../images/技能_mho81frl33im_2瞬发技能.png)

界面如上图，由于瞬发技能的所有逻辑都在技能释放瞬间触发，也不会调用动画。因此瞬发技能不可添加动作，且只保留开始事件轨道

## 3.长按技能

<span style="color: red; font-style: italic;">长按技能</span>支持创作者(奇匠)在动画时间轴上引用循环动画

![](../images/技能_mho81frl33im_3长按技能.png)

选择完循环动画栏位的动画后，可调整循环动画的<span style="color: red; font-style: italic;">持续时长</span>，在实际释放技能时：

如果角色进入该动画后输入保持长按状态，则该循环动画会持续播放，最多播放到持续时长

如果角色进入该动画后未保持输入长按，则动画会立即中断，并根据<span style="color: red; font-style: italic;">分支轨道</span>配置跳转到对应的分支

![](../images/技能_mho81frl33im_3长按技能_2.png)

### (1)分支

点击下图中的按钮可添加或删除分支，每个分支代表了多个捆绑好的动画，在实际的技能释放过程中，根据技能长按的松开时机，会转入到某一个分支中

![](../images/技能_mho81frl33im_1分支.png)

每一个分支可配置三段非循环动画，在进入对应的分支后，会顺序进行播放

![](../images/技能_mho81frl33im_1分支_2.png)

### (2)分支轨道

分支轨道定义了如何跳转至各个分支的具体规则，点击分支轨道，会在界面右侧弹出分支事件编辑界面

![](../images/技能_mho81frl33im_2分支轨道.png)

<span style="color: blue; font-style: italic;">可跳转分支数</span>：该技能支持几种分支跳转情境，该配置会使分支轨道被划分为对应数量的段落

<span style="color: blue; font-style: italic;">响应</span>：支持由创作者(奇匠)配置分支轨道的每一个段落跳转到哪一个具体分支上

在分支轨道上，创作者(奇匠)可以通过调节每个段落的长度，来精细化调节分支转入的条件。在实际的运行时，当玩家停止长按时，当前的动画进度落在哪一个响应段落内，则动画会自动转入该段落所对应配置的分支

## 4.连段技能

<span style="color: red; font-style: italic;">连段技能</span>支持创作者(奇匠)配置多个独立的动作，并通过定义动作间的跳转规则和输入窗口期，来实现“连招”的效果。与此同时连段技能也提供了转入蓄力分支的功能，在配置上有两个页签：连段技能动画页签及蓄力分支动画页签

* **连段技能动画编辑页签**

![](../images/技能_mho81frl33im_4连段技能.png)

* **蓄力分支动画编辑页签**

![](../images/技能_mho81frl33im_4连段技能_2.png)

连段技能的配置界面如上图，与普通技能的编辑不同的是，连段技能中配置的技能槽位在技能释放时并不会顺序播放，而是依赖连段轨道上的配置和创作者(奇匠)实际的输入进行跳转

### (1)连段轨道

连段轨道是连段技能的专有轨道。在连段轨道上，创作者(奇匠)可以配置连段响应事件，一个连段响应事件由一个预输入阶段与多个响应阶段构成：

![](../images/技能_mho81frl33im_1连段轨道.png)

<span style="color: blue; font-style: italic;">预输入阶段</span>：在预输入阶段点按技能，会接受该次预输入，并在进入第一个响应阶段时直接触发响应进行相应的动画跳转。在预输入阶段长按技能，若满足<span style="color: red; font-style: italic;">蓄力成功时长</span>则会立即跳转到蓄力分支动画

<span style="color: blue; font-style: italic;">响应阶段</span>：在响应阶段点按技能，会立即触发响应并进行相应的动画跳转

一个连段响应事件的具体编辑界面如下图：

![](../images/技能_mho81frl33im_1连段轨道_2.png)

<span style="color: blue; font-style: italic;">跳转设置</span>：连段动画之间的跳转规则配置

<span style="color: blue; font-style: italic;">可响应段数</span>：定义了该动作存在几个响应阶段

<span style="color: blue; font-style: italic;">响应跳转动画</span>：每一个响应阶段接受输入时转到的目标动画槽位

<span style="color: blue; font-style: italic;">蓄力设置</span>：在预输入阶段跳转进蓄力分支的相关逻辑配置

<span style="color: blue; font-style: italic;">当前预输入是否可跳转蓄力分支</span>：跳转到蓄力分支的开关

<span style="color: blue; font-style: italic;">蓄力成功时长</span>：在预输入阶段长按蓄力达到该配置值时，会立即转入蓄力分支

### (2)公共前摇

公共前摇是一个特殊的动画槽位：

1.角色从待机动画短按技能初次进入连段技能动画时，会优先播放公共前摇配置的动作

2.角色从待机动画长按技能直接进入蓄力分支动画时，也会优先播放公共前摇配置的动作

## 5.瞄准技能

<span style="color: red; font-style: italic;">瞄准技能</span>对应了弓箭角色的蓄力瞄准动作，其特点在于：

* 瞄准技能提供了三个动画槽位，但不支持分别配置，而是采用成套动作的方式进行配置，当创作者(奇匠)选中一套动作时，会同时填充全部三个动画槽位

![](../images/技能_mho81frl33im_5瞄准技能.png)

* 瞄准技能也提供了分支以及分支轨道，但每个分支只提供了一个动画槽位
* 不同于长按技能当循环动画时长达到循环时间时会退出动画并转入对应分支，瞄准技能的蓄力动作在到达持续时长后会保持在动作的最后时刻，即轨道的结尾处。直到玩家主动解除瞄准后，再转入对应分支

![](../images/技能_mho81frl33im_5瞄准技能_2.png)

除以上特性外，瞄准技能的事件轨道和分支轨道配置和其他技能相同。在状态轨道上存在两种需要配合使用的状态事件：进入瞄准状态及开启准星：

### (1)进入瞄准状态

![](../images/技能_mho81frl33im_1进入瞄准状态.png)

<span style="color: blue; font-style: italic;">镜头视野</span>：进入瞄准状态后的视野范围

<span style="color: blue; font-style: italic;">瞄准视角偏移</span>：进入瞄准状态后，镜头位置的偏移值

<span style="color: blue; font-style: italic;">俯仰角度范围</span>：进入瞄准状态后，玩家可调整的镜头俯仰角范围

<span style="color: blue; font-style: italic;">进入过渡时长(秒)</span>：从原始镜头切换至瞄准镜头的过渡时长

<span style="color: blue; font-style: italic;">退出过渡时长(秒)</span>：从瞄准镜头切换至原始镜头的过渡时长

对比是否应用该事件的瞄准技能表现：

* 使用瞄准状态：

![](../images/技能_mho81frl33im_1进入瞄准状态_2.png)

* 不使用瞄准状态：

![](../images/技能_mho81frl33im_1进入瞄准状态_3.png)

### (2)开启准星

![](../images/技能_mho81frl33im_2开启准星.png)

无可配置参数，开启后的效果：

![](../images/技能_mho81frl33im_2开启准星_2.png)

# 四、技能槽位

*技能槽位*决定了技能会被显示在UI的哪个位置，以及释放该技能对应的输入。目前开放了五个技能槽位

* *<span style="color: blue; font-style: italic;">普通攻击</span>：对应PC端鼠标左键*
* *<span style="color: blue; font-style: italic;">技能1</span>：对应PC端键盘E键*
* *<span style="color: blue; font-style: italic;">技能2</span>：对应PC端键盘Q键*
* *<span style="color: blue; font-style: italic;">技能3</span>：对应PC端键盘R键*
* *<span style="color: blue; font-style: italic;">技能4</span>：对应PC端键盘T键*

# 五、技能的添加

技能的添加主要有两种途径，一是职业的默认配置，在[职业](职业_mhodlcrpht3q.md)文档内有详细的使用说明

第二种是通过节点图进行添加

## 1.通过节点图修改技能

![](../images/技能_mho81frl33im_1通过节点图修改技能.png)

![](../images/技能_mho81frl33im_1通过节点图修改技能_2.png)

![](../images/技能_mho81frl33im_1通过节点图修改技能_3.png)

## 2.查询角色技能

![](../images/技能_mho81frl33im_2查询角色技能.png)
