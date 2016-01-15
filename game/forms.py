from mezzanine.generic.forms import ThreadedCommentForm

class MyCommentForm(ThreadedCommentForm):
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
