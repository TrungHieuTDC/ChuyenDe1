from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth  import authenticate,  login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm,BlogPostForm,CommentForm
from django.views.generic import UpdateView
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect 
from django.http import JsonResponse
from django.db.models import Count
#User
def Register(request):
    if request.method=="POST":   
        username = request.POST['username']
        password = request.POST['password']          
        re_password = request.POST['re_password']
        email = request.POST['email']
        gender = request.POST['gender']
        birthdate = request.POST['birthdate']
        avatar = request.FILES['avatar']
        if password != re_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/blog/register')   
        
        user = User.objects.create_user(username, email, password)
        user_profile = Profile(user=user, gender=gender, birthdate=birthdate,avatar=avatar)
        user_profile.save()
        messages.success(request, "Chỉnh sửa thành công!")
        return render(request, 'login.html')   
    return render(request, "register.html")
def Login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials")
        return render(request, 'base.html')   
    return render(request, "login.html")

def profile_user(request,user_id):
    user = get_object_or_404(User, id=user_id)
    context = {
        'user': user
    }
    return render(request, 'blog_profile.html', context)    
@login_required
def save_profile(request):
    if request.method == 'POST':
        # Lấy dữ liệu
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        birthdate = request.POST.get('birthdate')
        bio = request.POST.get('bio')
        avatar = request.FILES.get('avatar')
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
        # Cập nhật thông tin hồ sơ
        profile.user.email = email
        profile.gender = gender
        profile.birthdate = birthdate
        profile.bio = bio
        if avatar:
            profile.avatar = avatar

        # Lưu thông tin hồ sơ
        profile.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def get_loved_posts(user):
    loved_posts = BlogPost.objects.filter(love=user)
    return loved_posts
    
def user_posts(request, user_id):
    current_user = request.user
    loved_posts = get_loved_posts(current_user)
    user = get_object_or_404(User, id=user_id)
    blog_posts = BlogPost.objects.filter(user=user).order_by('-datetime')
    posts_per_page = 5
    if blog_posts.exists():
        paginator = Paginator(blog_posts, posts_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    # if loved_posts.exists():
    #     paginator1 = Paginator(loved_posts, posts_per_page)
    #     page_number1 = request.GET.get('page')
    #     page_objj = paginator1.get_page(page_number1)
    else:
        page_obj = None
    return render(request, 'blog_profile.html', {'user': user, 'page_obj': page_obj,'page_objj': loved_posts})

def Logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/login')

#Blogs
def blogs(request):
    published_posts = BlogPost.objects.filter(status='published').annotate(comment_count=Count('comment')).order_by('-datetime')
    random = BlogPost.objects.order_by('?')[:3]
    paginator = Paginator(published_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "blog_index.html", {'page_obj': page_obj, 'random': random})

def blogs_draft(request):
    draft_posts = BlogPost.objects.filter(status='draft').annotate(comment_count=Count('comment')).order_by('-datetime')
    return render(request, "blog_draft.html", {'posts': draft_posts})

def publish_blog(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    post.status = 'published'  
    post.save()
    messages.success(request, 'The blog post has been published successfully.')
    return redirect('/draft/')

def blogs_detail(request, slug):
    post = BlogPost.objects.filter(slug=slug).first()
    randoms = BlogPost.objects.order_by('?')[:2]
    random_recent = BlogPost.objects.order_by('?')[:3]  # Truy vấn 3 bài viết ngẫu nhiên
    comments = Comment.objects.filter(blog=post)
    if request.method=="POST":
        user = request.user
        content = request.POST.get('content')
        
        comment = Comment(user = user, content = content, blog=post)
        comment.save()
    post.views = post.views + 1
    post.save()
    return render(request, "blog_detail.html", {'post':post, 'comments':comments,'randoms':randoms,'random_recent':random_recent})
def manage(request):
    return render(request,"base_manage.html")

@login_required(login_url = '/login')
def blog_add(request):
    form = BlogPostForm()
    if request.method == "POST":
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = request.user
            blogpost = form.save(commit=False)
            blogpost.user = user
            blogpost.status = 'draft'  
            blogpost.save()
            object = form.instance
            alert = True
            return render(request, "blog_add.html", {'obj': object, 'alert': alert})
    else:
        form = BlogPostForm()
    return render(request, "blog_add.html", {'form': form})
def blog_delete(request, slug):
    post = BlogPost.objects.get(slug=slug)
    if request.method == "POST":
        is_draft = post.status == 'draft'
        post.delete()
        
        if is_draft:
            return redirect('/draft/')
        else:
            return redirect('/')
    
    return render(request, 'blog_delete.html', {'post': post, 'alert': True})
class UpdatePostView(UpdateView):
    model = BlogPost
    template_name = 'blog_edit.html'
    form_class = BlogPostForm
    # Ghi đè success_url
    def get_success_url(self):
        if self.object.status == 'draft':
            return '/draft/'  # Chuyển hướng về trang draft
        else:
            return '/'
    #Ghi đè get_form của UpdatePostView
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

def blog_search(request):
    query = request.GET.get('search')  
    random_search = BlogPost.objects.order_by('?')[:3]  # Truy vấn 3 bài viết ngẫu nhiên
    if query:
        # Tìm kiếm các bài viết có tiêu đề chứa query
        posts = BlogPost.objects.filter(Q(title__icontains=query))  
        paginator = Paginator(posts, 5)  
        page_number = request.GET.get('page')  
        page_obj = paginator.get_page(page_number) 
        context = {
        'posts': posts,
        'query': query,
        'random_search': random_search,
        'page_obj': page_obj, 
        }
        return render(request, 'blog_search_result.html', context)
    else:
        # Nếu không có query, hiển thị tất cả bài viết
        print("Empty")  
        posts = None
    return render(request, 'blog_search_result.html', {'posts': posts,'query': query})

def blog_random_post(request):
    random = BlogPost.objects.order_by('-datetime')[:3]  # Truy vấn 3 bài viết ngẫu nhiên
    return render(request, 'blog_recent.html', {'random': random})

def react_love_post(request, slug):
    post = BlogPost.objects.get(slug=slug)
    user = request.user

    if user in post.love.all():
        post.love.remove(user)
    else:
        post.love.add(user)

    post.save()
    #love_count = post.loved_posts.count()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def most_view_post(request):
    most_view_post = BlogPost.objects.annotate(total_comments=Count('comment')).order_by('-views') 
    paginator = Paginator(most_view_post, 5)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj, 
        } 
    return render(request, 'blog_most_views.html', context)
def most_loved_post(request):
    most_loved_posts = BlogPost.objects.annotate(total_love=Count('love')).annotate(total_comments=Count('comment')).order_by('-total_love')
    paginator = Paginator(most_loved_posts, 5)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj, 
    } 
    return render(request, 'blog_most_loved.html', context)
def most_comment_post(request):
    most_commented_posts = BlogPost.objects.annotate(total_comments=Count('comment')).order_by('-total_comments')
    paginator = Paginator(most_commented_posts, 5)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj, 
    } 
    return render(request, 'blog_most_comment.html', context)
def reply_comment(request, comment_id):
    if request.method == 'POST':
        parent_comment = Comment.objects.get(pk=comment_id)
        reply_text = request.POST.get('reply_text')
        Reply.objects.create(user=request.user, text=reply_text, parent=parent_comment)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    return JsonResponse({'message': 'Invalid request.'}, status=400)

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id) 
    # Kiểm tra xem người dùng hiện tại có quyền xóa bình luận hay không
    if comment.user == request.user:
        # Xóa tất cả các reply thuộc bình luận
        comment.replies.all().delete()
        # Xóa bình luận
        comment.delete() 
    blog_id = comment.blog.slug   
    return redirect(f'/blog/{blog_id}')

def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog_edit_comment', slug=comment.blog.slug)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'blog_edit_comment.html', {'form': form})




    