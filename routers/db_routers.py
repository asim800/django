

'''
will run after the setup
 -- settings.DATABASES is improperly configured
> manage.py migrate --database=auth_db
 -- please supply the engine value if you don't migrate

 -- connection doesn't exist if you misspell db name

> manage.py createsuperuser --database=auth_db

 -- add sessions and admin app if you want to use the admin here

'''

# class AuthRouter:
# 	"""
# 	A router to control all database operations on models in the
# 	auth and contenttypes applications.
# 	"""
# 	# redirecting to a different db based on app label
# 	route_app_labels = {'auth', 'contenttypes', 'sessions', 'admin'} 	# which apps are routed here

# 	def db_for_read(self, model, **hints):
# 		"""
# 		Attempts to read auth and contenttypes models go to auth_db.
# 		"""
# 		if model._meta.app_label in self.route_app_labels:
# 				return 'auth_db'
# 		return None

# 	def db_for_write(self, model, **hints):
# 		"""
# 		Attempts to write auth and contenttypes models go to auth_db.
# 		"""
# 		if model._meta.app_label in self.route_app_labels:
# 				return 'auth_db'
# 		return None

# 	def allow_relation(self, obj1, obj2, **hints):
# 		"""
# 		Allow relations if a model in the auth or contenttypes apps is
# 		involved.
# 		"""
# 		if (
# 				obj1._meta.app_label in self.route_app_labels or
# 				obj2._meta.app_label in self.route_app_labels
# 		):
# 				return True
# 		return None

# 	def allow_migrate(self, db, app_label, model_name=None, **hints):
# 		"""
# 		Make sure the auth and contenttypes apps only appear in the
# 		'auth_db' database.
# 		"""
# 		if app_label in self.route_app_labels:
# 				return db == 'auth_db'
# 		return None

'''
 database label: blogs_db (used for routing - I think)
 database label is not the same as db name
 manage.py migrate --database=blog_db



 1997  python manage.py runserver
 1998  python manage.py makemigrations
 2004  python manage.py migrate
 1999  python manage.py migrate --database=blog_db
 2001  python manage.py createsuperuser
 2000  python manage.py runserver


'''

class BlogRouter:
	"""
	A router to control all database operations on models in the
	auth and contenttypes applications.
	"""
	# redirecting to a different db based on app label
	route_app_labels = {'blogs'} 	# which apps are routed here

	def db_for_read(self, model, **hints):
		"""
		Attempts to read auth and contenttypes models go to auth_db.
		"""
		if model._meta.app_label in self.route_app_labels:
				return 'blog_db'
		return None

	def db_for_write(self, model, **hints):
		"""
		Attempts to write auth and contenttypes models go to auth_db.
		"""
		if model._meta.app_label in self.route_app_labels:
				return 'blog_db'
		return None

	# def allow_relation(self, obj1, obj2, **hints):
	# 	"""
	# 	Allow relations if a model in the auth or contenttypes apps is
	# 	involved.
	# 	"""
	# 	if (
	# 			obj1._meta.app_label in self.route_app_labels or
	# 			obj2._meta.app_label in self.route_app_labels
	# 	):
	# 			return True
	# 	return None

	def allow_migrate(self, db, app_label, model_name=None, **hints):
		"""
		Make sure the auth and contenttypes apps only appear in the
		'auth_db' database.
		"""
		if app_label in self.route_app_labels:
				return db == 'blog_db'
		return None
