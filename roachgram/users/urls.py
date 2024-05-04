from django.urls import path
from . import views
from django.contrib.auth import views as authViews

urlpatterns = [
    # auth routes
    path("register" , views.registeration , name="register-user"),
    path("login" , authViews.LoginView.as_view(template_name="login.html" , redirect_authenticated_user=True) , name="login-user"),
    path("logout" , authViews.LogoutView.as_view() , name="logout-user"),

    # profile route
    path("profile/",  views.updateUser , name="update-user"),

    # change password route
    path("change-password" , views.changesPassword , name="change-password"),

    # password reset
    path("password-reset-done" , authViews.PasswordResetDoneView.as_view(template_name="password_reset_done.html") , name="password-reset-done"),
    path("password-reset" , views.ResetPassword.as_view() , name="password-reset"),
    path("password-reset-confirm/<uidb64>/<token>/" , authViews.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html") , name="password_reset_confirm"),
    path("password-reset-complete" , authViews.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html") , name="password_reset_complete"),

    path("<str:username>/" , views.userPage , name="user-page"),
    path("<str:username>/likes" , views.userPageLikes , name="user-page-likes"),
    path("<str:username>/replies" , views.userPageReplies , name="user-page-replies"),
    path("<str:username>/follow/" , views.followUser , name="follow-user"),
    path("<str:username>/unfollow/" , views.unfollowUser , name="unfollow-user"),
    path("<str:username>/followers" , views.userFollowers , name="user-followers-page"),
    path("<str:username>/followings" , views.userFollowings , name="user-followings-page"),
    
    
    
]