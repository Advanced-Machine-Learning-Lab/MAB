MAB项目分为四个模块：
- agent
- algorithm
- simulator
- example


`Simulator`:

每个agent内部维护时间t、事件-时间队列

在agent队列中找最快要发生事件的agent:

    `next_t` = `agent.update()`

    next_t是该agent下一次发生事件的时间

    将(agent, next_t)放回队列


考虑到`Simulator`每次选择的Agent是「最早发生事件」`的Agent`

那么`Simulator`内部应维护一个按照「最早发生事件」所对应「时间t」来对`Agent`进行排序的「队列」。

另外，考虑到`Agent`在队列中可能会出现「饥饿」问题，所有进入队列的Agent都会搭上时间戳，Agent出队后再次进队时、时间戳+1。


首先比较的是`Agent`最近发送事件的时间t，先取出最近发生事件的`Agent`。

然后比较的是时间戳timestamp。每个Agent进入队列前都会打上时间戳。在时间t相等的情况下，更早进入队列的Agent会被更优先选择。

注意：当取出一个agent后，该`agent`可能会改变队列中其他agent的时间（`agent`发送了消息给邻居），所以这个队列不是静态的
        目前的实现没有用最小堆、而是数组
        
        
使用方法：
1. 定义好`Factory`类、写好`Factory`中`get_agent_list()`静态方法 
2. 实例化一个`MultiAgentSimulator`，传入`Factory`和`data`文件夹地址
3. 运行`MultiAgentSimulator`中的`main()`

`example`中实现了两个例子，以供参考。

`todo:本文档有待完善`

