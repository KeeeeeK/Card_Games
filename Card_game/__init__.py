# Если функция не меняет класс, метод будет начинаться с символов "i_". (information)

# Если функция может не отработать и это нормально для игры, то:
# 1. Метод будет возвращать None при ошибке
# 2. Метод будет начинаться с "n_". (None)

# Сам по себе вызов некоторых функций невозможен, пока в игре не задан КОНТЕКСТ.
# Название таких функций будет будет начинатся с "c_"

# Поля некоторых классов необходимо изменить при импортировании.
# (Просто они задаются для всей игры и никогда не изменяются)
# Это:
# source_phases в Game
# lst_of_indexes_res в Resources
