function loadTable (hotelArray) {
     $('#hotelTable').dataTable({
                data: hotelArray,
                "dom": 'fltip',
                "columns":[
                    {data: "hotel_admin_id"},
                    {data: "hotel_country"},
                    {data: "hotel_city"},
                    {data: "hotel_name"},
                    {data: "hotel_name_certification"},
                    {data: "hotel_ip_address"},
                    {data: "hotel_port"},
                    {data: "hotel_vpn_ip_address"},
                    {data: "hotel_vpn_port"},
                    {data: "hotel_date_of_creation_certificate"},
                    {data: "editHotel"}
                     ],
                 });
    document.getElementById("hotelTable_filter").style.textAlign = "left";
    document.getElementById("hotelTable_length").style.textAlign = "right";
}

function get_hotel_json(){
    var request = new XMLHttpRequest();
    request.open('GET', '/vpn/hotel/get_json/', true);
    request.onload = function (){
        if (this.status >=200 && this.status < 400) {
            var hotel_data = JSON.parse(this.response);
            let hotelArray = [];
            hotel_data.forEach(function (item){
                editValue = '<a href=edit_hotel/'+ item.id + '>edit hotel</a>'
                item["editHotel"] = editValue
                hotelArray.push(item)
            });
            loadTable(hotelArray)

        }
    };
    request.send();
}

async function createHotel() {
    checkForm = new FormData(document.getElementById("form_hotel"));
    let response = await fetch('/vpn/hotel/create_hotel/', {
        method: 'POST',
        body: checkForm
    });
    if (response.ok) {
        let hotel_data = await response.json();
        smoke.alert('<h5>Hotel added</h5>');
        document.getElementById("form_hotel").reset();
        hide_form();
        $("#hotelTable").dataTable().fnDestroy();
        let hotelArray = [];
        hotel_data.forEach(function (item){
                editValue = '<a href=edit_hotel/'+ item.id + '>edit hotel</a>'
                item["editHotel"] = editValue
                hotelArray.push(item)
            });
        loadTable(hotelArray)
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

window.onload = get_hotel_json


