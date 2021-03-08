// That functions makes requests to django and get data about installed tasks and packages
//
const start_deploy_button = document.getElementById('start_deploy_server');

async function packages_status() {
    if (isStopped) return;

    let installedForm = new FormData()
    installedForm.append("hotel_id", document.getElementById('hotel_id').value)
    installedForm.append("csrfmiddlewaretoken", document.querySelector('[name=csrfmiddlewaretoken]').value)
    let response = await fetch('/deploy/get_status_installed_packages/', {
        method: 'POST',
        body: installedForm
    });

    if (response.ok) {
        let result = await response.json();
        result = JSON.parse(result["install_list"]);
        // console.log(result);
        result.forEach(function (item) {
            var installed = item.fields.installed;
            var non_install = item.fields.non_install;
            var task_completed = item.fields.task_completed;
            var task_non_completed = item.fields.task_non_completed;
            if (installed !== "") {
                var newlabel = document.createElement("label");
                newlabel.innerHTML = installed
                document.getElementsByTagName('body')[0].appendChild(newlabel)
                var img = document.createElement("IMG");
                img.setAttribute("src", "/static/img/ok.png");
                img.setAttribute("width", "12");
                img.setAttribute("height", "12");
                packages_message.appendChild(newlabel)
                packages_message.appendChild(img);
                packages_message.appendChild(document.createElement('br'))
            }
            if (non_install !== "") {
                var newlabel = document.createElement("label");
                newlabel.innerHTML = non_install;
                document.getElementsByTagName('body')[0].appendChild(newlabel);
                var img = document.createElement("IMG");
                img.setAttribute("src", "/static/img/fail.png");
                img.setAttribute("width", "12");
                img.setAttribute("height", "12");
                packages_message.appendChild(newlabel);
                packages_message.appendChild(img);
                packages_message.appendChild(document.createElement('br'));
            }
            if (task_completed !== "") {
                var tasklabel = document.createElement("label");
                tasklabel.innerHTML = task_completed;
                document.getElementsByTagName('body')[0].appendChild(tasklabel);
                var task_img = document.createElement("IMG");
                task_img.setAttribute("src", "/static/img/ok.png");
                task_img.setAttribute("widht", "12");
                task_img.setAttribute("height", "12");
                task_message.appendChild(tasklabel);
                task_message.appendChild(task_img);
                task_message.appendChild(document.createElement('br'));
            }
            if (task_non_completed !== "") {
                var tasklabel = document.createElement("label");
                tasklabel.innerHTML = task_non_completed;
                document.getElementsByTagName('body')[0].appendChild(tasklabel);
                var task_img = document.createElement("IMG");
                task_img.setAttribute("src", "/static/img/fail.png");
                task_img.setAttribute("widht", "12");
                task_img.setAttribute("height", "12");
                task_message.appendChild(tasklabel);
                task_message.appendChild(task_img);
                task_message.appendChild(document.createElement('br'));
            }
        });
    }
}


async function tasks_and_configs() {
    let taskData = new FormData()
        taskData.append("hotel_id", document.getElementById('hotel_id').value);
        taskData.append("csrfmiddlewaretoken", document.querySelector('[name=csrfmiddlewaretoken]').value)
    let response = await fetch('/deploy/get_process_status/', {
        method: 'POST',
        body: taskData
    });
    if (response.ok) {
        let status_bar = await response.json();
        console.log(status_bar)

        status_bar.forEach(function (item) {
            console.log(item)
            document.getElementById('process_status').style.width = String(item.status) + '%';
            document.getElementById('status_bar_text').innerText = 'deploy  ' + String(item.task);
            document.getElementById('git_bar_text').innerText = 'Download  ' + String(item.git_task);
        });
        // status_bar = JSON.parse(status_bar["result"]);
        // console.log("STATUS BAR")
        // console.log(status_bar)
        // console.log(status_bar["fields"])

    }
}



setInterval( function (){
    if(isStopped === false ){
        packages_status()
        tasks_and_configs()

    }

  },3000)

// start_deploy_button.onclick = () => {
//     isStopped = false;
// }
