# 变换原生碰撞可见性和创建设置

**URL**: https://act.mihoyo.com/ys/ugc/tutorial/detail/mhuqbn9yn5bu

**爬取时间**: 2026-01-04 08:07:17

---

## 变换原生碰撞可见性和创建设置


# 一、变换

## 1.变换的含义

描述单位在场景中的几何信息，一般包含位置、旋转与缩放

![](../images/变换原生碰撞可见性和创建设置_mhuqbn9yn5bu_1变换的含义.png)

<span style="color: blue; font-style: italic;">位置</span>：在世界坐标系下的位置

<span style="color: blue; font-style: italic;">旋转</span>：在世界坐标系下的旋转

<span style="color: blue; font-style: italic;">缩放</span>：物件被放大的倍率

<span style="color: blue; font-style: italic;">锁定变换</span>：编辑时属性，如果该属性为“开启”则无法修改实体的变换信息

## 2.节点图相关

可通过节点图查询获取位置信息

![](../images/变换原生碰撞可见性和创建设置_mhuqbn9yn5bu_2节点图相关.png)

# 二、原生碰撞

## 1.原生碰撞的含义

<span style="color: blue; font-style: italic;">原生碰撞</span>指物件的基础碰撞，相比于<span style="color: blue; font-style: italic;">额外碰撞组件</span>所添加的碰撞，更加精细贴合模型。

相对的，原生碰撞作为*基础信息*，其形状无法被修改，玩家仅能控制碰撞的<span style="color: blue; font-style: italic;">初始生效</span>和<span style="color: blue; font-style: italic;">是否可攀爬</span>开关。

![](../images/变换原生碰撞可见性和创建设置_mhuqbn9yn5bu_1原生碰撞的含义.png)

<span style="color: blue; font-style: italic;">初始生效</span>：单位被初始化时，原生碰撞是否生效

<span style="color: blue; font-style: italic;">是否可攀爬</span>：原生碰撞是否可以被角色攀爬，同时要求角色本身必须具有攀爬能力

<span style="color: blue; font-style: italic;">原生碰撞预览</span>：编辑时的功能，如果勾选即可在编辑界面预览到碰撞的外形，见上图

## 2.节点图相关

修改碰撞开关

![](../images/变换原生碰撞可见性和创建设置_mhuqbn9yn5bu_2节点图相关_2.png)

修改碰撞可攀爬性

![](../images/变换原生碰撞可见性和创建设置_mhuqbn9yn5bu_2节点图相关_3.png)

# 三、可见性

## 1.可见性的含义

该*基础信息*描述了运行时*实体*的<span style="color: blue; font-style: italic;">模型</span>是否对玩家可见。仅影响模型，不影响<span style="color: blue; font-style: italic;">碰撞</span>，<span style="color: blue; font-style: italic;">触发器</span>，<span style="color: blue; font-style: italic;">节点图</span>等其他逻辑

推荐制作一些隐藏实体相关的功能

![](../images/变换原生碰撞可见性和创建设置_mhuqbn9yn5bu_1可见性的含义.png)

## 2.节点图相关

![](../images/变换原生碰撞可见性和创建设置_mhuqbn9yn5bu_2节点图相关_4.png)

# 四、创建设置

## 1.创建设置的含义

指当*实体*被布设在场上后，关卡初始化时，是否创建。如果该开关为“关闭”，则需要后续通过节点图动态创建。

![](../images/变换原生碰撞可见性和创建设置_mhuqbn9yn5bu_1创建设置的含义.png)

## 2.节点图相关

当实体被销毁或移除后，也可以使用该节点再次创建

![](../images/变换原生碰撞可见性和创建设置_mhuqbn9yn5bu_2节点图相关_5.png)
