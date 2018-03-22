import base64
import hashlib
import os.path

import diff_match_patch as dmp_module

from protocol import GrailProtocol, GrailException


class Grail(object):
    def __init__(self, default_path=""):
        self.__init = False
        self.__algorithm = "sha1"
        self.__patches = []
        self.__last_grail = ""
        self.__block_chain = []
        self.__protocol = GrailProtocol(default_path)
        self.__prev_hash = None
        self.__header_hash = None
        self.__key = None
        self.__login = ""

    @staticmethod
    def __encrypt_str(x: str) -> bytes:
        """Кодируем входную строку в base64.

        :param x: base str.
        :type x: str
        :return: encrypted string
        """
        return base64.b64encode(x.encode('utf-8'))

    def __is_open(self):
        """
        Проверка Grail на истинность.
        """
        if not self.__init:
            raise GrailException("First you need to open the Grail")

    def __is_valid(self):
        """
        Проверка Grail на истинность.
        """
        if not self.valid():
            raise GrailException("Grail is not valid")

    def __insert(self, raw_str_diff: str):
        """
        Добавляет в конец grail новую запись.

        Новый хэш равен сумме предыдущего хэша и хэш новой записи.

        :param raw_str_diff: Строка, которую нужно внести в Grail
        """
        # Создаём объект хэша на основе предыдущего.
        next_hash = hashlib.new(self.__algorithm, self.__prev_hash)

        # Кодируем входную строку в base64 и дополняем хэш.
        record = self.__encrypt_str(raw_str_diff)
        next_hash.update(record)

        # Обновляем последний хэш.
        # Теперь последнем хэшем является текущий хэш.
        self.__prev_hash = next_hash.digest()

        # Добавляем индексацию.
        self.__block_chain.append((record, self.__prev_hash))

    def close(self):
        if self.__init:
            self.save()
            self.__init = False
            self.__key = None
            self.__patches.clear()

    def save(self, force=True):
        """

        :param force:
        :return:
        """
        self.__is_open()
        self.__is_valid()

        file = self.__protocol.return_path(self.__login)

        if force and os.path.exists(file):
            os.unlink(file)

        self.__protocol.create(self.__login, self.__key, self.__algorithm, self.__block_chain)

    def open(self, login: str, password: str):
        """
        Попытка инициализировать Grail из файла.
        """
        self.close()

        self.__key = self.__protocol.gen_password_key(password)

        # Проверка занятости файл.
        if not os.path.exists(self.__protocol.return_path(login)):
            # Физическое создание файл Grail.
            self.__protocol.create(login, self.__key)

        self.__algorithm, self.__header_hash, self.__block_chain = self.__protocol.open(login, self.__key)

        if len(self.__block_chain) > 0:
            _, self.__prev_hash = self.__block_chain[-1]
        else:
            self.__prev_hash = self.__header_hash

        self.__init = True

    def valid(self):
        """
        Проверка Grail на истинность.

        :return: Истинность Grail.
        """
        # Получение первого хэша.
        prev = self.__header_hash

        for record, chain in self.__block_chain:
            # Инициализация следующего хэша.
            next_hash = hashlib.new(self.__algorithm)
            next_hash.update(prev)
            next_hash.update(record)

            # Обновление предыдущего хэша новым.
            prev = next_hash.digest()

            if prev != chain:
                return False

        return True

    def update(self, new_grail: str):
        """
        Обновляет Grail добовляя изменения.

        :param new_grail: Новая форма Grail.
        :raise GrailException: Возникает, если Grail был не инициализирован.
        :raise GrailException: Возникает, если Grail повреждён или не валиден.
        """
        self.__is_open()
        self.__is_valid()

        # Инициализация модуля diff_match_patch.
        dmp = dmp_module.diff_match_patch()

        # Создания патча.
        patch = dmp.patch_make(self.__last_grail, new_grail)

        # Запись патча в память для ускорения работы системы.
        self.__patches.append(patch)

        # Добавления в блокчейн новой записи.
        self.__insert(dmp.patch_toText(patch))

        # Обновляем последнее состояния Grail.
        self.__last_grail = new_grail

    def get(self, patch_count=None) -> str:
        """
        Восстанавливает Grail.

        :param patch_count: Количество патчей, которые нужно применить.
        :type patch_count: int
        :raise GrailException: Возникает, если Grail был не инициализирован.
        :raise GrailException: Возникает, если Grail повреждён или не валиден.
        :return: Grail.
        """
        self.__is_open()
        self.__is_valid()

        # Инициализация модуля diff_match_patch.
        dmp = dmp_module.diff_match_patch()

        # Начало с нуля.
        grail = ''

        if patch_count is None:
            # Принятия всех патчей.
            for patch in self.__patches:
                grail, _ = dmp.patch_apply(patch, grail)
        else:
            # Принятия определённое количество патчей.
            for i in range(patch_count):
                grail, _ = dmp.patch_apply(self.__patches[i], grail)

        return grail

    def get_diff(self, idx: int) -> str:
        """
        Получить интерпретацию тачка по номеру.

        :param idx: Порядковый номер патча.
        :type idx: int
        :raise ValueError: idx < 0
        :raise ValueError: idx out of range.
        :return: Патч в текстовом формате.
        """
        if idx < 0:
            raise ValueError()

        try:
            record, = self.__block_chain[idx]

            diff = base64.b64decode(record)
            return diff.decode('utf-8')

        except IndexError as e:
            raise ValueError(e)
