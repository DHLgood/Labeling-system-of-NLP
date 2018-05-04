targetURL ="http://10.1.11.18:8914/nlp/segment";
var returnAnalysisRst = null ;
var returnObj=null;
var myname = 'lmy';

// global json object storing the ltp server return va
$(document).ready(function () {
	 //-----main view-----
     $.ajax({
         url : targetURL,
         type : "get",
         dataType:"text",
        // data:JSON.stringify(test2),
         //contentType:"application/json;charset=utf-8",
         data : {method:"loadseg",adminName:myname},
         crossDomain: true,
         timeout : 10000 ,
         success : function (returnVal) {
             console.log(JSON.parse(returnVal));
             console.log(JSON.parse(returnVal).result);
             outerlisten();
             returnObj = JSON.parse(returnVal);
             returnAnalysisRst = JSON.parse(returnVal).result;

             if (returnAnalysisRst == false)
                 alert("没数据了");
             else
                 initdom(DRAW_PARENT_ID, returnAnalysisRst);
      }
    });

$("#analysisContent").on('click','.bigCon',function(event){
    console.log("dnasdas");
}
);
});
    




