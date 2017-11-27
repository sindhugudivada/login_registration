from __future__ import unicode_literals
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import bcrypt
my_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class BlogManager(models.Manager):
    def basic_validator_registration(self, postData):
        errors = {}
        print "checking postdata",postData
        print len(postData['fname'])
        print postData['fname'].isalpha()
        if len(postData['fname']) < 2 and postData['fname'].isalpha() == False:
            errors['fname'] = " firstname should be more than 2 characters"
        if len(postData['lname']) < 2 and postData['lname'].isalpha() == False:
            errors['lname'] = " lastname should be more than 2 characters" 
        if len(postData['email']) < 1 or not EMAIL_REGEX.match(postData['email']):
            errors['email']="Invalid Email format!"
        if len(postData['password']) < 8:
            errors['password'] = "password should be greater than 8"
        if postData['password'] != postData["confirm_password"]:
            errors['password']="Passwords are not matching!"
        return errors
    def basic_validator_login(self, postData):
        errors = {}
        hash1 = postData['password'].encode()
        if not my_re.match(postData['email']):
            errors['email'] = "Enter a valid email id"
        if len(postData['email']) < 1:
            errors['email']="please enter email!"
        if len(postData["password"]) < 1:
            errors['password']="no password"
        try:
            user = User.objects.get(email = postData['email'])
            if user:
                if bcrypt.checkpw(postData['password'].encode(),user.password.encode()):
                    print "logged in" 
                else:
                    errors['password']="password does not exists"    
        except:
            errors['email']="email does not exists"
        return errors    
        

class User(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BlogManager()
