import datetime
from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.http import HttpRequest
from django.core.urlresolvers import resolve
from django.core.exceptions import ValidationError 
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from unittest import skip
from cms.models import Topic, UserTopics, Material, Task, TopicTable, DepartmentTable, Professor, TABLE_PERIODS, TABLE_DAYS, UserContribution
from cms.views import update_user_topics
from users.models import Department, UserProfile, Faculty, University


class TopicTest(TestCase):
	def test_add_valid_topic(self):
		# Setup test
		dep = Department.objects.create()
		t 	= Topic.objects.create(name = 'test topic with spaces', desc = 'ddddd', term = 1, department = dep)

		# Exercise test
		query = Topic.objects.get()

		# Assert test
		self.assertEqual('test topic with spaces', query.name)
		self.assertEqual(dep, query.department)

	def test_add_invalid_topic_name(self):
		# Setup test
		dep = Department.objects.create()
		t 	= Topic.objects.create(name = '123', desc = 'ddddd', term = 1, department = dep)
		
		# Exercise test
		# Assert test
		self.assertRaises(ValidationError, t.clean())

	def test_add_repeated_topic_name(self):
		# Setup test
		dep = Department.objects.create()
		t 	= Topic.objects.create(name = 'topic name', desc = 'ddddd', term = 1, department = dep)
		t2 	= Topic.objects.create(name = 'topic name', desc = 'ddddd', term = 1, department = dep)
		
		# Exercise test
		# Assert test
		self.assertRaises(ValidationError, t2.clean)

class UserTopicsTest(TestCase):
	def make_messages_available(self, request):
		"""
		Takes request and make django's messages available for it.
		"""
		setattr(request, 'session', 'session')
		messages = FallbackStorage(request)
		setattr(request, '_messages', messages)

	def setUp(self):
		self.user 			= User.objects.create(username = 'test_username', email = 'tesssst@test.com', password = 'secrettt23455')
		self.fac 			= Faculty.objects.create()
		self.dep 			= Department.objects.create(faculty = self.fac)
		self.user.profile 	= UserProfile.objects.create(department = self.dep, faculty = self.fac)
		self.topic 			= Topic.objects.create(name = 'topic name', desc = 'ddddd', term = 1, department = self.dep)

	def test_return_user_topics(self):
		# Setup test	
		self.user.profile.topics.add(self.topic)

		# Exercise test
		topics = UserTopics.get_user_topics(self.user)
		
		# Assert test
		self.assertEqual(len(topics), 1)
		self.assertEqual(topics[0], self.topic)

	def test_return_user_topics_with_no_profile(self):
		# Setup test	
		user2 = User.objects.create(username = 'test_2', email = 'tesssst@test.com', password = 'secrettt23455')

		# Exercise test
		topics = UserTopics.get_user_topics(user2)
		
		# Assert test
		self.assertEqual(len(topics), 0)

	def test_return_available_topics(self):
		# Setup test	
		self.user.profile.topics.add(self.topic)
		dep2 = Department.objects.create(name = "test_dep", faculty = self.fac)
		
		# Exercise test
		topics 	= UserTopics.get_topics_choices(self.user)
		
		# Assert test
		self.assertIn(self.topic.department.name, topics)
		# Assure that results include all departments within same faculty.
		self.assertIn(dep2.name, topics)

	def test_update_topics_with_correct_ids(self):
		# Setup test	
		self.user.profile.topics.add(self.topic)
		new_topic 	= []
		t1 			= Topic.objects.create(name = 'topic_new_2', desc = 'ddddd', term = 1, department = self.dep)
		new_topic.append(t1.id)
		t2 			= Topic.objects.create(name = 'topic_new_3', desc = 'ddddd', term = 2, department = self.dep)
		new_topic.append(t2.id)
		t3 			= Topic.objects.create(name = 'topic_new_4', desc = 'ddddd', term = 3, department = self.dep)
		new_topic.append(t3.id)


		# Exercise test
		request 		= RequestFactory()
		request 		= request.post(reverse('update_user_topics'), data = {'chosen_list[]':new_topic})
		request.user 	= self.user
		
		# Making messages available for request.
		self.make_messages_available(request)

		update_user_topics(request)

		
		# Assert test
		self.assertEqual(self.user.profile.topics.all().count(), 3)

	def test_update_topics_with_empty_list(self):
		# Setup test	
		self.user.profile.topics.add(self.topic)
		new_topic 	= []


		# Exercise test
		request 		= RequestFactory()
		request 		= request.post(reverse('update_user_topics'), data = {'chosen_list[]':new_topic})
		request.user 	= self.user
		
		# Making messages available for request.
		self.make_messages_available(request)

		update_user_topics(request)

		
		# Assert test
		self.assertEqual(self.user.profile.topics.all().count(), 1)

	def test_update_topics_with_all_incorrect_ids(self):
		# Setup test	
		self.user.profile.topics.add(self.topic)
		new_topic 	= [990, 1200, 1510]


		# Exercise test
		request 		= RequestFactory()
		request 		= request.post(reverse('update_user_topics'), data = {'chosen_list[]':new_topic})
		request.user 	= self.user

		# Making messages available for request.
		self.make_messages_available(request)

		update_user_topics(request)

		
		# Assert test
		self.assertEqual(self.user.profile.topics.all().count(), 1)

	def test_update_topics_with_half_correct_half_incorrect(self):
		# Setup test	
		self.user.profile.topics.add(self.topic)
		new_topic 	= []
		t1 			= Topic.objects.create(name = 'topic_new_2', desc = 'ddddd', term = 1, department = self.dep)
		new_topic.append(t1.id)
		t2 			= Topic.objects.create(name = 'topic_new_3', desc = 'ddddd', term = 2, department = self.dep)
		new_topic.append(t2.id)
		t3 			= Topic.objects.create(name = 'topic_new_4', desc = 'ddddd', term = 3, department = self.dep)
		new_topic.append(t3.id)
		new_topic.append(990)
		new_topic.append(5300)
		new_topic.append(8000)


		# Exercise test
		request 		= RequestFactory()
		request 		= request.post(reverse('update_user_topics'), data = {'chosen_list[]':new_topic})
		request.user 	= self.user

		# Making messages available for request.
		self.make_messages_available(request)

		update_user_topics(request)

		
		# Assert test
		self.assertEqual(self.user.profile.topics.all().count(), 3)

	def test_update_topics_with_correct_ids_that_user_cannot_access(self):
		# Setup test	
		self.user.profile.topics.add(self.topic)
		another_faculty 				= Faculty.objects.create()
		another_dep_user_cannot_access 	= Department.objects.create(faculty = another_faculty)
		new_topic 	= []
		t1 			= Topic.objects.create(name = 'topic_new_2', desc = 'ddddd', term = 1, department = another_dep_user_cannot_access)
		new_topic.append(t1.id)
		t2 			= Topic.objects.create(name = 'topic_new_3', desc = 'ddddd', term = 2, department = another_dep_user_cannot_access)
		new_topic.append(t2.id)
		t3 			= Topic.objects.create(name = 'topic_new_4', desc = 'ddddd', term = 3, department = another_dep_user_cannot_access)
		new_topic.append(t3.id)


		# Exercise test
		request 		= RequestFactory()
		request 		= request.post(reverse('update_user_topics'), data = {'chosen_list[]':new_topic})
		request.user 	= self.user
		
		# Making messages available for request.
		self.make_messages_available(request)

		update_user_topics(request)

		
		# Assert test
		self.assertEqual(self.user.profile.topics.all().count(), 1)

class MaterialTest(TestCase):
	def setUp(self):
		self.uni 			= University.objects.create(name = 'Test university')
		self.fac 			= Faculty.objects.create(name = 'Test faculty')
		self.dep 			= Department.objects.create(name = 'Test dep')
		self.topic 			= Topic.objects.create(name = 'test topic with spaces', desc = 'ddddd', term = 1, department = self.dep, weeks = 5)
		self.user 			= User.objects.create_user(username = 'ibrahemmmmm', email = 'test_@test.com', password = '000000555555ddd5f5f')
		self.user.profile 	= UserProfile.objects.create(university = self.uni, faculty = self.fac, department = self.dep)
		self.material 		= Material.objects.create(
				name 			= 'test_material',
				content 		= 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
				link 			= 'http://www.docs.google.com',
				year 			= '2017-1-5',
				term 			= 1,
				content_type 	= 1,
				week_number 	= 1,
				user 			= self.user,
				topic 			= self.topic
			)

	def test_add_material(self):
		# Setup test
		material_test = Material.objects.create(
				name 			= 'test_material',
				content 		= 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
				link 			= 'http://www.docs.godogle.com',
				year 			= '2017-1-5',
				term 			= 1,
				content_type 	= 1,
				week_number 	= 1,
				user 			= self.user,
				topic 			= self.topic
			)

		# Exercise test
		materials_in_db = Material.objects.latest('id')
		
		# Assert test
		self.assertEqual(material_test, materials_in_db)

	def test_add_material_with_invalid_name(self):
		# Setup test
		material_test = Material.objects.create(
				name 			= '123material',
				content 		= 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
				link 			= 'http://www.docs.gofogle.com',
				year 			= '2017-1-5',
				term 			= 1,
				content_type 	= 1,
				week_number 	= 0,
				user 			= self.user,
				topic 			= self.topic
			)

		# Exercise test
		# Assert test
		self.assertRaises(ValidationError, lambda: material_test.full_clean())

	def test_add_material_with_empty_content(self):
		# Setup test
		material_test = Material.objects.create(
				name 			= 'material',
				content 		= '',
				link 			= 'http://www.docs.googlce.com',
				year 			= '2017-1-5',
				term 			= 1,
				content_type 	= 1,
				week_number 	= 0,
				user 			= self.user,
				topic 			= self.topic
			)

		# Exercise test
		# Assert test
		self.assertRaises(ValidationError, lambda: material_test.full_clean())

	def test_add_material_with_content_less_than_50(self):
		# Setup test
		material_test = Material.objects.create(
				name 			= 'material',
				content 		= 'f',
				link 			= 'http://www.docs.gosogle.com',
				year 			= '2017-1-5',
				term 			= 1,
				content_type 	= 1,
				week_number 	= 2,
				user 			= self.user,
				topic 			= self.topic
			)

		# Exercise test
		# Assert test
		self.assertRaises(ValidationError, lambda: material_test.full_clean())

	def test_add_material_with_week_number_that_doesnot_exist(self):
		# Setup test
		material_test = Material.objects.create(
				name 			= 'material',
				content 		= 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
				link 			= 'http://www.docs.googssle.com',
				year 			= '2123-1-5',
				term 			= 1,
				content_type 	= 1,
				week_number 	= 99,
				user 			= self.user,
				topic 			= self.topic
			)

		# Exercise test
		# Assert test
		self.assertRaises(ValidationError, lambda: material_test.full_clean())	

	def test_material_topic_lays_outside_user_scope(self):
		# Setup test
		another_user = User.objects.create_user(username = 'test_user', password = '12684szsf4df8f5d')
		material_test = Material.objects.create(
				name 			= 'material',
				content 		= 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
				link 			= 'http://www.docs.googssle.com',
				year 			= '2123-1-5',
				term 			= 1,
				content_type 	= 1,
				week_number 	= 1,
				user 			= another_user,
				topic 			= self.topic
			)

		# Exercise test
		# Assert test
		self.assertRaises(ValidationError, lambda: material_test.full_clean())

	def test_user_add_material_in_topic_in_another_dep(self):
		# Setup test
		another_dep = Department.objects.create(name = 'Test dep2')
		another_topic = Topic.objects.create(name = 'test with spaces', desc = 'ddddd', term = 1, department = another_dep, weeks = 5)
		self.user.profile.topics.add(another_topic)
		material_test 	= Material.objects.create(
				name 			= 'material',
				content 		= 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
				link 			= 'http://www.docs.googssle.com',
				year 			= '2123-1-5',
				term 			= 1,
				content_type 	= 1,
				week_number 	= 1,
				user 			= self.user,
				topic 			= another_topic
			)

		# Exercise test
		topic_materials = another_topic.primary_materials.all()
		
		# Assert test
		self.assertIn(material_test, topic_materials)
		self.assertEqual(None, material_test.full_clean())

class TaskTest(TestCase):
	def setUp(self):
		self.uni       	= University.objects.create(name = 'Test university')
		self.fac        = Faculty.objects.create(name = 'Test faculty')
		self.dep        = Department.objects.create(name = 'Test dep')
		self.topic      = Topic.objects.create(pk = 1, name = 'test topic with spaces', desc = 'ddddd', term = 1, department = self.dep, weeks = 5)
		self.user 		= User.objects.create_user(username = 'ibrahemmmmm', email = 'test_@test.com', password = '000000555555ddd5f5f') 
		self.profile   	= UserProfile.objects.create(user = self.user, department = self.dep, faculty = self.fac)
		self.material 	= Material.objects.create(
				name 			= 'test_material',
				content 		= 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
				link 			= 'http://www.docs.google.com',
				year 			= '2017-1-5',
				term 			= 1,
				content_type 	= 1,
				week_number 	= 1,
				user 			= self.user,
				topic 			= self.topic
			)

		self.task 	 	= Task.objects.create(
				name 			= 'test_tasks',
				content 		= 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
				link 			= 'http://www.docs.testtask.com',
				year 			= '2017-1-5',
				term 			= 1,
				content_type 	= 1,
				week_number 	= 1,
				user 			= self.user,
				topic 			= self.topic,
				deadline 		= '2018-5-1',

			)

		self.user.profile.topics.add(self.topic)

	def test_add_basic_valid_task(self):
		# Setup test
		task_test =	Task.objects.create(
				name 			= 'test',
				content 		= 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
				link 			= 'http://www.docs.testtasktwo.com',
				year 			= '2017-1-5',
				term 			= 1,
				content_type 	= 1,
				week_number 	= 1,
				user 			= self.user,
				topic 			= self.topic,
				deadline 		= '2018-5-1',

			)
		
		# Exercise test
		db_result = Task.objects.filter(deadline = '2018-5-1').count()

		# Assert test
		self.assertEqual(2, db_result)

	def test_deadline_with_passed_date(self):
		# Setup test
		task_test =	Task.objects.create(
				name 			= 'test tasks',
				content 		= 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
				link 			= 'http://www.docs.testtasktwo.com',
				year 			= '2017-1-5',
				term 			= 1,
				content_type 	= 3,
				week_number 	= 1,
				user 			= self.user,
				topic 			= self.topic,
				deadline 		= '2010-5-1',

			)
		
		# Exercise test
		# Assert test
		self.assertRaises(ValidationError, lambda: task_test.full_clean())

	def test_deadline_with_date_less_than_3_days_ahead(self):
		# Setup test
		now 		= datetime.datetime.now()
		task_test 	= Task.objects.create(
				name 			= 'test tasks',
				content 		= 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
				link 			= 'http://www.docs.testtasktwo.com',
				year 			= '2017-1-5',
				term 			= 1,
				content_type 	= 3,
				week_number 	= 1,
				user 			= self.user,
				topic 			= self.topic,
				deadline 		= now,

			)
		
		# Exercise test
		# Assert test
		self.assertRaises(ValidationError, lambda: task_test.full_clean())

	def test_get_closest_three_dates_from_five(self):
		# Setup test
		now = datetime.datetime.now()

		# Create tasks with days starts with tomorrow ends with today+5 days. Should return 3 tasks.
		for i in range(2, 7):	
			task_test 	= Task.objects.create(
					name 			= 'test tasks',
					content 		= 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
					link 			= 'http://www.docs.'+str(i)+'.com',
					year 			= '2017-1-5',
					term 			= 1,
					content_type 	= 3,
					week_number 	= 1,
					user 			= self.user,
					topic 			= self.topic,
					deadline 		= now+datetime.timedelta(days = i),

				)
		
		# Exercise test
		request = HttpRequest()
		request.user = self.user

		# Assert test
		self.assertEqual(3, len(Task.get_closest_tasks(request)))

class TopicTableTest(TestCase):
	def setUp(self):
		self.uni       	= University.objects.create(name = 'Test university')
		self.fac        = Faculty.objects.create(name = 'Test faculty')
		self.dep        = Department.objects.create(name = 'Test dep')
		self.topic      = Topic.objects.create(pk = 1, name = 'test topic with spaces', desc = 'ddddd', term = 1, department = self.dep, weeks = 5)
		self.user 		= User.objects.create_user(username = 'ibrahemmmmm', email = 'test_@test.com', password = '000000555555ddd5f5f') 
		self.profile   	= UserProfile.objects.create(user = self.user, department = self.dep, faculty = self.fac)

	def test_initiate_topic_table(self):
		"""Tests that table is created successfully."""

		# Setup test
		week = [[0] * 6] * 7
		topics = week
		topics[1][1] = 'Lecture'
		table = TopicTable.objects.create(topic=self.topic, topics=topics)

		# Exercise test
		table_in_db = TopicTable.objects.count()
		
		# Assert test
		self.assertTrue(table_in_db > 0)

	def test_table_display_correct_table_list(self):
		"""Tests wether or not set return correct table list."""

		# Setup test
		week = [['']*6 for i in range(7)]
		topics = [['']*6 for i in range(7)]
		places = [['']*6 for i in range(7)]
		topics[1][1] = 'Lecture'
		places[1][1] = 'Hall 1'

		# Exercise test
		table = TopicTable.objects.create(topic=self.topic, topics=topics, places=places)
		t_json = table.set_final_table()
		
		# Assert test
		self.assertEqual(topics[1][1]+' @ '+places[1][1], t_json[1][1])

	def test_table_display_correct_table_list_when_string_given(self):
		"""Tests wether or not set return correct table list."""

		# Setup test
		week = [['']*6 for i in range(7)]
		topics = [['']*6 for i in range(7)]
		places = [['']*6 for i in range(7)]
		topics[1][1] = 'Lecture'
		places[1][1] = 'Hall 1'

		# Exercise test
		table = TopicTable.objects.create(topic=self.topic, topics=str(topics), places=str(places))
		t_json = table.set_final_table()
		
		# Assert test
		self.assertEqual(topics[1][1]+' @ '+places[1][1], t_json[1][1])

class DepartmentTableTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username = 'test_username', email = 'tesssst@test.com', password = 'secrettt23455')
		self.fac = Faculty.objects.create()
		self.dep = Department.objects.create(faculty = self.fac)
		self.user.profile = UserProfile.objects.create(department = self.dep, faculty = self.fac)
		self.topic = Topic.objects.create(name = 'topic name', desc = 'ddddd', term = 1, department = self.dep)
		self.topic2 = Topic.objects.create(name = 'topic name2', desc = 'ddddd', term = 2, department = self.dep)
		self.topic.professors.add(Professor.objects.create(name="gamal", faculty=self.fac))
		self.topic2.professors.add(Professor.objects.create(name="meshmesh", faculty=self.fac))

	def test_return_user_topics_and_dep_topics(self):
		"""Tests that class return a set of user and dep topics."""
		# Setup test
		fac2 = Faculty.objects.create()
		dep2 = Department.objects.create(faculty = fac2)
		topic3 = Topic.objects.create(name = 'topic in user', desc = 'ddddd', term = 2, department = dep2)
		self.user.profile.topics.add(topic3)

		# Exercise test
		dep_table = DepartmentTable(self.user)

		# Assert test
		self.assertIn(topic3, dep_table.available_topics)
		self.assertIn(self.topic2, dep_table.available_topics)

	def test_return_dep_topics_only(self):
		"""Returns dep topics when user topics is none."""
		# Setup test
		fac2 = Faculty.objects.create()
		dep2 = Department.objects.create(faculty = fac2)
		topic3 = Topic.objects.create(name = 'topic in user', desc = 'ddddd', term = 2, department = dep2)

		# Exercise test
		dep_table = DepartmentTable(self.user)

		# Assert test
		self.assertNotIn(topic3, dep_table.available_topics)
		self.assertIn(self.topic2, dep_table.available_topics)

	def test_nothing_when_user_excpetion(self):
		"""Returns none."""
		# Setup test
		another_user = User.objects.create_user(
							username='ffffsds',
							email='tesssst@test.dd',
							password='secrettt23455'
						)

		# Exercise test
		dep_table = DepartmentTable(another_user)

		# Assert test
		self.assertEqual([], dep_table.available_topics)

	def test_return_all_professors(self):
		"""Returns all professors for available topics"""
		# Setup test

		# Exercise test
		dep_table = DepartmentTable(self.user)

		# Assert test
		self.assertEqual(2, len(dep_table.professors))

	def test_ignores_empty_professors(self):
		"""Returns all professors who have data for available topics"""
		# Setup test
		fac2 = Faculty.objects.create()
		dep2 = Department.objects.create(faculty = fac2)
		topic3 = Topic.objects.create(name = 'topic in user', desc = 'ddddd', term = 2, department = dep2)
		topic4 = Topic.objects.create(name = 'topic in user', desc = 'ddddd', term = 2, department = dep2)
		self.user.profile.topics.add(topic3, topic4)

		# Exercise test
		dep_table = DepartmentTable(self.user)

		# Assert test
		self.assertEqual(2, len(dep_table.professors))		

class UserTableTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username = 'test_username', email = 'tesssst@test.com', password = 'secrettt23455')
		self.fac = Faculty.objects.create()
		self.dep = Department.objects.create(faculty = self.fac)
		UserProfile.objects.create(user=self.user, department = self.dep, faculty = self.fac)
		self.topic = Topic.objects.create(name = 'topic name', desc = 'ddddd', term = 1, department = self.dep)
		self.topic2 = Topic.objects.create(name = 'topic name2', desc = 'ddddd', term = 2, department = self.dep)
		self.topic.professors.add(Professor.objects.create(name="gamal", faculty=self.fac))
		self.topic2.professors.add(Professor.objects.create(name="meshmesh", faculty=self.fac))

	def test_assign_user_table(self):
		"""updates user table for non-existing table (first time)."""
		
		# Setup test
		topics = [['']*6 for i in range(7)]
		places = [['']*6 for i in range(7)]
		topics[1][1] = 'topic_test_user'
		topics[2][3] = 'another_test'
		topic_table = TopicTable.objects.create(topic=self.topic, topics=topics, places=places)
		index1 = str(self.topic.id)+'_'+'1'+'_'+'1'
		index2 = str(self.topic.id)+'_'+'2'+'_'+'3'
		data = {'choices[]': [index1, index2]}

		# Exercise test
		url = reverse('web_user_table')
		request = self.client.login(username="test_username", password="secrettt23455")
		request = self.client.post(url, data=data)

		# Assert test
		self.assertIn('topic_test_user', self.user.profile.table.topics)

	def test_update_user_table(self):
		"""updates user table for an existing table."""
		
		# Setup test
		topics = [['']*6 for i in range(7)]
		places = [['']*6 for i in range(7)]
		topics[1][1] = 'topic_test_user'
		topics[2][3] = 'another_test'
		topics[5][1] = 'existing_table'
		topics[4][3] = 'another_cell'
		topics[1][1] = 'same_cell_as_previous'
		topic_table = TopicTable.objects.create(topic=self.topic, topics=topics, places=places)
		index1 = str(self.topic.id)+'_'+'1'+'_'+'1'
		index2 = str(self.topic.id)+'_'+'2'+'_'+'3'
		data = {'choices[]': [index1, index2]}
		url = reverse('web_user_table')
		request = self.client.login(username="test_username", password="secrettt23455")
		request = self.client.post(url, data=data)

		# Exercise test
		data = {'choices[]': ['1_5_1', '1_4_3', '1_1_1']}
		request = self.client.post(url, data=data)


		# Assert test
		self.assertIn('existing_table', self.user.profile.table.topics)
		self.assertIn('same_cell_as_previous', self.user.profile.table.topics)

	def test_assign_user_table_with_fake_topics(self):
		"""updates user table for non-existing table (first time)."""
		
		# Setup test
		topics = [['']*6 for i in range(7)]
		places = [['']*6 for i in range(7)]
		topics[1][1] = 'topic_test_user'
		topics[2][3] = 'another_test'
		topic_table = TopicTable.objects.create(topic=self.topic, topics=topics, places=places)
		data = {'choices[]': ['1_5_1', '5_5_5', '1_4_3', '1_1_1', '2_3_4']}

		# Exercise test
		url = reverse('web_user_table')
		request = self.client.login(username="test_username", password="secrettt23455")
		request = self.client.post(url, data=data)

		# Assert test
		self.assertIn('topic_test_user', self.user.profile.table.topics)

class QueryTableTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username = 'test_username', email = 'tesssst@test.com', password = 'secrettt23455')
		self.fac = Faculty.objects.create()
		self.dep = Department.objects.create(faculty = self.fac)
		UserProfile.objects.create(user=self.user, department = self.dep, faculty = self.fac)
		self.topic = Topic.objects.create(name = 'topic name', desc = 'ddddd', term = 1, department = self.dep)
		self.topic2 = Topic.objects.create(name = 'topic name2', desc = 'ddddd', term = 2, department = self.dep)
		self.topic3 = Topic.objects.create(name = 'topic name3', desc = 'ddddd', term = 3, department = self.dep)
		self.topic.professors.add(Professor.objects.create(name="gamal", faculty=self.fac))
		self.topic2.professors.add(Professor.objects.create(name="meshmesh", faculty=self.fac))
		self.user.profile.topics.add(self.topic)
		self.user.profile.topics.add(self.topic2)
		self.user.profile.topics.add(self.topic3)

	def test_query_just_professors(self):
		# Setup test
		topics = [['']*6 for i in range(7)]
		places = [['']*6 for i in range(7)]
		topics[1][1] = 'Lecture'
		places[1][1] = 'Hall 1'
		topics[1][3] = 'Section'
		places[1][3] = 'Hall 2'
		TopicTable.objects.create(topic=self.topic, topics=topics, places=places)
		topics[4][4] = 'another_lecture'
		places[4][4] = 'another_lecture'
		TopicTable.objects.create(topic=self.topic3, topics=topics, places=places)
		professors = [1,2]
		data = {'professors': professors}
		
		# Exercise test
		url = reverse('web_query_table')
		request = self.client.login(username="test_username", password="secrettt23455")
		request = self.client.post(url, data=data)

		# Assert test
		self.assertIn(topics[1][1]+' @ '+places[1][1], request.context['table'][1][1])
		self.assertNotIn(topics[4][4]+' @ '+places[4][4], request.context['table'][4][4])

	def test_query_just_topics(self):
		# Setup test
		topics = [['']*6 for i in range(7)]
		places = [['']*6 for i in range(7)]
		topics[1][1] = 'Lecture'
		places[1][1] = 'Hall 1'
		topics[1][3] = 'Section'
		places[1][3] = 'Hall 2'
		TopicTable.objects.create(topic=self.topic, topics=topics, places=places)
		topics[4][4] = 'another_lecture'
		places[4][4] = 'another_lecture'
		TopicTable.objects.create(topic=self.topic3, topics=topics, places=places)
		topics_list = [self.topic.id, self.topic3.id]
		data = {'topics': topics_list}
		
		# Exercise test
		url = reverse('web_query_table')
		request = self.client.login(username="test_username", password="secrettt23455")
		request = self.client.post(url, data=data)

		# Assert test
		self.assertIn(topics[1][1]+' @ '+places[1][1], request.context['table'][1][1])
		self.assertIn(topics[4][4]+' @ '+places[4][4], request.context['table'][4][4])
	
	def test_query_just_days(self):
		# Setup test
		topics = [['']*6 for i in range(7)]
		places = [['']*6 for i in range(7)]
		topics[1][1] = 'Lecture'
		places[1][1] = 'Hall 1'
		topics[1][3] = 'Section'
		places[1][3] = 'Hall 2'
		TopicTable.objects.create(topic=self.topic, topics=topics, places=places)
		days = [1]
		data = {'days': days}
		
		# Exercise test
		url = reverse('web_query_table')
		request = self.client.login(username="test_username", password="secrettt23455")
		request = self.client.post(url, data=data)

		# Assert test
		# ['result_1'] is the dict key of where model combines topic and place.
		self.assertIn(topics[1][1]+' @ '+places[1][1], request.context['table'][1][1])
		self.assertIn(topics[1][3]+' @ '+places[1][3], request.context['table'][1][3])

	def test_query_just_periods(self):
		# Setup test
		topics = [['']*6 for i in range(7)]
		places = [['']*6 for i in range(7)]
		topics[1][1] = 'Lecture'
		places[1][1] = 'Hall 1'
		topics[1][2] = 'Lecture'
		places[1][2] = 'Hall 1'
		TopicTable.objects.create(topic=self.topic, topics=topics, places=places)
		topics[2][3] = 'Section'
		places[2][3] = 'Hall 2'
		TopicTable.objects.create(topic=self.topic2, topics=topics, places=places)
		periods = [3, 2]
		data = {'periods': periods}
		
		# Exercise test
		url = reverse('web_query_table')
		request = self.client.login(username="test_username", password="secrettt23455")
		request = self.client.post(url, data=data)

		# Assert test
		self.assertIn(topics[1][2]+' @ '+places[1][2], request.context['table'][1][2])

	def test_query_with_all_options(self):
		# Setup test
		topics = [['']*6 for i in range(7)]
		places = [['']*6 for i in range(7)]
		topics[1][1] = 'Lecture'
		places[1][1] = 'Hall 1'
		topics[1][2] = 'Lecture'
		places[1][2] = 'Hall 1'
		TopicTable.objects.create(topic=self.topic, topics=topics, places=places)
		topics[2][3] = 'Section'
		places[2][3] = 'Hall 2'
		TopicTable.objects.create(topic=self.topic2, topics=topics, places=places)
		periods = [i for i in range(6)]
		days = [i for i in range(7)]
		topics_ids = [1, 2, 3]
		professors = [1, 2]
		data = {'periods': periods, 'days':days, 'professors':professors, 'topics':topics_ids}
		
		# Exercise test
		url = reverse('web_query_table')
		request = self.client.login(username="test_username", password="secrettt23455")
		request = self.client.post(url, data=data)

		# Assert test
		self.assertIn(topics[1][2]+' @ '+places[1][2], request.context['table'][1][2])
	
	def test_query_with_topic_has_no_table(self):
		# Setup test
		topics_ids = [3]
		data = {'topics':topics_ids}
		
		# Exercise test
		url = reverse('web_query_table')
		request = self.client.login(username="test_username", password="secrettt23455")
		request = self.client.post(url, data=data)
		empty_query = table = [ [ [0] for k in range(20) ] for j in range(TABLE_PERIODS) for i in range(TABLE_DAYS) ]

		# Assert test

		self.assertEqual(empty_query, request.context['table'])

class UserContributionTest(TestCase):
	def setUp(self):
		self.uni 			= University.objects.create(name = 'Test university')
		self.fac 			= Faculty.objects.create(name = 'Test faculty')
		self.dep 			= Department.objects.create(name = 'Test dep')
		self.topic 			= Topic.objects.create(name = 'test topic with spaces', desc = 'ddddd', term = 1, department = self.dep, weeks = 5)
		self.user 			= User.objects.create_user(username = 'ibrahemmmmm', email = 'test_@test.com', password = '000000555555ddd5f5f')
		self.user.profile 	= UserProfile.objects.create(university = self.uni, faculty = self.fac, department = self.dep)
		self.material 		= UserContribution.objects.create(
				name = 'test_material',
				content = 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
				link = 'http://www.docs.google.com',
				year = datetime.datetime.now(),
				term = 1,
				content_type = 1,
				week_number = 1,
				user = self.user,
				topic = self.topic,
				deadline = datetime.datetime.now(),
				supervisior_id = 0
			)
		self.user.profile.topics.add(self.topic)

	def test_user_add_material_in_topic_in_another_dep(self):
		# Setup test
		another_dep = Department.objects.create(name = 'Test dep2')
		another_topic = Topic.objects.create(name = 'test with spaces', desc = 'ddddd', term = 1, department = another_dep, weeks = 5)
		self.user.profile.topics.add(another_topic)
		material_test 	= UserContribution.objects.create(
				name 			= 'material',
				content 		= 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
				link 			= 'http://www.docs.googssle.com',
				year 			= '2123-1-5',
				term 			= 1,
				content_type 	= 1,
				week_number 	= 1,
				user 			= self.user,
				topic 			= another_topic,
				deadline = datetime.datetime.now(),
				supervisior_id = 0
			)

		# Exercise test
		topic_materials = another_topic.secondary_materials.all()
		
		# Assert test
		self.assertIn(material_test, topic_materials)
		self.assertEqual(None, material_test.full_clean())

	def test_user_add_task_with_current_deadline(self):
		# Setup test
		another_dep = Department.objects.create(name = 'Test dep2')
		another_topic = Topic.objects.create(name = 'test with spaces', desc = 'ddddd', term = 1, department = another_dep, weeks = 5)
		self.user.profile.topics.add(another_topic)
		material_test 	= UserContribution.objects.create(
				name 			= 'material',
				content 		= 'this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
				link 			= 'http://www.docs.googssle.com',
				year 			= datetime.datetime.now(),
				term 			= 1,
				content_type 	= 3,
				week_number 	= 1,
				user 			= self.user,
				topic 			= another_topic,
				deadline = datetime.datetime.now(),
				supervisior_id = 0
			)

		# Exercise test
		topic_materials = another_topic.secondary_materials.all()
		
		# Assert test
		with self.assertRaisesRegexp(ValidationError, 'Deadline date should be 3 days ahead at least.'):
			material_test.full_clean()
		self.assertRaises(ValidationError, lambda: material_test.full_clean())

	def test_get_closest_tasks_with_user_contributions(self):
		# Setup test
		now = datetime.datetime.now()

		# Create tasks with days starts with tomorrow ends with today+5 days. Should return 3 primary tasks.
		# Should return 2 secondary tasks, as there're just 2 approved.
		for i in range(2, 7):	
			task_test 	= Task.objects.create(
				name='test tasks',
				content='this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
				link='http://www.docs.'+str(i)+'.com',
				year='2017-1-5',
				term=1,
				content_type=3,
				week_number=1,
				user=self.user,
				topic=self.topic,
				deadline=now+datetime.timedelta(days = i),
			)
			material_test 	= UserContribution.objects.create(
				name='material',
				content='this is loooooooooooooooooooooong connnnnnnnnnteeeeeent',
				link='http://www.dosscs.'+str(i)+'.com',
				year=datetime.datetime.now(),
				term=1,
				content_type=3,
				week_number=1,
				user=self.user,
				topic=self.topic,
				deadline=now+datetime.timedelta(days = i),
				supervisior_id=0,
				status=3 if not i%2 else 1
			)
		
		# Exercise test
		request = HttpRequest()
		request.user = self.user

		# Assert test
		self.assertEqual(5, len(Task.get_closest_tasks(request)))
