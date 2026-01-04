# 特效播放

**URL**: https://act.mihoyo.com/ys/ugc/tutorial/detail/mh4ppo02m1o8

**爬取时间**: 2026-01-04 08:14:28

---

## 特效播放


# 一、特效播放组件的功能

特效播放组件包含两部分的功能

1、*节点图*播放的特效必须依赖特效播放组件，没有该组件的情况下无法通过节点图播放特效

2、允许通过组件挂载一些默认的*循环特效*，这些特效会与实体一同创建

特效播放组件上同时可生效多个特效

# 二、特效播放组件的编辑

## **1.添加**特效播放组件

![](../images/特效播放_mh4ppo02m1o8_1添加特效播放组件.png)

(1)切换到实体或元件的组件页签

(2)找到或新增一个特效播放组件

特效播放组件是所有单位的默认挂载组件（即实体创建时会默认挂载），因此对于新建的实体或元件，可以在组件页签直接找到特效播放组件

如果不存在，可以通过添加通用组件按钮新增一个特效播放组件

## **2.**新增特效播放

在特效播放组件的详情页面，可以点击【添加特效】来新增一个特效配置

![](../images/特效播放_mh4ppo02m1o8_2新增特效播放.png)

## **3.**配置特效播放

![](../images/特效播放_mh4ppo02m1o8_3配置特效播放.png)


|  |  |
| --- | --- |
| **参数名** | **参数说明** |
| <span style="color: blue; font-style: italic;">特效播放器序号</span> | 特效播放器的序号 |
| <span style="color: blue; font-style: italic;">特效播放器名称</span> | 特效播放器的名称，同一个实体上的名称不可以重复 |
| <span style="color: blue; font-style: italic;">特效资产类型</span> | 可选*循环特效*和*限时特效*，决定了使用的特效资产库  特效相关资产见[特效](特效_mhe1030vx380.md) |
| <span style="color: blue; font-style: italic;">特效资产</span> | 可以选择特效资产。选择了特效资产后，可以在场景中预览播放 |
| <span style="color: blue; font-style: italic;">跟随位置</span> | 是否跟随组件的拥有者一起运动 |
| <span style="color: blue; font-style: italic;">跟随旋转</span> | 是否跟随组件的拥有者一起旋转，仅当【跟随位置】为【是】时才生效 |
| <span style="color: blue; font-style: italic;">挂接点</span> | 特效播放挂接的位置，可以选择实体上已配置的*固有挂接点*或*额外挂接点* |
| <span style="color: blue; font-style: italic;">缩放比例</span> | 特效的缩放比例 |
| <span style="color: blue; font-style: italic;">偏移</span> | 特效播放位置相对于挂接点的偏移 |
| <span style="color: blue; font-style: italic;">旋转</span> | 特效播放位置相对于挂接点的旋转 |
| <span style="color: blue; font-style: italic;">本地过滤器</span> | 可引用本地过滤器节点图，用于判断指定特效播放与否，两种过滤器的区分和使用请看节点图  本地过滤器会在特效挂载实体在场期间内，持续进行检测  对应本地过滤器节点图中的基础节点，进行说明  * 获取自身实体  输出参数为挂载特效组组件的实体  * 获取目标实体  无  * 获取当前角色  输出参数为本地角色 |

**