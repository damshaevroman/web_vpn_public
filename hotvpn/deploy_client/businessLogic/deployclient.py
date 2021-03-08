# It is deploy_client
import json, logging, tempfile, re
import ansible_runner, paramiko
from scp import SCPClient

from deploy_client.models import Installed_packeges, Task_and_Status
from django.core import serializers
from django.db.models import F
from deploy_client.serializer import InstalledPackegesSerializer, TaskStatusSerializer

'''This class with functions witch deploy on client servers configs and pprogramm packages'''


class ConnectionDeployServer:

    def __init__(self):
        pass

    def write_status_bar(self, hotel_id, deploy_status_bar_count, packages):
        """ update status and task in database """
        try:
            write_status = Task_and_Status.objects.filter(hotel_id=hotel_id)
            write_status.update(task=packages)
            write_status.update(status=F('status') + deploy_status_bar_count)
        except Exception as error:
            logging.warning(error)

    def check_sudo_pass(self, data):
        """ check sudo passwords for access server """
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(data["client_ip"], port=int(data["client_port"]), timeout=10, username=data["client_login"],
                        password=data["client_password"])
            stdin, stdout, stderr = ssh.exec_command("sudo -l", get_pty=True, timeout=8)
            stdin.write(data["client_sudo_password"] + '\n')
            stdin.flush()
            stdout = stdout.read()
            stdout = stdout.decode("utf-8")
            if '(ALL : ALL) ALL' in stdout:
                stdin, stdout, stderr = ssh.exec_command("ls /sys/class/net/", get_pty=True, timeout=8)
                stdout = stdout.read()
                stdout = stdout.decode("UTF-8").replace('\t', ' ').replace('\r', ' ').replace('\n', ' ')
                int_data = stdout.split(' ')
                # int_data = tuple(int_data)
                int_data = list(filter(None, int_data))
                return 'OK', int_data
            else:
                return False
        except Exception as error:
            logging.warning(error)
            return False

    def data_install_packeges_field(self, install_packages):
        """ data processing install_packages"""
        install_packages = re.sub("^\s+|\n|\r|\s+$", ' ', install_packages)
        install_packages = install_packages.split()
        logging.info('install_packages update')
        return install_packages

    def create_host_config(self, client_login, client_ip, client_port, client_password, client_sudo_password):
        """ Create config host file for using with playbook """
        temp_host = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
        temp_host.write(
            client_ip + ' ansible_user=' + client_login + ' ansible_host=' + client_ip + ' ansible_port=' + client_port +
            ' ansible_password=' + client_password + ' ansible_become_pass=' + client_sudo_password +
            ' ansible_connection=paramiko ansible_python_interpreter=/usr/bin/python3')
        temp_host.seek(0)
        logging.info('Client host inventory create')
        return temp_host

    def update_server(self, temp_host):
        """Just update server"""
        try:
            with tempfile.TemporaryDirectory() as temp_dir_playbook:

                temp_sudo = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
                temp_sudo.write(
                    '---\n- hosts: all\n  gather_facts: no\n  tasks:\n  - name: Update System\n    become: yes\n    apt:  update_cache=yes')
                temp_sudo.seek(0)
                startPlaybok = ansible_runner.run(private_data_dir=temp_dir_playbook, playbook=temp_sudo.name,
                                                  inventory=temp_host.name, json_mode=True)
                playbookdata = startPlaybok.stdout
                playbookdata = playbookdata.read()

                if "ok=1" in playbookdata:
                    return 'OK'
                else:
                    return 'SUDO password incorrect'
        except Exception as error:
            logging.warning(error)
            return 'Wrong password'

    def deploy_packeges(self, temp_host, install_packages, hotel_id, deploy_status_bar_count):
        """deploy packages from list Textarea"""
        with tempfile.TemporaryDirectory() as temp_dir_playbook:
            for packages in install_packages:
                self.write_status_bar(hotel_id, deploy_status_bar_count, packages)
                temp_play = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
                temp_play.write(
                    '---\n- hosts: all\n  gather_facts: no\n  tasks:\n  - name: install ' + packages + '\n' + '    become: yes\n    apt: name=' + packages)
                temp_play.seek(0)
                startPlaybok = ansible_runner.run(private_data_dir=temp_dir_playbook, playbook=temp_play.name,
                                                  inventory=temp_host.name, json_mode=True)
                playbookdata = startPlaybok.stdout
                playbookdata = playbookdata.read()
                if "ok=1" in playbookdata:
                    try:
                        add_task_in_base = Installed_packeges()
                        add_task_in_base.installed = packages
                        add_task_in_base.hotel_id = hotel_id
                        add_task_in_base.save()
                        logging.info('installed packeges - ' + packages)
                    except Exception as error:
                        logging.warning(error)
                else:
                    try:
                        add_task_in_base = Installed_packeges()
                        add_task_in_base.non_install = packages
                        add_task_in_base.hotel_id = hotel_id
                        add_task_in_base.save()
                        logging.info('installed package - ' + packages)
                    except Exception as error:
                        logging.warning(error)

    def dhcp_deploy(self, request, temp_host, hotel_id, deploy_status_bar_count):
        """get data from front and copy config dhcp to server"""
        dhcp_network = request.POST.get("dhcp_network")
        dhcp_mask = request.POST.get("dhcp_mask")
        dhcp_range_start = request.POST.get("dhcp_range_start")
        dhcp_range_end = request.POST.get("dhcp_range_end")
        dhcp_dns = request.POST.get("dhcp_dns")
        dhcp_gateway = request.POST.get("dhcp_gateway")
        dhcp_broadcast = request.POST.get("dhcp_broadcast")
        dhcp_range = dhcp_range_start + ' ' + dhcp_range_end
        dhcp_interface = request.POST.get("dhcp_interface")
        install_packages = ['isc-dhcp-server']
        print('DHCP' + str(dhcp_broadcast))
        self.deploy_packeges(temp_host, install_packages, hotel_id, deploy_status_bar_count)
        with tempfile.TemporaryDirectory() as temp_dir_playbook:
            dest = '/etc/dhcp/dhcpd.conf'
            dhcpd = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
            dhcpd.write('subnet ' + str(dhcp_network) + ' netmask ' + str(dhcp_mask) + ' {\n' +
                        '  range ' + str(dhcp_range) + ';\n' +
                        '  option domain-name-servers ' + str(dhcp_dns) + ';\n' +
                        '  option domain-name "vpnserver.local";\n'
                        '  option subnet-mask ' + str(dhcp_mask) + ';\n'
                        '  option routers ' + str(dhcp_gateway) + ';\n' +
                        '  option broadcast-address ' + str(dhcp_broadcast) +';\n' +
                        '  default-lease-time 600;\n'
                        '  max-lease-time 7200;\n '
                        '}')
            dhcpd.seek(0)

            playbook_dhcp = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
            playbook_dhcp.write(
                '---\n- hosts: all\n'
                '  gather_facts: no\n'
                '  tasks:\n  - name: copy\n'
                '    become: yes\n    copy:\n'
                '       src: ' + dhcpd.name + '\n' + '       dest: ' + dest + '\n''       owner: root\n       group: root\n  - name: added dhcp interface\n'
                                                                       '    become: yes\n    lineinfile:\n       path: /etc/default/isc-dhcp-server\n' + '       regexp: INTERFACESv4=""\n' + '       line: ' + 'INTERFACESv4="' + dhcp_interface + '"')
            playbook_dhcp.seek(0)
            startPlaybok = ansible_runner.run(private_data_dir=temp_dir_playbook, playbook=playbook_dhcp.name,
                                              inventory=temp_host.name, json_mode=True)
            playbookdata = startPlaybok.stdout
            playbookdata = playbookdata.read()
            playbook_dhcp.close()
            dhcpd.close()
            if "ok=2" in playbookdata:
                try:
                    add_task_in_base = Installed_packeges()
                    add_task_in_base.task_completed = "dhcp server deploy"
                    add_task_in_base.hotel_id = hotel_id
                    add_task_in_base.save()
                    logging.info('dhcp config copied')
                except Exception as error:
                    logging.warning(error)
            else:
                try:
                    add_task_in_base = Installed_packeges()
                    add_task_in_base.task_non_completed = "dhcp config"
                    add_task_in_base.hotel_id = hotel_id
                    add_task_in_base.save()
                    logging.info('dhcp config non copied')
                except Exception as error:
                    logging.warning(error)

    def nginx_deploy(self, request, temp_host, hotel_id, deploy_status_bar_count):
        """copy nginx config to server"""
        client_login = request.POST.get("client_login")
        packages = "nginx config"
        self.write_status_bar(hotel_id, deploy_status_bar_count, packages)
        with tempfile.TemporaryDirectory() as temp_dir_playbook:
            dest = '/etc/nginx/sites-available/default'
            nginx = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
            nginx.write('server {\n'
                        '        listen 80 default_server;\n'
                        '        root /home/' + client_login + '/hadmin;\n'
                                                               '        index index.html index.htm index.nginx-debian.html;\n'
                                                               '        server_name _;\n'
                                                               '        location / {\n'
                                                               '                try_files $uri $uri/ =404;\n'
                                                               '        }\n}')
            nginx.seek(0)

            playbook_nginx = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
            playbook_nginx.write('---\n- hosts: all\n'
                                 '  gather_facts: no\n'
                                 '  tasks:\n'
                                 '  - name: copy\n'
                                 '    become: yes\n'
                                 '    copy:\n'
                                 '       src: ' + nginx.name + '\n'
                                                               '       dest: ' + dest + '\n'
                                                                                        '       owner: root\n'
                                                                                        '       group: root\n'
                                                                                        '       mode: "0755"\n')
            playbook_nginx.seek(0)
            startPlaybook = ansible_runner.run(private_data_dir=temp_dir_playbook, playbook=playbook_nginx.name,
                                               inventory=temp_host.name, json_mode=True)
            playbookdata = startPlaybook.stdout
            playbookdata = playbookdata.read()
            playbook_nginx.close()
            nginx.close()
            if "ok=1" in playbookdata:
                try:
                    add_task_in_base = Installed_packeges()
                    add_task_in_base.task_completed = "nginx config"
                    add_task_in_base.hotel_id = hotel_id
                    add_task_in_base.save()
                    logging.info('nginx config  copied')
                except Exception as error:
                    logging.warning(error)
            else:
                try:
                    add_task_in_base = Installed_packeges()
                    add_task_in_base.task_non_completed = "nginx config"
                    add_task_in_base.hotel_id = hotel_id
                    add_task_in_base.save()
                    logging.info('nginx config non copied')
                except Exception as error:
                    logging.warning(error)

    def crontab_deploy(self, request, temp_host, hotel_id, deploy_status_bar_count):
        """ add to crontab script"""
        packages = "crontab config"
        self.write_status_bar(hotel_id, deploy_status_bar_count, packages)

        with tempfile.TemporaryDirectory() as temp_dir_playbook:
            hotel_id = request.POST.get("hotel_id")
            client_login = request.POST.get("client_login")
            playbook_crontab = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
            playbook_crontab.write('---\n'
                                   '- hosts: all\n'
                                   '  tasks:\n'
                                   '  - cron:\n'
                                   '      name: hadmin_syn\n'
                                   '      user: ' + client_login + '\n'
                                                                   '      minute: "*/10"\n'
                                                                   '      hour: "*"\n'
                                                                   '      job: "/home/' + client_login + '/hadmin/utils/download.sh -h ' + hotel_id + ' > /dev/null"\n'
                                                                                                                                                      '  - name: Create log hadmin_sync\n'
                                                                                                                                                      '    become: true\n'
                                                                                                                                                      '    shell:\n'
                                                                                                                                                      '      cmd: echo "start" >> /var/log/hadmin_sync.log\n'
                                                                                                                                                      '  - name: Access to hadmin_sync.log\n'
                                                                                                                                                      '    become: true\n'
                                                                                                                                                      '    file:\n'
                                                                                                                                                      '      path: /var/log/hadmin_sync.log\n'
                                                                                                                                                      '      owner: ' + client_login + '\n'
                                                                                                                                                                                       '      group: ' + client_login + '\n'
                                                                                                                                                                                                                        '      mode: "775"\n'
                                                                                                                                                                                                                        '  - name: create hadmin_sync file\n'
                                                                                                                                                                                                                        '    become: true\n'
                                                                                                                                                                                                                        '    file:\n'
                                                                                                                                                                                                                        '         path: "/etc/logrotate.d/hadmin_sync"\n'
                                                                                                                                                                                                                        '         state: touch\n'
                                                                                                                                                                                                                        '         owner: ' + client_login + '\n'
                                                                                                                                                                                                                                                            '         group: ' + client_login + '\n'
                                                                                                                                                                                                                                                                                                '         mode: "775"\n'
                                                                                                                                                                                                                                                                                                '  - name: copy conf to Logrotate to server\n'
                                                                                                                                                                                                                                                                                                '    become: yes\n'
                                                                                                                                                                                                                                                                                                '    blockinfile:\n'
                                                                                                                                                                                                                                                                                                '        path: /etc/logrotate.d/hadmin_sync\n'
                                                                                                                                                                                                                                                                                                '        block: |\n'
                                                                                                                                                                                                                                                                                                '                    /var/log/hadmin_sync.log {\n'
                                                                                                                                                                                                                                                                                                '                        weekly\n'
                                                                                                                                                                                                                                                                                                '                        missingok\n'
                                                                                                                                                                                                                                                                                                '                        rotate 8\n'
                                                                                                                                                                                                                                                                                                '                        compress\n'
                                                                                                                                                                                                                                                                                                '                        delaycompress\n'
                                                                                                                                                                                                                                                                                                '                        create 640 admin admin\n'
                                                                                                                                                                                                                                                                                                '                        }')
            playbook_crontab.seek(0)
            startPlaybook = ansible_runner.run(private_data_dir=temp_dir_playbook, playbook=playbook_crontab.name,
                                               inventory=temp_host.name, json_mode=True)
            playbookdata = startPlaybook.stdout
            playbookdata = playbookdata.read()
            playbook_crontab.close()
            if "ok=6" in playbookdata:
                try:
                    add_task_in_base = Installed_packeges()
                    add_task_in_base.task_completed = "crontab config"
                    add_task_in_base.hotel_id = hotel_id
                    add_task_in_base.save()
                    logging.info('crontab copied')
                except Exception as error:
                    logging.warning(error)
            else:
                try:
                    add_task_in_base = Installed_packeges()
                    add_task_in_base.task_non_completed = "crontab config"
                    add_task_in_base.hotel_id = hotel_id
                    add_task_in_base.save()
                    logging.info('crontab config non copied')
                except Exception as error:
                    logging.warning(error)

    def systemctl_deploy(self, temp_host, hotel_id, deploy_status_bar_count):
        """add configuration sysctl on server"""
        packages = "systemctl.conf config"
        self.write_status_bar(hotel_id, deploy_status_bar_count, packages)

        with tempfile.TemporaryDirectory() as temp_dir_playbook:
            playbook_rc_local = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
            playbook_rc_local.write('---\n- hosts: all\n'
                                    '  gather_facts: no\n'
                                    '  tasks:\n'
                                    '  - name: add ti sysctl.conf\n'
                                    '    become: yes\n'
                                    '    blockinfile:\n'
                                    '        path: /etc/sysctl.conf\n'
                                    '        block: |\n'
                                    '                net.ipv4.ip_forward=1\n'
                                    '                net.ipv4.conf.all.rp_filter=0\n'
                                    '                net.ipv4.conf.default.rp_filter=0\n'
                                    '                net.ipv4.conf.all.mc_forwarding=1\n'
                                    '                net.ipv4.conf.default.mc_forwarding=1')
            playbook_rc_local.seek(0)

            startPlaybook = ansible_runner.run(private_data_dir=temp_dir_playbook, playbook=playbook_rc_local.name,
                                               inventory=temp_host.name, json_mode=True)
            playbookdata = startPlaybook.stdout
            playbookdata = playbookdata.read()
            playbook_rc_local.close()
            if "ok=1" in playbookdata:
                try:
                    add_task_in_base = Installed_packeges()
                    add_task_in_base.task_completed = "systemctl config"
                    add_task_in_base.hotel_id = hotel_id
                    add_task_in_base.save()
                    logging.info('systemctl copied')
                except Exception as error:
                    logging.warning(error)


            else:
                try:
                    add_task_in_base = Installed_packeges()
                    add_task_in_base.task_non_completed = "systemctl config"
                    add_task_in_base.hotel_id = hotel_id
                    add_task_in_base.save()
                    logging.info('systemctl config non copied')
                except Exception as error:
                    logging.warning(error)

    def rclocal_deploy(self, request, temp_host, hotel_id, uplink_interface, deploy_status_bar_count):
        """ add to server service rc.local and config"""
        packages = "rc.local config"
        dhcp_interface = request.POST.get("dhcp_interface")
        if dhcp_interface == '':
            dhcp_interface = uplink_interface
        self.write_status_bar(hotel_id, deploy_status_bar_count, packages)
        with tempfile.TemporaryDirectory() as temp_dir_playbook:
            playbook_rc_local = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
            playbook_rc_local.write('---\n'
                                    '- hosts: all\n'
                                    '  gather_facts: no\n'
                                    '  tasks:\n'
                                    '  - name: create rc.local\n'
                                    '    become: true\n'
                                    '    file:\n'
                                    '         path: /etc/rc.local\n'
                                    '         state: touch\n'
                                    '         owner: root\n'
                                    '         group: root\n'
                                    '         mode: 0755\n'
                                    '  - name: add rc.local to service\n'
                                    '    become: yes\n'
                                    '    blockinfile:\n'
                                    '        path: /etc/rc.local\n'
                                    '        marker: ""\n'
                                    '        block: |\n'
                                    '                #!/bin/bash\n'
                                    '                /etc/init.d/pdaemondaemon start\n'
                                    '                route add -net 224.0.0.0/4 dev ' + str(dhcp_interface) + '\n'
                                    '                iptables -w --table nat -A POSTROUTING -o ' + str(uplink_interface) + ' -j MASQUERADE\n'
                                    '                exit 0\n'
                                    '  - name: create rc.local service file\n'
                                    '    become: true\n'
                                    '    file:\n'
                                    '         path: /etc/systemd/system/rc-local.service\n'
                                    '         state: touch\n'
                                    '         owner: root\n'
                                    '         group: root\n'
                                    '         mode: 0755\n'
                                    '  - name: add file to system\n'
                                    '    become: yes\n'
                                    '    blockinfile:\n'
                                    '        path: /etc/systemd/system/rc-local.service\n'
                                    '        marker: ""\n'
                                    '        block: |\n'
                                    '                [Unit]\n'
                                    '                 Description=/etc/rc.local Compatibility\n'
                                    '                 ConditionPathExists=/etc/rc.local\n'
                                    '                [Service]\n'
                                    '                 Type=forking\n'
                                    '                 ExecStart=/etc/rc.local start\n'
                                    '                 TimeoutSec=0\n'
                                    '                 StandardOutput=tty\n'
                                    '                 RemainAfterExit=yes\n'
                                    '                [Install]\n'
                                    '                 WantedBy=multi-user.target\n'
                                    '  - name: enable rclocal\n'
                                    '    become: yes\n'
                                    '    shell: systemctl enable rc-local\n'
                                    '  - name: Remove blank lines blockinfile put in\n'
                                    '    become: yes\n'
                                    '    lineinfile :\n'
                                    '        path: /etc/rc.local\n'
                                    '        state: absent\n'
                                    '        regexp: "^$"\n'
                                    '  - name: Remove blank lines blockinfile put in\n'
                                    '    become: yes\n'
                                    '    lineinfile :\n'
                                    '        path: /etc/systemd/system/rc-local.service\n'
                                    '        state: absent\n'
                                    '        regexp: "^$"')
            playbook_rc_local.seek(0)
            startPlaybook = ansible_runner.run(private_data_dir=temp_dir_playbook,
                                               playbook=playbook_rc_local.name,
                                               inventory=temp_host.name, json_mode=True)
            playbookdata = startPlaybook.stdout
            playbookdata = playbookdata.read()
            playbook_rc_local.close()
            if "ok=7" in playbookdata:
                try:
                    add_task_in_base = Installed_packeges()
                    add_task_in_base.task_completed = "rc.local"
                    add_task_in_base.hotel_id = hotel_id
                    add_task_in_base.save()
                    logging.info('rc.local')
                except Exception as error:
                    logging.warning(error)

            else:
                try:
                    add_task_in_base = Installed_packeges()
                    add_task_in_base.task_non_completed = "rc.local not deploy"
                    add_task_in_base.hotel_id = hotel_id
                    add_task_in_base.save()
                    logging.info('rc.local not deploy')
                except Exception as error:
                    logging.warning(error)

        '''Change hostname of server'''

    def hostname_change(self, temp_host, data, deploy_status_bar_count):
        packages = "change hostname"

        self.write_status_bar(data["hotel_id"], deploy_status_bar_count, packages)
        with tempfile.TemporaryDirectory() as temp_dir_playbook:
            hostname = data["hostname"]
            playbook_hostname = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
            playbook_hostname.write('---\n- hosts: all\n'
                                    '  gather_facts: no\n'
                                    '  tasks:\n'
                                    '  - name: /et/cloud/cloud.cfg\n'
                                    '    become: yes\n'
                                    '    lineinfile:\n'
                                    '        path: /etc/cloud/cloud.cfg\n'
                                    '        regexp: "preserve_hostname:"\n'
                                    '        line: "preserve_hostname: true"\n'
                                    '  - name: change hostname\n'
                                    '    become: yes\n'
                                    '    shell: sudo hostnamectl set-hostname ' + hostname)
            playbook_hostname.seek(0)
            startPlaybok = ansible_runner.run(private_data_dir=temp_dir_playbook, playbook=playbook_hostname.name,
                                              inventory=temp_host.name, json_mode=True)
            playbookdata = startPlaybok.stdout
            playbookdata = playbookdata.read()
            playbook_hostname.close()
            if "ok=2" in playbookdata:
                try:
                    add_task_in_base = Installed_packeges()
                    add_task_in_base.task_completed = "hostname changed"
                    add_task_in_base.hotel_id = data["hotel_id"]
                    add_task_in_base.save()
                    logging.info('hostname copied')
                except Exception as error:
                    logging.warning(error)
            else:
                try:
                    add_task_in_base = Installed_packeges()
                    add_task_in_base.task_non_completed = "hostname did not change"
                    add_task_in_base.hotel_id = data["hotel_id"]
                    add_task_in_base.save()
                    logging.info('hostname config did not change')
                except Exception as error:
                    logging.warning(error)

    def git_load(self, temp_host, git):
        """ Download from bitbuchet directory hadmin, pdaemondaemon"""
        package = ['git']
        self.deploy_packeges(temp_host, package, git["hotel_id"], 0)
        git_list = git["git_checkbox"]
        git_list = git_list.split(',')
        git_status = Task_and_Status.objects.filter(hotel_id=git["hotel_id"])
        for task in git_list:
            git_status.update(git_task=task)
            if 'hadmin' in task:
                with tempfile.TemporaryDirectory() as temp_dir_playbook:
                    playbook_bitbucket = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
                    playbook_bitbucket.write('---\n'
                                             '- hosts: all\n'
                                             '  gather_facts: no\n'
                                             '  tasks:\n'
                                             '  - name: install hadminTV\n'
                                             '    git:\n'
                                             '      repo: "https://' + git["git_login"] + ':' + git["git_password"] + '@bitbucket.org/hadminteam/tv.git"\n'
                                             '      dest: /home/' + git["client_login"] + '/hadmin\n'
                                             '      version: develop\n' 
                                             '  - name: create directory c\n'
                                             '    file:\n'
                                             '       path: /home/' + git["client_login"] + '/hadmin/c\n'
                                             '       state: directory\n'
                                             '  - name: Copy config.js\n'
                                             '    shell:\n'
                                             '        cmd: cp /home/' + git["client_login"] + '/hadmin/tv/config_def.js /home/' + git["client_login"] + '/hadmin/tv/config.js\n'
                                             '  - name: Copy config.css\n'
                                             '    shell:\n'
                                             '        cmd: cp /home/' + git["client_login"] + '/hadmin/tv/config_def.css /home/' + git["client_login"] + '/hadmin/tv/config.css')
                    try:
                        playbook_bitbucket.seek(0)
                        startPlaybok = ansible_runner.run(private_data_dir=temp_dir_playbook,
                                                          playbook=playbook_bitbucket.name,
                                                          inventory=temp_host.name, json_mode=True)
                        playbookdata = startPlaybok.stdout
                        playbookdata = playbookdata.read()
                        playbook_bitbucket.close()
                    except Exception as error:
                        logging.warning(error)
                    if "ok=4" in playbookdata:
                        try:
                            add_task_in_base = Installed_packeges()
                            add_task_in_base.installed = "hadmin TV"
                            add_task_in_base.hotel_id = git["hotel_id"]
                            add_task_in_base.save()
                        except Exception as error:
                            logging.warning(error)
                    else:
                        try:
                            add_task_in_base = Installed_packeges()
                            add_task_in_base.non_install = "hadmin TV"
                            add_task_in_base.hotel_id = git["hotel_id"]
                            add_task_in_base.save()
                        except Exception as error:
                            logging.warning(error)

            if 'pdaemondaemon' in task:
                with tempfile.TemporaryDirectory() as temp_dir_playbook:
                    playbook_bitbucket = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
                    playbook_bitbucket.write('---\n'
                                             '- hosts: all\n'
                                             '  gather_facts: no\n'
                                             '  tasks:\n'
                                             '  - name: install git pdaemondaemon\n'
                                             '    git:\n'
                                             '      repo: "https://' +  git["git_login"] + ':' + git["git_password"] + '@bitbucket.org/hadminteam/pdaemondaemon.git"\n'
                                             '      dest: /home/' + git["client_login"] + '/pdaemondaemon\n'
                                             '  - name: Install pdaemondaemon\n'
                                             '    become: yes\n'
                                             '    command: python3 setup.py install --force\n'
                                             '    args:\n'
                                             '       chdir: /home/' + git["client_login"] + '/pdaemondaemon/\n'
                                             '  - name: added hotel number to pdaemon\n'
                                             '    become: yes\n'
                                             '    lineinfile:\n'
                                             '        path: /etc/pdaemondaemon.cfg\n'
                                             '        regexp: "^hotel_id = "\n'
                                             '        line: "hotel_id = ' + git["hotel_id"] + '"')
                    try:
                        playbook_bitbucket.seek(0)
                        startPlaybok = ansible_runner.run(private_data_dir=temp_dir_playbook,
                                                          playbook=playbook_bitbucket.name,
                                                          inventory=temp_host.name, json_mode=True)
                        playbookdata = startPlaybok.stdout
                        playbookdata = playbookdata.read()
                        playbook_bitbucket.close()
                    except Exception as error:
                        logging.warning(error)
                    if "ok=3" in playbookdata:
                        try:
                            add_task_in_base = Installed_packeges()
                            add_task_in_base.installed = "pdaemondaemon"
                            add_task_in_base.hotel_id = git["hotel_id"]
                            add_task_in_base.save()
                        except Exception as error:
                            logging.warning(error)
                    else:
                        try:
                            add_task_in_base = Installed_packeges()
                            add_task_in_base.non_install = "pdaemondaemon not downloaded"
                            add_task_in_base.hotel_id = git["hotel_id"]
                            add_task_in_base.save()
                        except Exception as error:
                            logging.warning(error)
        git_status.update(git_task=' git completed')
        return 'Finish'

    ''' pdaemondaemon deploy in /etc/init.d/ and added hotel id in /etc pdaemondeamon.cfg'''

    def pdaemondaemon_deploy(self, request, temp_host, hotel_id, deploy_status_bar_count):
        packages = "pdaemondaemon config"
        self.write_status_bar(hotel_id, deploy_status_bar_count, packages)

        client_login = request.POST.get("client_login")
        with tempfile.TemporaryDirectory() as temp_dir_playbook:
            playbookpdaemon = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
            playbookpdaemon.write('---\n- hosts: all\n'
                              '  gather_facts: no\n'
                              '  tasks:\n'
                              '  - name: pdaemondaemon deploy\n'
                              '    become: yes\n'
                              '    command: python3 setup.py install --force\n'
                              '    args:\n'
                              '      chdir: /home/' + client_login + '/pdaemondaemon/\n'
                                                                     '  - name: add ID hotel to /etc/pdaemondaemon\n'
                                                                     '    become: yes\n'
                                                                     '    lineinfile:\n'
                                                                     '        path: /etc/pdaemondaemon.cfg\n'
                                                                     '        regexp: "^hotel_id = 0"\n'
                                                                     '        line: "hotel_id = ' + str(hotel_id) + '"')
            playbookpdaemon.seek(0)
            startPlaybook = ansible_runner.run(private_data_dir=temp_dir_playbook, playbook=playbookpdaemon.name,
                                               inventory=temp_host.name, json_mode=True)
            playbookdata = startPlaybook.stdout
            playbookdata = playbookdata.read()
            playbookpdaemon.close()
            if "ok=2" in playbookdata:
                try:
                    add_task_in_base = Installed_packeges()
                    add_task_in_base.task_completed = "pdaemondamon config"
                    add_task_in_base.hotel_id = hotel_id
                    add_task_in_base.save()
                    logging.info('hostname copied')
                except Exception as error:
                    logging.warning(error)
            else:
                try:
                    add_task_in_base = Installed_packeges()
                    add_task_in_base.task_non_completed = "pdaemondeamon config"
                    add_task_in_base.hotel_id = hotel_id
                    add_task_in_base.save()
                    logging.info('hostname config non copied')
                except Exception as error:
                    logging.warning(error)

    ''' request to database in table DeployClient_installed_packeges '''

    def check_intalled_packeges(self, hotel_id):
        try:
            hotel_id = int(hotel_id)
            data_list = Installed_packeges.objects.filter(hotel_id=hotel_id)
            install_list = serializers.serialize('json', data_list)
            Installed_packeges.objects.filter(hotel_id=hotel_id).delete()
            return install_list
        except Exception as error:
            logging.warning(error)

    '''create first record with status in databese'''

    def primary_record_to_base(self, hotel_id, status_value, status_task):
        try:
            primary_record = Task_and_Status()
            primary_record.hotel_id = hotel_id
            primary_record.status = status_value
            primary_record.task = status_task
            primary_record.save()
        except Exception as error:
            logging.warning(error)

    ''' write finished record in database'''
    def write_finish(self, hotel_id, status_value, status_task):
        try:
            pass
            write_status = Task_and_Status.objects.filter(hotel_id=hotel_id)
            write_status.update(task="Finish")
            write_status.update(status=100)
        except Exception as error:
            logging.warning(error)

    ''' get data in database and send to frontend'''
    def check_status_bar(self, hotel_id):
        try:
            deploy_status_bar = Task_and_Status.objects.filter(hotel_id=hotel_id)
            result = TaskStatusSerializer(deploy_status_bar, many=True)
            return result
        except Exception as error:
            logging.warning(error)

    ''' erase record in database Task_and_Status'''
    def erase_record_from_base(self, hotel_id):
        Task_and_Status.objects.filter(hotel_id=hotel_id).delete()

    def erase_Task_and_Status(self):
        try:
            Task_and_Status.objects.all().delete
            Task_and_Status.save()
            return "OK"
        except Exception as error:
            logging.warning(error)


    def add_backrsync(self, temp_host, data, deploy_status_bar_count):
        """ add backup rsync script"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(data["client_ip"], port=int(data["client_port"]), timeout=10, username=data["client_login"], password=data["client_password"])
            scp = SCPClient(ssh.get_transport())
            scp.put('/var/www/backup_rsync', recursive=True, remote_path='/home/' + data["client_login"])
            scp.close()
            copied = True
        except Exception as error:
            copied = False
            logging.warning(error)
        packages = "backup rsycnc"
        self.write_status_bar(data["hotel_id"], deploy_status_bar_count, packages)
        with tempfile.TemporaryDirectory() as temp_dir_playbook:
            pathcert = '"' + "{{ lookup('file', lookup('env','HOME') + '/root/.ssh/key_hotbackup/id_rsa.pub') }}" + '"'
            playbook_crontab = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
            playbook_crontab.write('---\n'
                                   '- hosts: all\n'
                                   '  tasks:\n'
                                   '  - cron:\n'
                                   '      name: Backtask\n'
                                   '      user: ' + data["client_login"] + '\n'
                                   '      minute: "0"\n'
                                   '      hour: "0"\n'
                                   '      day: "23"\n'                                        
                                   '      job: "/home/' + data["client_login"] + '/backup_rsync/start.sh"\n'
                                   '  - name: Add the user hotbackup\n'                                        
                                   '    user:\n'
                                   '      name: hotbackup\n'
                                   '      shell: /bin/bash\n'
                                   '      append: yes\n'
                                   '    become: yes\n'                                                    
                                   '  - name: Add key hotbackup\n'
                                   '    authorized_key:\n'
                                   '      user: hotbackup\n'
                                   '      state: present\n'
                                   '      key: ' + pathcert + '\n'
                                   '    become: yes\n'
                                   )
            playbook_crontab.seek(0)
            startPlaybook = ansible_runner.run(private_data_dir=temp_dir_playbook, playbook=playbook_crontab.name,
                                               inventory=temp_host.name, json_mode=True)
            playbookdata = startPlaybook.stdout
            playbookdata = playbookdata.read()
            playbook_crontab.close()
            if "ok=4" in playbookdata and copied == True:
                try:
                    add_task_in_base = Installed_packeges()
                    add_task_in_base.task_completed = "backup rsycnc copied"
                    add_task_in_base.hotel_id = data["hotel_id"]
                    add_task_in_base.save()
                    logging.info('backup rsycnc copied')
                except Exception as error:
                    logging.warning(error)
            else:
                try:
                    add_task_in_base = Installed_packeges()
                    add_task_in_base.task_non_completed = "backup rsycnc did not copy"
                    add_task_in_base.hotel_id = data["hotel_id"]
                    add_task_in_base.save()
                    logging.info('backup rsycnc did not copy')
                except Exception as error:
                    logging.warning(error)




