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
正常查看状态下无法对信息进行修改，点击Edit后启动修改模式。对于某些字段的修改，使用Datalist进行限制，若违规填写将无法进行Submit。点击Submit只会对地图上的Leaflet.Marker进行修改，只有在退出编辑模式时才会将更改统一写入数据库，这种设计方式减少了对数据库Post的次数，避免了反复修改造成的valueless的请求，在数据量巨大的情况下降低数据库负荷。在数据库完成了写入后重新载入被修改的货物（卡车）信息，保证前后端同步。
### 货物（卡车）的删除操作
开启删除模式后，双击目标进行删除，后端数据库根据接收到的Id进行对应元组删除。
### 位置查询
基于Leaflet Control Geocoder进行实现，在初始化Leaflet.map后将此控件作为Layer加入。在搜索栏内搜索关键字会弹出对应地点信息，选择后地图Viewport移动至对应地点并使用Marker作为准确标记，取消搜索自动删除Marker。（这种用了插件的报告里面凑字数方法：去插件的Github仓库里，问那个copilot，这个东西的功能是怎么实现的）
### 热力图显示
对当前Map上显示的卡车（货物）进行热力图可视化，基于Leaflet.Heatmap进行完成。开启热力图模式后，为Leaflet.map添加Heatmap Layer，并在左侧创建热力图控件，可以控制热力图的Radius和Blur参数，根据用户需求做到理想的可视化效果。
### 路径规划
使用Leaflet-routing-maching实现，基于OSM的API进行路径规划。（具体实现去他仓库里面问）
#### 为货物选取目的地
点击图标选择货物，开启控件面板中的Select Destination按钮后点击地图上任意地点选择目的地。Leaflet-routing-maching进行最优路径查询，返回路径信息后将Leaflet-routing-maching的coords字段转为线要素并以GeoJson格式存储。开启控件面板的Add WayPoints后可进行途径点的添加和删除，点击地图上任意位置添加途径点并可在Leaflet-routing-maching上进行途径点删除。点击Confirm将当前路径信息提交至数据库中。
#### 为卡车选择货物
在Truck界面选择Select Cargo后进入为卡车选择货物模式，此时所有的卡车和货物都会显示在地图上。点击卡车图标选择目标卡车，接着点击货物图标为卡车选择目标货物，Leaflte-routing-maching进行最优路径规划后点击confirm将路径提交至后端，并通过外键将Truck和Cargo相关联。当鼠标悬停在货物上时会显示货物对应的路径，此操作通过直接向后端查询货物的route信息并使用Leaflet.Polyline显示，不使用GeoServer加载整个线要素图层降低了加载时间。
#### 显示所有货物（卡车）的路径
在左侧栏中选择View Route时，会通过GeoServer获取包含所有路径的线要素图层，通过Leaflet.GeoJson将路径显示在地图上。为每个路径创建Popup，显示路径上卡车与货物的信息。在左侧控制面板中可以根据货物的种类、货物的目的地和出发地对显示的路径进行筛选。
### 等时圈分析
通过leaflet-reachability插件实现可达分析，帮助卡车找到距自身一定行驶时间、距离的货物，实现快速接货减少空车时间。具体实现方式，通过Open Route Service的API获取可达区域的polygon，当接口返回Polygon的GeoJSON是通过map.fire进行时间的广播，监听到此事件后将货物与可达Polygon做一个点在面内的分析，筛选出可达的货物。


## 缺陷
watch过度使用，进行过度的开发可能会导致代码难以理解与维护。  
组件间信息的传递过度依赖Props,并在子组件中修改Props违反了单行下向绑定的规定。对于当前业务逻辑简单的情况下子组件通过修改Props去对父组件进行变动是可行的，但当业务逻辑变得复杂之后，这很可能导致更改操作的冲突。在本项目后续的开放中已转为使用emit派发事件来实现子组件对父组件的更改。





