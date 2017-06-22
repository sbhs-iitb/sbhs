from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os, requests
from sbhs_server import settings
from django.http import HttpResponse
from myadmin.views import checkadmin
from sbhs_server.tables.models import Board


def load_image(mid):
    """ Displays the image of the SBHS onto the user screen.
    
        Input: mid: machine-id of the concerned SBHS.
    """
# for images on server 15, it will gstream the photos on reload
    if int(mid) in range(8,17):
    	command = "streamer -q -f jpeg -c /dev/video" + str(mid)
    	command += " -o " + settings.WEBCAM_DIR + "/image" + str(mid) + ".jpeg" 
    	os.system(command)

    else:
	take_snapshot = requests.get("http://10.102.152.16:8080/webcams/%d/take_snapshot" % int(mid))
        get_image_link = "http://10.102.152.16:8080/webcams/%d/get_image_data"  % int(mid)
        
        command = "curl -s %s > %s/image%d.jpeg" % (get_image_link, str(settings.WEBCAM_DIR), int(mid))
        os.system(command)
def reload(req, mid):
    """ Refreshes the image of the SBHS
    
        Input: req:request object, mid: machine-id of the concerned SBHS.
        Output: HttpResponse object.
    """
    load_image(mid)
    return HttpResponse("")

@login_required(redirect_field_name=None)
def show_video(req):
    """ Shows the video of the SBHS.
    
        Input: req:request object.
        Output: HttpResponse object.
    """
    board = req.user.board

    image_link = board.image_link()
    mid = str(board.mid)    

#	image_link = board.image_link()

    return render(req, "webcam/show_video.html", {"image_link": image_link, "mid": mid})


@login_required(redirect_field_name=None)
def show_video_to_admin(req, mid):
    """ Shows the video of the SBHS to the admin.
    
        Input: req:request object.
        Output: HttpResponse object.
    """
    checkadmin(req)
    board = Board.objects.get(mid=int(mid))
    image_link = board.image_link()
    mid = str(board.mid)
    return render(req, "webcam/show_video.html", {"image_link": image_link, "mid": mid})
