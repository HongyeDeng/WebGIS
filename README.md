# WebGIS

## 设计目的
为卡车司机和货主提供一个端到端的物流平台，去除物流公司作为中间商，让运输和货物端之间直接对接。

## 建库过程
建库代码 Flask/CreateTable
三个表Cargo、Truck、Order（这个表没用上，报告写上糊弄一下）
表的设计：Cargo、Truck在存储自身数据之余还有一个外键用于互相关联，体现出了卡车司机和货主之间的这个端到端。Order表用于存储所有的运输路径信息。

## 使用到的技术
Vue ：渐进式开发框架，有更高DOM的运行效率，将网页分割为组件，基于组件进行开发可以方便组内分工合作，代码复用，提高开发效率。
GeoServer 发布地图服务：存储欧洲SHP，路径线要素，卡车货物位置点要素
Piana 状态管理：监控当前页面状态，位于那个页面，选了哪个选项
Flask 后端数据查询：与Postgres + PostGis进行交互，获取数据库信息并返回给前端

## 具体功能
### 卡车和货物的位置显示
使用Leaflet.Marker实现，主要代码位于BasicMap.vue。当切换页面时，触发事件监听器，清除Leaflet上所有的Marker后向后端查询所有的卡车（货物），获得返回的Json后根据位置字段将所有Marker放在对应位置。根据卡车（货物）的信息为每个Marker动态创建对应的Popup，使用CreateApp新建一个Vue App作为Popup的content，保证创建的Popup也具有Vue的特性。
### 信息的修改
正常查看状态下无法对信息进行修改，点击Edit后启动修改模式。
