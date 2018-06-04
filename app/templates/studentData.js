var studentName="HRISHIKESH URALATH";
var blockNum="D";
var roomNum="519";
var idNum="2016AAPS0202U";
var amount="50.0";

var docName = document.getElementById("name");
var docblock = document.getElementById("blockNum");
var docRoom = document.getElementById("roomNo");
var docID = document.getElementById("idNum");
var docKey = document.getElementById("keyl");
var docTable = document.getElementById("tablel");
var docChair = document.getElementById("chairl");
var docMisc = document.getElementById("miscl");



var editBut = document.getElementById("Edit").onclick= function(){ myFunction(); };
var saveBut = document.getElementById("Save");
var editDate = document.getElementById("editDate");
$("#back").on('click',function(){window.location.assign("http://172.16.100.8:5000/next")});
/*docName.value=studentName;
docblock.value=blockNum;
docRoom.value=roomNum;
docID.value=idNum;
docAmount.value=amount;*/

docName.readOnly=true;
docblock.readOnly=true;
docRoom.readOnly=true;
docID.readOnly=true;
docKey.readOnly=true;
docTable.readOnly=true;
docChair.readOnly=true;
docMisc.readOnly=true;


saveBut.disabled=true;


function myFunction() {
    docblock.readOnly=false;
    docRoom.readOnly=false;

docKey.readOnly=false;
docTable.readOnly=false;
docChair.readOnly=false;
docMisc.readOnly=false;
    saveBut.disabled=false;
    editBut.disabled=true;
}


saveBut.onclick=function(){
    studentName= docName.value.toUpperCase();
    blockNum=docblock.value.toUpperCase();
    roomNum=docRoom.value;
    idNum=docID.value.toUpperCase();
    roomNum=docRoom.value;
    tablel=docTable.value;
    keyl=docKey.value;
    chairl=docChair.value;
    miscl=docMisc.value;
    $.post("http://172.16.100.8:5000/dataSave",{s:studentName,b:blockNum,r:roomNum,i:idNum,t:tablel,k:keyl,c:chairl,m:miscl})
    console.log(studentName);
    console.log(blockNum);
    console.log(roomNum);
    console.log(idNum);
    

    editBut.disabled=false;
    saveBut.disabled=true;
    docKey.readOnly=true;
docTable.readOnly=true;
docChair.readOnly=true;
docMisc.readOnly=true;
/*    docName.readOnly=true;
*/    docblock.readOnly=true;
    docRoom.readOnly=true;
/*    docID.readOnly=true;
*/   

    
}

