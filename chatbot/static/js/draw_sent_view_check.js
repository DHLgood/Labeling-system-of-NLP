/**
 * Created by Administrator on 2016/8/24.
 */
var getSentent = null, // function to get sentent from the drawStruct's segment words
    initdom=null,// function to init the list dom dynamicly
    DRAW_PARENT_ID = "analysisContent", // parent id            ul的id
    listen = null,
    worddrop = null,
    dblclickAction = null,
    drawsen = null,
    speechdrop = null,
    createSet=null,
    outerlisten = null;



createSet =function () {
    set=[];
    for(var i=0;i<returnAnalysisRst.length;i++){
        var sum=0;
        var tempSet=[];
        for(var j=0;j<returnAnalysisRst[i].originSeg.length;j++){
            var temp={};
            temp.cont = returnAnalysisRst[i].originSeg[j].cont;
            temp.pos = "LW";
            sum+=returnAnalysisRst[i].originSeg[j].cont.length;
            temp.startIndex = sum-returnAnalysisRst[i].originSeg[j].cont.length;
            temp.endIndex = sum-1;
            tempSet.push(temp);
        }
        set.push(tempSet);
    }
};
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
drawsen = function (nextId,sentsObj,sum) {
    var divEle;//存放字的div块
    var text;//存放字信息
    var Container;
    var Seg=[];
    var eleCopy;
    var dEle=document.createElement("div");
    //把句子添加进去
    document.getElementById(nextId).parentNode.insertBefore(dEle,document.getElementById(nextId).previousSibling);
    dEle.setAttribute("class","well-well-sm");
    dEle.style.cssText='border:1px solid #ccc;display:inline-block;margin-top:8px';

    if ('tagedSeg' in sentsObj)
        Seg=sentsObj.tagedSeg;
    else
        Seg=sentsObj.originSeg;

    //wordlist数组放置当前句子中的字
    var wordlist= [];
    for (var k = 0;k < Seg.length;k++) {
        var cxEle = document.createElement("div");
        var bigCon = document.createElement("div");
        bigCon.setAttribute("class", "bigCon");
        bigCon.style.cssText = 'border:1px solid #ddd;float:left';
        //给词性节点赋予词性值
        cxEle.appendChild(document.createTextNode("LW"));
        // cxEle.style.fontStyle = "italic";
        cxEle.style.fontSize = "12pt";
        ////对每个词块进行判断是否为一个字 如果大于1个字把div字块塞入div词块
        if (Seg[k].cont.length > 1) {
            Container = document.createElement("div");
            Container.setAttribute("class", "panel-panel-default");
            Container.style.float = "left";
            Container.style.marginLeft = "25px";
            Container.style.marginRight = "25px";
            Container.style.marginTop = "7px";
            Container.style.marginBottom="4px";

            var count=0;
            for (var i = 0; i < set[nextId].length; i++) {
                if (set[nextId][i].cont == Seg[k].cont && set[nextId][i].startIndex == wordlist.length) {
                    count++;
                    break;
                }
            }
            if(count!=1) {
                Container.style.color = 'red';
                cxEle.style.color = "red";
            }
            if(count == 1 && set[nextId][i].pos != Seg[k].pos)
                cxEle.style.color = "red";

            var b = Seg[k].cont.split("");
            for (var l = 0; l < b.length; l++) {
                wordlist.push(b[l]);
                divEle = document.createElement("div");
                text = document.createTextNode(b[l]);
                divEle.appendChild(text);
                Container.appendChild(divEle);
                //wordlist数组是当前句子中的字，数组长度-1与此句子之前句子的总字数等于字的id中的编号
                var s = wordlist.length - 1+sum;
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
        else if (Seg[k].cont.length == 1) {
            Container = document.createElement("div");
            Container.setAttribute("class", "panel-panel-default");
            Container.style.float = "left";
            Container.style.marginLeft = "25px";
            Container.style.marginRight = "25px";
            Container.style.marginTop = "7px";
            Container.style.marginBottom="2px";

            var count=0;
            for (var i = 0; i<set[nextId].length; i++) {
                if (set[nextId][i].cont == Seg[k].cont && set[nextId][i].startIndex == wordlist.length) {
                    count++;
                    break;
                }
            }
            if(count != 1) {
                Container.style.color = 'red';
                cxEle.style.color = "red";
            }
            if(count == 1 && set[nextId][i].pos != Seg[k].pos)
                cxEle.style.color = "red";

            wordlist.push(Seg[k].cont);
            divEle = document.createElement("div");
            text = document.createTextNode(Seg[k].cont);
            divEle.appendChild(text);



            //a数组是当前句子中的字，数组长度-1与此句子之前句子的总字数等于字的id中的编号
            var e = wordlist.length - 1+sum;
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
initdom=function (parentId,sentsObj) {
    createSet();
    var wordList=[];
    var divEle;//存放标注后字的div块
    var text;//存放标注后字信息
    var text0;//存放标注后的词的信息
    var Container;  //存放词的div块  这是仅供修改的词块
    var Container0;  //存放词的div块 这是仅供展示的词块
    var seg=[];
    var parentContainer = document.getElementById(parentId),
        liEle = document.createElement("LI"),
        itemDivEle = document.createElement("DIV"),
        eleCopy;
    //初始化ul：删除所有的子元素，进行初始化
    while (parentContainer.childNodes.length > 0)
        parentContainer.removeChild(parentContainer.lastChild);
    liEle.style.cssText='border:1px solid #ccc; border-radius:10px ; margin:32px 10px 40px 9px; padding:10px; ';    ///////////////////////////////////////////////////////////////
    liEle.setAttribute("class","liEle");
    itemDivEle.setAttribute("class", "text-item");
    itemDivEle.style.height="auto";
    itemDivEle.style.fontSize="13pt";
    liEle.appendChild(itemDivEle);

    for (var j = 0; j < sentsObj.length; j++) {//the numbers of sents
        //<li>标签的复制包含子元素
        eleCopy = liEle.cloneNode(true);
        var words= [];//存放每个句子中字的数量
        var dEle=document.createElement("div");//
        var dEle0=document.createElement("div");//原始分词结果仅供观看的句子
        var nmb=document.createElement("div");////使得下个div另起一行
        var nmba=document.createElement("div");//使得下个div另起一行
        var btn = document.createElement("button");//添加回退按钮
        btn.setAttribute("class","btn btn-info btn-lg");
        btn.setAttribute("id",j);//设置btn的id ，根据此id 可以重新方便的写回退功能
        btn.textContent = "回退";
        dEle0.setAttribute("class","text-class");
        dEle.setAttribute("class","well-well-sm");

        //保证句子的词内联排列，动态根据框架的大小而变化
        dEle.style.cssText='border:1px solid #ccc;display:inline-block;margin-top:8px';
        dEle0.style.cssText='border-bottom:1px solid #9d9d9d;border-left : 3px solid #0099cc ;display:inline-block';
        eleCopy.appendChild(dEle0);//展示的句子
        eleCopy.appendChild(nmb); //使得下个div另起一行
        eleCopy.appendChild(dEle);//修改的句子
        eleCopy.appendChild(nmba);//使得下个div另起一行
        eleCopy.appendChild(btn);//添加回退按钮
        eleCopy.firstChild.setAttribute("y", j);

        if ('tagedSeg' in sentsObj[0])
            seg=sentsObj[j].tagedSeg;
        else
            seg=sentsObj[j].originSeg;

        //调用getSentent方法，将分词拼接成字符串句子
        var sentent = getSentent(seg);
        var textNode = document.createTextNode([ "句子", returnAnalysisRst[j].id, ":", sentent].join(""));
        eleCopy.firstChild.appendChild(textNode);
        parentContainer.appendChild(eleCopy);



        //!!!!!!标注后的分词结果输出(仅供展示)
        //给每个字富裕div字块，每个词赋予div词块， div词块的监听在下个函数
        //对每个词块进行判断是否为一个字
        for(var m=0;m<seg.length; m++){
            var box=document.createElement("div");
            box.style.cssText='border:1px solid #ddd;float:left';
            var speechEle=document.createElement("div");
            speechEle.style.fontSize = "12pt";
            speechEle.appendChild(document.createTextNode(seg[m].pos));
            Container0=document.createElement("div");
            Container0.setAttribute("class","panel");
            Container0.style.cssText='border:1px solid #ccc;';
            Container0.style.float="left";
            Container0.style.marginLeft="25px";
            Container0.style.marginRight="26px";
            Container0.style.marginTop="7px";
            Container0.style.marginBottom="2px";
            Container0.style.fontSize="23pt";
            text0 = document.createTextNode(seg[m].cont);
            Container0.appendChild(text0);
            box.appendChild(Container0);
            box.appendChild(speechEle);
            dEle0.appendChild(box);
        }

        //!!!!!!标注后的分词结果输出(仅供修改)
        for (var k = 0; k < seg.length; k++) {
            //给词性节点赋予词性值
            var cxEle = document.createElement("div");
            var bigCon = document.createElement("div");//存放词和词性的大div
            bigCon.setAttribute("class","bigCon");
            bigCon.style.cssText='border:1px solid #ddd;float:left';
            cxEle.style.fontSize = "12pt";
            cxEle.appendChild(document.createTextNode(seg[k].pos));

            ////对每个词块进行判断是否为一个字 如果大于1个字把div字块塞入div词块
            if (seg[k].cont.length > 1) {
                Container=document.createElement("div");
                //.panel-panel-default的css在init.css里
                Container.setAttribute("class","panel-panel-default");
                Container.style.float="left";
                Container.style.marginLeft="25px";
                Container.style.marginRight="25px";
                Container.style.marginTop="7px";
                Container.style.marginBottom="2px";
                //检查标红
                var count=0;
                for (var i = 0; i < set[j].length; i++) {
                    if (set[j][i].cont == seg[k].cont && set[j][i].startIndex == words.length) {
                        count++;
                        break;
                    }
                }
                    if(count==0) {
                        Container.style.color = 'red';
                        cxEle.style.color = "red";
                    }
                    if(count==1&&set[j][i].pos != seg[k].pos)
                            cxEle.style.color = "red";

                //b数组存放一个词包含的字，wordlist数组存放所有的字，将div字块塞入div词块
                var  b = seg[k].cont.split("");
                for (var l = 0; l < b.length; l++) {
                    wordList.push(b[l]);
                    words.push(b[l]);
                    divEle = document.createElement("div");
                    text = document.createTextNode(b[l]);
                    divEle.appendChild(text);
                    Container.appendChild(divEle);
                    var s = wordList.length - 1;
                    divEle.setAttribute("id", "dragEle" + s);
                    divEle.setAttribute("draggable", "true");
                    divEle.style.float = "left";
                    divEle.style.height="34px";
                    divEle.setAttribute("class","drag");
                    divEle.style.fontSize="23.0pt";
                    bigCon.appendChild(Container);
                    bigCon.appendChild(cxEle);
                    dEle.appendChild(bigCon);
                }
            }
            //一个字就是单独的div词块
            else if (seg[k].cont.length == 1) {
                Container = document.createElement("div");
                Container.setAttribute("class","panel-panel-default");
                Container.style.float="left";
                Container.style.marginLeft="25px";
                Container.style.marginRight="25px";
                Container.style.marginTop="7px";
                Container.style.marginBottom="2px";
                //检查标红
                var count=0;
                for (var i = 0; i < set[j].length; i++) {
                    if (set[j][i].cont == seg[k].cont && set[j][i].startIndex == words.length) {
                        count++;
                        break;
                    }
                }
                    if(count!=1) {
                        Container.style.color = 'red';
                        cxEle.style.color = "red";
                    }
                    if(count==1&&set[j][i].pos != seg[k].pos)
                            cxEle.style.color = "red";

                wordList.push(seg[k].cont);
                words.push(seg[k].cont);
                divEle = document.createElement("div");
                text = document.createTextNode(seg[k].cont);
                divEle.appendChild(text);
                var e = wordList.length - 1;
                divEle.setAttribute("id", "dragEle" + e);
                divEle.setAttribute("draggable", "true");
                divEle.style.float = "left";
                divEle.setAttribute("class","drag");
                divEle.style.height="34px";
                divEle.style.fontSize="23.0pt";
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
listen=function () {
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
    $(".panel-panel-default").on('drop',function (event) { //$("#div)[0] 将jquery对象转化为dom对象  $(dom对象)：即dom对象转化为jquery对象
        worddrop(event);
        event.preventDefault();
    });
    $(".drag").on("dragstart" , function (event) {

        event.originalEvent.dataTransfer.setData("Text", event.currentTarget.id);
    });
    $(".drag").on("mouseover",function () {   //mouse on the ele
        this.style.cursor = "pointer";   //style="cursor:pointer"   手型鼠标；
    });
    $(".bigCon").on("dragover",function (event) {

        event.preventDefault() ;
    });
    //包含词和词性的整体的监听，drop事件：只允许词性放置
    $(".bigCon").on("drop",function (event) {
        speechdrop(event);
    });
    //回退按钮，删除句子，重新绘制原始句子
    $(".btn.btn-info.btn-lg").on("click",function () {
        var sum=0;
        var num = Number(this.getAttribute("id"));
        //计算当前句子之前的句子中的所有的字的数量，方便给将要绘制的句子中的字给id中的数字
        //计算已经有多少个字
        for (var i = 0;i<num;i++){
            if('tagedSeg' in returnAnalysisRst[i])
                for(var k = 0 ;k < returnAnalysisRst[i].tagedSeg.length;k++){
                    sum+=returnAnalysisRst[i].tagedSeg[k].cont.length;
                }
            else {
                for (var k = 0; k < returnAnalysisRst[i].originSeg.length; k++) {
                    sum += returnAnalysisRst[i].originSeg[k].cont.length;
                }
            }
        }
        //删除当前要回退的句子
        $(this.previousSibling.previousSibling).remove();
        //再次绘制分词器给我的句子
        drawsen(num,returnAnalysisRst[num],sum);
    });
};

//词性drop
speechdrop = function (event) {
    var id = event.originalEvent.dataTransfer.getData("Text");
    //若放置的是字，直接函数返回
    if (id.slice(0,7)=="dragEle") {
        return ;
    }
    //若放置的是词性div，则修改词性
    event.currentTarget.childNodes[1].textContent=$("#"+id)[0].textContent;
    event.currentTarget.childNodes[1].style.color="red";
};

//外部监听函数，即除了句子之外的监听
outerlisten =function () {
    //词性拖动监听
    $(".label-label-primary").on("dragstart",function (event) {
        event.originalEvent.dataTransfer.setData("Text", event.target.id);
    });

    //点击修改词性
    $("#label-explanation-response-btn").on("click",function () {
        $("#label-explanation-panel-one").show();
        $("#label-explanation-panel-two").show();
        $("#label-explanation-response-btn").hide();
        $("#label-explanation-back-btn").hide();
        $("#label-explanation-check-btn").hide();
        $("#label-explanation-send-btn").hide();
    });
    //关闭按钮
    $(".btn.btn-default.btn-xs").on("click",function () {
        $("#label-explanation-panel-one").hide();
        $("#label-explanation-panel-two").hide();
        $("#label-explanation-response-btn").show();
        $("#label-explanation-back-btn").show();
        $("#label-explanation-check-btn").show();
        $("#label-explanation-send-btn").show();
    });




    //检查结果发送，post请求
    $("#send-check-rlt").on("click",function (){
        var result=[];
        var j=0;
        //遍历每个句子
        $(".well-well-sm").each(function () {
            var flag=true;
            var i=0;
            var sendSen=[];
            //遍历每个句子的每个词块
            console.log(this);
            $(this).children().each(function () {
                if(this.firstChild.textContent!="") {
                    var temp = {};
                    temp.id = i;
                    temp.cont = this.firstChild.textContent;
                    temp.pos = this.lastChild.textContent;
                    //检查跟初始数据有木有不同，有不同，给flag赋值false
                    if (!(temp.cont===returnAnalysisRst[j].tagedSeg[i].cont&&temp.id===returnAnalysisRst[j].tagedSeg[i].id&&temp.pos===returnAnalysisRst[j].tagedSeg[i].pos))
                        flag=false;
                    i++;
                    sendSen.push(temp);
                }
            });
            var compSen={};

            compSen.id=returnAnalysisRst[j].id;
            compSen.tag=sendSen;
            if (flag==false)
                compSen.checkStatus=1;
            else if (flag==true)
                compSen.checkStatus=2;
            j++;
            result.push(compSen);
        });
        var zhongji={};
        zhongji.adminName=returnObj.adminName;
        zhongji.method="checktag";
        zhongji.tag=result;
        console.log(zhongji);

        $.ajax({
            url : targetURL,
            type : "post",
            dataType:"text",
            contentType:"application/json;charset=utf-8",
            crossDomain: true,
            data:JSON.stringify(zhongji),
            timeout : 10000 ,
            success : function (returnVal) {
                returnObj=JSON.parse(returnVal);
                returnAnalysisRst=returnObj.result;
                console.log(returnAnalysisRst);
                if(returnAnalysisRst.length==0) {
                    alert("没数据了");
                    var parentContainer = document.getElementById("analysisContent");
                    while (parentContainer.childNodes.length > 0)
                        parentContainer.removeChild(parentContainer.lastChild);

                }
                else{
                    initdom(DRAW_PARENT_ID,returnAnalysisRst);
                    $('body').scrollTop(0);
                    /*outerlisten();*/
                }

            }
        });
       
    });

};

//字drop
worddrop=function (event) {

    var id = event.originalEvent.dataTransfer.getData("Text");
    //如果拖拽的是词性div则阻止默认事件发生，触发上层的bigCon绑定的监听的事件：即词性drop
    if(id.slice(0,7)!="dragEle")
        return false;

    var end=Number(id.slice(7));//拖拽的字的id中的数字
    //左移 用被拖拽的字的id数字与放置的词的末子元素的id数字比较，将这中间的字块 全部添加到词的末尾
    if(Number(id.slice(7))>Number($(event.currentTarget).children("div:last-child").attr("id").slice(7))) {
        var begin=Number($(event.currentTarget).children("div:last-child").attr("id").slice(7));
        document.getElementById(id).parentNode.style.color = "red";
        for(var i=begin+1;i<end+1;i++){
            (event.currentTarget).appendChild(document.getElementById("dragEle"+i));
            event.currentTarget.style.color ="red";
        }
        //如果目标元素的父亲节点为空则删除空的div词节点的父节点
        $(".panel-panel-default").each(function () {
            if(this.textContent=="")
                $(this.parentNode).remove();
        });
    }
    //右移 用被拖拽的字的id数字与放置的词的第一个子元素的id数字比较，将这中间的字块 全部添加到词块的开头
    else if(Number(id.slice(7))<Number($(event.currentTarget).children("div:first-child").attr("id").slice(7))){
        var begin=Number($(event.currentTarget).children("div:first-child").attr("id").slice(7));
        document.getElementById(id).parentNode.style.color = "red";
        for(var i=begin-1;i>end-1;i--){
            $(event.currentTarget).prepend($("#dragEle"+i));
            event.currentTarget.style.color ="red";
        }
        //如果目标元素的父亲节点为空则删除空的div词节点的父节点
        $(".panel-panel-default").each(function () {
            if(this.textContent=="")
                $(this.parentNode).remove();
        });
    }
    event.preventDefault();
};

//对词进行双击事件的监听，双击将词内的字全部分开，单独成词，同时赋予词应该有的监听事件,以及包含词和词性的大div 应该有的监听事件
dblclickAction=function (event) {
    console.log(event);
    var num = $(event.currentTarget).children().length;   //number of words
    for (var y = 0; y < num - 1; y++) {
        var Container = document.createElement("div");
        var bigCon = document.createElement("div");
        bigCon.setAttribute("class","bigCon");
        bigCon.style.cssText="border:1px solid #ddd ;float:left";
        var cixEle = document.createElement("div");
        cixEle.appendChild(document.createTextNode("LW"));
       /* cixEle.style.color="red";*/
        cixEle.style.fontSize = "12pt";
        Container.setAttribute("class", "panel-panel-default");
        Container.style.float = "left";
        Container.style.marginLeft = "25px";
        Container.style.marginRight = "25px";
        Container.style.marginTop="7px";
        Container.style.marginBottom="2px";
        Container.style.color = "red";
        Container.appendChild(event.currentTarget.childNodes[0]);
        bigCon.appendChild(Container);
        bigCon.appendChild(cixEle);
        //创建一个div词块，将每个字放入依次放入词块中
        event.currentTarget.parentNode.parentNode.insertBefore(bigCon, event.currentTarget.parentNode);
        //监听事件
        $(bigCon).on('dragover',function (event) {
            event.preventDefault();     //  preventDefault() 方法阻止元素发生默认的行为（例如，当点击提交按钮时阻止对表单的提交）。
        });
        $(bigCon).on('drop',function (event) {
            speechdrop(event);
        });
        $(Container).on('dblclick',function (event) {
            dblclickAction(event);
        });
        $(Container).on('dragover', function (event) {
            event.preventDefault();
        });
        $(Container).on ('drop' , function (event) {
            worddrop(event);
        });
    }
    event.currentTarget.style.color="red";
};

