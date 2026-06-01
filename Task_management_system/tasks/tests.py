from datetime import timedelta

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Task


# Tests for Task model behavior and task-related views.
# These tests exercise both core logic and page rendering in the Task app.


class TaskModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Create a sample task once for the model tests.
        cls.today = timezone.localdate()
        cls.task = Task.objects.create(
            title='Sample task',
            description='A simple test task.',
            priority=Task.PRIORITY_MEDIUM,
            due_date=cls.today + timedelta(days=2),
            completed=False,
        )

    def test_task_str_returns_title(self) -> None:
        # The string representation should return the task title.
        self.assertEqual(str(self.task), 'Sample task')

    def test_is_overdue_returns_false_for_future_due_date(self) -> None:
        # A future due date should not be considered overdue.
        self.assertFalse(self.task.is_overdue)

    def test_due_status_returns_open_when_not_completed(self) -> None:
        # Open tasks should report 'Open' status.
        self.assertEqual(self.task.due_status, 'Open')

    def test_due_status_returns_completed_when_completed(self) -> None:
        # Completed tasks should report 'Completed' status.
        self.task.completed = True
        self.task.save()
        self.assertEqual(self.task.due_status, 'Completed')

    def test_due_status_returns_overdue_when_past_due(self) -> None:
        # A task with a past due date and not completed should report 'Overdue'.
        task = Task(
            title='Overdue task',
            due_date=self.today - timedelta(days=1),
            completed=False,
        )
        self.assertEqual(task.due_status, 'Overdue')

    def test_clean_raises_validation_error_for_past_due_date(self) -> None:
        # Validation should reject a due date that is before today.
        task = Task(
            title='Invalid due date',
            due_date=self.today - timedelta(days=1),
        )
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_save_sets_completed_at_when_completed(self) -> None:
        # Saving a completed task should populate the completed_at timestamp.
        self.task.completed = True
        self.task.save()
        self.assertIsNotNone(self.task.completed_at)

    def test_save_clears_completed_at_when_uncompleted(self) -> None:
        # Clearing completed status should also clear completed_at.
        self.task.completed = True
        self.task.save()
        self.task.completed = False
        self.task.save()
        self.assertIsNone(self.task.completed_at)

    def test_get_absolute_url_returns_detail_url(self) -> None:
        self.assertEqual(self.task.get_absolute_url(), reverse('tasks:task-detail', kwargs={'pk': self.task.pk}))


class TaskFormTests(TestCase):
    def setUp(self) -> None:
        self.today = timezone.localdate()

    def test_task_form_valid_data(self) -> None:
        data = {
            'title': 'Form test',
            'description': 'Testing task form',
            'assigned_to': 'Tester',
            'priority': Task.PRIORITY_HIGH,
            'due_date': self.today + timedelta(days=5),
            'completed': False,
        }
        from .forms import TaskForm

        form = TaskForm(data=data)
        self.assertTrue(form.is_valid())

    def test_task_form_rejects_past_due_date(self) -> None:
        data = {
            'title': 'Bad due date',
            'due_date': self.today - timedelta(days=1),
        }
        from .forms import TaskForm

        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)


class TaskViewTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Create a task to use in view tests.
        cls.task = Task.objects.create(
            title='View test task',
            description='Task used for view tests.',
            due_date=timezone.localdate() + timedelta(days=3),
        )

    def test_task_list_view_status_code(self) -> None:
        # Task list page should load successfully and show the task title.
        response: HttpResponse = self.client.get(reverse('tasks:task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.assertContains(response, 'View test task')

    def test_task_detail_view_status_code(self) -> None:
        # Task detail page should load successfully for an existing task.
        response: HttpResponse = self.client.get(reverse('tasks:task-detail', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_detail.html')
        self.assertContains(response, 'View test task')

    def test_task_create_view_status_code(self) -> None:
        # The task creation form page should be reachable.
        response: HttpResponse = self.client.get(reverse('tasks:task-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')

    def test_task_update_view_status_code(self) -> None:
        # The task edit form should be reachable for an existing task.
        response: HttpResponse = self.client.get(reverse('tasks:task-edit', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')

    def test_task_delete_view_status_code(self) -> None:
        # The task delete confirmation page should be reachable.
        response: HttpResponse = self.client.get(reverse('tasks:task-delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_confirm_delete.html')

    def test_task_create_view_creates_task(self) -> None:
        response = self.client.post(
            reverse('tasks:task-create'),
            data={
                'title': 'New task',
                'description': 'Created via test',
                'assigned_to': 'Tester',
                'priority': Task.PRIORITY_LOW,
                'due_date': timezone.localdate() + timedelta(days=4),
                'completed': False,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='New task').exists())

    def test_task_update_view_updates_task(self) -> None:
        response = self.client.post(
            reverse('tasks:task-edit', args=[self.task.pk]),
            data={
                'title': 'Updated task title',
                'description': self.task.description,
                'assigned_to': self.task.assigned_to,
                'priority': self.task.priority,
                'due_date': self.task.due_date,
                'completed': self.task.completed,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated task title')

    def test_task_delete_view_deletes_task(self) -> None:
        response = self.client.post(reverse('tasks:task-delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_complete_marks_completed(self) -> None:
        response = self.client.post(reverse('tasks:task-complete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)
        self.assertIsNotNone(self.task.completed_at)
