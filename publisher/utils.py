class SSIContentResolver(object):
    """
    Renders either an SSI tag or normal content based on SSI mode and user uniqueness.
    """
    user_unique = False
    login_required = False
    receive_post = False

    def get_leaf(self):
        try:
            return self.as_leaf_class()
        except AttributeError:
            return self
        
    def render(self, context, *args, **kwargs):
        """
        Returns either self.render_ssi or self.render_content based on self.user_unique 
        and settings.SSI_ENABLED.  self.render_content to be implimented by subclasses.

        Return render_content in the case of the receive_post being true and the 
        request being a post. (In other words don't render ssi for stuff expecting POSTS).
        """
        request = context['request']
        leaf = self.get_leaf()
        
        if leaf.login_required and not context['request'].user.is_authenticated():
            path = urlquote(request.get_full_path())
            tup = settings.LOGIN_URL, REDIRECT_FIELD_NAME, path
            return HttpResponseRedirect('%s?%s=%s' % tup)

        if leaf.user_unique and settings.SSI_ENABLED:
            if leaf.receive_post and request.method == 'POST':
                return leaf.render_content(context, *args, **kwargs)
            else:
                return leaf.render_ssi(context, *args, **kwargs)
        else:
            return leaf.render_content(context, *args, **kwargs)
                
    def render_ssi(self, context, *args, **kwargs):
        """
        Renders SSI tag. URL is reversed ssi view and added get params determined
        through nginx passed key.
        """
        leaf = self.get_leaf()
        request = context['request']
       
        cache_key = request.META.get('MEMCACHED_KEY', request.get_full_path())
        url = self.get_ssi_url(request)
        try:
            url += '?%s' % cache_key.split('?')[1]
        except IndexError:
            pass

        # XXX: investigate why wait has to be set to true in order
        # for nginx to correctly fetch includes from cache.
        return '<!--# include virtual="%s" wait="yes" -->' % url

    def render_content(self, context, *args, **kwargs):
        raise NotImplementedError("Should have implemented this")
    
    def get_ssi_url(self, request):
        raise NotImplementedError("Should have implemented this")
