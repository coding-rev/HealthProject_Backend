from django.urls import path
from .import views 

urlpatterns = 'users'   

urlpatterns=[
	path('register', views.RegistrationView.as_view(), name='register'),
	path('login', views.LoginView.as_view(), name="login"),
	path('logout', views.Logout.as_view(), name="logout"),

	# users
	path("all-doctors", views.GetAllDoctorsView.as_view(), name="all-doctors"),
	path("all-patients", views.GetAllPatientsView.as_view(), name="all-patients"),

	# updates
	path('edit-profile-pic/<int:id>', views.EditProfilePicView.as_view(), name="profile-pic"),
	path('edit/delete/user/<int:id>', views.EditUser.as_view(), name="edit-user-info"),

	# Delete

]