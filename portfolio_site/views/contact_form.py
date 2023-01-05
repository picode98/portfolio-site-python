from typing import Optional

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.http import QueryDict

from google.cloud import recaptchaenterprise_v1

from portfolio_site.views.site_views import SiteTemplateView


def validate_recaptcha(token: str, expected_action_name: str):
    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient.from_service_account_json(
        settings.RECAPTCHA_GCLOUD_CREDENTIALS)

    event = recaptchaenterprise_v1.Event()
    event.site_key = settings.RECAPTCHA_SITE_KEY
    event.token = token

    assessment = recaptchaenterprise_v1.Assessment()
    assessment.event = event

    request = recaptchaenterprise_v1.CreateAssessmentRequest()
    request.assessment = assessment
    request.parent = settings.RECAPTCHA_GCLOUD_PROJECT

    response = client.create_assessment(request)
    if not response.token_properties.valid:
        return False, f'The ReCAPTCHA token was not valid: {response.token_properties.invalid_reason}'
    elif response.token_properties.action != expected_action_name:
        return False, f'The action "{response.token_properties.action}" that the ReCAPTCHA token was submitted for' \
                      f'does not match the expected action name "{expected_action_name}".'
    elif response.risk_analysis.score < 0.5:
        return False, f'ReCAPTCHA detected unusual activity related to the form.'
    else:
        return True, None


class ContactForm(forms.Form):
    return_email = forms.EmailField(label='Return e-mail address (optional, but I cannot reply to you if it is not supplied):', required=False)
    message_subject = forms.CharField(label='Message subject:', required=True)
    message_text = forms.CharField(widget=forms.Textarea, label='Message text:', required=True)
    recaptcha_token = None
    recaptcha_action_name = 'contact_form_submit'
    recaptcha_valid = None

    def __init__(self, form_data: Optional[QueryDict] = None):
        if form_data is not None and 'g-recaptcha-response' in form_data:
            self.recaptcha_token = form_data['g-recaptcha-response']
        super().__init__(form_data)

    def clean(self):
        other_fields = super().clean()

        if self.recaptcha_valid is None:
            self.recaptcha_valid, reason = validate_recaptcha(self.recaptcha_token, self.recaptcha_action_name)

            if not self.recaptcha_valid:
                raise ValidationError(f'ReCAPTCHA validation failed: {reason}')

        return other_fields


class ContactFormView(SiteTemplateView):
    template_name = 'about/contact_me.html'
    display_name = 'Contact Me'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **{**kwargs, 'contact_form': ContactForm(),
                                              'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY})

    def post(self, request, *args, **kwargs):
        filled_form = ContactForm(request.POST)
        print(f'Form POSTed: {filled_form}')

        if filled_form.is_valid():
            message = EmailMessage(subject=f'Contact form message: {filled_form.cleaned_data["message_subject"]}',
                                   body=filled_form.cleaned_data["message_text"],
                                   from_email=settings.CONTACT_FORM_FROM_ADDRESS,
                                   to=[settings.CONTACT_FORM_TO_ADDRESS],
                                   reply_to=[filled_form.cleaned_data["return_email"]]
                                            if len(filled_form.cleaned_data["return_email"]) > 0 else None)
            message.send()

        context = self.get_context_data(**kwargs)
        return self.render_to_response({**context, 'contact_form': filled_form,
                                        'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY,
                                        'form_posted': True})


contact_form = ContactFormView.as_view()
