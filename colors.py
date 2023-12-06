class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def color_factory(color):

    def color_function(s):
        return f"{color}{s}{bcolors().ENDC}"

    return color_function

green = color_factory(bcolors().OKGREEN)
cyan = color_factory(bcolors().OKCYAN)
blue = color_factory(bcolors().OKBLUE)
yellow = color_factory(bcolors().WARNING)
red = color_factory(bcolors().FAIL)
bold = color_factory(bcolors().BOLD)
