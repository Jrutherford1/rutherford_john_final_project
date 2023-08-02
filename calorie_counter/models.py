from django.db import models
from django.urls import reverse


class Member(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    e_mail = models.EmailField(max_length=254, unique=True)
    height = models.IntegerField(help_text="Height in inches")
    weight = models.IntegerField(help_text="Weight in pounds")
    age = models.IntegerField(help_text="Age in years")
    sex = models.CharField(help_text="Male = M, Female = F", max_length=1, choices=SEX_CHOICES)
    date_joined = models.DateField()
    disambiguator = models.CharField(max_length=45, blank=True, default='')

    def __str__(self):

        if self.disambiguator == '':
            result = '%s %s ' % (self.last_name, self.first_name)
        else:
            result = '%s, %s (%s)' % (self.last_name, self.first_name, self.disambiguator)
        return result

    def get_absolute_url(self):
        return reverse('calorie_counter_member_detail_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_update_url(self):
        return reverse('calorie_counter_member_update_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_delete_url(self):
        return reverse('calorie_counter_member_delete_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    class Meta:
        ordering = ['last_name', 'first_name', 'disambiguator']
        constraints = [
            models.UniqueConstraint(fields=['last_name', 'first_name', 'e_mail'], name='unique_member')
        ]


class DailyMacroGoal(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey('Member', related_name='dailymacrogoals', on_delete=models.CASCADE)
    protein_goal = models.IntegerField(help_text="grams")
    carbohydrate_goal = models.IntegerField(help_text="grams")
    fat_goal = models.IntegerField(help_text="grams")
    date = models.DateField(help_text="00/00/0000")

    def get_absolute_url(self):
        return reverse('calorie_counter_dailymacrogoal_detail_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_update_url(self):
        return reverse('calorie_counter_dailymacrogoal_update_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_delete_url(self):
        return reverse('calorie_counter_dailymacrogoal_delete_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def __str__(self):
        return 'Macro goal for %s on %s' % (self.member, self.date)


class Food(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    calories_per_serving = models.IntegerField()
    protein_grams = models.IntegerField(help_text="grams")
    carbohydrates_grams = models.IntegerField(help_text="grams")
    fat_grams = models.IntegerField(help_text="grams")

    def __str__(self):
        return '%s' % self.name

    def get_absolute_url(self):
        return reverse('calorie_counter_food_detail_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_update_url(self):
        return reverse('calorie_counter_food_update_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_delete_url(self):
        return reverse('calorie_counter_food_delete_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_food')
        ]


class MealFood(models.Model):
    meal_log = models.ForeignKey('MealLog', related_name='mealfoods', on_delete=models.CASCADE)
    food = models.ForeignKey(Food, related_name='mealfoods', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2, help_text="Serving size:")

    def get_absolute_url(self):
        return reverse('calorie_counter_mealfood_detail_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_update_url(self):
        return reverse('calorie_counter_mealfood_update_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_delete_url(self):
        return reverse('calorie_counter_mealfood_delete_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def __str__(self):
        return "%s -- Quantity:  %s" % (self.food, self.quantity)


class MealLog(models.Model):
    MEAL_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack'),
    ]

    id = models.AutoField(primary_key=True)
    date = models.DateField(help_text="00/00/0000")
    time = models.TimeField(help_text="00:00:00")
    meal_type = models.CharField(max_length=50, choices=MEAL_CHOICES)
    member = models.ForeignKey('Member', related_name='meallogs', on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse('calorie_counter_meallog_detail_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_update_url(self):
        return reverse('calorie_counter_meallog_update_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_delete_url(self):
        return reverse('calorie_counter_meallog_delete_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def __str__(self):
        return '%s for %s on %s' % (self.meal_type, self.member, self.date)


class Exercise(models.Model):
    EXERCISE_TYPE_CHOICES = [
        ('Aerobic', 'Aerobic'),
        ('Anaerobic', 'Anaerobic'),
    ]

    id = models.AutoField(primary_key=True)
    exercise_type = models.CharField(max_length=50)
    exercise_category = models.CharField(max_length=10, choices=EXERCISE_TYPE_CHOICES, default='Aerobic')
    calories_burned_per_minute = models.IntegerField()

    def __str__(self):
        return '%s' % self.exercise_type

    def get_absolute_url(self):
        return reverse('calorie_counter_exercise_detail_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_update_url(self):
        return reverse('calorie_counter_exercise_update_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_delete_url(self):
        return reverse('calorie_counter_exercise_delete_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['exercise_type'], name='unique_exercise')
        ]


class ExerciseLog(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    duration = models.DecimalField(max_digits=5, decimal_places=2, help_text="Duration in minutes")
    member = models.ForeignKey('Member', related_name='exerciselogs', on_delete=models.CASCADE)
    exercise = models.ForeignKey('Exercise', related_name='exerciselogs', on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse('calorie_counter_exerciselog_detail_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_update_url(self):
        return reverse('calorie_counter_exerciselog_update_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_delete_url(self):
        return reverse('calorie_counter_exerciselog_delete_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def __str__(self):
        return 'Exercise Log: %s on %s' % (self.member, self.date)


class CalorieGoal(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey('Member', related_name='caloriegoals', on_delete=models.CASCADE)
    target_calories = models.IntegerField()
    begin_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('calorie_counter_caloriegoal_detail_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_update_url(self):
        return reverse('calorie_counter_caloriegoal_update_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_delete_url(self):
        return reverse('calorie_counter_caloriegoal_delete_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def __str__(self):
        return '%s calories goal for %s' % (self.target_calories, self.member)
