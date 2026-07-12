from django.db import models


class StudentModel(models.Model):
    id         = models.CharField(max_length=50, primary_key=True)
    matricule  = models.CharField(max_length=50, unique=True)
    name       = models.CharField(max_length=100)

    class Meta:
        db_table = "students"

    def __str__(self):
        return self.name


class CourseModel(models.Model):
    id      = models.CharField(max_length=50, primary_key=True)
    name    = models.CharField(max_length=100)
    credits = models.IntegerField()

    class Meta:
        db_table = "courses"

    def __str__(self):
        return self.name


class NoteModel(models.Model):
    id         = models.CharField(max_length=50, primary_key=True)
    student    = models.ForeignKey(StudentModel, on_delete=models.CASCADE, related_name="notes")
    course     = models.ForeignKey(CourseModel, on_delete=models.CASCADE, related_name="notes")
    value      = models.FloatField()

    class Meta:
        db_table = "notes"

    def __str__(self):
        return f"{self.student} - {self.course} - {self.value}"