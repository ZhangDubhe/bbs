from django.contrib import admin
from . import models

class UserAdmin(admin.ModelAdmin):
# 定制Action行为具体方法
    def patch(self, request, queryset):
        print(self, request, queryset)
        print(request.POST.getlist('_selected_action'))

    patch.short_desc = "中文显示自定义描述"
    actions = [patch,]


admin.site.register(models.Article,UserAdmin)
admin.site.register(models.ArticleDetail)
admin.site.register(models.ArticleUpDown)
admin.site.register(models.Article2Tag)
admin.site.register(models.UserInfo)
admin.site.register(models.Comment)
admin.site.register(models.Tag)
admin.site.register(models.Category)
admin.site.register(models.Blog)
