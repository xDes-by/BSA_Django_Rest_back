from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class ShopHistory(models.Model):
    steamID = models.IntegerField(verbose_name='Пользователь')
    coins = models.IntegerField(verbose_name='Монет', default=0)

class ProductCategory(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категория товаров'

class Product(models.Model):
    name = models.CharField(max_length=64, default=None, verbose_name="Товар")
    price = models.IntegerField(default=0, verbose_name="Цена")
    upgrade_price = models.IntegerField(default=0, verbose_name="Цена улучшения")
    rp_price = models.IntegerField(default=0, verbose_name="Цена в РП")
    rp_upgrade_price = models.IntegerField(default=0, verbose_name="Цена улучшения в РП")
    item_level = models.IntegerField(default=1, verbose_name="Уровень предмета")
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name="Категория")
    # image = models.ImageField(upload_to='images/product/', verbose_name="Фото")
    can_upgrade = models.BooleanField(default=False, verbose_name='Улучшаемый')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class User(models.Model):
    steamID = models.IntegerField(verbose_name='Пользователь')
    coins = models.IntegerField(verbose_name='Монет', default=0)
    rp = models.IntegerField(verbose_name='РП', default=0)
    total_coins = models.IntegerField(verbose_name='Суммарный донат', default=0)
    ban_status = models.BooleanField(default=False, verbose_name='Бан')

    def __str__(self):
        return str(self.steamID)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name='profile', on_delete=models.CASCADE, verbose_name='Профиль')
    wins = models.IntegerField(default=0, verbose_name="Побед")
    lose = models.IntegerField(default=0, verbose_name="Поражений")
    games = models.IntegerField(default=0, verbose_name="Игр") 
    level = models.IntegerField(default=1, verbose_name="Уровень")
    player_exp = models.IntegerField(default=0, verbose_name="Опыт")
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")
    skill_points = models.IntegerField(default=0, verbose_name="Поинтов")
    str = models.IntegerField(default=0, verbose_name="Сила")
    agi = models.IntegerField(default=0, verbose_name="Ловкость")
    int = models.IntegerField(default=0, verbose_name="Итлеллект")
    hpr = models.IntegerField(default=0, verbose_name="Реген ХП")
    mpr = models.IntegerField(default=0, verbose_name="Реген МП")
    movespeed = models.IntegerField(default=0, verbose_name="Скорость передвижения")
    armor = models.IntegerField(default=0, verbose_name="Броня")
    mresist = models.IntegerField(default=0, verbose_name="Резист магии")
    exp = models.IntegerField(default=0, verbose_name="Опыт за крипа")
    coolddown = models.IntegerField(default=0, verbose_name="Перезарядка")
    damage = models.IntegerField(default=0, verbose_name="Урон")
    attack_speed = models.IntegerField(default=0, verbose_name="Скорость атаки")
    evasion = models.IntegerField(default=0, verbose_name="Уклонение")
    spellamp = models.IntegerField(default=0, verbose_name="Усиление закленаний")

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профиль'       

class UserItems(models.Model):
    user = models.ForeignKey(User, related_name='product', on_delete=models.CASCADE,  default=None, verbose_name='Items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None, verbose_name='Предмет')
    count = models.IntegerField(default=1, verbose_name='Количество')
    active = models.BooleanField(default=False, verbose_name='Активность')

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'    


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance
        )