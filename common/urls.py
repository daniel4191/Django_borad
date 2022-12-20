from django.urls import path
from django.contrib.auth import views as auth_views


# code line
app_name = 'common'

urlpatterns = [
    # login 매핑
    # 설정되어있기를, LoginView를 사용하게 되면 registration 디렉토리에 들어있는 login.html을 찾는다.
    path('login/', auth_views.LoginView.as_view(
        # 하지만 LoginView의 기본설정에도 불구하고 이렇게 지정해주면
        # 이제는 common이라는 폴더 안에있는 login.html파일을 찾게된다.
        # common이라는 폴더는 templates안에 만들면 된다
        template_name='common/login.html'
    ), name='login'),
    # logout 매핑
    # 내장함수를 써줬기 때문에 따로 views는 안만져줘도 된다.
    path('logout/', auth_views.LogoutView.as_view(), name="logout")
]
