from django.conf import settings
from django.core import urlresolvers
from django.core.urlresolvers import Resolver404
from django.utils.encoding import smart_str

from publisher.models import View

def resolve_pattern(request):
    urlconf = getattr(request, "urlconf", settings.ROOT_URLCONF)
    self = urlresolvers.RegexURLResolver(r'^/', urlconf)
    path = request.path_info
    
    tried = []
    match = self.regex.search(path)
    if match:
        new_path = path[match.end():]
        for pattern in self.url_patterns:
            try:
                sub_match = pattern.resolve(new_path)
            except Resolver404, e:
                sub_tried = e.args[0].get('tried')
                if sub_tried is not None:
                    tried.extend([(pattern.regex.pattern + '   ' + t) for t in sub_tried])
                else:
                    tried.append(pattern.regex.pattern)
            else:
                if sub_match:
                    sub_match_dict = dict([(smart_str(k), v) for k, v in match.groupdict().items()])
                    sub_match_dict.update(self.default_kwargs)
                    for k, v in sub_match[2].iteritems():
                        sub_match_dict[smart_str(k)] = v
                    return pattern
                tried.append(pattern.regex.pattern)
        raise Resolver404, {'tried': tried, 'path': new_path}
    raise Resolver404, {'path' : path}

def render_view(request, *args, **kwargs):
    pattern = resolve_pattern(request)
    view = View.objects.filter(page=pattern.name)
    if view:
        view = view[0]
    else:
        raise NotImplementedError("View not configured for page '%s'" % pattern.name)
    return view.as_leaf_class().render(request, *args, **kwargs)
