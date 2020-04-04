# doweb_server
a docker visual interface

##Project architecture/项目架构/プロジェクト アーキテクチャー

<center>|Browser|　<<==http/https==>　|doweb_server| <<==http/https==>> |doweb_controller1/2/3...|</center>


##doweb_server architecture/doweb_server架构/doweb_server アーキテクチャー

<center>|NGINX| <<==proxy==>> |doweb_server|&|webssh| </center>

input `python run.py` to run
输入 `python run.py` 运行
`python run.py`を入力ください。 

go to [doweb_controller](https://github.com/ChoungJX/doweb_controller)