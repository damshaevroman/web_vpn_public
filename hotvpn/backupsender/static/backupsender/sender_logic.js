
function start(){
    console.log(report_data)
    let succesTable = document.getElementById("successTable");
    let errorTable = document.getElementById("errorTable");
    let wrongTable = document.getElementById("wrongTable");
    addToHead(succesTable)
    addToHead(errorTable)
    addToHead(wrongTable)
    report_data.forEach(function(item) {
        console.log(item.fields)
        if (item.fields.type === "success"){
            table = succesTable
            addToTable(table, item)
        }
        if (item.fields.type === "error"){
            table = errorTable
            addToTable(table, item)
        }
        if (item.fields.type === "wrong"){
            table = wrongTable
            addToTable(table, item)
        }

    });
}

function addToTable(table, item){
        let tr = document.createElement('tr');
        let td_id_hotel = document.createElement('td');
        let td_name_hotel = document.createElement('td');
        let td_status = document.createElement('td');
        let td_date_update = document.createElement('td');
        td_id_hotel.innerHTML = item.fields.hotel_id;
        td_name_hotel.innerHTML = item.fields.hotel_name;
        td_status.innerHTML = item.fields.status;
        td_date_update.innerHTML = item.fields.date_update;
        tr.appendChild(td_id_hotel);
        tr.appendChild(td_name_hotel);
        tr.appendChild(td_status);
        tr.appendChild(td_date_update);
        table.appendChild(tr);
}


function addToHead(table){
        let tr = document.createElement('tr');
        let td_id_hotel = document.createElement('td');
        let td_name_hotel = document.createElement('td');
        let td_status = document.createElement('td');
        let td_date_update = document.createElement('td');
        td_id_hotel.innerHTML = '<h6 class="m-0 font-weight-bold text-primary" style="text-align:center">Hotel ID</h6>';
        td_name_hotel.innerHTML = '<h6 class="m-0 font-weight-bold text-primary" style="text-align:center">Hotel name</h6>';
        td_status.innerHTML = '<h6 class="m-0 font-weight-bold text-primary" style="text-align:center">Status</h6>';
        td_date_update.innerHTML = '<h6 class="m-0 font-weight-bold text-primary" style="text-align:center">Update date</h6>';
        tr.appendChild(td_id_hotel);
        tr.appendChild(td_name_hotel);
        tr.appendChild(td_status);
        tr.appendChild(td_date_update);
        table.appendChild(tr);
}

// var bool = true
// function hideShow() {
//     console.log('YOOOOOO')
//     bool = !bool
//     if (bool === false) {
//         document.getElementById("successTable").style.direction = "none"
//     }
// }
window.onload = start
