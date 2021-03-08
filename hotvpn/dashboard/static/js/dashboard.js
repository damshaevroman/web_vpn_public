var isStopped = false
//This function count of created hotels and user sertifications
function get_hotel_data(){
    isStopped = true
    var request = new XMLHttpRequest();
    request.open('GET', '/dashboard/counter_members/', true);
    request.onload = function (){
        if (this.status >=200 && this.status < 400) {
            var count_data = JSON.parse(this.response);
            document.getElementById("count_hotels").innerText= count_data.count_context.count_hotel;
            document.getElementById("count_users").innerText= count_data.count_context.count_user;
            document.getElementById("active_hotels").innerText= count_data.count_context.count_ping_active;
            document.getElementById("lost_hotels").innerText= count_data.count_context.count_ping_lost;
            isStopped = false
        }
    };
    request.send();
}
// This Function ajax reqest to server GET status of unavaible ping vpn hosts and host without vpn addresses
check_non_ip_hotels()
function check_non_ip_hotels(){
    isStopped = true
    var request = new XMLHttpRequest();
    request.open('GET', '/dashboard/check_non_ip_host/', true);
    request.onload = function (){
        if (this.status >=200 && this.status < 400) {
            var count_data = JSON.parse(this.response);
            var non_ip_vpn = JSON.parse(count_data.count_context)
            var list_unavailible_host = JSON.parse(count_data.list_unavailible_host);
            document.getElementById("non_ping_hotel").innerHTML = "";
            document.getElementById("table_hosts_without_ip").innerHTML = "";
            var table_non_ip_vpn = document.getElementById('table_hosts_without_ip');
            var table_list_unavailible_host = document.getElementById('non_ping_hotel');
            // no ip address hosts
            var tr_non_ip = document.createElement('tr')
            var td_id_hotel = document.createElement('td');
            var td_name_hotel = document.createElement('td');
            var ip_address = document.createElement('td');
            var edit_hotel = document.createElement('td');
            td_name_hotel.innerHTML = '<h6 class="m-0 font-weight-bold text-primary">Hotel name</h6>';
            td_id_hotel.innerHTML ='<h6 class="m-0 font-weight-bold text-primary">Hotel ID</h6>';
            ip_address.innerHTML ='<h6 class="m-0 font-weight-bold text-primary">VPN IP</h6>';
            edit_hotel.innerHTML ='<h6 class="m-0 font-weight-bold text-primary">Edit Hotel</h6>';

            tr_non_ip.appendChild(td_id_hotel);
            tr_non_ip.appendChild(td_name_hotel);
            tr_non_ip.appendChild(ip_address);
            tr_non_ip.appendChild(edit_hotel);

            table_non_ip_vpn.appendChild(tr_non_ip);

             // this is block add records to table "hosts_without_ip"

            non_ip_vpn.forEach(function (item) {
                console.log(item.hotel_admin_id)
                var tr = document.createElement('tr');
                var td_id_hotel = document.createElement('td');
                var td_name_hotel = document.createElement('td');
                var td_nonvpn_hotel = document.createElement('td');
                var td_edit_hotel = document.createElement('td');
                td_id_hotel.innerHTML = item.fields.hotel_admin_id;
                td_name_hotel.innerHTML = item.fields.hotel_name;
                td_nonvpn_hotel.innerHTML = item.fields.hotel_vpn_ip_address;
                td_edit_hotel.innerHTML = '<a href=/vpn/hotel/edit_hotel/' + item.pk + '>Edit</a>'
                tr.appendChild(td_id_hotel);
                tr.appendChild(td_name_hotel);
                tr.appendChild(td_nonvpn_hotel);
                tr.appendChild(td_edit_hotel);
                table_non_ip_vpn.appendChild(tr);

            });


            // no ping hosts
            var tr_non_availible = document.createElement('tr')
            var td_id_hotel = document.createElement('td');
            var td_name_hotel = document.createElement('td');
            var td_vpn_address_hotel = document.createElement('td');
            td_name_hotel.innerHTML = '<h6 class="m-0 font-weight-bold text-primary">Hotel name</h6>';
            td_id_hotel.innerHTML ='<h6 class="m-0 font-weight-bold text-primary">Hotel ID</h6>';
            td_vpn_address_hotel.innerHTML ='<h6 class="m-0 font-weight-bold text-primary">VPN address</h6>';
            tr_non_availible.appendChild(td_id_hotel);
            tr_non_availible.appendChild(td_name_hotel);
            tr_non_availible.appendChild(td_vpn_address_hotel);
            table_list_unavailible_host.appendChild(tr_non_availible);

            // this is block add records to table "non_ping_hotel"
            list_unavailible_host.forEach(function (item){
                    var tr = document.createElement('tr');
                    var td_id_hotel = document.createElement('td');
                    var td_name_hotel = document.createElement('td');
                    var td_vpn_adress = document.createElement('td');
                    td_id_hotel.innerHTML = item.fields.hotel_admin_id;
                    td_name_hotel.innerHTML = item.fields.hotel_name;
                    td_vpn_adress.innerHTML = item.fields.hotel_vpn_ip_address;
                    tr.appendChild(td_id_hotel);
                    tr.appendChild(td_name_hotel);
                    tr.appendChild(td_vpn_adress)
                    table_list_unavailible_host.appendChild(tr);

            isStopped = false
            });
        }
    };
    request.send();
}



// This is function get from server information about cou and memory utilization
server_status()
    function server_status(){
        var request = new XMLHttpRequest();
        request.open('GET', '/dashboard/server_status/', true);
        request.onload = function (){
            if (this.status >=200 && this.status < 400) {
                var data = JSON.parse(this.response);
                server = JSON.parse(data["server_status"]);
                cpu = JSON.parse(data["cpu2"])
                memory_availble = server.memory_availble;
                cpu_freq = server.cpu_freq;
                if (server.cpu_utilization < 50){
                    document.getElementById("cpu_utilization").className = "progress-bar bg-success"
                }
                if(server.cpu_utilization > 50 && server.cpu_utilization < 90){
                    document.getElementById("cpu_utilization").className = "progress-bar bg-warning"
                }
                if (server.cpu_utilization > 90){
                    document.getElementById("cpu_utilization").className = "progress-bar bg-danger"
                }

                if (server.memory_percent < 50){
                    document.getElementById("memory_utilization").className = "progress-bar bg-success"
                }
                if(server.memory_percent > 50 && server.cpu_utilization < 90){
                    document.getElementById("memory_utilization").className = "progress-bar bg-warning"
                }
                if (server.memory_percent > 90){
                    document.getElementById("memory_utilization").className = "progress-bar bg-danger"
                }
                cpu_utilization = String(server.cpu_utilization) + "%";
                memory_utilization = String(server.memory_percent) +"%";

                document.getElementById("cpu_percent").innerText = cpu_utilization;
                document.getElementById("cpu_utilization").style.width = cpu_utilization;
                document.getElementById("memory_utilization").style.width = memory_utilization;
                document.getElementById("memory_percent").innerText = memory_utilization;
            }
        };
        request.send();
    };


setInterval( function (){
    server_status()
    if(isStopped == false){
        get_hotel_data()
        check_non_ip_hotels()
    }

  },10000)


window.onload = get_hotel_data
