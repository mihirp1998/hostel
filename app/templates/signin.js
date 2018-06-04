function signin(){
    var x=document.getElementById('name');
    var y=document.getElementById('password');

    if(x.value=="admin"){
        if(y.value=="1234"){

             window.location.assign('http://172.16.100.8:5000/next');
    
        }

        else{
            alert("Wrong password!!");
        }
    }

    else{
        alert("Wrong username!!");
    }
}