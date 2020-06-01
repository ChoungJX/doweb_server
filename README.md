# doweb_server
a docker visual interface (control server)

Docker可视化界面 (控制端)

Docker ビジュアルインターフェイス (control server)

## Project architecture/项目架构/プロジェクト アーキテクチャー
<center> |Browser|　<<==http/https==>　|doweb_server| <<==http/https==>> |doweb_controller1/2/3...| </center>

## doweb_server architecture/doweb_server架构/doweb_server アーキテクチャー
<center> |NGINX| <<==proxy==>> |doweb_server|&|webssh| </center>

input `python run.py` to run

输入 `python run.py` 运行

`python run.py`を入力ください。 

## other code/其他代码/ほかのコード
### node code/节点端
go to node server code[doweb_controller](https://github.com/ChoungJX/doweb_controller)

访问节点端代码[doweb_controller](https://github.com/ChoungJX/doweb_controller)

node serverコードを入る[doweb_controller](https://github.com/ChoungJX/doweb_controller)

### client/客户端
go to client[doweb_client](https://github.com/ChoungJX/doweb_client)

点击访问客户端代码[doweb_client](https://github.com/ChoungJX/doweb_client)

node serverコードを入る[doweb_client](https://github.com/ChoungJX/doweb_client)