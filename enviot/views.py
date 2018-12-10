from django.views.generic import TemplateView


class HomePageView(TemplateView):
    """[summary]
    
    Parameters
    ----------
    TemplateView : [type]
        [description]
    
    """
    template_name = "index.html"
