在STM32单片机上实现coap的过程中，发现coap协议的测试工具不多。
网上搜到的主要有两个：
1、CoAP-cli，一个基于NodeJS的CoAP命令行工具，其核心是基于Node-CoAP库。
2、FireFox Copper， 一个Firefox的插件。这个在FireFox 55版本以下的才可用。
两个使用起来都不是很方便。
于是就想着自己写一个测试工具，刚好最近在学python，也就不考虑python是否适合做这样的工具。
目前做为一个客户端测试工具，基本可用。
