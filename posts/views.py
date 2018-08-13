from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import BlogPostForm
from django.db.models import Q

# Create your views here.
def posts_list(request):
    posts = Post.objects.all().order_by("-published_date")
    return render(request, "posts/posts_list.html", {'posts': posts})
    

def search_posts(request):
    query = request.GET['q']
    
    query_by_title = Q(title__contains=query)
    query_by_content = Q(content__contains=query)
    sorted_posts = Post.objects.filter(query_by_title | query_by_content).order_by("-published_date")
    return render(request, "posts/posts_list.html", {'posts': sorted_posts})

def show_views(request):
    posts = Post.objects.all().order_by("-views")
    return render(request, "posts/posts_list.html", {'posts': posts})

def show_likes(request):
    posts = Post.objects.all().order_by("-liked_by")
    return render(request, "posts/posts_list.html", {'posts': posts})   
    
def post_detail(request, id):
    post = get_object_or_404(Post, pk=id)
    post.views += 1
    post.save()
    
    can_edit = request.user == post.author or request.user.is_superuser
    does_like = request.user.profile in post.liked_by.all()
    
    return render(request, "posts/post_detail.html", {'post': post, 'can_edit': can_edit, 'does_like': does_like})

def add_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("posts_list")  
        else:
            return render(request, "posts/post_form.html", {"form": form})
    else:
        form = BlogPostForm()
        return render(request, "posts/post_form.html", {"form": form})



def edit_post(request, id):
    # Load the post we're changing, from the DB
    post = get_object_or_404(Post, pk=id)

    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        return update_post(form)
    else:
        form = BlogPostForm(instance=post)
        return render(request, "posts/post_form.html", {"form": form})
    
    
def update_post(form):
    # Update the DB with the differences
    if form.is_valid():
        post = form.save()
        return redirect("post_detail", id=post.id) 
    else:
         return render(request, "posts/post_form.html", {"form": form})


    
