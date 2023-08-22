# work-task-manager
1. 设计宗旨：帮助用户管理日常工作内容
2. 开发技术：代码使用 `Python` 开发，GUI界面使用 `PyQt6` 模块开发，系统中缓存的数据使用 `sqlite` 数据库存储，数据库地址：`家目录/.work_task_manager_db/work_task_manager_db`
3. 使用方法：
   1. 首先添加或导入数据字典项
   2. 添加项目数据
   3. 添加任务数据
4. 程序启动：切换到程序目录下，安装 `requirement.txt` 中所需要的依赖包，`pip install -r requirement.txt`，另外开发程序时使用的 `Python` 版本为 `3.9`，没有对低版本进行测试
5. 打包方法：切换到程序目录下，执行 `pyinstaller main.spec`，需要将 `main.spec` 文件中 `pathex` 变量指定为实际打包时的项目地址，`datas` 变量中包含一个元祖，元祖第一个元素指定为实际打包时项目静态资源文件目录，第二个元素为在项目中使用的地址，无需改动