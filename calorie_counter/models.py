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
        result = ''
        if self.disambiguator == '':
            result = '%s %s ' % (self.first_name, self.last_name)
        else:
            result = '%s, %s (%s)' % (self.first_name, self.last_name, self.disambiguator)
        return result

    def get_absolute_url(self):
        return reverse('calorie_counter_member_detail_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_update_url(self):
        return reverse('calorie_counter_member_update_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['first_name', 'last_name', 'e_mail'], name='unique_member')
        ]


class DailyMacroGoal(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey('Member', related_name='daily_macro_goals', on_delete=models.CASCADE)
    protein_goal = models.IntegerField()
    carbohydrate_goal = models.IntegerField()
    fat_goal = models.IntegerField()
    date = models.DateField()

    def get_absolute_url(self):
        return reverse('calorie_counter_daily_macro_goal_detail_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_update_url(self):
        return reverse('calorie_counter_daily_macro_goal_update_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def __str__(self):
        return 'Macro goal for %s on %s' % (self.member, self.date)


class Food(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    calories_per_serving = models.IntegerField()
    protein_grams = models.IntegerField()
    carbohydrates_grams = models.IntegerField()
    fat_grams = models.IntegerField()

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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_food')
        ]


class MealFood(models.Model):
    meal_log = models.ForeignKey('MealLog', related_name='meal_foods', on_delete=models.CASCADE)
    food = models.ForeignKey(Food, related_name='meal_foods', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2, help_text="Serving size:")

    def get_absolute_url(self):
        return reverse('calorie_counter_meal_food_detail_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_update_url(self):
        return reverse('calorie_counter_meal_food_update_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def __str__(self):
        return "%s in %s" % (self.food, self.quantity)


class MealLog(models.Model):
    MEAL_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack'),
    ]

    id = models.AutoField(primary_key=True)
    date = models.DateField()
    time = models.TimeField()
    meal_type = models.CharField(max_length=50, choices=MEAL_CHOICES)
    member = models.ForeignKey('Member', related_name='meal_logs', on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse('calorie_counter_meal_log_detail_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_update_url(self):
        return reverse('calorie_counter_meal_log_update_urlpattern',
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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['exercise_type'], name='unique_exercise')
        ]


class ExerciseLog(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    duration = models.DecimalField(max_digits=5, decimal_places=2, help_text="Duration in minutes")
    member = models.ForeignKey('Member', related_name='exercise_logs', on_delete=models.CASCADE)
    exercise = models.ForeignKey('Exercise', related_name='exercise_logs', on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse('calorie_counter_exercise_log_detail_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_update_url(self):
        return reverse('calorie_counter_exercise_log_update_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def __str__(self):
        return 'Exercise Log: %s on %s' % ( self.member, self.date )


class CalorieGoal(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey('Member', related_name='calorie_goals', on_delete=models.CASCADE)
    target_calories = models.IntegerField()
    begin_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('calorie_counter_calorie_goal_detail_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_update_url(self):
        return reverse('calorie_counter_calorie_goal_update_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def __str__(self):
       return '%s calories goal for %s' % (self.target_calories, self.member)


