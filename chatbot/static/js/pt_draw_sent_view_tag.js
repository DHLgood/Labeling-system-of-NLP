var getSentent = null, // function to get sentent from the drawStruct's segment words
    initdom = null,// function to init the list dom dynamicly
    DRAW_PARENT_ID = "analysisContent", // parent id            ul的id
    listen = null,
    worddrop = null,
    dblclickAction = null,
    drawsen = null,
    speechdrop = null,
    outerlisten = null;


//将分词拼接成句子字符串
getSentent = function (sentEle) {
    //console.log(sentEle)
    var wsList = [],
        enReg = /^[A-Za-z']*$/;
    for (var i = 0; i < sentEle.length; i++) {
        wsList.push(sentEle[i].cont);
        // add the logic for English sentence !
        if (enReg.test(sentEle[i].cont) && i < sentEle.length - 1 && enReg.test(sentEle[i + 1].cont)) {
            wsList.push(" ");
        }
    }
    return wsList.join("");//把数组的元素放入一个字符窜

};

//回退功能 重新绘制删除的句子的分词器的原始结果
drawsen = function (nextId, sentsObj, sum) {
    var divEle;//存放字的div块
    var text;//存放字信息
    var Container;
    var Seg = [];
    var eleCopy;
    var dEle = document.createElement("div");
    //把句子添加进去
    document.getElementById(nextId).parentNode.insertBefore(dEle, document.getElementById(nextId).previousSibling);
    dEle.setAttribute("class", "well-well-sm");
    dEle.style.cssText = 'border:1px solid #ccc;display:inline-block;margin-top:8px';

    // whether sentsObj has been tagged
    // if ('taggedSeg' in sentsObj)
    //     Seg = sentsObj.taggedSeg;
    // else
    //     Seg = sentsObj.originSeg;

    Seg = sentsObj.tokens_and_pos;


    //a数组   放置当前句子中的字
    var wordlist = [];
    for (var k = 0; k < Seg.length; k++) {
        var pos = "LW"
        if ('pos' in Seg[k]) {
            pos = Seg[k].pos;
        }
        var cxEle = document.createElement("div");
        var bigCon = document.createElement("div");
        bigCon.setAttribute("class", "bigCon");
        bigCon.style.cssText = 'border:1px solid #ddd;float:left';
        //给词性节点赋予词性值
        cxEle.appendChild(document.createTextNode(pos));
        // cxEle.style.fontStyle = "italic";
        cxEle.style.fontSize = "12pt";
        ////对每个词块进行判断是否为一个字 如果大于1个字把div字块塞入div词块
        if (Seg[k].token.length > 1) {
            Container = document.createElement("div");
            Container.setAttribute("class", "panel-panel-default");
            Container.style.float = "left";
            Container.style.marginLeft = "25px";
            Container.style.marginRight = "25px";
            Container.style.marginTop = "7px";
            Container.style.marginBottom = "4px";
            var b = Seg[k].token.split("");
            for (var l = 0; l < b.length; l++) {
                wordlist.push(b[l]);
                divEle = document.createElement("div");
                text = document.createTextNode(b[l]);
                divEle.appendChild(text);
                Container.appendChild(divEle);
                //a数组是当前句子中的字，数组长度-1与此句子之前句子的总字数等于字的id中的编号
                var s = wordlist.length - 1 + sum;
                divEle.setAttribute("id", "dragEle" + s);
                divEle.setAttribute("draggable", "true");
                divEle.style.float = "left";
                divEle.style.height = "34px";
                divEle.setAttribute("class", "drag");
                divEle.style.fontSize = "23.0pt";
                bigCon.appendChild(Container);
                bigCon.appendChild(cxEle);
                dEle.appendChild(bigCon);
            }
        }
        //一个字就是单独的div词块
        else if (Seg[k].token.length == 1) {
            Container = document.createElement("div");
            Container.setAttribute("class", "panel-panel-default");
            Container.style.float = "left";
            Container.style.marginLeft = "25px";
            Container.style.marginRight = "25px";
            Container.style.marginTop = "7px";
            Container.style.marginBottom = "4px";
            wordlist.push(Seg[k].token);
            divEle = document.createElement("div");
            text = document.createTextNode(Seg[k].token);
            divEle.appendChild(text);
            //a数组是当前句子中的字，数组长度-1与此句子之前句子的总字数等于字的id中的编号
            var e = wordlist.length - 1 + sum;
            divEle.setAttribute("id", "dragEle" + e);
            divEle.setAttribute("draggable", "true");
            divEle.style.float = "left";
            divEle.setAttribute("class", "drag");
            divEle.style.height = "34px";
            divEle.style.fontSize = "23.0pt";
            Container.appendChild(divEle);
            bigCon.appendChild(Container);
            bigCon.appendChild(cxEle);
            dEle.appendChild(bigCon);
        }
    }
    //对动态生成dom对象的区域进行事件监听
    listen();
};



//展示句子：分词结果和词性
initdom = function (parentId, sentsObj) {
    var wordList = [];
    var divEle;//存放字的div块
    var text;//存放字信息
    var text0;//存放词的信息
    var Container;  //存放词的div块  这是仅供修改的词块
    var Container0;  //存放词的div块 这是仅供展示的词块
    var seg = [];
    var parentContainer = document.getElementById(parentId),
        liEle = document.createElement("LI"),
        itemDivEle = document.createElement("DIV"),
        eleCopy;
    //初始化ul：删除所有的子元素，进行初始化
    while (parentContainer.childNodes.length > 0)
        parentContainer.removeChild(parentContainer.lastChild);
    liEle.style.cssText = 'border:1px solid #ccc; border-radius:10px ; margin:32px 10px 40px 9px; padding:10px; ';    ///////////////////////////////////////////////////////////////
    liEle.setAttribute("class", "liEle");
    itemDivEle.setAttribute("class", "text-item");
    itemDivEle.style.height = "auto";
    itemDivEle.style.fontSize = "13pt";
    liEle.appendChild(itemDivEle);

    for (var j = 0; j < sentsObj.length; j++) {//the numbers of sents
        //<li>标签的复制包含子元素
        eleCopy = liEle.cloneNode(true);
        var dEle = document.createElement("div");//
        var dEle0 = document.createElement("div");//原始分词结果仅供观看的句子
        var nmb = document.createElement("div");////使得下个div另起一行
        var nmba = document.createElement("div");//使得下个div另起一行
        var btn = document.createElement("button");//添加回退按钮
        btn.setAttribute("class", "btn btn-info btn-lg");
        btn.setAttribute("id", j);//设置btn的id ，根据此id 可以重新方便的写回退功能
        btn.textContent = "回退";
        dEle0.setAttribute("class", "text-class");
        dEle.setAttribute("class", "well-well-sm");

        //保证句子的词内联排列，动态根据框架的大小而变化
        dEle.style.cssText = 'border:1px solid #ccc;display:inline-block;margin-top:8px';
        dEle0.style.cssText = 'border-bottom:1px solid #9d9d9d;border-left : 3px solid #0099cc ;display:inline-block';
        eleCopy.appendChild(dEle0);//展示的句子
        eleCopy.appendChild(nmb); //使得下个div另起一行
        eleCopy.appendChild(dEle);//修改的句子
        eleCopy.appendChild(nmba);//使得下个div另起一行
        eleCopy.appendChild(btn);//添加回退按钮
        eleCopy.firstChild.setAttribute("y", j);

        // if ('tagedSeg' in sentsObj[0])
        //     seg=sentsObj[j].tagedSeg;
        // else
        //     seg=sentsObj[j].originSeg;

        //调用getSentent方法，将分词拼接成字符串句子
        // var sentent = getSentent(seg);
        // console.log(sentsObj)
        // var textNode = document.createTextNode([ "句子", returnAnalysisRst[j].id , ":", sentent].join(""));
        // eleCopy.firstChild.appendChild(textNode);
        // parentContainer.appendChild(eleCopy);

        // var sentence = seg.join("");
        var sentTextNode = document.createTextNode("id: " + sentsObj[j].id);
        eleCopy.firstChild.appendChild(sentTextNode);
        parentContainer.appendChild(eleCopy);

        seg = sentsObj[j].tokens_and_pos;


        //!!!!!!原始的分词结果输出(仅供展示)
        //给每个字富裕div字块，每个词富裕赋予div词块， div词块的监听在下个函数
        //对每个词块进行判断是否为一个字
        for (var m = 0; m < seg.length; m++) {
            var pos = 'LW';
            if ('pos' in seg[m]) {
                pos = seg[m].pos;
            }
            var box = document.createElement("div");
            box.style.cssText = 'border:1px solid #ddd;float:left';
            var speechEle = document.createElement("div");
            speechEle.style.fontSize = "12pt";
            speechEle.appendChild(document.createTextNode(pos));
            Container0 = document.createElement("div");
            Container0.setAttribute("class", "panel");
            Container0.style.cssText = 'border:1px solid #ccc;';
            Container0.style.float = "left";
            Container0.style.marginLeft = "25px";
            Container0.style.marginRight = "26px";
            Container0.style.marginTop = "7px";
            Container0.style.marginBottom = "2px";
            Container0.style.fontSize = "23pt";
            // text0 = document.createTextNode(seg[m].cont);

            // console.log(seg[m])

            text0 = document.createTextNode(seg[m].token);
            Container0.appendChild(text0);
            box.appendChild(Container0);
            box.appendChild(speechEle);
            dEle0.appendChild(box);
        }

        //!!!!!!原始的分词结果输出(仅供修改)
        for (var k = 0; k < seg.length; k++) {
            var pos = 'LW';
            if ('pos' in seg[k]) {
                pos = seg[k].pos;
            }
            //给词性节点赋予词性值
            var cxEle = document.createElement("div");
            var bigCon = document.createElement("div");//存放词和词性的大div
            bigCon.setAttribute("class", "bigCon");
            bigCon.style.cssText = 'border:1px solid #ddd;float:left';
            cxEle.style.fontSize = "12pt";
            cxEle.appendChild(document.createTextNode(pos));
            ////对每个词块进行判断是否为一个字 如果大于1个字把div字块塞入div词块
            // if (seg[k].cont.length > 1) {
            if (seg[k].token.length > 1) {
                Container = document.createElement("div");
                //.panel-panel-default的css在init.css里
                Container.setAttribute("class", "panel-panel-default");
                Container.style.float = "left";
                Container.style.marginLeft = "25px";
                Container.style.marginRight = "25px";
                Container.style.marginTop = "7px";
                Container.style.marginBottom = "4px";
                //b数组存放一个词包含的字，a数组全局变量，存放所有的字，将div字块塞入div词块
                var  b = seg[k].token.split("");
                // var b = seg[k].split("");
                for (var l = 0; l < b.length; l++) {
                    wordList.push(b[l]);
                    divEle = document.createElement("div");
                    text = document.createTextNode(b[l]);
                    divEle.appendChild(text);
                    Container.appendChild(divEle);
                    var s = wordList.length - 1;
                    divEle.setAttribute("id", "dragEle" + s);
                    divEle.setAttribute("draggable", "true");
                    divEle.style.float = "left";
                    divEle.style.height = "34px";
                    divEle.setAttribute("class", "drag");
                    divEle.style.fontSize = "23.0pt";
                    bigCon.appendChild(Container);
                    bigCon.appendChild(cxEle);
                    dEle.appendChild(bigCon);
                }
            }
            //一个字就是单独的div词块
            else if (seg[k].token.length == 1) {
                Container = document.createElement("div");
                Container.setAttribute("class", "panel-panel-default");
                Container.style.float = "left";
                Container.style.marginLeft = "25px";
                Container.style.marginRight = "25px";
                Container.style.marginTop = "7px";
                Container.style.marginBottom = "4px";
                wordList.push(seg[k].token);
                divEle = document.createElement("div");
                text = document.createTextNode(seg[k].token);
                divEle.appendChild(text);
                var e = wordList.length - 1;
                divEle.setAttribute("id", "dragEle" + e);
                divEle.setAttribute("draggable", "true");
                divEle.style.float = "left";
                divEle.setAttribute("class", "drag");
                divEle.style.height = "34px";
                divEle.style.fontSize = "23.0pt";
                Container.appendChild(divEle);
                bigCon.appendChild(Container);
                bigCon.appendChild(cxEle);
                dEle.appendChild(bigCon);
            }
        }
    }
    //对句子里的词、字、包含词和词性的整体进行事件监听
    listen();
};

//句子里的监听包括 div字和div词和词性的大容器
listen = function () {
    $(".panel-panel-default").on('dblclick', function (event) {
        //对div词块进行双击监听
        dblclickAction(event);
    });
    $(".panel-panel-default").on('drag', function (event) {

        event.preventDefault();
    });
    //必须ondragover事件， event.preventDefault()允许其他元素能放到这个元素上
    $(".panel-panel-default").on('dragover', function (event) {
        event.preventDefault();
    });
    $(".panel-panel-default").on('drop', function (event) { //$("#div)[0] 将jquery对象转化为dom对象  $(dom对象)：即dom对象转化为jquery对象
        worddrop(event);
        event.preventDefault();
    });
    $(".drag").on("dragstart", function (event) {

        event.originalEvent.dataTransfer.setData("Text", event.currentTarget.id);
    });
    $(".drag").on("mouseover", function () {
        this.style.cursor = "pointer";
    });
    $(".bigCon").on("dragover", function (event) {

        event.preventDefault();
    });
    //包含词和词性的整体的监听，drop事件：只允许词性放置
    $(".bigCon").on("drop", function (event) {
        speechdrop(event);
    });
    //回退按钮，删除句子，重新绘制原始句子
    $(".btn.btn-info.btn-lg").on("click", function () {
        var sum = 0;
        var num = this.getAttribute("id");
        //计算当前句子之前的句子中的所有的字的数量，方便给将要绘制的句子中的字给id中的数字
        //计算已经有多少个字
        for (var i = 0; i < Number(num); i++) {
            // if ('tagedSeg' in returnAnalysisRst[i])
            //     for (var k = 0; k < returnAnalysisRst[i].tagedSeg.length; k++) {
            //         sum += returnAnalysisRst[i].tagedSeg[k].cont.length;
            //     }
            // else {
            //     for (var k = 0; k < returnAnalysisRst[i].originSeg.length; k++) {
            //         sum += returnAnalysisRst[i].originSeg[k].cont.length;
            //     }
            // }
            segs = returnAnalysisRst[i].tokens_and_pos
            for (var k = 0; k < segs.length; k++) {
                sum += segs[k].token.length;
            }
        }
        //删除当前要回退的句子
        $(this.previousSibling.previousSibling).remove();
        //再次绘制分词器给我的句子
        console.log(sum);
        console.log(returnAnalysisRst[num]);
        drawsen(num, returnAnalysisRst[num], sum);
    });
};

//词性drop
speechdrop = function (event) {
    var id = event.originalEvent.dataTransfer.getData("Text");
    //若放置的是字，直接函数返回
    if (id.slice(0, 7) == "dragEle") {
        return;
    }
    //若放置的是词性div，则修改词性
    event.currentTarget.childNodes[1].textContent = $("#" + id)[0].textContent;
    event.currentTarget.childNodes[1].style.color = "red";
};


//字drop
worddrop = function (event) {

    var id = event.originalEvent.dataTransfer.getData("Text");
    //如果拖拽的是词性div则阻止默认事件发生，触发上层的bigCon绑定的监听的事件：即词性drop
    if (id.slice(0, 7) != "dragEle")
        return false;

    var end = Number(id.slice(7));//拖拽的字的id中的数字
    //左移 用被拖拽的字的id数字与放置的词的末子元素的id数字比较，将这中间的字块 全部添加到词的末尾
    if (Number(id.slice(7)) > Number($(event.currentTarget).children("div:last-child").attr("id").slice(7))) {
        var begin = Number($(event.currentTarget).children("div:last-child").attr("id").slice(7));
        document.getElementById(id).parentNode.style.color = "red";
        for (var i = begin + 1; i < end + 1; i++) {
            (event.currentTarget).appendChild(document.getElementById("dragEle" + i));
        }
        event.currentTarget.style.color = "red";
        //如果目标元素的父亲节点为空则删除空的div词节点的父节点
        $(".panel-panel-default").each(function () {
            if (this.textContent == "")
                $(this.parentNode).remove();
        });
    }
    //右移 用被拖拽的字的id数字与放置的词的第一个子元素的id数字比较，将这中间的字块 全部添加到词块的开头
    else if (Number(id.slice(7)) < Number($(event.currentTarget).children("div:first-child").attr("id").slice(7))) {
        var begin = Number($(event.currentTarget).children("div:first-child").attr("id").slice(7));
        document.getElementById(id).parentNode.style.color = "red";
        for (var i = begin - 1; i > end - 1; i--) {
            $(event.currentTarget).prepend($("#dragEle" + i));
        }
        event.currentTarget.style.color = "red";
        //如果目标元素的父亲节点为空则删除空的div词节点的父节点
        $(".panel-panel-default").each(function () {
            if (this.textContent == "")
                $(this.parentNode).remove();
        });
    }
    event.preventDefault();
};

//对词进行双击事件的监听，双击将词内的字全部分开，单独成词，同时赋予词应该有的监听事件,以及包含词和词性的大div 应该有的监听事件
dblclickAction = function (event) {
    var num = $(event.currentTarget).children().length;
    for (var y = 0; y < num - 1; y++) {
        var Container = document.createElement("div");
        var bigCon = document.createElement("div");
        bigCon.setAttribute("class", "bigCon");
        bigCon.style.cssText = "border:1px solid #ddd ;float:left";
        var cixEle = document.createElement("div");
        cixEle.appendChild(document.createTextNode("LW"));
        cixEle.style.fontSize = "12pt";
        Container.setAttribute("class", "panel-panel-default");
        Container.style.float = "left";
        Container.style.marginLeft = "25px";
        Container.style.marginRight = "25px";
        Container.style.marginTop = "7px";
        Container.style.marginBottom = "2px";
        Container.style.color = "red";
        Container.appendChild(event.currentTarget.childNodes[0]);
        bigCon.appendChild(Container);
        bigCon.appendChild(cixEle);
        //创建一个div词块，将每个字放入依次放入词块中
        event.currentTarget.parentNode.parentNode.insertBefore(bigCon, event.currentTarget.parentNode);
        //监听事件
        $(bigCon).on('dragover', function (event) {
            event.preventDefault();
        });
        $(bigCon).on('drop', function (event) {
            speechdrop(event);
        });
        $(Container).on('dblclick', function (event) {
            dblclickAction(event);
        });
        $(Container).on('dragover', function (event) {
            event.preventDefault();
        });
        $(Container).on('drop', function (event) {
            worddrop(event);
        });
    }
    event.currentTarget.style.color = "red";
};

