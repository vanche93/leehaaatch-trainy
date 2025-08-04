from django.db import models

class Student(models.Model):
    name = models.CharField(verbose_name='Имя', blank=True, null=True, unique=False)
    tg_name = models.CharField(verbose_name='Ник telegram', blank=False, unique=False)
    tg_id = models.CharField(verbose_name='Telegram ID', blank=False, unique=True)
    notes = models.TextField(verbose_name='Заметки',blank=True)

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'

    def __str__(self):
        return f'{self.name}({self.tg_name})'

class TrainingTime(models.Model):
    time = models.TimeField(verbose_name='Время', unique=True)

    class Meta:
        verbose_name = 'Время начала тренировки'
        verbose_name_plural = 'Времена начала тренировки'

    def __str__(self):
        return self.time.strftime('%H:%M')

class TrainingTopic(models.Model):
    name = models.CharField(verbose_name='Имя', unique=True)
    description = models.TextField(verbose_name='Описание',blank=True)
    image = models.ImageField(verbose_name='Изображение',blank=True)

    class Meta:
        verbose_name = 'Тема тренировки'
        verbose_name_plural = 'Темы тренировки'

    def __str__(self):
        return self.name

class Training(models.Model):
    name = models.CharField(verbose_name='Имя', blank=True, null=True)
    description = models.TextField(verbose_name='Описание',blank=True)
    date = models.DateField(verbose_name='Дата')
    training_times = models.ManyToManyField(TrainingTime, verbose_name='Времена начала тренировки')
    topics = models.ManyToManyField(TrainingTopic, verbose_name='Темы тренировки')
    image = models.ImageField(verbose_name='Изображение',blank=True)
    max_participants = models.IntegerField(verbose_name='Кол-во участников',default=4)
    participants = models.ManyToManyField(Student, verbose_name='Участники', blank=True)
    final_time = models.ForeignKey(TrainingTime, verbose_name='Время начала тренировки',
                                   on_delete=models.PROTECT, related_name='final_time',
                                   blank=True, null=True)
    final_topic= models.ForeignKey(TrainingTopic, verbose_name='Тема тренировки',
                                   on_delete=models.PROTECT, related_name='final_topic',
                                   blank=True, null=True)
    status = models.CharField(verbose_name='Статус', default='created', choices=[
        ('created', 'Создана'),
        ('open', 'Открыта для записи'),
        ('full', 'Мест нет (заполнена)'),
        ('completed', 'Завершена'),
        ('canceled', 'Отменена')
    ])

    class Meta:
        verbose_name = 'Тренировка'
        verbose_name_plural = 'Тренировки'

    def __str__(self):
        return f' {self.date.strftime('%d.%m.%Y')}: {self.name}'

class TrainingReq(models.Model):
    student = models.ForeignKey(Student, verbose_name='Ученик', on_delete=models.PROTECT)
    training = models.ForeignKey(Training, verbose_name='Тренировка', on_delete=models.PROTECT)
    training_times = models.ManyToManyField(TrainingTime, verbose_name='Время начала тренировки')
    topics = models.ManyToManyField(TrainingTopic, verbose_name='Темы тренировки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        verbose_name = 'Запрос на тренировку'
        verbose_name_plural = 'Запросы на тренировку'
        unique_together = ('student', 'training')

    def __str__(self):
        return f'{self.student}, {self.training}'