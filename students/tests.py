from django.test import TestCase
from django.urls import reverse
from .models import Student

class StudentModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            name="John Doe",
            email="john@example.com",
            age=20
        )

    def test_student_string_representation(self):
        self.assertEqual(str(self.student), "John Doe")

    def test_student_get_absolute_url(self):
        self.assertEqual(
            self.student.get_absolute_url(),
            reverse('student_detail', kwargs={'pk': self.student.pk})
        )


class StudentViewsTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            name="Jane Doe",
            email="jane@example.com",
            age=22
        )

    def test_student_list_view(self):
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_list.html')
        self.assertContains(response, "Jane Doe")

    def test_student_detail_view(self):
        response = self.client.get(reverse('student_detail', kwargs={'pk': self.student.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_detail.html')
        self.assertContains(response, "Jane Doe")
        self.assertContains(response, "jane@example.com")

    def test_student_detail_view_not_found(self):
        response = self.client.get(reverse('student_detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)

    def test_student_create_view_get(self):
        response = self.client.get(reverse('student_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_form.html')

    def test_student_create_view_post(self):
        data = {
            'name': 'Bob Smith',
            'email': 'bob@example.com',
            'age': 25
        }
        response = self.client.post(reverse('student_create'), data=data)
        self.assertEqual(response.status_code, 302)  # Redirects to list
        self.assertEqual(Student.objects.filter(name='Bob Smith').count(), 1)

    def test_student_update_view_get(self):
        response = self.client.get(reverse('student_update', kwargs={'pk': self.student.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_form.html')

    def test_student_update_view_post(self):
        data = {
            'name': 'Jane Updated',
            'email': 'jane.up@example.com',
            'age': 23
        }
        response = self.client.post(
            reverse('student_update', kwargs={'pk': self.student.pk}),
            data=data
        )
        self.assertEqual(response.status_code, 302)
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, 'Jane Updated')
        self.assertEqual(self.student.age, 23)

    def test_student_delete_view_get(self):
        response = self.client.get(reverse('student_delete', kwargs={'pk': self.student.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_confirm_delete.html')

    def test_student_delete_view_post(self):
        response = self.client.post(reverse('student_delete', kwargs={'pk': self.student.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Student.objects.filter(pk=self.student.pk).count(), 0)
