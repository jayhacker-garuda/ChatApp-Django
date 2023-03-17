from django import forms

from .models import Room


class CreateRoomForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateRoomForm, self).__init__(*args, **kwargs)

        for field in self.fields:

            self.fields[field].widget.attrs.update({
                'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-[#fd913c] focus:border-[#fd913c] sm:text-sm'
            })
            self.fields[field].error_messages.update({
                'required': 'This %s field is required' % field
            })

    class Meta:
        model = Room
        fields = ['name']
