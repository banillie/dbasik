from django.conf import settings
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from django.shortcuts import get_object_or_404

from .forms import (
    CreateDatamapForm,
    UploadDatamap,
    EditDatamapLineForm,
    CreateDatamapLineForm,
)
from .models import Datamap, DatamapLine
from register.models import Tier
from exceptions import IllegalFileUpload, IncorrectHeaders, DatamapLineValidationError
from helpers import CSVUploadedFile, delete_datamap


class DatamapList(ListView):
    model = Datamap


def edit_datamapline(request, dml_pk):
    instance = get_object_or_404(DatamapLine, pk=dml_pk)
    if request.method == "POST":
        form = EditDatamapLineForm(request.POST, instance)
        if form.is_valid():
            key = form.cleaned_data["key"]
            sheet = form.cleaned_data["sheet"]
            cell_ref = form.cleaned_data["cell_ref"]
            slug = instance.datamap.slug
            existing_dml = DatamapLine.objects.get(pk=dml_pk)
            existing_dml.key = key
            existing_dml.sheet = sheet
            existing_dml.cell_ref = cell_ref
            existing_dml.save()
            return HttpResponseRedirect(f"/datamap/{slug}")
    else:
        instance_data = {
            "key": instance.key, "sheet": instance.sheet, "cell_ref": instance.cell_ref
        }
        form = EditDatamapLineForm(instance_data)

    return render(
        request, "datamap/edit_datamapline.html", {"form": form, "dml_pk": dml_pk}
    )


def datamap_detail(request, slug):
    dm_lines = DatamapLine.objects.filter(datamap__slug=slug).order_by("id")
    dm_name = get_object_or_404(Datamap, slug=slug).name
    dm = get_object_or_404(Datamap, slug=slug)
    context = {"dm_lines": dm_lines, "dm_name": dm_name, "dm": dm}
    return render(request, "datamap/datamap.html", context)


def delete_datamap_view(request, slug):
    dm = get_object_or_404(Datamap, slug=slug)
    delete_datamap(dm)
    return HttpResponseRedirect("/datamaps")


def create_datamap(request):
    if request.method == "POST":
        form = CreateDatamapForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            tier = form.cleaned_data["tier"]
            pf_obj = get_object_or_404(Tier, pk=tier.id)
            new_dm = Datamap(name=name, tier=pf_obj)
            try:
                new_dm.save()
                return HttpResponseRedirect("/uploaddatamap")
            except IntegrityError:
                messages.add_message(
                    request,
                    messages.INFO,
                    "Please ensure unique datamap name for this Tier",
                )
                dms_l = Datamap.objects.all()
    else:
        form = CreateDatamapForm()
        # list of current datamaps
        dms_l = Datamap.objects.all()

    return render(
        request, "datamap/create_datamap.html", {"form": form, "dms_l": dms_l}
    )


def upload_datamap(request):

    field_keys = settings.DATAMAP_FIELD_KEYS

    if request.method == "POST":
        form = UploadDatamap(request.POST, request.FILES)
        if form.is_valid():
            slug = get_object_or_404(
                Datamap, pk=form.cleaned_data["target_datamap"].id
            ).slug
            f = request.FILES["uploaded_file"]
            dm = form.cleaned_data["target_datamap"]
            if "replace_all_entries" in request.POST:
                replace = form.cleaned_data["replace_all_entries"]
            else:
                replace = "off"
            if f.content_type == "text/csv":
                try:
                    CSVUploadedFile(f, dm.id, field_keys, replace).process()
                    return HttpResponseRedirect(reverse("datamap-detail", args=[slug]))
                except IllegalFileUpload:  # TODO: implement this - was removed in refactor
                    messages.add_message(request, messages.INFO, "Illegal file type")
                except IncorrectHeaders as e:
                    messages.add_message(request, messages.INFO, e.args[0])
                except DatamapLineValidationError as e:
                    msg = (
                        f"Validation error in field: {e.args[0][0].error_field}\n"
                        f"{e.args[0][0].django_validator_message} {e.args[0][0].field_given_value}"
                    )
                    messages.add_message(request, messages.INFO, msg)

        elif form.errors:
            for v in form.errors.values():
                messages.add_message(request, messages.INFO, v)

    else:
        form = UploadDatamap()

    return render(
        request, "datamap/upload_datamap.html", {"form": form, "field_keys": field_keys}
    )


def create_datamapline(request, slug):
    dm = Datamap.objects.get_object_or_404(slug=slug)
    if request.method == "POST":
        form = CreateDatamapLineForm(request.POST)
        if form.is_valid():
            key = form.cleaned_data["key"]
            sheet = form.cleaned_data["sheet"]
            cell_ref = form.cleaned_data["cell_ref"]
            dml = DatamapLine.objects.create(
                datamap=dm, key=key, sheet=sheet, cell_ref=cell_ref
            )
            dml_pk = dml.id
            return HttpResponseRedirect(f"/datamap/{slug}")
    else:
        form = CreateDatamapLineForm()
        dml_pk = None
    return render(
        request,
        "datamap/create_datamapline.html",
        {"form": form, "dml_pk": dml_pk, "slug": slug},
    )
