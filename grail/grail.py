from base64 import b64encode, b64decode
from hashlib import new
from os.path import exists
from os import remove
from diff_match_patch import diff_match_patch as dmp_module

from protocol import GrailProtocol


class GrailIsNotValid(Exception):
    pass


class GrailIsNotInit(Exception):
    pass


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

    def __format__(self, format_spec):
        return self.get()

    @staticmethod
    def __encoding_str(x: str) -> bytes:
        """Кодируем входную строку в base64.

        :param x: base str.
        :type x: str
        :return: encrypted string
        """
        return b64encode(x.encode('utf-8'))

    @staticmethod
    def __decoding_str(x: bytes) -> str:
        """

        :param x:
        :return:
        """
        return b64decode(x).decode("utf-8")

    def __is_open(self):
        """
        Проверка Grail на истинность.
        """
        if not self.__init:
            raise GrailIsNotInit()

    def __is_valid(self):
        """
        Проверка Grail на истинность.
        """
        if not self.valid():
            raise GrailIsNotValid()

    def __insert(self, raw_str_diff: str):
        """
        Добавляет в конец grail новую запись.

        Новый хэш равен сумме предыдущего хэша и хэш новой записи.

        :param raw_str_diff: Строка, которую нужно внести в Grail
        """
        # Создаём объект хэша на основе предыдущего.
        next_hash = new(self.__algorithm, self.__prev_hash)

        # Кодируем входную строку в base64 и дополняем хэш.
        record = self.__encoding_str(raw_str_diff)
        next_hash.update(record)

        # Обновляем последний хэш.
        # Теперь последнем хэшем является текущий хэш.
        self.__prev_hash = next_hash.digest()

        # Добавляем индексацию.
        self.__block_chain.append((record, self.__prev_hash))

    def __destroy(self):
<<<<<<< Updated upstream
        """

        :return:
        """
        grail = self.__protocol.return_path(self.__login)

        if exists(grail):
            remove(grail)

    def get_header_hash(self) -> bytes:
        """

        :return:
        """
=======
        grail = self.__protocol.return_path(self.__login)

        if os.path.exists(grail):
            os.remove(grail)

    def get_header_hash(self):
>>>>>>> Stashed changes
        self.__is_open()
        self.__is_valid()

        return self.__header_hash

    def get_last_hash(self) -> bytes:
<<<<<<< Updated upstream
        """

        :return:
        """
=======
>>>>>>> Stashed changes
        self.__is_open()
        self.__is_valid()

        if len(self.__block_chain) > 0:
            _, chain = self.__block_chain[-1]
            return chain

        return self.__header_hash

    def get_hash_list(self) -> list:
        self.__is_open()
        self.__is_valid()

        result = []

        for _, chain in self.__block_chain:
            result.append(chain)

        return result

    def close(self):
        if self.__init:
            self.save()
            self.__init = False
            self.__login = ""
            self.__key = None
            self.__last_grail = ""
            self.__patches.clear()

    def get_grail_file(self):
<<<<<<< Updated upstream
        """

        :raise Gra
        :return:
        """
=======
>>>>>>> Stashed changes
        self.__is_open()

        return self.__protocol.return_path(self.__login)

    def destroy(self, close=True):
        self.__is_open()

        self.__destroy()
        self.close()

    def save(self, force=True):
        """

        :param force:
        :return:
        """
        self.__is_open()
        self.__is_valid()

        if force:
            self.__destroy()

        self.__protocol.write(self.__login, self.__key, self.__algorithm, self.__block_chain)

    def open(self, login: str, password: str):
        """
        Попытка инициализировать Grail из файла.

        :param login:
        :param password:
        :raise GrailIsNotValid:
        :raise ValueError:
        :return:
        """
        self.close()

        self.__key = self.__protocol.gen_password_key(password)
        self.__login = login

        # Проверка занятости файл.
<<<<<<< Updated upstream
        if not exists(self.__protocol.return_path(self.__login)):
            # Физическое создание файл Grail.
            self.__protocol.write(self.__login, self.__key)

        self.__algorithm, self.__header_hash, self.__block_chain = self.__protocol.read(self.__login, self.__key)

        self.__is_valid()
=======
        if not os.path.exists(self.__protocol.return_path(self.__login)):
            # Физическое создание файл Grail.
            self.__protocol.create(self.__login, self.__key)

        self.__algorithm, self.__header_hash, self.__block_chain = self.__protocol.open(self.__login, self.__key)
>>>>>>> Stashed changes

        if len(self.__block_chain) > 0:
            _, self.__prev_hash = self.__block_chain[-1]

            # Инициализация модуля diff_match_patch.
<<<<<<< Updated upstream
            dmp = dmp_module()

            for record, _ in self.__block_chain:
                patch = self.__decoding_str(record)
=======
            dmp = dmp_module.diff_match_patch()

            for record, chain in self.__block_chain:
                patch = base64.b64decode(record).decode("utf-8")
>>>>>>> Stashed changes

                self.__patches.append(dmp.patch_fromText(patch))
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
            next_hash = new(self.__algorithm)
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
        :raise GrailIsNotInit: Возникает, если Grail был не инициализирован.
        :raise GrailIsNotValid: Возникает, если Grail повреждён или не валиден.
        """
        self.__is_open()
        self.__is_valid()

        # Инициализация модуля diff_match_patch.
        dmp = dmp_module()

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
        :raise GrailIsNotInit: Возникает, если Grail был не инициализирован.
        :raise GrailIsNotValid: Возникает, если Grail повреждён или не валиден.
        :return: Grail.
        """
        self.__is_open()
        self.__is_valid()

        if patch_count == 0:
            return ""

        # Инициализация модуля diff_match_patch.
        dmp = dmp_module()

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
            raise ValueError(f"{idx} < 0")

        # Инициализация модуля diff_match_patch.
<<<<<<< Updated upstream
        dmp = dmp_module()
=======
        dmp = dmp_module.diff_match_patch()
>>>>>>> Stashed changes

        try:
            return dmp.patch_toText(self.__patches[idx])

        except IndexError as e:
            raise ValueError(e)
