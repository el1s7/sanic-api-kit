import os
from functions import rand

class BaseConfig():

	#MYSQL
	DB_HOST = "localhost"
	DB_USER = "root"
	DB_PASS = ""
	DB_NAME = ""
      
	#File Uploads
	ALLOWED_EXTENSIONS=['jpg', 'jpeg', 'png', 'bmp', 'gif','jfif','pjpeg','pjp']
	ALLOWED_MIME=['image/bmp','image/jpeg','image/gif','image/png']
	MAX_CONTENT_LENGTH=3 * 1024 * 1024
	
	BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
	LOCAL_UPLOAD_FOLDER=os.path.join(BASE_DIR, 'public/uploads/')
	LOCAL_UPLOAD_LINK="/uploads"
	
	AWS_ACCESS_KEY_ID=""
	AWS_ACCESS_KEY_SECRET=""
	AWS_REGION=""
	AWS_BUCKET=""
	AWS_BUCKET_FOLDER=""
	AWS_BUCKET_LINK=""
	
	
	#Key Generating
	RANDOM_LENGTH = 32
	
	#JWT
	JWT_SECRET= rand()
	   
	#SMTP
	SMTP_USER = ""
	SMTP_PASS = ""


class DevConfig(BaseConfig):
	DEBUG = True
	

class ProdConfig(BaseConfig):
	DEBUG = False