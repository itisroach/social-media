# RoachGram

RoachGram is a social media platform where users can share their thoughts and posts and whatever they like also can interact with each other.



## API Endpoints

* #### this porject also has API endpoints for authentication, creating posts, etc....

* ##### regiseter endpoint: /api/auth/register/

* ##### login endpoint: /api/auth/login/

* ##### chanege user information endpoint: /api/auth/edit-user/

* ##### change user password: /api/auth/change-password/

* ##### get all users: /api/users/

* ##### get user's notifications: /api/users/notifications/

* ##### search users: /api/users?search=(search query)/

* ##### following and unfollowing an user endpoint: /api/auth/follow/ (if already followed it will unfollow)

* ##### get single user enpoint: /api/users/<username>/

* ##### get single user followers endpoint: /api/users/<useranme>/followers/

* ##### get single user followings endpoint: /api/users/<username>/followings/

* ##### get all posts: /api/posts/ (depends on user's followings) 

* ##### search posts: /api/posts/find?search=(search query)

* ##### creating a post: /api/posts/ (POST METHOD)

* ##### deleting a post: /api/posts/ (DELETE METHOD)

* ##### get single post: /api/posts/(id)

* ##### get post's comments: /api/posts/(id)/comments

* ##### creating a comment: /api/posts/(id)/comments (POST METHOD)

* ##### deleting a comment: /api/posts/(id)/comments (DELETE METHOD)

* ##### get an user's posts: /api/posts/users/(username)

* ##### like and unlike a post: /api/posts/like (POST METHOD AND IF ALREADY LIKED IT WILL UNLIKE IT)

* ##### bookmark and remove bookmark of a post: /api/posts/bookmark (POST METHOD AND IFALREADY BOOKMARKED IT WILL REMOVE FROM BOOKMARKS)

## websocket urls:

* ##### /chats/<room name>/ (room name contains logged in user id and user the logged in user wants to chat wit, like this: "LOGGEDINUSER-ANOTHERUSER")

* #### /notifications/<username>/ always connected to this for receiving realtime notifications and send request to add notification in these actions -> ["follow" , "like" , "comment" , "bookmark"]. data needed for this route is =>  type: on of previous listed request, user_to_notif: user we want to send notification to, triggered_by: user who performed action  

* #### /notification/<username>/<last-notif-id>/seen/ when user enters to notification page send request with last notification id to mark notification as seen. no data needed except those in url 


* #### RoachGram is live on: [https://amiraliashoori6.pythonanywhere.com/](https://amiraliashoori6.pythonanywhere.com/)

# Notes

* Be aware that I didn't spend much time on UI of this project.

* main purpose of this project is to improve my skills and learn new things as a junior programmer.

* the authentication of this project is JWT based.

* when using API if user is not logged in gets latest 15 posts and if they are logged in get posts of their followers and suggest some posts to them (for detecting if a post is suggested or not, you should check if the user is following the author of post)

* this website is hosted for free on [pythonanywhere](https://pythonanywhere.com/).

* beacuse the website is free hosted it's a little slow

* the media that users upload will be stored on server not on a cloud platform (because of some limitations) and only image types accepted because of that.

* API uses [cursor pagination](https://www.django-rest-framework.org/api-guide/pagination/#cursorpagination) when fetching large data for improving response time.
