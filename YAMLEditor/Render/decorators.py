from .render import render_with_yaml

def admins_only(view):
    def _decorated(request, *args, **kwargs):
        if not request.user.is_staff:
            return render_with_yaml(request, 'no_access.html')
        return view(request, *args, **kwargs)
    return _decorated
