from django.contrib import admin
from .models import Tournament, ParentProfile, TournamentDirector, Banner

admin.site.register(Tournament)
admin.site.register(ParentProfile)
admin.site.register(TournamentDirector)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'link_url')
    search_fields = ('link_url',)
