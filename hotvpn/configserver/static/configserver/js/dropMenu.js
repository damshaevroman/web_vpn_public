/*Dropdown Menu*/
$('.dropdown').click(function () {
        $(this).attr('tabindex', 1).focus();
        $(this).toggleClass('active');
        $(this).find('.dropdown-menu').slideToggle(300);
    });
    $('.dropdown').focusout(function () {
        $(this).removeClass('active');
        $(this).find('.dropdown-menu').slideUp(300);
    });
    $('.dropdown .dropdown-menu li').click(function () {
        $(this).parents('.dropdown').find('span').text($(this).text());
        $(this).parents('.dropdown').find('input').attr('value', $(this).attr('id'));
    });
/*End Dropdown Menu*/

$('.dropdown-menu li').click(function () {
  var input = '<strong>' + $(this).parents('.dropdown').find('input').val() + '</strong>',
      msg = '<span class="msg">Hidden input value: ';
});

// This function update text if choose file.
function updateUploadText(){
     console.log('WORk update')
     document.getElementById('labelCrt').innerText = document.getElementById("crt").value;
     document.getElementById('labelCert').innerText = document.getElementById("cert").value;
     document.getElementById('labelKey').innerText = document.getElementById("key").value;
     document.getElementById('labelDh').innerText = document.getElementById("dh").value;
     document.getElementById('labelTa').innerText = document.getElementById("ta").value;
}



async function createServer(){
    console.log("PRESS createServer")
    checkForm = new FormData(document.getElementById("serverConfigForm"));
    let response = await fetch('/configserver/createServer/', {
            method: 'POST',
            body: checkForm
        });
        if (response.ok) {
            console.log('READY')
            smoke.alert(response.ok)
            }
        else {
            let error = ''
            // document.getElementById("client_login").style.color = "red"
            let result = await response.json();
            console.log(result)
            // console.log(Object.entries(result).forEach(([key, value]) => console.log(`${key}: ${value}`)));
            Object.entries(result).forEach(function([key, value]) {
                 error =  error + '<h6 align="center">' + `${key}: ${value} ` + '</h6>'

            });
            smoke.alert('<h4>Check errors</h4>' + error)
        }
}
