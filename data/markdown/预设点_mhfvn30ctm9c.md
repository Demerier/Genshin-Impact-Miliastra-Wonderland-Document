# 预设点

**URL**: https://act.mihoyo.com/ys/ugc/tutorial/detail/mhfvn30ctm9c

**爬取时间**: 2026-01-04 08:27:53

---

## 预设点


# 一、预设点是什么

预设点是一组场景中的世界位置和朝向的数据信息。

预设点可以被需要点位信息的功能所引用，例如出生点、复苏点、节点图获取点位等。

# 二、预设点的编辑

## 1.编辑入口

![](../images/预设点_mhfvn30ctm9c_1编辑入口.png)

## **2.整体编辑界面**

![](../images/预设点_mhfvn30ctm9c_2整体编辑界面.png)

### (1)预设点库

![](../images/预设点_mhfvn30ctm9c_1预设点库.png)

所有预设点在这个窗口枚举。

可管理对应预设点在布设场景的可见性

### **(2)编辑窗口预设点可见**性

![](../images/预设点_mhfvn30ctm9c_2编辑窗口预设点可见性.png)

<span style="color: blue; font-style: italic;">常驻显示开关开启</span>	关闭预设点管理工具，在编辑窗口也可以看到所有预设点

<span style="color: blue; font-style: italic;">常驻显示开关关闭</span>* *关闭预设点管理工具，所有预设点不可见

### **(3)创建预设**点

![](../images/预设点_mhfvn30ctm9c_3创建预设点.png)

通过点击“创建预设点”，在当前编辑窗口中央生成新的预设点。并自动开启命名编辑。

### **(4)预设点的参数**

![](../images/预设点_mhfvn30ctm9c_4预设点的参数.png)

<span style="color: blue; font-style: italic;">预设点名称</span>* *预设点的名称，可以修改

<span style="color: blue; font-style: italic;">预设点索引</span>		作为节点的入参，是预设点的唯一标识

![](../images/预设点_mhfvn30ctm9c_4预设点的参数_2.png)


|  |  |
| --- | --- |
| 配置参数 | 说明 |
| <span style="color: blue; font-style: italic;">锁定变换</span> | 勾选后不可调整预设点的位置和旋转 |
| <span style="color: blue; font-style: italic;">是否在场景中显示</span> | 取消勾选后，只留坐标轴，定点模型不可见 |
| <span style="color: blue; font-style: italic;">位置</span><span style="color: blue;"> </span> | 预设点的位置数据 |
| <span style="color: blue; font-style: italic;">旋转</span> | 预设点的朝向数据 |
| <span style="color: blue; font-style: italic;">单位标签</span> | 可以给预设点添加单位标签。详见[单位标签](单位标签_mhzldmiwdgu4.md) |
| ***<span style="color: blue; font-style: italic;">引用关系</span> |  |


# 三、预设点的引用

## 1.出生点

在“关卡设置”-出生点配置中，可通过<span style="color: blue; font-style: italic;">选择点位</span>引用预设点，作为出生点

![](../images/预设点_mhfvn30ctm9c_1出生点.png)

## 2.复苏点

在“关卡设置”-复苏点配置中，可通过<span style="color: blue; font-style: italic;">选择点位</span>引用预设点，作为复苏点

![](../images/预设点_mhfvn30ctm9c_2复苏点.png)

## 3.节点图

* **查询预设点位置旋转**

![](../images/预设点_mhfvn30ctm9c_3节点图.png)

通过预设点索引，可以查询其位置和旋转数据

通过点击，可展开所有预设点枚举，用于选择做入参

![](../images/预设点_mhfvn30ctm9c_3节点图_3.png)

* **以单位标签获取预设点位列表**

![](../images/预设点_mhfvn30ctm9c_3节点图_4.png)
