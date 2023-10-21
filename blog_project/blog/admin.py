from django.contrib import admin
from .models import Profile,BlogPost,Comment,Reply


class InfoAppModel(admin.ModelAdmin):
    fields = ('user', 'birthdate', 'gender','bio','avatar')
    search_fields = ('user','gender')
    list_display = ('user','birthdate','gender','avatar')
    
    # Cấu hình liên kết cho trường 'name'
    list_display_links = ('user',)
    list_editable = ('birthdate', 'gender')
class InfoBlog(admin.ModelAdmin):
    field = ('title','content','user','datetime','image')
    search_fields = ('title','user')
    list_display = ('title','content','user','datetime','image','views')
    list_display_links = ('title',)
class InfoComment(admin.ModelAdmin):
    field = ('user','content','blog','datetime')
    search_fields = ('user',)
    list_display = ('user','content','get_blog_title','datetime')
    list_display_links = ('user',)
    def get_blog_title(self, obj):
        return obj.blog.title if obj.blog else ""  

    get_blog_title.short_description = 'Blog Title' 
admin.site.register(Profile,InfoAppModel)
admin.site.register(BlogPost,InfoBlog)
admin.site.register(Comment,InfoComment)
admin.site.register(Reply)