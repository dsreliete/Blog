from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

class UserRole (models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return 'id: {0} and desc: {1}'.format(self.id, self.description)

class UserProfile (models.Model):
    user_role = models.ForeignKey(UserRole, related_name="role", on_delete=models.CASCADE)

    # Return True if user is a submitter
    def isSubmitter(self):
        return self.user_role.id == UserRole.objects.get(id=1).id

    # Return True if user is an editor
    def isEditor(self):
        return self.user_role.id == UserRole.objects.get(id=2).id

    # Return True if user is an administrator
    def isAdministrator(self):
        return self.user_role.id == UserRole.objects.get(id=3).id

    # Return the user role description
    def userRoleName(self):
        return UserRole.objects.get(id=self.user_role.id).description

    def __str__(self):
        return 'id: {0} and role: {1}'.format(self.id, self.user_role)
