class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        print str(f'Тип тренировки: {self.training_type};'
                  f'Длительность: {self.duration:.3f} ч.;'
                  f'Дистанция: {self.distance:.3f} км;'
                  f'Ср. скорость: {self.speed:.3f} км/ч;'
                  f'Потрачено ккал: {self.calories:.3f}.'
                  )


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        get_distance = self.action * self.LEN_STEP / self.M_IN_KM
        return get_distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        get_mean_speed = self.get_distance() / self.duration
        return get_mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage()


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        get_spent_calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                              * self.get_mean_speed()
                              + self.CALORIES_MEAN_SPEED_SHIFT)
                              * self.weight
                              * self.duration
                              * self.MIN_IN_H)
        return get_spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_mean_speed(self) -> float:
        self.mean_speed = (self.action * self.LEN_STEP
                           / self.duration / self.M_IN_KM)
        return self.mean_speed

    def get_spent_calories(self) -> float:
        KMH_TO_MSEC = self.get_mean_speed / self.M_IN_KM
        self.spent_calories = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                               + (KMH_TO_MSEC**2 / self.height)
                               * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                               * self.weight)
                               * self.duration * self.MIN_IN_H
                               )
        return self.spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 lenght_pool: float,
                 count_pool: float):
        super().__init__(action, duration, weight)
        self.lenght_pool = lenght_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        self.get_mean_speed = (self.lenght_pool
                               * self.count_pool
                               / self.M_IN_KM
                               / self.duration)
        return self.get_mean_speed

    def get_spent_calories(self) -> float:
        self.get_spent_calories = ((self.get_mean_speed
                                   + self.CALORIES_MEAN_SPEED_SHIFT)
                                   * self.CALORIES_WEIGHT_MULTIPLIER
                                   * self.weight
                                   * self.duration)
        return self.get_spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dic = {'SWM': Swimming,
                    'RUN': Running,
                    'WLK': SportsWalking}
    return training_dic[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
