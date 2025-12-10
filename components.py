class Components:
    main_window = None
    blocks_canvas = None
    object_canvas = None
    decors_canvas = None
    menu = None

    current_canvas = None

    map_size = None
    editor_map_size = None
    editor_scale = None

    brush_color = None


    @staticmethod
    def set_window(obj):
        Components.main_window = obj

    @staticmethod
    def get_window():
        return Components.main_window



    @staticmethod
    def set_canvas(obj):
        Components.blocks_canvas = obj

    @staticmethod
    def get_canvas():
        return Components.blocks_canvas



    @staticmethod
    def set_menu(obj):
        Components.menu = obj

    @staticmethod
    def get_menu():
        return Components.menu

