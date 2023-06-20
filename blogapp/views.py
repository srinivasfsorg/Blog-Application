from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.views.decorators.http import require_POST


def post_list(request):
    post_list = Post.published.all()
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
     posts = paginator.page(page_number)
    except PageNotAnInteger:
    # If page_number is not an integer deliver the first page
     posts = paginator.page(1)
    except EmptyPage:
      # If page_number is out of range deliver last page of results
      posts = paginator.page(paginator.num_pages)
    return render(request,
                 'blogapp/post/list.html',
                 {'posts': posts})


def post_detail(request,  year, month, day, post):
    post = get_object_or_404(Post,
                             
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    return render(request,
          'blogapp/post/detail.html',
           {'post': post,
          'comments': comments,
          'form': form})



class PostListView(ListView):
 """
 Alternative post list view
 """
 queryset = Post.published.all()
 context_object_name = 'posts'
 paginate_by = 3
 template_name = 'blogapp/post/list.html'

@require_POST
def post_comment(request, post_id):
 post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
 comment = None
 # A comment was posted
 form = CommentForm(data=request.POST)
 if form.is_valid():
 # Create a Comment object without saving it to the database
  comment = form.save(commit=False)
 # Assign the post to the comment
  comment.post = post
 # Save the comment to the database
  comment.save()
 return render(request, 'blogapp/post/comment.html',
 {'post': post,
 'form': form,
 'comment': comment})