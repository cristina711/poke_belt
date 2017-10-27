# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import User
from django.shortcuts import render, redirect
# from apps.poke.models import User, Poke
from django.db.models import Count
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'pokeapp/index.html')

def register(request):
    result = User.objects.validate_registration(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully registered!")
    return redirect('/success')

def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully logged in!")
    return redirect('/success')

def success(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'pokeapp/success.html', context)


def poke(request):

    poke = Poke.objects .get(id=poke_id)
    poked_by = User.objects.get(id= request.session['user_id']) 
    poke.poked_by . add(poked_by)

    return redirect('/poketable')





def poketable(request):
    	
	if "user_id" in request.session:
		users = User.objects.all().exclude(id=request.session['user_id'])
		pokes = Poke.objects.all().distinct('poked_id')
		user_poke_count = Poke.objects.all().filter(poked=request.session['user_id'])
		list_of_users = Poke.objects.filter(poked=request.session['user_id']).exclude(id=request.session['user_id']).distinct('poker')
		user = User.objects.get(id=request.session['user_id'])
		current_user = User.objects.get(id=request.session['user_id'])
		context = {'current_user': current_user,'user': user, 'users': users, 'pokes': pokes, 'user_poke_count': user_poke_count, 'list_of_users': list_of_users }
		return render(request, 'pokeapp/success.html', context)
	else:
		del request.session
		return redirect('/')

def pokeaction(request, user_id):
	poker = User.objects.get(id=request.session['user_id'])
	print (poker.first_name)
	poked = User.objects.get(id=user_id)
	print (poked.first_name)
	# Poke = Poke()
	Poke.poker = poker
	poke.poked = poked
	poke.created_at = timezone.now()
	poke.counter+=1
	poke.save()
	return redirect('/poketable')

def logout(request):
	print ("Logging Out")
	del request.session['user_id']
	return redirect('/')

# def logout(request):
#     request.session.clear()
#     return redirect('/')