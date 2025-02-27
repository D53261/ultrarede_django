from django.shortcuts import get_object_or_404, redirect, render
from ultrarede.models import Comments, Posts, Users
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

@login_required(login_url='/ultrarede/login/')
def home(request):
    users = Users.objects.all()
    posts = Posts.objects.all().order_by('created_at')
    comments = Comments.objects.all()
    return render(request, 'home.html', {'posts': posts, 'users': users, 'comments': comments})

@login_required(login_url='/ultrarede/login/')
def perfil(request, id):
    try:
        user = Users.objects.get(id=id)
    except Users.DoesNotExist:
        return render(request, 'profile.html', {'error': 'Usuário não encontrado.'})

    posts = Posts.objects.filter(user=user)
    comments = Comments.objects.all()

    return render(request, 'profile.html', {'user': user, 'posts': posts, 'comments': comments})

@login_required(login_url='/ultrarede/login/')
def profile(request):
    user = request.user
    posts = Posts.objects.filter(user=user)
    comments = Comments.objects.all()

    return render(request, 'profile.html', {'user': user, 'posts': posts, 'comments': comments})

@login_required(login_url='/ultrarede/login/')
def posts(request):
    if request.method == 'GET':
        return render(request, 'posts.html')
    elif request.method == 'POST':
        user = request.user
        content = request.POST.get('content')
        picture = request.FILES.get('picture')
        functioning = ''

        if not content and not picture:
            functioning = 'Preencha os campos'
            return render(request, 'posts.html', {'functioning': functioning})
        
        post = Posts.objects.create(
            user=user,
            content=content,
            picture=picture
        )

        post.save()
        return redirect('profile')

@login_required(login_url='/ultrarede/login/')
def logout_view(request):
    logout(request)
    return redirect('login')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        functioning = ''


        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        elif username == '' or password == '':
            functioning = "Preencha todos os campos"
            return render(request, 'login.html', {'functioning': functioning})
        elif Users.objects.filter(username=username).exists() == False:
            functioning = "Este usuário não está cadastrado"
            return render(request, 'login.html', {'functioning': functioning})
        else:
            functioning = "A senha está incorreta"
            return render(request, 'login.html', {'functioning': functioning})

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        functioning = ''

        if Users.objects.filter(username=name).exists() or Users.objects.filter(email=email).exists():
            functioning = "Usuário já cadastrado" 
            return render(request, 'signup.html', {'functioning': functioning})       
        elif password != confirm_password:
            functioning = "As senhas não conferem"
            return render(request, 'signup.html', {'functioning': functioning})
        elif name == "" or email == "" or password == "" or confirm_password == "":
            functioning = "Por favor, preencha todos os campos"
            return render(request, 'signup.html', {'functioning': functioning})
        
        user = Users.objects.create_user(
            username=name,
            email=email,
            password=password
        )

        user.save()
        return redirect('login')


@login_required(login_url='/ultrarede/login/')
def description(request):
    if request.method == 'POST':
        user = request.user
        description = request.POST.get('description')

        Users.objects.filter(username=user.username).update(description=description)
        return redirect('profile')
    
@login_required(login_url='/ultrarede/login/')
def change_description(request):
    user = request.user

    Users.objects.filter(username=user.username).update(description='')
    return redirect('profile')

@login_required(login_url='/ultrarede/login/')
def search(request):
    search = request.GET.get('input')
    try:
        user = Users.objects.get(username=search)
        posts = Posts.objects.filter(user=user).order_by('created_at')
        comments = Comments.objects.all()
        users = [user]
    except Users.DoesNotExist:
        posts = Posts.objects.none()
        users = []
        comments = Comments.objects.none()

    return render(request, 'home.html', {'users': users, 'posts': posts, 'comments': comments})

@login_required(login_url='/ultrarede/login/')
def picture(request):
    if request.method == 'POST':
        user = request.user
        picture = request.FILES.get('picture')

        if picture:
            user.picture = picture
            user.save()  

        return redirect('profile')
    
@login_required(login_url='/ultrarede/login/')
def change_picture(request):
    user = request.user

    Users.objects.filter(username=user.username).update(picture=None)
    return redirect('profile')

@login_required(login_url='/ultrarede/login/')
def comment(request, id):
    content = request.POST.get('comment')
    post = Posts.objects.get(id=id)
    user = request.user

    comments = Comments.objects.create(
        user=user,
        content=content,
        post=post
    )

    comments.save()
    return redirect('home')

@login_required(login_url='/ultrarede/login/')
def exclude(request, model, id):
    model_mapping = {
        'Comments': Comments,
        'Posts': Posts,
        'Users': Users,
    }

    if model not in model_mapping:
        print('Model inválido')
        return redirect('home')

    try:
        model_class = model_mapping[model]
        obj = get_object_or_404(model_class, id=id) 
        obj.delete()
        print(f"{model} excluído com sucesso.")
        if model_class == Users:
            Posts.objects.filter(user=id).delete()
            Comments.objects.filter(user=id).delete()
    except Exception as e:
        print(f"Erro ao deletar {model}: {e}")

    return redirect('home')


