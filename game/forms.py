from mezzanine.generic.forms import ThreadedCommentForm
from mezzanine.accounts.forms import ProfileForm
from nocaptcha_recaptcha.fields import NoReCaptchaField


class MyCommentForm(ThreadedCommentForm):
    """
        Custom comment form to remove the name, email and url
        Fields and make them empty strings on form submission
        we don't want them as we require users to be signed up
        in order to comment.
    """
    def __init__(self, request, *args, **kwargs):
        super(MyCommentForm, self).__init__(request, *args, **kwargs)
        del self.fields['name']
        del self.fields['email']
        del self.fields['url']

    def clean(self):
        cleaned_data = super(MyCommentForm, self).clean()
        cleaned_data["name"] = ""
        cleaned_data["email"] = ""
        cleaned_data["url"] = ""
        return cleaned_data


class MyProfileForm(ProfileForm):
    """
        Simple modification to the registration form to add
        reCAPTCHA to avoid spam.
    """
    captcha = NoReCaptchaField()        
