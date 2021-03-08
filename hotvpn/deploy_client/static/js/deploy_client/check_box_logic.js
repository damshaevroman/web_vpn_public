// POST data to Django server


$('#dhcp_checkbox').change(function () {
        if(this.checked){
            $("#dhcp_div").show();
            $("#dhcp_int").show();
        } else {
            $("#dhcp_div").hide();
            $("#dhcp_int").hide();
        }

    });

    $('#git_hadmin').change(function () {
        if(this.checked){
            $("#git_div").show();
            $("#gitDownload").show();
        } else {
            $("#git_div").hide()
            $("#gitDownload").hide()
        }

    });

     $('#git_pdaemondaemon').change(function () {
        if(this.checked){
            $("#git_div").show();
            $("#gitDownload").show();
        } else {
            $("#git_div").hide()
            $("#gitDownload").hide()
        }

    });




    $('#hostname_checkbox').change(function () {
        if(this.checked){
            $("#div_hostname").show();
        } else {
            $("#div_hostname").hide()
        }

    });




