


//render page and button if certificate create
if (status_cert == "True") {
    console.log("THIS is STATUS - "  + status_cert);
    var download_button = document.getElementById('div_download_certificate')
    download_button.style.display = 'block'
    getFile()

}
//save changing user inforttion  and exit
$("#save_and_exit").click(function() {
    var serdata = $("#save_edit_hotel_form").serialize();
    $.ajax({
        url: "/vpn/hotel/save_edit_hotel_form/",
        data: serdata,
        type: 'post',
        success: function(response) {
            $("#save_edit_hotel_form").focus();
            result = JSON.parse(JSON.stringify(response["result"]));
            smoke.alert(result);
            document.location.href = "/vpn/hotel/"
            return false;
        },
        error: function (response) {
            $("#label_server_status").trigger('reset');
            // smoke.alert the error if any error occured
            smoke.alert(JSON.stringify(response["responseJSON"]["error"]));
        }
    });
});
//delete hotel certificate and record in database
$("#delete_hotel").click(function() {
    smoke.confirm("Are you sure delete hotel?", function (result){
        if(result ===false) return ;
        var serdata = $("#save_edit_hotel_form").serialize();
        $.ajax({
            url: "/vpn/hotel/delete_hotel/",
            data: serdata,
            type: 'post',
            success: function (response) {
                $("#save_edit_hotel_form").focus();
                result = JSON.parse(JSON.stringify(response["result"]));
                smoke.alert(result, function (){document.location.href = "/vpn/hotel/"});
            },
            error: function (response) {
                $("#label_server_status").trigger('reset');
                // smoke.alert the error if any error occured
                smoke.alert(JSON.stringify(response["responseJSON"]["error"]));
            },
        });
    });
});


// create certificate
$("#create_certificate").click(function() {
    smoke.confirm("Create certificate?", function (answer) {
    if (answer === false) return;
    var serdata = $("#save_edit_hotel_form").serialize();
        console.log("CREATE")
        $.ajax({
            url: "/vpn/hotel/create_hotel_certificate/",
            data: serdata,
            type: 'post',
            success: function (response) {

                $("#save_edit_user_form").focus();
                result = JSON.parse(response["data"]);
                if (result["result"] === false) {
                    var download_button = document.getElementById('div_download_certificate');
                    download_button.style.display = 'block';
                    smoke.alert('Certificate exist');
                }
                if (result["result"] === true) {
                    console.log(result["date"])
                    getFile()
                    smoke.alert("Certificate created");
                    var download_button = document.getElementById('div_download_certificate');
                    download_button.style.display = 'block';
                    document.getElementById('cert_exist').textContent = ("Certificate exist: True");
                    document.getElementById('cert_date').textContent = ("Date of creation: " + result["date"]);
                    console.log(result);
                }
            },
            error: function (response) {
                $("#label_server_status").trigger('reset');
                // smoke.alert the error if any error occured
                smoke.alert(JSON.stringify(response["responseJSON"]["error"]));
            }
        });
    });
});


// copy certificate to server
$("#copy_cert_button").click(function() {
    ip_question = document.getElementById("id_hotel_ip_address").value;
    port_question = document.getElementById("id_hotel_port").value;
    smoke.confirm("Do you want sent certificate to host\n\n" + "ip address: " + ip_question, function (result){
        if(result ===false) return;
        var serdata = $("#save_edit_hotel_form").serialize();
        $.ajax({
            url: "/vpn/hotel/copy_certificate_to_host/",
            data: serdata,
            type: 'post',
            success: function (response) {

                $("#save_edit_hotel_form").focus();
                result = JSON.stringify(response["result"]);
                if (result == "true") {
                    smoke.alert('certificate copied to server')
                }
                if (result == "false") {
                    smoke.alert("Cannot connect to server");
                }
            },
            error: function (response) {
                $("#copy_cert_to_host").trigger('reset');
                // smoke.alert the error if any error occured
                smoke.alert(JSON.stringify(response["responseJSON"]["error"]));
            }
        });
    });
 });




// This method send request to server, receive file object (certificate) and create link for download.
async function getFile() {
    checkForm = new FormData(document.getElementById("save_edit_hotel_form"));
    let response = await fetch('/vpn/hotel/getFile/', {
        method: 'POST',
        body: checkForm
    });
    if (response.ok) {
        let data = await response.text();
        certName = document.getElementById("id_hotel_name_certification").value
        document.getElementById("download").download = certName + ".conf"
        let type = 'data:application/octet-stream;base64, ';
        let text = data
        let base = btoa(unescape(encodeURIComponent(text)));
        let res = type + base;
        document.getElementById('download').href = res;
    }
    else {
        smoke.alert("<h5>Server have not found certificate, press button 'Create certificate'</h5>")

        }

}



