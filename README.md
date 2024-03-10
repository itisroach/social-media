# RoachGram

RoachGram is a social media platform where users can share their thoughts and post whatever they like and interact whit each other.



## API Endpoints

* #### this porject also has API endpoints for authentication, creating posts, etc....

* ##### regiseter endpoint: /api/auth/register

* ##### login endpoint: api/auth/login

* ##### chanege user information endpoint: api/auth/edit-user

* ##### change user password: api/auth/change-password

* ##### get all users: api/auth/users

* ##### following and unfollowing an user endpoint: api/auth/follow (if already followed it will unfollow)

* ##### get single user enpoint: api/auth/users/<username>

* ##### get all posts: api/posts/ (depends on user's followings) 

* ##### creating a post: api/posts/ (POST METHOD)

* ##### deleting a post: api/posts/ (DELETE METHOD)

* ##### get single post: api/posts/<id>

* ##### get post's comments: api/posts/<id>/comments

* ##### creating a comment: api/posts/<id>/comments (POST METHOD)

* ##### deleting a comment: api/posts/<id>/comments (DELETE METHOD)

* ##### get an user's posts: api/posts/users/<username>

* ##### like and unlike a post: api/posts/like (POST METHOD AND IF ALREADY LIKED IT WILL UNLIKE IT)

* ##### bookmark and remove bookmark of a post: api/posts/bookmark (POST METHOD AND IFALREADY BOOKMARKED IT WILL REMOVE FROM BOOKMARKS)


* #### RoachGram is live on: [https://roach.pythonanywhere.com/](https://roach.pythonanywhere.com/)

# Notes

* Be aware that I didn't spend much time on UI of this project.

* main purpose of this project is to improve my skills and learn new things as a junior programmer.

* the authentication of this project is JWT based.

* this website is hosted for free on [pythonanywhere](https://pythonanywhere.com/).

* the media that users upload will be stored on server not on a cloud platform (because of some limitations) and only image types accepted because of that.

* API uses [cursor pagination](https://www.django-rest-framework.org/api-guide/pagination/#cursorpagination) when fetching large data for improving response time.
