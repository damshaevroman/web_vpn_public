from django import forms


'''models for create in database table record with information about hotel also that infomation need for create certificate '''

class Hotels_form(forms.Form):
	hotel_country = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Country', 'class': 'form-control form-control-user'}))
	hotel_city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control form-control-user'}))
	hotel_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control form-control-user'}))
	hotel_name_certification = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name Certification', 'class': 'form-control form-control-user', 'id': 'hotel_name_certification'}))
	hotel_admin_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Hotel ID', 'class': 'form-control form-control-user'}))
	hotel_ip_address = forms.GenericIPAddressField(widget=forms.TextInput(attrs={'placeholder': 'IP address', 'class': 'form-control form-control-user'}))
	hotel_port = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Port', 'class': 'form-control form-control-user'}))
	hotel_vpn_ip_address = forms.GenericIPAddressField(required=False, widget=forms.TextInput(attrs={'placeholder': 'IP address', 'class': 'form-control form-control-user'}))
	hotel_vpn_port = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Port', 'class': 'form-control form-control-user'}))
	login = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Host login', 'class': 'form-control form-control-user', 'form': 'save_edit_hotel_form'}))
	password = forms.CharField(required=False, max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Host password', 'form': 'save_edit_hotel_form'}))




'''forms for create in database table record with information about users also that information need for create user certificate '''

class Hotel_User_form(forms.Form):
	organisation = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Organisation', 'class': 'form-control form-control-user' , "id": "organisation"}))
	user_city = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control form-control-user', "id": "user_city"}))
	user_fio = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'FIO', 'class': 'form-control form-control-user', "id": "user_fio"}))
	user_cert = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Name certification', 'class': 'form-control form-control-user', "id": "user_cert"}))






