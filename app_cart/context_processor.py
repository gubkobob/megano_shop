from .services import ComparisonServicesMixin


def comparison(request):
    return {'comparison': ComparisonServicesMixin(request)}

