from django.test import TestCase
from django.urls import reverse
from .models import UserList

class ManageUsersTests(TestCase):
    def setUp(self):
        # Create an admin user
        self.admin_user = UserList.objects.create_user(
            username='admin_test',
            email='admin@test.com',
            password='adminpassword',
            role='Admin'
        )
        self.admin_user.plain_password = 'adminpassword'
        self.admin_user.save()

        # Create a non-admin user (Staff)
        self.staff_user = UserList.objects.create_user(
            username='staff_test',
            email='staff@test.com',
            password='staffpassword',
            role='Staff'
        )
        self.staff_user.plain_password = 'staffpassword'
        self.staff_user.save()

    def test_model_plain_password(self):
        user = UserList.objects.get(username='admin_test')
        self.assertEqual(user.plain_password, 'adminpassword')

    def test_manage_users_view_restricted_to_admin(self):
        # Log in as staff
        self.client.login(username='staff_test', password='staffpassword')
        response = self.client.get(reverse('manage_users'))
        # Should redirect to login
        self.assertRedirects(response, reverse('login'))

        # Log in as admin
        self.client.login(username='admin_test', password='adminpassword')
        response = self.client.get(reverse('manage_users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_users.html')
        self.assertContains(response, 'staff_test')
        self.assertContains(response, 'admin_test')

    def test_add_user_saves_plain_password(self):
        self.client.login(username='admin_test', password='adminpassword')
        response = self.client.post(reverse('add_user'), {
            'username': 'new_user',
            'email': 'new_user@test.com',
            'password': 'newpassword123',
            'role': 'Staff'
        })
        self.assertRedirects(response, reverse('manage_users'))
        
        # Verify user was created with plain password
        new_user = UserList.objects.get(username='new_user')
        self.assertEqual(new_user.plain_password, 'newpassword123')
        self.assertEqual(new_user.role, 'Staff')

    def test_edit_user(self):
        self.client.login(username='admin_test', password='adminpassword')
        
        # Edit staff_test to be Warden, change username, and change password
        response = self.client.post(reverse('edit_user', kwargs={'user_id': self.staff_user.id}), {
            'username': 'staff_test_edited',
            'email': 'staff_edited@test.com',
            'role': 'Warden',
            'password': 'newpassword789'
        })
        self.assertRedirects(response, reverse('manage_users'))
        
        self.staff_user.refresh_from_db()
        self.assertEqual(self.staff_user.username, 'staff_test_edited')
        self.assertEqual(self.staff_user.email, 'staff_edited@test.com')
        self.assertEqual(self.staff_user.role, 'Warden')
        self.assertEqual(self.staff_user.plain_password, 'newpassword789')
        self.assertTrue(self.staff_user.check_password('newpassword789'))

    def test_delete_user(self):
        self.client.login(username='admin_test', password='adminpassword')
        
        # Delete staff_test
        response = self.client.get(reverse('delete_user', kwargs={'user_id': self.staff_user.id}))
        self.assertRedirects(response, reverse('manage_users'))
        
        self.assertFalse(UserList.objects.filter(id=self.staff_user.id).exists())

    def test_cannot_delete_self(self):
        self.client.login(username='admin_test', password='adminpassword')
        
        # Attempt to delete own account
        response = self.client.get(reverse('delete_user', kwargs={'user_id': self.admin_user.id}))
        self.assertRedirects(response, reverse('manage_users'))
        
        # Admin should still exist
        self.assertTrue(UserList.objects.filter(id=self.admin_user.id).exists())


from student.models import Student
from room.models import Room

class AuthorizationTests(TestCase):
    def setUp(self):
        # Create Room
        self.room = Room.objects.create(block='A', room_no='101', capacity=2)
        
        # Create Student User A
        self.user_a = UserList.objects.create_user(
            username='student_a',
            email='student_a@test.com',
            password='password123',
            role='Student'
        )
        self.student_a = Student.objects.create(
            user=self.user_a,
            name='Student A',
            reg_number='REG001',
            dob='2000-01-01',
            course='CS',
            year='1',
            hostel_fee=50000,
            room=self.room
        )

        # Create Student User B
        self.user_b = UserList.objects.create_user(
            username='student_b',
            email='student_b@test.com',
            password='password123',
            role='Student'
        )
        self.student_b = Student.objects.create(
            user=self.user_b,
            name='Student B',
            reg_number='REG002',
            dob='2000-01-02',
            course='IS',
            year='1',
            hostel_fee=50000,
            room=self.room
        )

    def test_student_cannot_add_student(self):
        # Log in as Student A
        self.client.login(username='student_a', password='password123')
        # Attempt to access add student view
        response = self.client.get(reverse('add_student'))
        # Should redirect to login (since they are logged out on unauthorized access)
        self.assertRedirects(response, reverse('login'))
        
    def test_student_cannot_view_other_student_fee(self):
        # Log in as Student A
        self.client.login(username='student_a', password='password123')
        # Attempt to access Student B's fee page
        response = self.client.get(reverse('student_fee', kwargs={'id': self.student_b.id}))
        # Should redirect to login
        self.assertRedirects(response, reverse('login'))

    def test_student_cannot_view_other_student_profile(self):
        # Log in as Student A
        self.client.login(username='student_a', password='password123')
        # Attempt to access Student B's profile view page
        response = self.client.get(reverse('view_student', kwargs={'id': self.student_b.id}))
        # Should redirect to login
        self.assertRedirects(response, reverse('login'))

    def test_student_can_view_own_fee(self):
        # Log in as Student A
        self.client.login(username='student_a', password='password123')
        # Access own fee page
        response = self.client.get(reverse('student_fee', kwargs={'id': self.student_a.id}))
        self.assertEqual(response.status_code, 200)

    def test_student_can_view_own_profile(self):
        # Log in as Student A
        self.client.login(username='student_a', password='password123')
        # Access own profile view
        response = self.client.get(reverse('view_student', kwargs={'id': self.student_a.id}))
        self.assertEqual(response.status_code, 200)

    def test_404_redirects_to_login(self):
        # Access a non-existent URL
        response = self.client.get('/this-url-does-not-exist/')
        # Should redirect to login page
        self.assertRedirects(response, reverse('login'))


