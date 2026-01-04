# 音效播放器

**URL**: https://act.mihoyo.com/ys/ugc/tutorial/detail/mhwiv89yra02

**爬取时间**: 2026-01-04 08:15:01

---

## 音效播放器


# 一、音效播放器组件的功能

<span style="color: blue; font-style: italic;">音效播放器组件</span>提供了让单位额外播放音效的功能，组件提供了两种播放方式

1.默认配置在组件上，会在持有该组件的单位创建后自动播放

2.通过节点图进行播放，但必须要求播放音效的单位持有音效播放器组件

# 二、音效播放器组件的编辑

## 1.添加音效播放器组件

![](../images/音效播放器_mhwiv89yra02_1添加音效播放器组件.png)

(1)切换到实体或元件的组件页签

(2)找到或新增一个音效播放器组件

## 2.新增音效播放器

![](../images/音效播放器_mhwiv89yra02_2新增音效播放器.png)

点击【详细编辑】进入详情编辑页

![](../images/音效播放器_mhwiv89yra02_2新增音效播放器_2.png)

在音效播放器组的详情页面，可以点击【添加音效】来新增一个音效配置

## 3.配置音效播放器

![](../images/音效播放器_mhwiv89yra02_3配置音效播放器.png)

<span style="color: blue; font-style: italic;">序号</span>：音效播放器的识别序号

<span style="color: blue; font-style: italic;">名称</span>：播放器的名称

<span style="color: blue; font-style: italic;">音效资产</span>：引用具体要播放的音效资产

<span style="color: blue; font-style: italic;">音量</span>：影响音效播放时的响度大小

<span style="color: blue; font-style: italic;">播放速度</span>：音效资产的播放速度

<span style="color: blue; font-style: italic;">循环播放</span>：开启后，音效资产的播放完毕后会再次进行播放

<span style="color: blue; font-style: italic;">循环时间间隔（s）</span>：循环播放的音效在结束后会等待配置的间隔时间后再次播放

<span style="color: blue; font-style: italic;">3D音效</span>：是否是3D音效，如果勾选则可以进行相关配置

<span style="color: blue; font-style: italic;">范围预览</span>：开启后可以在场景内看到对应的音效传播范围

![](../images/音效播放器_mhwiv89yra02_3配置音效播放器_2.png)

<span style="color: blue; font-style: italic;">范围半径(m)</span>：可配置音效传播的范围

<span style="color: blue; font-style: italic;">挂接点</span>：可指定某个挂接点位置作为音效的音源位置

<span style="color: blue; font-style: italic;">衰减方式</span>：在使用3D音效的情况下，听者（大多数时候是角色）距离音源越远，则听到的音量越小，直至超过范围后音量变为0，衰减方式定了音量变小的趋势

<span style="color: blue; font-style: italic;">均匀衰减</span>：音量的衰减和听者距离音源的距离为线性关系

<span style="color: blue; font-style: italic;">先快后慢</span>：听者在音源较近处时，远离音源造成的音量衰减会更快

<span style="color: blue; font-style: italic;">先慢后快</span>：听者在音源较近处时，远离音源造成的音量衰减会更慢

<span style="color: blue; font-style: italic;">偏移</span>：音源的位置偏移

# 三、使用节点图控制音效

添加音效播放器

![](../images/音效播放器_mhwiv89yra02_三使用节点图控制音效.png)

调整指定音效播放器

![](../images/音效播放器_mhwiv89yra02_三使用节点图控制音效_2.png)

关闭指定音效播放器

![](../images/音效播放器_mhwiv89yra02_三使用节点图控制音效_3.png)

启动/暂停指定音效播放器

![](../images/音效播放器_mhwiv89yra02_三使用节点图控制音效_4.png)

玩家播放单次2D音效

![](../images/音效播放器_mhwiv89yra02_三使用节点图控制音效_5.png)
