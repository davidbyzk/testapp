from users.models import UserProfile
from django import forms

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('user', 'public_token', 'access_token', 'item_id',)