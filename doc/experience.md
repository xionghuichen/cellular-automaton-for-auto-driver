## 类的定义规范
1. 对于外部可访问的数据成员,使用property进行约束，不要直接进行变量的引用
    - 如果这个成员只读的，设置property
        - 对于通过初始化形成的只读属性，需要前面加下划线 __a
    - 如果成员是可读可写的，设置property 和 xxx.setter
2. 什么时候你需要使用getter和setter而不是直接开放某个数据成员
    - 这个属性的值会被频繁改变，这就意味着
        - 你可能需要对这个属性设置log，try，catch一类的操作
    - 这个属性内外的存储结构不一致，比如location是一个二维数组，第一个维度代表的是车道，第二个维度代表的是坐标
        - 你可能只需要得到某辆车的车道或者坐标，不需要整个location
        - 维护不变式关系，这个属性的获得需要经过一系列内部成员变量的计算而得到（比如一个类内部要维持连个变量a和b有a = b * 2的关系，那么在a和b的setter里计算就能维持这样的关系）
    - 一个属性如果过程中不会被改变，他唯一可能是被设计成只读属性，但是什么时候需要只读属性，而不是直接开放呢
        - 这个变量被修改会引起致命错误？
        - 你吃饱了撑着去改一个明显是常量的属性，这怪我代码太丑还是你太蠢？？
        - 不应该有“纯粹为了读写属性而写的getter/setter”，没有逻辑意义的getter/setter是不应该存在的
    - 提供一个debug的接口？
    - 一个属性的读或者写需要进行权限检验的时候
    - 可以将setter和getter用于lambda表达式，进行map操作～
3. 区别与setter和getter，用其他的动词代替这两个动词，使得你的方法设计出来表述更为清晰


## git 使用
1. 不能上传100m以上的文件，
这个链接有解决方案： https://help.github.com/articles/removing-files-from-a-repository-s-history/
注意，如果有多个分支涉及到100m以上的文件，你需要对每一个commit进行这个操作，最后在做一个 push才行
2. 使用 git reset origin/master 回到远程的分支的最后一个commit版本
3. git commit --amend 可以用于重新输入commit 的内容
4. .gitignore 的配置规则、
    配置文件用于配置不需要加入版本管理的文件，配置好该文件可以为我们的版本管理带来很大的便利，以下是个人对于配置 .gitignore 的一些心得。

    1、配置语法：

    　　以斜杠“/”开头表示目录；

    　　以星号“*”通配多个字符；

    　　以问号“?”通配单个字符

    　　以方括号“[]”包含单个字符的匹配列表；

    　　以叹号“!”表示不忽略(跟踪)匹配到的文件或目录；

    　　

    　　此外，git 对于 .ignore 配置文件是按行从上到下进行规则匹配的，意味着如果前面的规则匹配的范围更大，则后面的规则将不会生效；

    2、示例：

    　　（1）规则：fd1/*
    　　　　  说明：忽略目录 fd1 下的全部内容；注意，不管是根目录下的 /fd1/ 目录，还是某个子目录 /child/fd1/ 目录，都会被忽略；

    　　（2）规则：/fd1/*
    　　　　  说明：忽略根目录下的 /fd1/ 目录的全部内容；

    　　（3）规则：

    /*
    !.gitignore
    !/fw/bin/
    !/fw/sf/

    说明：忽略全部内容，但是不忽略 .gitignore 文件、根目录下的 /fw/bin/ 和 /fw/sf/ 目录；

## 应用列表产生式
1. reocord_velocity.extend([x.velocity*1.0 for key,x in output_cars.items() if x.velocity > 0])

## 拟合图像

```
    order = 8
    #绘制原始数据
    ax.plot(x,y,label=u'原始数据',color='m',linestyle='',marker='.')
    #计算多项式
    c=np.polyfit(x,y,order)#拟合多项式的系数存储在数组c中
    yy=np.polyval(c,x)#根据多项式求函数值
    #进行曲线绘制
    x_new=np.linspace(0, 365, 2000)
    f_liner=np.polyval(c,x_new)
    #ax.plot(x,y,color='m',linestyle='',marker='.')
    ax.plot(x_new,f_liner,label=u'拟合多项式曲线',color='g',linestyle='-',marker='')
    # labels标签设置
    ax.set_xlim(0, 366)
    ax.set_xlabel(u'天')
    ax.set_ylabel(u'盐度')
    ax.set_title(u'盐度的日变化', bbox={'facecolor':'0.8', 'pad':5})
    ax.legend()
    plt.show()
```

##　注意循环[多层循环]的迭代变量的初始化位置，位置不一样，可能导致下一次循环沿用了上次循环的结果