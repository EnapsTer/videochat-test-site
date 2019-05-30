"""views of the project"""
import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from googlesearch import search
import bleach
from django.db.models import Q, Count
from .models import *
from blogapp.forms import *


# region Main
def lending(request):
    """lending view"""
    context = {}
    return render(request, 'main/lending.html', context)


def main_page(request):
    """main page view"""
    post_list = Post.objects.annotate(total_comments=Count('comment'))
    tags = Tag.objects.all()
    users = User.objects.annotate(total_likes=Count('post__likes')).order_by('-total_likes')[:30]

    query = request.GET.get('q')
    if query:
        post_list = Post.objects.filter(
            Q(title__icontains=query) |
            Q(author__username__icontains=query) |
            Q(body__icontains=query)
        )

    tag = request.GET.get('searchtag')
    if tag:
        post_list = Post.objects.filter(tag__tag_name=tag)

    user = request.GET.get('searchuser')
    if user:
        post_list = Post.objects.filter(author=user)

    paginator = Paginator(post_list, 7)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if page is None:
        start_index = 0
        end_index = 7
    else:
        (start_index, end_index) = proper_pagination(posts, index=4)

    page_range = list(paginator.page_range)[start_index:end_index]

    q_tag = request.GET.get('qtag')
    if q_tag:
        tags = Tag.objects.filter(tag_name__icontains=q_tag)

    context = {'posts': posts,
               'page_range': page_range,
               'query': query,
               'tags': tags,
               'searchtag': tag,
               'users': users}

    if request.is_ajax():
        html = render_to_string('main/tag_section.html', context, request=request)
        return JsonResponse({'form': html})

    return render(request, 'main/main_page.html', context)


def proper_pagination(posts, index):
    """pagination function"""
    start_index = 0
    end_index = 7
    if posts.number > index:
        start_index = posts.number - index
        end_index = start_index + end_index
    return start_index, end_index


def chat_page(request, id, key):
    """chat (post) page view"""
    post = get_object_or_404(Post, id=id, private_key=key)
    comments = Comment.objects.filter(post=post).order_by('-timestap')

    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(
                post=post, user=request.user, content=content)
            comment.save()
    else:
        comment_form = CommentForm()

    context = {'post': post,
               'is_liked': is_liked,
               'comments': comments,
               'comment_form': comment_form,
               }
    try:
        context['links'] = recommend_links(post)
    except BaseException:
        pass

    if request.is_ajax():
        html = render_to_string('main/comment_section.html', context, request=request)
        return JsonResponse({'form': html})
    return render(request, 'main/chat_page.html', context)
# endregion


# region Post
@login_required
def like_post(request):
    """like post function"""
    post = get_object_or_404(Post, id=request.POST.get('id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    context = {'post': post,
               'is_liked': is_liked}
    if request.is_ajax():
        html = render_to_string('main/like_section.html', context, request=request)
        return JsonResponse({'form': html})


@login_required
def post_create(request):
    """post create view"""
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if request.POST.get('private'):
                post.private = 1
                key = ''.join(
                    [random.choice(string.ascii_lowercase + string.digits) for n in range(24)])
                post.private_key = key
            post.author = request.user
            post.save()
            post_tags = request.POST.getlist('tags')
            for post_tag in post_tags:
                post.tag.add(post_tag)
            return redirect('blogapp:post_recommend', id=post.id, key=post.private_key)
    else:
        form = PostCreateForm()

    tags = Tag.objects.all()
    q_tag = request.GET.get('qtag')
    if q_tag:
        tags = Tag.objects.filter(tag_name__icontains=q_tag)

    context = {
        'postform': form,
        'tags': tags,
    }

    if request.is_ajax():
        html = render_to_string('main/tag_section_create.html', context, request=request)
        return JsonResponse({'form': html})

    return render(request, 'main/post_create.html', context)


@login_required()
def post_edit(request, id):
    """post edit view"""
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        raise Http404()
    if request.method == 'POST':
        form = PostEditForm(request.POST or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if request.POST.get('private') and post.private_key == 'public':
                post.private = 1
                key = ''.join([random.choice(string.ascii_lowercase + string.digits) for n in range(24)])
                post.private_key = key
            if request.POST.get('private') is None and post.private_key != 'public':
                post.private = 0
                post.private_key = 'public'
            post.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostEditForm(instance=post)
    context = {'form': form,
               'post': post}
    return render(request, 'main/post_edit.html', context)


@login_required()
def post_delete(request, id):
    """post delete function"""
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        raise Http404
    post.delete()
    return redirect('main_page')


def recommend_links(post):
    query = "site:stackoverflow.com " + post.title
    try:
        query += bleach.clean(post.body, tags=[], attributes={}, styles=[], strip=True)
    except BaseException:
        pass

    recommend_array = []
    for url in search(query, tld="com", num=5, stop=5, pause=2):
        recommend_array.append(url)

    if len(recommend_array) < 5:
        length = 5 - len(recommend_array)
        query = "" + post.title
        try:
            query += bleach.clean(post.body, tags=[], attributes={}, styles=[], strip=True)
        except BaseException:
            pass
        recommend_array = []
        for url in search(query, tld="com", num=length, stop=length, pause=2):
            recommend_array.append(url)

    return recommend_array


@login_required()
def post_recommend(request, id, key):
    """post recommend view + search"""
    post = get_object_or_404(Post, id=id, private_key=key)
    context = {}
    try:
        context['links'] = recommend_links(post)
    except BaseException:
        pass

    if post.private:
        context['private_link'] = post.get_absolute_url()

    return render(request, 'main/post_recommend.html', context)
# endregion


# region Authentication
def user_login(request):
    """user login view"""
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('main_page'))
                else:
                    return HttpResponse('User is not active')
            else:
                context = {
                    'form': form,
                    'error': 'User with this login is not exist, or password is incorrect.'
                }
                return render(request, 'main/login.html', context)
    else:
        form = UserLoginForm()

    context = {
        'form': form
    }
    return render(request, 'main/login.html', context)


def user_logout(request):
    """user logout view"""
    logout(request)
    return redirect('main_page')


def register(request):
    """user registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('main_page')
    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'registration/register.html', context)


def check(request):
    """view that checks data from third parties auth"""
    if request.method == 'POST':
        edit_form = UserEditForm(request.POST or None, instance=request.user)
        profile_form = ProfileForm(
            request.POST or None, files=request.FILES, instance=request.user.profile)
        if edit_form.is_valid():
            edit_form.save()
            profile_form.save()
            return redirect('main_page')

    try:
        request.user.profile
    except BaseException:
        Profile.objects.create(user=request.user)

    if request.user.email == '' or request.user.first_name == ''\
            or request.user.last_name == '' or request.user.username == '':
        edit_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        context = {
            'form': edit_form,
            'profile': profile_form
        }
        return render(request, 'main/check.html', context)

    return redirect('main_page')
# endregion   


# region Profile
@login_required
def profile(request, id):
    """user profile page view"""
    if User.objects.get(id=id) is not None:
        user = User.objects.get(id=id)
        posts_count = Post.objects.filter(author=user).count()
        context = {
            'posts_count': posts_count,
            'user': user,
        }
        return render(request, 'main/profile.html', context)
    else:
        raise Http404()


@login_required
def edit_profile(request):
    """user edit profile view"""
    if request.method == 'POST':
        edit_form = UserEditForm(request.POST or None, instance=request.user)
        profile_form = ProfileForm(
            request.POST or None, files=request.FILES, instance=request.user.profile)
        if edit_form.is_valid():
            edit_form.save()
            profile_form.save()
            return redirect('main_page')
    else:
        edit_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    context = {
        'form': edit_form,
        'profile': profile_form
    }
    return render(request, 'main/edit_profile.html', context)


@login_required()
def user_delete(request, id):
    """user delete function"""
    user = get_object_or_404(User, id=id)
    profile = Profile.objects.get(user=user)
    if request.user != user:
        raise Http404
    user.delete()
    profile.delete()
    return redirect('main_page')
# endregion


# region Comment
@login_required()
def comment_delete(request, id, comid):
    """comment delete function"""
    comment = get_object_or_404(Comment, id=comid)
    if request.user != comment.user and not request.user.is_staff:
        raise Http404

    comment.delete()

    post = Post.objects.get(id=id)
    comments = Comment.objects.filter(post=post).order_by('-timestap')
    comment_form = CommentForm()

    context = {'post': post,
               'comments': comments,
               'comment_form': comment_form
               }

    if request.is_ajax():
        html = render_to_string('main/comment_section.html', context, request=request)
        return JsonResponse({'form': html})


def comment_refresh(request, id):
    """comment refresh function"""
    post = get_object_or_404(Post, id=id)
    comments = Comment.objects.filter(post=post).order_by('-timestap')
    comment_form = CommentForm()

    context = {'post': post,
               'comments': comments,
               'comment_form': comment_form
               }

    if request.is_ajax():
        html = render_to_string('main/comment_section.html', context, request=request)
        return JsonResponse({'form': html})
# endregion







