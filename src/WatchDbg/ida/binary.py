import idaapi


class Binary:
    @staticmethod
    def get_word_size():
        inf = idaapi.get_inf_structure()
        size = 2
        if inf.is_32bit():
            size = 4
        elif inf.is_64bit():
            size = 8
        return size
