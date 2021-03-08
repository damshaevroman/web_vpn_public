document.getElementById('install_packeges').innerText = 'nginx python3-distutils ' +
    'unzip zabbix-agent openvpn fail2ban traceroute vlc htop iftop iotop sysstat mc';
var isStopped = true;
var git_status = true;
var gitFinal = false;
var deployStopped = true;
var packages_message = document.getElementById("feedback_install_messsages")
var task_message = document.getElementById("feedback_task_messsages")



async function deployStart() {
    packages_message.innerText = "";
    task_message.innerText = "";
    isStopped = false;
    document.getElementById("start_deploy_server").style.display = "none"
    let DeployForm = new FormData(document.getElementById('FormDeploy'));
    DeployForm.append('install_packeges', document.getElementById("install_packeges").value);
    if (document.getElementById('hostname_checkbox').checked) {
        DeployForm.append('hostname', document.getElementById("hostname").value);
    }
    if (document.getElementById('dhcp_checkbox').checked) {
        let dhcpForm = new FormData(document.getElementById('dhcpForm'));
        for (let item of dhcpForm.entries()) {
            DeployForm.append(item[0], item[1])
        }
    }
    let response = await fetch('post_deploy/', {
        method: 'POST',
        body: DeployForm
    });
    if (response.ok) {
        if (document.getElementById('git_hadmin').checked || document.getElementById('git_hadmin').checked) {
            while (gitFinal != true) {
                isStopped = false;
            }
        }
        smoke.alert("<h5>Remote server installed.</h5><br>Check fail points and reboot client server");
        isStopped = true;
        document.getElementById("start_deploy_server").style.display = "block"
    } else {
        let resultError = '<h4>Check fields</h4>'
        let result = await response.json();
        for (let dataerror in result) {
            resultError = resultError + `${dataerror} - ${result[dataerror][0]}` + '<br>'
            console.log(`${dataerror} - ${result[dataerror][0]}`)
        }
        isStopped = true;
        smoke.alert(resultError)
        document.getElementById("start_deploy_server").style.display = "block"

    }
}
async function downloadGit() {
    gitList = []
    console.log('Start git');
    let gitForm = new FormData(document.getElementById('FormDeploy'));
    if (document.getElementById('git_hadmin').checked) {
        gitList.push('hadmin');
        }
    if (document.getElementById('git_pdaemondaemon').checked) {
        gitList.push('pdaemondaemon');
        }
    gitForm.append('git_checkbox', gitList);
    gitForm.append('git_login', document.getElementById('git_login').value);
    gitForm.append('git_password', document.getElementById('git_password').value);
    let response = await fetch('downloadGit/', {
        method: 'POST',
        body: gitForm
    });
    if (response.ok){
        gitFinal = true;
        git_status = true;
    }
    else{
        gitFinal = true;
        git_status = false;

    }
}

async function checkPass(){
    checkForm = new FormData(document.getElementById("FormDeploy"));
    let response = await fetch('/deploy/check_passwords/', {
            method: 'POST',
            body: checkForm
        });
        if (response.ok) {

            document.getElementById("client_login").style.color = "ForestGreen"
            document.getElementById("client_password").style.color = "ForestGreen"
            document.getElementById("client_sudo_password").style.color = "ForestGreen"
            document.getElementById("client_ip").style.color = "ForestGreen"
            document.getElementById("client_port").style.color = "ForestGreen"
            document.getElementById("check_passwords").innerHTML = "Server available"
            document.getElementById("check_passwords").style.color = "ForestGreen"
            document.getElementById("start_deploy_server").style.display = "block"
            let result = await response.json();
            console.log(result["finish"]);
            }
        else {

            document.getElementById("client_login").style.color = "red"
            document.getElementById("client_password").style.color = "red"
            document.getElementById("client_sudo_password").style.color = "red"
            document.getElementById("client_ip").style.color = "red"
            document.getElementById("client_port").style.color = "red"
            document.getElementById("check_passwords").innerHTML = "Server unavailable, check entered data and user sudo permission"
            document.getElementById("check_passwords").style.color = "red"
            let result = await response.json();
            smoke.alert(result["finish"])
        }
}

function erase_tasks(){
    fetch('/erase_Task_and_Status/', {
    method: 'GET'
})
}




function startInstall(){
    deployStart();
    if (document.getElementById('git_hadmin').checked || document.getElementById('git_hadmin').checked ){
        console.log('GIT CHECKED')
        downloadGit();
    }

}


