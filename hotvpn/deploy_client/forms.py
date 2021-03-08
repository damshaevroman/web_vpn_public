from django import forms


'''This is form  for deploy remote server'''

class DataForm(forms.Form):
    client_login = forms.CharField(label="Login", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Login',
                                                                               'class': 'form-control form-control-user', 'id': 'client_login'}))

    client_ip = forms.GenericIPAddressField(label='IP address', widget=forms.TextInput(attrs={'placeholder': 'IP server',
                                                                                              'class': 'form-control form-control-user', 'id': 'client_ip'}))

    client_port = forms.CharField(label="port", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Port server',
                                                                                              'class': 'form-control form-control-user', 'id': 'client_port'}))

    client_password = forms.CharField(label="password", max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user',
                                                                                                          'placeholder': 'Password', 'id': 'client_password'}))

    client_sudo_password = forms.CharField(label="sudo password", max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user',
                                                                                                                    'placeholder': 'Sudo password', 'id': "client_sudo_password", "onblur": "checkPass()"}))

    git_password = forms.CharField(required=False, label="git password", max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user',
                                                                                                                           'placeholder': 'Git password', 'id': 'git_password'}))

    git_login = forms.CharField(required=False, label="git_login", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Git_Login',
                                                                                                                 'class': 'form-control form-control-user', 'id': 'git_login'}))

    install_packeges = forms.CharField(label="installation list", widget=forms.Textarea(attrs={'class': 'form-control form-control-user', 'id': 'install_packeges'}))

    my_checkbox = forms.CharField(required=False, label="my_checkbox", widget=forms.TextInput(attrs={'type': 'checkbox',
                                                                                                     'id': 'my_checkbox', 'class': 'form-check-input'}))

    dhcp_checkbox = forms.CharField(required=False, label="Deploy dhcp", widget=forms.TextInput(attrs={'type': 'checkbox',
                                                                                                       'id': 'dhcp_checkbox',
                                                                                                       'class': 'form-check-input',
                                                                                                       'form': 'deployForm'}))



    git_tv = forms.CharField(required=False, label="TVTV",
                                   widget=forms.TextInput(attrs={'type': 'checkbox',
                                                                 'id': 'tv',
                                                                 'class': 'form-check-input',
                                                                 'form': 'deployForm'}))

    git_daemon = forms.CharField(required=False, label="daemon",
                                   widget=forms.TextInput(attrs={'type': 'checkbox',
                                                                 'id': 'git_daemon',
                                                                 'class': 'form-check-input',
                                                                 'form': 'deployForm'}))

    git_streamer = forms.CharField(required=False, label="streamer",
                                   widget=forms.TextInput(attrs={'type': 'checkbox',
                                                                 'id': 'git_streamer',
                                                                 'class': 'form-check-input',
                                                                 'form': 'deployForm'}))






    hostname_checkbox = forms.CharField(required=False, label="Change hostname", widget=forms.TextInput(attrs={'type': 'checkbox',
                                                                                                               'id': 'hostname_checkbox',
                                                                                                               'class': 'form-check-input',
                                                                                                               'form': 'deployForm'}))

    dhcp_network = forms.GenericIPAddressField(required=False, widget=forms.TextInput(attrs={'placeholder': 'DHCP NETWORK',
                                                                                             'class': 'form-control form-control-user', 'id': "dhcp_network"}))
    dhcp_mask = forms.GenericIPAddressField(required=False, widget=forms.TextInput(attrs={'placeholder': 'NETWORK MASK',
                                                                                          'class': 'form-control form-control-user', 'id': "dhcp_mask"}))
    dhcp_range_start = forms.GenericIPAddressField(required=False, widget=forms.TextInput(attrs={'placeholder': 'DHCP RANGE START',
                                                                                                 'class': 'form-control form-control-user', 'id': "dhcp_range_start"}))
    dhcp_range_end = forms.GenericIPAddressField(required=False, widget=forms.TextInput(attrs={'placeholder': 'DHCP RANGE END',
                                                                                               'class': 'form-control form-control-user', 'id': "dhcp_range_end"}))
    dhcp_dns = forms.GenericIPAddressField(required=False, widget=forms.TextInput(attrs={'placeholder': 'DNS SERVER',
                                                                                         'class': 'form-control form-control-user', 'id': "dhcp_dns"}))
    domain_name = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={'placeholder': 'DOMAINE NAME',
                                                                                               'class': 'form-control form-control-user', 'id': "domain_name"}))
    dhcp_gateway = forms.GenericIPAddressField(required=False, widget=forms.TextInput(attrs={'placeholder': 'GATEWAY',
                                                                                             'class': 'form-control form-control-user', 'id': "dhcp_gateway"}))
    dhcp_broadcast = forms.GenericIPAddressField(required=False, widget=forms.TextInput(attrs={'placeholder': 'BROADCAST',
                                                                                               'class': 'form-control form-control-user', 'id': "dhcp_broadcast"}))

    uplink_interface = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={'placeholder': 'uplink internet interface ',
                                                                                                    'class': 'form-control form-control-user', 'id': "uplink_interface"}))
    dhcp_interface = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={'placeholder': 'enter name DHCP interface',
                                                                                                    'class': 'form-control form-control-user', 'id': "dhcp_interface"}))
    hotel_id = forms.CharField(label="hotel_id", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Hotel ID',
                                                                                                               'class': 'form-control form-control-user',
                                                                                                              'id': 'hotel_id',
                                                                                                              'form': 'FormDeploy'}))
    hostname = forms.CharField(required=False, label="hostname", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Change hostname',
                                                                                                               'class': 'form-control form-control-user', 'id': 'hostname'}))



