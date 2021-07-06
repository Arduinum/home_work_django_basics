from django.contrib.auth.forms import AuthenticationForm

from .models import ShopUser


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)

        for field_name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control'
