from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os, requests
from sbhs_server import settings
from django.http import HttpResponse
from myadmin.views import checkadmin
from sbhs_server.tables.models import Board, Webcam
# Create your views here.
# 

def reload(req, mid):

	Webcam.load_image(mid)
	return HttpResponse("")

@login_required(redirect_field_name=None)
def show_video(req):
	board = req.user.board

	image_link = board.image_link()
	mid = str(board.mid)

	return render(req, "webcam/show_video.html", {"image_link": image_link, "mid": mid})


@login_required(redirect_field_name=None)
def show_video_to_admin(req, mid):
	checkadmin(req)
	board = Board.objects.get(mid=int(mid))
	image_link = board.image_link()
	mid = str(board.mid)
	return render(req, "webcam/show_video.html", {"image_link": image_link, "mid": mid})
