import ida_kernwin


class Modal:
    @staticmethod
    def request_string(prompt, default=""):
        string = ida_kernwin.ask_str(default, 98, str(prompt))
        if string == None:
            string = ""
        return string
