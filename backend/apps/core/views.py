from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages

from apps.bookings.forms import BookingForm


class LandingPageView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = kwargs.get('form', BookingForm())

        context['services'] = [
            {
                'id': 1,
                'icon': 'refrigerator',
                'title': 'Refrigerator Repair',
                'description': 'Expert repair for all refrigerator brands including Samsung, LG, Whirlpool, and more.',
            },
            {
                'id': 2,
                'icon': 'washing-machine',
                'title': 'Washer & Dryer Repair',
                'description': 'Fast and reliable washing machine and dryer repairs.',
            },
            {
                'id': 3,
                'icon': 'dishwasher',
                'title': 'Dishwasher Repair',
                'description': 'Professional dishwasher repair service.',
            },
            {
                'id': 4,
                'icon': 'oven',
                'title': 'Oven & Stove Repair',
                'description': 'Gas and electric oven repairs.',
            },
        ]
        return context

    def post(self, request, *args, **kwargs):
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)

            booking.ip_address = request.META.get('REMOTE_ADDR')
            booking.user_agent = request.META.get('HTTP_USER_AGENT')

            booking.save()

            messages.success(request, "Thank you! We will contact you shortly.")
            return redirect('core:landing')

        context = self.get_context_data(form=form)
        messages.error(request, "Please fix the errors below.")
        return self.render_to_response(context)