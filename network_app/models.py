from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    profession = models.CharField(max_length=100)
    interests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Connection(models.Model):
    person_from = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='connections_from')
    person_to = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='connections_to')
    CONNECTION_TYPES = [
        ('friend', 'Friend'),
        ('family', 'Family'),
        ('colleague', 'Colleague'),
        ('other', 'Other'),
    ]
    connection_type = models.CharField(max_length=20, choices=CONNECTION_TYPES)
    strength = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)