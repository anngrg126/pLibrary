# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# Create your models here.

class userManager(models.Manager):
	def validateRegistration(self, postData):
		errors = []
		if len(postData['firstName'])<2 or len(postData['lastName'])<2:
			errors.append("Names should be 2 characters or more")
		if len(postData['pw'])<8:
			errors.append("Password should be more than 7 characters")
		if not re.match(NAME_REGEX, postData['firstName']) or not re.match(NAME_REGEX, postData['lastName']):
			errors.append("Name format not valid")	
		if not re.match(EMAIL_REGEX, postData['email']):
			errors.append("Invalid Email")
		if postData['pw'] != postData['confirmPw']:
			errors.append("Passwords do not match")

		hashed = bcrypt.hashpw((postData['pw'].encode()), (bcrypt.gensalt(5)))


		if not errors:
			newUser = self.create(
				firstName = postData['firstName'], 
				lastName = postData['lastName'],
				email = postData['email'],
				password = hashed, 

				)
			return newUser
			#create a new user
			#return new user
		return errors 

	def validateLogin(self, postData):
		errors = []

		if len(self.filter(email = postData['email']))>0:
			user = self.filter(email= postData['email'])[0]
			if not (bcrypt.checkpw((postData['pw'].encode()), (user.password.encode()))):
				errors.append("Invalid Password")
		else:
			errors.append("Invalid Email")

		if not errors: 
			return user
		return errors

class User(models.Model):
	firstName = models.CharField(max_length = 45)
	lastName = models.CharField(max_length = 45)
	email = models.EmailField(unique = True)
	password = models.CharField(max_length = 45)

	objects = userManager()

	def __str__(self):
		return self.firstName