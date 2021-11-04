from django.shortcuts import get_object_or_404, render, redirect
from .forms import NewTopicForm, PostForm
from .models import Board, Topic, Post
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator

# Create your views here.

def HomeView(request):
    """
    This is home page view with all boards listings

    """
    boards = Board.objects.all()
    context = {"boards":boards}
    return render(request, "home.html", context)

def TopicsView(request, pk):
    """
    This is page with linked topics for board
    
    """   
    board = get_object_or_404(Board,pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count("posts") - 1)
    context = {"board":board,"topics":topics}           
    return render(request, "topics.html", context)

@login_required
def NewTopicView(request, pk):
    """
    This is page add new topic to the board
    
    """ 
    # if board does not exist get 404 page
    board = get_object_or_404(Board, pk=pk) 
    # get currenly logged user
    #user = User.objects.first() # To do
    # If request method is post use following form form forms.py and pass data there
    if request.method == "POST":
        form = NewTopicForm(request.POST)
        #if form is valid push cleaned data to database
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message = form.cleaned_data["message"],
                topic   = topic,
                created_by = request.user
            )
            return redirect("topic_posts",pk=pk, topic_pk=topic.pk)
    else:
        #else if request is not POST get blank form
        form = NewTopicForm()

    # store data form models
    context = {"board": board, "form": form}
    return render(request, "new_topic.html",context)

def TopicPostView(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})

@login_required
def ReplyTopicView(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect("topic_posts", pk=pk, topic_pk=topic_pk )
    else:
        form = PostForm()
    context = {"topic":topic, "form": form }
    return render(request,"reply_topic.html", context)

@method_decorator(login_required, name="dispatch")
class PostUpdateView(UpdateView):
    model = Post
    fields = ("message",)
    template_name = "edit_post.html"
    pk_url_kwarg = "post_pk"
    context_object_name = "post"

    def form_valid(self,form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect("topic_posts", pk=post.topic.board.pk, topic_pk=post.topic.pk)

