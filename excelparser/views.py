from django.views.generic import FormView

from excelparser.forms import ProcessPopulatedTemplateForm


class ProcessPopulatedTemplate(FormView):
    form_class = ProcessPopulatedTemplateForm
    template_name = "excelparser/process_populated_template.html"