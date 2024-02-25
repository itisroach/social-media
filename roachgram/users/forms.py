from django import forms
from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from .models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout , Row , Column , Field , Submit

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=255)
    class Meta:
        model = User
        fields = ("profile" , "name" , "username", "email" , "password1" , "password2" , "about")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Row(
                Column(Field("profile"))
            ),
            Row(
                Column(Field("name"), css_class="px-2"),   
                Column(Field("username"), css_class="px-2"),   
                Column(Field("email"), css_class="px-2"),   
            ),
            Row(
                Column(Field("password1"), css_class="px-2"),   
                Column(Field("password2"), css_class="px-2")
            ),
            Row(
                Column(Field("about"), css_class="resize"),   
            ),
            Submit('submit', 'Submit', css_class='bg-green-500 px-6 py-2 text-white rounded-lg cursor-pointer')
            
        )


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("profile",'name',"username","email","about")
    name = forms.CharField(max_length=255 , widget=forms.TextInput(attrs={"class": "bg-black"}))
    profile = forms.ImageField(widget=forms.FileInput(attrs={"class": "hidden" , "onchange": "previewProfile(this)"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(Field("profile"))
            ),
            Row(
                Column(Field("name"), css_class="px-2 w-1/3"),   
                Column(Field("username"), css_class="px-2 w-1/3"),   
                Column(Field("email"), css_class="px-2 w-1/3 text-white"),   
            ),
            Row(
                Column(Field("about"), css_class="resize"),   
            ),
            Submit('submit', 'Update', css_class='bg-green-500 px-6 my-6 py-2 text-white rounded-lg cursor-pointer')
            
        )