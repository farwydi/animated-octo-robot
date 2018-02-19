import hashlib


class GrailList:
    def __init__(self):
        self.list = []

    def push(self, message):
        data_hash = hashlib.md5(message.encode('utf-8'))

        print(data_hash)

        if len(self.list) > 0:
            a = self.pull()

            self.list.append(hashlib.md5("%s%s" % (self.pull(), data_hash)))
        else:
            self.list.append(data_hash)

    def pull(self):
        return self.list[-1]

    def show(self):
        for l in self.list:
            print(l)


a = GrailList()
a.push("1")
a.push("2")
a.push("3")
a.show()
