# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
import datetime
from django.db import models

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []
        # check DB for post_data['email']
        if len(self.filter(email=post_data['email'])) > 0:
            # check this user's password
            user = self.filter(email=post_data['email'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('email/password incorrect')
        else:
            errors.append('email/password incorrect')

        if errors:
            return errors
        return user

    def validate_registration(self, post_data):
        errors = []
        # check length of name fields
        if len(post_data['first_name']) < 2 or len(post_data['last_name']) < 2:
            errors.append("name fields must be at least 3 characters")
        # check length of name password
        if len(post_data['password']) < 8:
            errors.append("password must be at least 8 characters")
        # check name fields for letter characters 
        # if not post_data['first_name'].isalpha():           
        if not re.match(NAME_REGEX, post_data['first_name']) or not re.match(NAME_REGEX, post_data['last_name']):
            errors.append('name fields must be letter characters only')
        # check emailness of email
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("invalid email")
        # check uniqueness of email
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors.append("email already in use")
        # check password == password_confirm
        if post_data['password'] != post_data['confirmation_password']:
            errors.append("passwords do not match")

        if not errors:
            # make our new user
            # hash password
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                first_name=post_data['first_name'],
                last_name=post_data['last_name'],
                email=post_data['email'],
                password=hashed
            )
            return new_user
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    objects = UserManager()
    def __str__(self):
        return self.email


class Poke(models.Model):
    pokes = models.ForeignKey(User, related_name="userwhopoke")
    poked_by = models.ManyToManyField(User, related_name='pokes')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __repr__(self):
        return "Poke: \n{}\n{}\n{}\n".format(self.pokes, self.poked_by, self.created_at)
    




# class Poke(models.Model):
# 	poker = models.ForeignKey(User, related_name="userwhopoke")
# 	poked = models.ForeignKey(User, related_name="beingpoked")
# 	created_at = models.DateField(null=True)
# 	counter = models.IntegerField(blank=False, default=0, null=True)
# 	total = models.IntegerField(blank=False, default=0, null=True)
	# class Meta:
    # 		db_table = 'poke'
		

# class Poke(models.Model):
#     # poker = models.ForeignKey(User, related_name="pokerpokes")
# 	# poked = models.ForeignKey(User, related_name="pokedpokes")
#     pokes = models.ManyToManyField('self', related_name="poked_by")
# 	# created_at = models.DateField(auto_now_add = True) 
# 	counter = models.IntegerField(blank=False, default=0, null=True)
# 	total = models.IntegerField(blank=False, default=0, null=True)
#     def __str__(self):
# return self.pokes
