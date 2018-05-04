/**
 * Created by Administrator on 2016/8/24.
 */
targetURL ="http://10.1.11.18:8914/nlp/segment";
var returnAnalysisRst = null ;
var returnObj=null;
var myname = 'lmy';
var set = [];

$(document).ready(function () {
    //-----main view-----
    $.ajax({
        url : targetURL,
        type : "get",
        dataType:"text",
        // data:JSON.stringify(test2),
        //contentType:"application/json;charset=utf-8",
        data : {method:"checktag",adminName:myname},
        crossDomain: true,
        timeout : 10000 ,
        success : function (returnVal) {
            console.log(JSON.parse(returnVal));
            console.log(JSON.parse(returnVal).result);
            outerlisten();
            returnObj = JSON.parse(returnVal);
            returnAnalysisRst = returnObj.result;
            if (returnAnalysisRst.length == 0)
                alert("没数据了");
            else{
                initdom(DRAW_PARENT_ID, returnAnalysisRst);
            }
        }
    });
    /*$("#analysisContent").on('click','.bigCon',function(event){
     console.log("dnasdas");
     }
     );*/
});
    





