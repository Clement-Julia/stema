from django.urls import path
from .views import ProfileView, FriendListView, AddFriendView, ManageFriendRequestView, SearchUsersView,RemoveFriendView,ChatView,create_conversation

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile_with_pk'),
    path('friendlist/', FriendListView.as_view(), name='friendlist'),
    path('friendlist/<int:pk>/', FriendListView.as_view(), name='friendlist_with_pk'),
    path('add_friend/', AddFriendView.as_view(), name='add_friend'),
    path('manage_friend_request/<int:request_id>/', ManageFriendRequestView.as_view(), name='manage_friend_request'),
    path('search_users/', SearchUsersView.as_view(), name='search_users'),
    path('remove_friend/<int:friend_id>/', RemoveFriendView.as_view(), name='remove_friend'),
    path('chat/<int:conversation_id>/', ChatView.as_view(), name='chatroom'),
    path('create_conversation/', create_conversation, name='create_conversation'),
]
