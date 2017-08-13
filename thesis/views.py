from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .backend.driver import *
import json

def index(request):
	return render(request, 'thesis/index.html')

def vis(request):
	tweet_word_cloud = {}
	profile_word_cloud = {}
	graph = {}
	stats = {}
	with open('tweetWordCounts.json') as json_data:
		tweet_word_cloud = json.load(json_data)
	with open('profileWordCounts.json') as json_data:
		profile_word_cloud = json.load(json_data)
	with open('vis.json') as json_data:
		graph = json.load(json_data)
	with open('stats.json') as json_data:
		stats = json.load(json_data)
	context = {
		'tweet_word_cloud': tweet_word_cloud,
		'profile_word_cloud': profile_word_cloud,
		'graph': graph,
		'locations': stats["location"]
	}
	return render(request, 'thesis/index.html', context)

def run(request):
	paramVal = request.POST['param']
	algoVal = request.POST['algo']
	measureVal = request.POST['measure']
	k = None
	if 'kval' in request.POST:
		k = request.POST['kval']
	output = start(paramVal, algoVal, measureVal,k)
	request.session['output'] = output
	return HttpResponseRedirect(reverse('thesis:vis'))
