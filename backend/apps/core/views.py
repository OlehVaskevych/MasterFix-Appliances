from django.views.generic import TemplateView


class LandingPageView(TemplateView):
    """
    Main landing page view.
    """
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
                'description': 'Fast and reliable washing machine and dryer repairs to get your laundry running.',
            },
            {
                'id': 3,
                'icon': 'dishwasher',
                'title': 'Dishwasher Repair',
                'description': 'Professional dishwasher repair service with same-day appointments available.',
            },
            {
                'id': 4,
                'icon': 'oven',
                'title': 'Oven & Stove Repair',
                'description': 'Gas and electric oven repairs by certified technicians with guaranteed work.',
            },
        ]
        return context
