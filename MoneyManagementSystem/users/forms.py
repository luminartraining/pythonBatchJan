from django.forms import ModelForm
from users.models import Users,Expense
from django import forms

class UserCreationForm(ModelForm):
    model=Users
    class Meta:
        model = Users
        fields='__all__'


class UserLoginForm(forms.Form):
    username=forms.CharField(max_length=120)
    password=forms.CharField(max_length=120,widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username=cleaned_data.get("username")

        if(Users.objects.filter(username=username)):
            pass
        else:
            msg = "no user exist in this name"
            self.add_error('username', msg)


class AddExpenseForm(ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:


        model=Expense
        fields=["category","amount","shortnote","date"]
