from django.shortcuts import render, HttpResponse, redirect
from .models import User, Quote, Favorite
import bcrypt
from django.contrib import messages

def index(request):
    return render(request, "exam/login.html")

def login(request):
	if request.method == "POST":
		#do this
		#return render(request, "login/success.html")
		answer = User.userManager.login(request.POST.get('email'), request.POST.get('password'))
		if answer.has_key('errors'):
			messages.add_message(request, messages.ERROR, answer['errors'])
			return redirect('/')
		else:
			theUser = answer['theUser']
			request.session['user'] = theUser.first_name
			request.session['id'] = theUser.id
			return redirect('/home')
	else:
		return redirect('/')

def register(request):
	if request.method == "POST":
		#do this
		answer = User.userManager.register(request.POST.get('first'), request.POST.get('last'), request.POST.get('email'), request.POST.get('password'), request.POST.get('confirm'))
		print(answer)
		if answer.has_key('errors'):
			if len(answer['errors']) > 1:
				for error in answer['errors']:
					messages.add_message(request, messages.ERROR, error)
				return redirect('/')
			else:
				messages.add_message(request, messages.ERROR, answer['errors'])
				return redirect('/')	
		else:
			return redirect('/')
	else:
		return redirect('/')

def home(request):
	quotes = Quote.quote_manager.all()
	user = User.userManager.get(id=request.session['id'])
	favorites = Favorite.objects.filter(user = user)
	for fave in favorites:
		quotes = quotes.exclude(id=fave.quote.id)
	context = {"quotes": quotes, "favorites": favorites}
	return render(request, "exam/index.html", context)

def addQuote(request):
	if request.method == "POST":
		user = User.userManager.get(id=request.session['id'])
		answer = Quote.quote_manager.validate(request.POST.get('author'),request.POST.get('text'),user)
		if answer.has_key('errors'): 
			if len(answer['errors']) > 1:
				for error in answer['errors']:
					messages.add_message(request, messages.ERROR, error)
				return redirect('/home')
			else:
				messages.add_message(request, messages.ERROR, answer['errors'])
				return redirect('/home')
		else:
			return redirect('/home')
	return redirect('/home')

def addToFavorites(request, id):
	user = User.userManager.get(id = request.session['id'])
	quote = Quote.quote_manager.get(id = id)
	favorite = Favorite.objects.create(user = user, quote = quote)
	return redirect('/home')

def removeFavorite(request,id):
	favorite = Favorite.objects.get(id=id)
	favorite.delete()
	return redirect('/home')

def userPage(request, id):
	user = User.userManager.get(id = id)
	quotes = Quote.quote_manager.filter(user = user)
	context = {"user": user, "quotes": quotes}
	return render(request, "exam/userPage.html", context)

def logout(request):
	request.session.pop('id', None)
	request.session.pop('user', None)
	return redirect('/')