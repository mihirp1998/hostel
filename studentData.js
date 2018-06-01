var studentName="HRISHIKESH URALATH";
var blockNum="D";
var roomNum="519";
var idNum="2016AAPS0202U";
var amount="50.0";

var docName = document.getElementById("name");
var docblock = document.getElementById("blockNum");
var docRoom = document.getElementById("roomNo");
var docID = document.getElementById("idNum");
var editBut = document.getElementById("Edit").onclick= function(){ myFunction(); };
var docAmount = document.getElementById("amount");
var saveBut = document.getElementById("Save");
var editDate = document.getElementById("editDate");

/*docName.value=studentName;
docblock.value=blockNum;
docRoom.value=roomNum;
docID.value=idNum;
docAmount.value=amount;*/

docName.readOnly=true;
docblock.readOnly=true;
docRoom.readOnly=true;
docID.readOnly=true;
docAmount.readOnly=true;

saveBut.disabled=true;


function myFunction() {
    docName.readOnly=false;
    docblock.readOnly=false;
    docRoom.readOnly=false;
    docID.readOnly=false;
    docAmount.readOnly=false;

    saveBut.disabled=false;
    editBut.disabled=true;
}


saveBut.onclick=function(){
    studentName= docName.value.toUpperCase();
    blockNum=docblock.value.toUpperCase();
    roomNum=docRoom.value;
    idNum=docID.value.toUpperCase();
    amount=docAmount.value;
    $.post("http://localhost:5000/dataSave",{s:studentName,b:blockNum,r:roomNum,i:idNum})
    console.log(studentName);
    console.log(blockNum);
    console.log(roomNum);
    console.log(idNum);
    console.log(amount);

    editBut.disabled=false;
    saveBut.disabled=true;

    docName.readOnly=true;
    docblock.readOnly=true;
    docRoom.readOnly=true;
    docID.readOnly=true;
    docAmount.readOnly=true;

    
}

