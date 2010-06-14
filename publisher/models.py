from django.db import models
from django.contrib.contenttypes.models import ContentType

class Publisher(models.Model):
    title = models.CharField(
        max_length=64
    )
    content_type = models.ForeignKey(
        ContentType, 
        editable=False, 
        null=True
    )
    class_name = models.CharField(
        max_length=32, 
        editable=False, 
        null=True
    )

    def __unicode__(self):
        return "%s - %s" % (self._meta.verbose_name, self.title)
    
    def as_leaf_class(self):
        """
        Returns the leaf class no matter where the calling instance is in the inheritance hierarchy.
        Inspired by http://www.djangosnippets.org/snippets/1031/
        """
        try:
            return self.__getattribute__(self.class_name.lower())
        except AttributeError:
            content_type = self.content_type
            model = content_type.model_class()
            if(model == ModelBase):
                return self
            return model.objects.get(id=self.id)
    
    def publish(self, instance):
        self.as_leaf_class().publish(instance)    
    
    def save(self, *args, **kwargs):
        # set leaf class content type
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        
        # set leaf class class name
        if not self.class_name:
            self.class_name = self.__class__.__name__

        super(Publisher, self).save(*args, **kwargs)

class Buzz(Publisher):
    # TODO: Add setup fields and methods to publish
    class Meta:
        ordering = ('title',)
        verbose_name = 'Buzz'
        verbose_name_plural = 'Buzz'

class Facebook(Publisher):
    # TODO: Add setup fields and methods to publish
    class Meta:
        ordering = ('title',)
        verbose_name = 'Facebook'
        verbose_name_plural = 'Facebook'

    def publish(self, instance):

        import facebook
        fb = facebook.Facebook('c5e0e45e0b134230f43a137dbb1ff4f0', '63a2fbff39e0ba6e1e9620a4218974ca')
        fb.auth.createToken()
        fb.login()
        import pdb; pdb.set_trace()
        session = fb.auth.getSession()

        import pdb; pdb.set_trace()
        fb.session_key = session['session_key']
        #fb.session_key = u'2.gKHR49pQHpuhIF5oUxaC8g__.3600.1275494400-100001158248236'        
        
        fb.uid = session['uid']
        #fb.uid = 100001158248236L
        
        #id_of_message = fb.stream.publish(message='my test message')
        fb(method='stream_publish', args={'session_key': fb.session_key, 'uid': '113183762059616', 'target_id': 'NULL', 'message':'MESSAGE_HERE1'})


        

        """
        import facebook  
        fb = facebook.Facebook('c5e0e45e0b134230f43a137dbb1ff4f0', '63a2fbff39e0ba6e1e9620a4218974ca') 
        fb.secret = '63a2fbff39e0ba6e1e9620a4218974ca'
        #fb.auth.createToken()  
        #fb.login(popup=False)

        session_key = '2.9IFBJreCj7woKkOfQMhHGA__.3600.1275490800-100001158248236'
        fb.session_key = session_key
            
        #id_of_message = fb.stream.publish(message='my test message', uid='test')  

        fb(method='stream_publish', args={'session_key': session_key, 'uid': "1", 'target_id': 'NULL', 'message':'MESSAGE_HERE'})

         
        session = fb.auth.getSession()
        import pdb; pdb.set_trace()

        try:  
            id_of_message = fb.stream.publish(message='my test message', uid='test')  
        except Exception, e:  
            error_code = None  
            try:  
                error_code = e.code  
            except AttributeError:  
                pass  

            if error_code:  
                print  "Facebook returned an error - sorry! %s %s" % (str(e.code), repr(e))  
            else:  
                print  "Facebook returned an error - sorry (no error code)! %s" % (repr(e))  

        import pdb; pdb.set_trace()
        """

class Mobile(Publisher):
    # TODO: Add setup fields and methods to publish
    class Meta:
        ordering = ('title',)
        verbose_name = 'Mobile'
        verbose_name_plural = 'Mobile'

class Twitter(Publisher):
    # TODO: Add setup fields and methods to publish
    class Meta:
        ordering = ('title',)
        verbose_name = 'Twitter'
        verbose_name_plural = 'Twitter'

class SocialBookmark(Publisher):
    # TODO: Add setup fields and methods to publish
    pass

class Web(Publisher):
    # TODO: Add setup fields and methods to publish
    class Meta:
        ordering = ('title',)
        verbose_name = 'Web'
        verbose_name_plural = 'Web'

#TODO: Add publishers for Mxit, Grid, Jil, Geo (Foursquare), Vlive, MTNPlay, V360, MyWeb.
