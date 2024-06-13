from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from .models import FriendRequest,Friendship,Conversation,Message,Membership
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import json
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import UserProfile, Friendship, FriendRequest
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_conversation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        friends_ids = data.get('friends')

        if not friends_ids:
            return JsonResponse({'status': 'error', 'message': 'No friends selected'})

        friends = User.objects.filter(id__in=friends_ids)

        if not friends.exists():
            return JsonResponse({'status': 'error', 'message': 'Selected friends do not exist'})

        conversation = Conversation.objects.create(title=title)
        Membership.objects.create(conversation=conversation, member=request.user)

        for friend in friends:
            Membership.objects.create(conversation=conversation, member=friend)

        return JsonResponse({'status': 'success', 'conversation_id': conversation.id})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

class ChatView(TemplateView):
    template_name = "chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        conversation_id = self.kwargs.get('conversation_id')
        
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id)
            messages = Message.objects.filter(conversation=conversation).order_by('timestamp')
            context['conversation'] = conversation
            context['messages'] = messages
            context['participants'] = conversation.participants.all()
        else:
            context['conversation'] = None
            context['messages'] = []

        # Récupérer la liste des amis de l'utilisateur connecté
        user = self.request.user
        friends = Friendship.objects.filter(
            Q(user1=user) | Q(user2=user)
        ).select_related('user1', 'user2')

        context['friends'] = friends

        return context

class ProfileView(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        if pk:
            user = get_object_or_404(User, pk=pk)
        else:
            user = request.user

        user_profile, created = UserProfile.objects.get_or_create(user=user)
        print(user_profile)
        conversations = Conversation.objects.filter(participants=user)
        
        # Récupérer les amis de l'utilisateur
        # friends = User.objects.filter(
        #     Q(friends__user1=user) | Q(_friends__user2=user)
        # ).distinct()
        friends = Friendship.objects.filter(
            Q(user1=user) | Q(user2=user)
        ).select_related('user1', 'user2')

        for friend in friends:
            if friend.user1 == user:
                friend.conversation = Conversation.objects.filter(participants=friend.user2).filter(participants=user).first()
            else:
                friend.conversation = Conversation.objects.filter(participants=friend.user1).filter(participants=user).first()
        return render(request, 'profile.html', {
            'user_profile': user_profile,
            'conversations': conversations,
            'friends': friends,
        })


class FriendListView(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        if pk:
            user = get_object_or_404(User, pk=pk)
        else:
            user = request.user
        
        friends = Friendship.objects.filter(
            Q(user1=user) | Q(user2=user)
        ).select_related('user1', 'user2')

        for friend in friends:
            if friend.user1 == user:
                friend.conversation = Conversation.objects.filter(participants=friend.user2).filter(participants=user).first()
            else:
                friend.conversation = Conversation.objects.filter(participants=friend.user1).filter(participants=user).first()

        return render(request, 'friendlist.html', {'friends': friends, 'user': user})
    

class AddFriendView(LoginRequiredMixin, View):
    def get(self, request):
        friend_requests = FriendRequest.objects.filter(to_user=request.user)
        return render(request, 'add_friend.html', {'friend_requests': friend_requests})
    
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        to_user = get_object_or_404(User, username=username)
        friend_request, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
        if created:
            return JsonResponse({'status': 'request sent'})
        return JsonResponse({'status': 'request already exists'})

    def search_users(request):
        query = request.GET.get('q', '')
        if query:
            users = User.objects.filter(username__icontains=query)
            return render(request, 'user_search_results.html', {'users': users})
        return render(request, 'empty_search_results.html')

class ManageFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, request_id):
        action = request.POST.get('action')
        friend_request = get_object_or_404(FriendRequest, id=request_id)
        
        if friend_request.to_user == request.user:
            if action == 'accept':
                friendship1 = Friendship.objects.filter(user1=request.user, user2=friend_request.from_user).first()
                friendship2 = Friendship.objects.filter(user1=friend_request.from_user, user2=request.user).first()

                if not friendship1 and not friendship2:
                    Friendship.objects.create(user1=request.user, user2=friend_request.from_user)
                    existing_conversation = Conversation.objects.filter(membership__member=request.user).filter(membership__member=friend_request.from_user).first()
                    if not existing_conversation:
                        conversation = Conversation.objects.create()
                        Membership.objects.create(conversation=conversation, member=request.user)
                        Membership.objects.create(conversation=conversation, member=friend_request.from_user)

                friend_request.delete()
            elif action == 'decline':
                friend_request.delete()

        return redirect('friendlist')


class SearchUsersView(ListView):
    model = User
    template_name = 'user_search_results.html'
    context_object_name = 'users'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        current_user = self.request.user
        if query:
            friend_ids_user1 = Friendship.objects.filter(user1=current_user).values_list('user2_id', flat=True)
            friend_ids_user2 = Friendship.objects.filter(user2=current_user).values_list('user1_id', flat=True)
            
            users_queryset = User.objects.filter(username__icontains=query).exclude(id=current_user.id)
            users_queryset = users_queryset.exclude(id__in=friend_ids_user1)
            users_queryset = users_queryset.exclude(id__in=friend_ids_user2)
            return users_queryset
        
        return User.objects.none()
    

class RemoveFriendView(View):
    def post(self, request, friend_id):
        friendship = get_object_or_404(Friendship, id=friend_id)
        if friendship.user1 == request.user or friendship.user2 == request.user:
            friendship.delete()
        return redirect('friendlist')
    
@method_decorator(csrf_exempt, name='dispatch')
class AddParticipantsView(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        conversation_id = data.get('conversation_id')
        friend_id = data.get('friend_id')

        conversation = get_object_or_404(Conversation, id=conversation_id)
        
        friend = get_object_or_404(User, id=friend_id)
        Membership.objects.create(conversation=conversation, member=friend)
        
        return JsonResponse({'status': 'success'})