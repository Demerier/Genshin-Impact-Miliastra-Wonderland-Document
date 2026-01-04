# 基础运动器

**URL**: https://act.mihoyo.com/ys/ugc/tutorial/detail/mhnmcmipncrg

**爬取时间**: 2026-01-04 08:11:34

---

## 基础运动器


# 一、基础运动器组件的功能

<span style="color: blue; font-style: italic;">基础运动器组件</span>赋予*物件实体*按规则运动的功能。

基础运动器组件在联机游玩时，会优先保证各端的体验一致。

基础运动器组件可支持同时生效多个基础运动器，他们的运动会进行叠加，也有一些基础运动器是互斥的。

# 二、基础运动器组件的编辑

![](../images/基础运动器_mhnmcmipncrg_二基础运动器组件的编辑.png)

(1)在实体/元件编辑界面中，打开组件编辑页签

(2)点击下方的“添加通用组件”，选择并点击“基础运动器”，成功添加

(3)点击“详细编辑”，展开编辑页

# 三、基础运动器的类型

## 1.匀速直线运动器

<span style="color: blue; font-style: italic;">匀速直线运动器</span>是描述朝某个固定方向匀速直线运动的运动器，描述朝向基于世界坐标系。

匀速直线运动器参数如下图所示：

![](../images/基础运动器_mhnmcmipncrg_1匀速直线运动器.png)

<span style="color: blue; font-style: italic;">初始生效</span>：开启则表示实体创建时立即生效

<span style="color: blue; font-style: italic;">生效时长</span>：运动器在生效时长结束后会自动停止

<span style="color: blue; font-style: italic;">速度向量</span>：描述实体在三个轴向上的速度分量

<span style="color: blue; font-style: italic;">速度</span>：转换成朝向三维向量后的初始速度

<span style="color: blue; font-style: italic;">相对位置</span>：运行时无意义，在编辑时会预测该运动器单独生效时，经过生效时长后实体所在的位置

## 2.匀速旋转运动器

描述绕某个旋转轴匀速旋转的运动器，旋转轴基于世界坐标系。

<span style="color: blue; font-style: italic;">匀速旋转运动器</span>参数如下图所示：

![](../images/基础运动器_mhnmcmipncrg_2匀速旋转运动器.png)

<span style="color: blue; font-style: italic;">初始生效</span>：开启则表示实体创建时立即生效

<span style="color: blue; font-style: italic;">生效时长</span>：运动器在生效时长结束后会自动停止

<span style="color: blue; font-style: italic;">相对旋转轴朝向</span>：定义旋转轴

<span style="color: blue; font-style: italic;">角速度</span>：单位为角度每秒

## 3.朝向目标旋转运动器

描述让物体在指定时间内转向到指定角度的旋转运动器。

<span style="color: blue; font-style: italic;">朝向目标旋转运动器</span>参数如下图所示：

![](../images/基础运动器_mhnmcmipncrg_3朝向目标旋转运动器.png)

<span style="color: blue; font-style: italic;">初始生效</span>：开启则表示实体创建时立即生效

<span style="color: blue; font-style: italic;">生效时长</span>：运动器在生效时长结束后会自动停止

<span style="color: blue; font-style: italic;">绝对目标角度</span>：运动器单独生效时，生效时长结束后，实体的预期朝向

## 4.路径运动器

描述让物体沿指定路径运动的运动器，路径通过有序的多个路径点连接组成。

![](../images/基础运动器_mhnmcmipncrg_4路径运动器.png)

<span style="color: blue; font-style: italic;">初始生效</span>：开启则表示实体创建时立即生效

<span style="color: blue; font-style: italic;">循环类型</span>：提供了三种循环类型

* *<span style="color: blue; font-style: italic;">单程</span>：到达路径终点后停止运动，关闭运动器*
* *<span style="color: blue; font-style: italic;">往返</span>：每当到达路径终点后反向运动回起点*
* *<span style="color: blue; font-style: italic;">循环</span>：每当到达路径终点后瞬移到路径起点并重新开始路径*

<span style="color: blue; font-style: italic;">路点列表</span>：

<span style="color: blue; font-style: italic;">到达时长</span>：从上一个点到当前点所需要的时长

<span style="color: blue; font-style: italic;">运动路线</span>：表示从上一个点到当前的轨迹

<span style="color: blue; font-style: italic;">相对位置</span>：路径点相对于实体的位置

<span style="color: blue; font-style: italic;">绝对旋转</span>：路径点对世界坐标的旋转

<span style="color: blue; font-style: italic;">到达通知节点图</span>：勾选时，对象到达对应路点会向自身挂载的节点图发出“路径到达路点”事件

## 5.定点运动器

描述让物体运动到指定位置与旋转的运动器

![](../images/基础运动器_mhnmcmipncrg_5定点运动器.png)

<span style="color: blue; font-style: italic;">初始生效</span>：实体创建时立即生效

<span style="color: blue; font-style: italic;">运动方式</span>：提供了以下两种运动方式

<span style="color: blue; font-style: italic;">匀速直线</span>：以恒定的速率和转向角速率移动到目标位置和目标旋转

<span style="color: blue; font-style: italic;">立即抵达</span>：无视其他的运动描述配置，立即将物件的坐标和旋转设置到目标位置和目标旋转

<span style="color: blue; font-style: italic;">抵达方式</span>：选择使用何种方式来描述移动速率

<span style="color: blue; font-style: italic;">固定速率</span>：直接配置指定速率

<span style="color: blue; font-style: italic;">运动速率（m/s）</span>：直接填写速率值

<span style="color: blue; font-style: italic;">固定时间</span>：通过填写抵达所需时间来换算速率

<span style="color: blue; font-style: italic;">运动时长（s）</span>：填写抵达所需时间

<span style="color: blue; font-style: italic;">目标位置</span>：运动器的目标位置

<span style="color: blue; font-style: italic;">目标旋转</span>：运动器的目标旋转

<span style="color: blue; font-style: italic;">跟随旋转</span>：配置为否则运动时该运动器不会将旋转变化作用于物件

## 6.关卡路径运动器

描述让物体沿指定路径运动的运动器，路径通过有序的多个路径点连接组成，区别于路径运动器，关卡路径运动器引用一条路径管理工具内的关卡路径，在开始运动时，物件会先以配置的方式前往路径的第一个点，之后再沿路径运动

![](../images/基础运动器_mhnmcmipncrg_6关卡路径运动器.png)

关卡路径运动器的大部分配置与路径运动器一致，以下着重说明存在差异的配置

<span style="color: blue; font-style: italic;">关卡路径</span>：引用的路径，在选择一个路径后，会根据路径管理中的路点配置自动生成路点信息

<span style="color: blue; font-style: italic;">至路点1</span>：区别于路径运动器，关卡路径运动器需要描述如何前往第一个路点

<span style="color: blue; font-style: italic;">运动方式</span>：提供了以下两种运动方式

<span style="color: blue; font-style: italic;">匀速直线</span>：以恒定的速率和转向角速率移动到目标位置和目标旋转

<span style="color: blue; font-style: italic;">立即抵达</span>：无视其他的运动描述配置，立即将物件的坐标和旋转设置到目标位置和目标旋转

<span style="color: blue; font-style: italic;">抵达方式</span>：选择使用何种方式来描述移动速率

<span style="color: blue; font-style: italic;">固定速率</span>：直接配置指定速率

<span style="color: blue; font-style: italic;">运动速率（m/s）</span>：直接填写速率值

<span style="color: blue; font-style: italic;">固定时间</span>：通过填写抵达所需时间来换算速率

<span style="color: blue; font-style: italic;">运动时长（s）</span>：填写抵达所需时间

<span style="color: blue; font-style: italic;">到达通知节点图</span>：勾选时，对象到达对应路点会向自身挂载的节点图发出“路径到达路点”事件

<span style="color: blue; font-style: italic;">显示路点信息</span>：开启后，会显示路点的详细数据，但在运动器内无法更改

# 四、基础运动器的状态

基础运动器存在以下三种状态：

* *<span style="color: blue; font-style: italic;">未激活</span>**：**默认配置在组件上的基础运动器，初始未生效时的状态。*
* *<span style="color: blue; font-style: italic;">运作中</span>**：**基础运动器正常生效时的状态。*
* *<span style="color: blue; font-style: italic;">暂停中</span>**：**基础运动器被暂停时的状态，区别于停止，暂停中的运动器会记录当前的运动进度，并在恢复后继续运动。*

# 五、基础运动器的叠加规则

## 1.同类型叠加

相同类型的基础运动器中，位移运动器可以同时生效多个，且朝向可叠加。

其他类型的基础运动器，均只允许同时生效一个。

## 2.不同类型叠加

不同类型的运动器之间，可以互相叠加。

特殊的，旋转运动器、朝向运动器和定点运动器之间不可叠加，

路径运动器和关卡路径运动器不可叠加

更加详细的叠加规则可以参照以下二维表格

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
|  | 匀速直线 | 匀速旋转 | 朝向目标旋转 | 路径运动 | 定点运动 | 关卡路径运动 |
| 匀速直线 | 可叠加 | 可叠加 | 可叠加 | 可叠加 | 可叠加 | 可叠加 |
| 匀速旋转 | 可叠加 | 不可叠加 | 不可叠加 | 不可叠加 | 可叠加 | 不可叠加 |
| 朝向目标旋转 | 可叠加 | 不可叠加 | 不可叠加 | 不可叠加 | 可叠加 | 不可叠加 |
| 路径运动 | 可叠加 | 不可叠加 | 不可叠加 | 不可叠加 | 可叠加 | 不可叠加 |
| 定点运动 | 可叠加 | 可叠加 | 可叠加 | 可叠加 | 不可叠加 | 不可叠加 |
| 关卡路径运动 | 可叠加 | 不可叠加 | 不可叠加 | 不可叠加 | 不可叠加 | 不可叠加 |

# 

# 六、基础运动器的冲突规则

基础运动器以<span style="color: blue; font-style: italic;">名称</span>字段作为唯一引用方式，在一个基础运动器组件所维护的所有基础运动器中，运动器名称不可以是重复的，当发生以下情境时，会触发基础运动器的冲突。

* 开启了同名的运动器
* 开启的运动器类型不满足叠加规则

判断基础运动器的冲突时，只会考虑处于运作中或暂停中状态的运动器，而不会考虑未激活的运动器。

当一个新生效的运动器与一个已存在的运动发生冲突时，会先停止（而非暂停）已存在的运动器，之后正常激活新的运动器。

# 七、使用节点图控制基础运动器

* 激活基础运动器

![](../images/基础运动器_mhnmcmipncrg_七使用节点图控制基础运动器.png)

* 创建运动器

根据不同的运动器类型，有不同的节点

![](../images/基础运动器_mhnmcmipncrg_七使用节点图控制基础运动器_2.png)![](../images/基础运动器_mhnmcmipncrg_七使用节点图控制基础运动器_3.png)![](../images/基础运动器_mhnmcmipncrg_七使用节点图控制基础运动器_4.png)

* 停止并删除基础运动器

![](../images/基础运动器_mhnmcmipncrg_七使用节点图控制基础运动器_5.png)

* 暂停基础运动器

![](../images/基础运动器_mhnmcmipncrg_七使用节点图控制基础运动器_6.png)

* 恢复基础运动器

![](../images/基础运动器_mhnmcmipncrg_七使用节点图控制基础运动器_7.png)

* 事件节点

![](../images/基础运动器_mhnmcmipncrg_七使用节点图控制基础运动器_8.png)

![](../images/基础运动器_mhnmcmipncrg_七使用节点图控制基础运动器_9.png)
