from django import forms
from django.core.validators import FileExtensionValidator
from .models import PortfolioFamily, Datamap
from helpers import acceptable_types

file_validator = FileExtensionValidator(
    allowed_extensions=acceptable_types, message="Needs to be a CSV or Excel file."
)


def datamap_choices():
    d_maps = Datamap.objects.all()
    x = [(x.id, x.name) for x in d_maps]
    return tuple(reversed(sorted(x, key=lambda dm: dm[0])))


class UploadDatamap(forms.Form):
    file_name = forms.CharField(max_length=30)
    target_datamap = forms.ChoiceField(choices=datamap_choices)
    uploaded_file = forms.FileField(validators=[file_validator])
    replace_all_entries = forms.BooleanField(initial=True, required=False)


class CreateDatamapForm(forms.Form):

    pfs = PortfolioFamily.objects.all()

    name = forms.CharField(max_length=50)
    portfolio_family = forms.ChoiceField(choices=[(p.id, p.name) for p in pfs])
