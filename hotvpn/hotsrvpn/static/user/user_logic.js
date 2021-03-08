function loadTable (userArray) {
     $('#userTable').dataTable({
                data: userArray,
                "dom": 'fltip',
                "columns":[
                    {data: "user_city"},
                    {data: "organisation"},
                    {data: "user_fio"},
                    {data: "user_cert"},
                    {data: "user_date_of_creation_certificate"},
                    {data: "editUser"}
                     ],
                 });
    document.getElementById("userTable_filter").style.textAlign = "left";
    document.getElementById("userTable_length").style.textAlign = "right";
}

function get_user_json(){
    var request = new XMLHttpRequest();
    request.open('GET', '/vpn/user/get_json/', true);
    request.onload = function (){
        if (this.status >=200 && this.status < 400) {
            var user_data = JSON.parse(this.response);
            let userArray = [];
            user_data.forEach(function (item){
                editValue = '<a href=edit_user/'+ item.id + '>edit user</a>'
                item["editUser"] = editValue
                userArray.push(item)
            });
            loadTable(userArray)

        }
    };
    request.send();
}

async function createUser() {
    checkForm = new FormData(document.getElementById("form_user"));
    let response = await fetch('/vpn/user/create_user/', {
        method: 'POST',
        body: checkForm
    });
    if (response.ok) {
        let user_data = await response.json();
        smoke.alert('<h5>User added</h5>');
        document.getElementById("form_user").reset();
        hide_form();
        $("#userTable").dataTable().fnDestroy();
        let userArray = [];
        user_data.forEach(function (item){
                editValue = '<a href=edit_user/'+ item.id + '>edit user</a>'
                item["editUser"] = editValue
                userArray.push(item)
            });
        console.log(userArray)
        loadTable(userArray)
    }
    else {
        response.json().then(function (data) {
            let backErros = '<h5>Fix errors</h5>\n'
            for (const [key, value] of Object.entries(data)) {
                backErros = backErros + `<h6> ${key}: ${value} </h6>`
            }
            smoke.alert(backErros)
        });
    }
}

function show_form() {
      var show_form = document.getElementById("create_form");
      show_form.style.display = "block";
      var show_form_button = document.getElementById("show_form_button");
      var hide_form_button = document.getElementById("hide_form_button");
      show_form_button.style.display = "none";
      hide_form_button.style.display = "block";
 }
 function hide_form() {
      var show_form = document.getElementById("create_form");
      show_form.style.display = "none";
      var show_form_button = document.getElementById("show_form_button");
      var hide_form_button = document.getElementById("hide_form_button");
      show_form_button.style.display = "block";
      hide_form_button.style.display = "none";
 }

window.onload = get_user_json
