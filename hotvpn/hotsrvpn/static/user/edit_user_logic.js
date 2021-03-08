console.log(status_cert)
if (status_cert === "True") {
    console.log("THIS is STATUS - "  + status_cert);
    var download_button = document.getElementById('div_download_certificate')
    download_button.style.display = 'block'
    getUserFile()

}


//save changing user inforttion  and exit
    $("#save_and_exit").click(function() {
        var serdata = $("#save_edit_user_form").serialize();
        $.ajax({
            url: "/vpn/user/save_edit_user_form/",
            data: serdata,
            type: 'post',
            success: function(response) {
                $("#save_edit_user_form").focus();
                result = JSON.parse(JSON.stringify(response["result"]));
                smoke.alert(result);
                document.location.href = "/vpn/user/"
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
        smoke.confirm("Are you sure delete hotel?", function (result) {
            if (result === false) return;
                var serdata = $("#save_edit_user_form").serialize();
                $.ajax({
                    url: "/vpn/user/delete_user/",
                    data: serdata,
                    type: 'post',
                    success: function (response) {
                        $("#save_edit_user_form").focus();
                        result = JSON.parse(JSON.stringify(response["result"]));
                        smoke.alert(result, function (){ document.location.href = "/vpn/user/"});
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
             var serdata = $("#save_edit_user_form").serialize();
             $.ajax({
                 url: "/vpn/user/create_user_certificate/",
                 data: serdata,
                 type: 'post',
                 success: function (response) {
                     $("#save_edit_user_form").focus();
                     result = JSON.parse(response["data"]);
                     if (result["result"] === false) {
                         console.log("отработал ТРУ");
                         var download_button = document.getElementById('div_download_certificate');
                         download_button.style.display = 'block';
                         smoke.alert('Certificate exist');
                     }
                     if (result["result"] === true) {
                          console.log(result["date"])
                         getUserFile()
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

async function getUserFile() {
checkForm = new FormData(document.getElementById("save_edit_user_form"));
let response = await fetch('/vpn/user/getUserFile/', {
    method: 'POST',
    body: checkForm
});
if (response.ok) {
    let data = await response.text();
    LinuxCertName = document.getElementById("user_cert").value
    WindowsCertName = document.getElementById("user_cert").value
    document.getElementById("download_linux").download = LinuxCertName + ".conf"
    document.getElementById("download_windows").download = WindowsCertName + ".ovpn"
    let type = 'data:application/octet-stream;base64, ';
    let text = data
    let base = btoa(unescape(encodeURIComponent(text)));
    let res = type + base;
    document.getElementById('download_linux').href = res;
    document.getElementById('download_windows').href = res;
}
else {
    smoke.alert("<h5>Server have not found certificate, press button 'Create certificate'</h5>")

    }

}


// window.onload = cert_status
