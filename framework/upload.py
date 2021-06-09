import config
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config as AWSConfig
import io.BytesIO

class Upload:
	
	ALLOWED_EXTENSIONS=config.ALLOWED_EXTENSIONS
	ALLOWED_MIME=config.ALLOWED_MIME
	
	LOCAL_UPLOAD_FOLDER=config.LOCAL_UPLOAD_FOLDER
	LOCAL_UPLOAD_LINK=config.LOCAL_UPLOAD_LINK
	
	
	AWS_ACCESS_KEY_ID=config.AWS_ACCESS_KEY_ID
	AWS_ACCESS_KEY_SECRET=config.AWS_ACCESS_KEY_SECRET
	AWS_REGION=config.AWS_REGION
	AWS_BUCKET=config.AWS_BUCKET
	AWS_BUCKET_FOLDER=config.AWS_BUCKET_FOLDER
	AWS_BUCKET_LINK=config.AWS_BUCKET_LINK

	def __init__(self, file, allowed_extensions=[], allowed_mime=[]):
		self.allowed_extensions = (allowed_extensions + self.ALLOWED_EXTENSIONS) if self.and hasattr(self. 'ALLOWED_EXTENSIONS') else allowed_extensions
		self.allowed_mime = (allowed_mime + self.ALLOWED_MIME) if self.and hasattr(self. 'ALLOWED_MIME') else allowed_mime
		
		self.file = file
		name, ext = self.get_file_ext(file.name)
		self.meta = {
			'full_name': file.name,
			'name': name,
			'ext': ext,
			'mime': file.type
		}
		self.full_name, self.name, self.ext, self.mime = [self.meta['full_name'], self.meta['name'], self.meta['ext'], self.meta['mime']]
		
		self.check()
	
	def check(self):
		if not self.meta['ext'] or self.meta['ext'] not in allowed_extensions or self.meta['mime'] not in allowed_mime or not self.meta['name']:
			raise Exception("File type not allowed")
	
	def save_local(self, name=None, ext=None, dir=None, private=False):
		name = name if name else self.meta['name']
		ext = ext if ext else self.meta['ext']
		path = os.path.join(self.LOCAL_UPLOAD_FOLDER, dir)
		
		self.upload_type = 'local'
		self.save_dir = dir
		self.save_name = save_name = "{}.{}".format(name, ext)
		self.save_full_path = save_full_path = os.path.join(path, save_name)
		
		self.save_file(save_full_path)
		
		return self
	
	def save_aws(self, name=None, ext=None, dir=None, private=False):
		name = name if name else self.meta['name']
		ext = ext if ext else self.meta['ext']
		aws_upload_folder = self.AWS_UPLOAD_FOLDER if hasattr(self. 'AWS_BUCKET_FOLDER') and self.AWS_UPLOAD_FOLDER else '/'
		path = os.path.join(aws_upload_folder, dir).replace("\\","/")
		acl = "public-read" if not private else "private"
		
		self.upload_type = 'aws'
		self.save_dir = dir
		self.save_name = save_name = "{}.{}".format(name, ext)
		self.save_full_path = save_full_path = os.path.join(path, save_name)
		
		s3 = boto3.client('s3',
			aws_access_key_id=self.AWS_ACCESS_KEY_ID,
			aws_secret_access_key=self.AWS_ACCESS_KEY_SECRET,
			region_nam =self.AWS_REGION
		)
		try:
			s3.upload_fileobj(io.BytesIO(self.file.body), self.AWS_BUCKET, save_full_path,
				ExtraArgs={'ContentType': self.meta['mime'], 'ACL': acl}
			)
		except ClientError as e:
			raise Exception(e)
			
		return self
			
	def public_link(self, name=None, dir=None, upload_type=None):
		dir = dir if dir else self.save_dir
		name = name if name else self.save_name
		upload_type = upload_type if upload_type else self.upload_type
		
		if upload_type == 'local':
			return "{}/{}/{}".format(self.LOCAL_UPLOAD_LINK, dir, name)
		
		if upload_type == 'aws':
			return "{}/{}/{}".format(self.AWS_BUCKET_LINK, dir, name)
			
	def get_file_ext(name):
		fn = name.rsplit('.', 1)
		fd = {
			'name': fn[0] if len(fn) > 0 and fn[0] else False,
			'ext': fn[1].lower() if len(fn) > 1 and fn[1] else False
		}
		return [fd['name'],fd['ext']]
		
	def save_file(self, dst, buffer_size=16384):
        from shutil import copyfileobj
        close_dst = False
        if isinstance(dst, string_types):
            dst = open(dst, 'wb')
            close_dst = True
        try:
            copyfileobj(self.file.body, dst, buffer_size)
        finally:
            if close_dst:
                dst.close()