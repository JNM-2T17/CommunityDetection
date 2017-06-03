from django.shortcuts import render
from .backend.driver import *
import json

def index(request):
	return render(request, 'thesis/index.html')

def vis(request):
	return render(request, 'thesis/vis.html')

def run(request):
	paramVal = request.POST['param']
	algoVal = request.POST['algo']
	start(paramVal, algoVal)
	directed = "true" if paramVal != "2" else "false"
	word_cloud = {}
	graph = {}
	with open('wordCounts.json') as json_data:
		word_cloud = json.load(json_data)
	with open('vis.json') as json_data:
		graph = json.load(json_data)
	context = {
		'word_cloud': word_cloud,
		'graph': graph,
		'directed': directed
	}
	return render(request, 'thesis/vis.html', context)