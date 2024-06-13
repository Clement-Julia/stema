from django.contrib import admin
from .models import FriendRequest,Friendship,Conversation,Message,Membership


class FriendRequestAdmin(admin.ModelAdmin):
    pass
class FriendshipAdmin(admin.ModelAdmin):
    pass
class ConversationAdmin(admin.ModelAdmin):
    pass
class MessageAdmin(admin.ModelAdmin):
    pass
class MembershipAdmin(admin.ModelAdmin):
    pass


admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(Friendship, FriendshipAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Membership, MembershipAdmin)