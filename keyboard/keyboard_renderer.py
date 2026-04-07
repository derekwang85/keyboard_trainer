#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
键盘渲染器，负责渲染键盘和按键高亮
"""

import pygame
from font_loader import load_font

class KeyboardRenderer:
    """键盘渲染器类"""
    
    def __init__(self, config):
        """
        初始化键盘渲染器
        
        参数:
        - config: 游戏配置
        """
        self.config = config
        
        # 键盘位置和大小
        self.keyboard_width = config.KEYBOARD_WIDTH
        self.keyboard_height = config.KEYBOARD_HEIGHT
        self.keyboard_x = config.KEYBOARD_POS_X
        self.keyboard_y = config.KEYBOARD_POS_Y
        
        # 按键大小和间距
        self.key_width = 40
        self.key_height = 40
        self.key_margin = 2
        
        # 按键颜色
        self.key_bg_color = (200, 200, 200)
        self.key_text_color = (0, 0, 0)
        self.key_border_color = (100, 100, 100)
        self.key_highlight_color = (100, 200, 255)
        self.key_pressed_color = (50, 150, 200)
        self.key_error_color = (255, 100, 100)
        
        # 高亮状态：支持多键，duration=None 表示持续高亮
        self.highlights = {}
        
        # 按键映射
        self.key_map = self._create_key_map()
        
        # 手指颜色映射（用于指法指导）
        self.finger_colors = {
            'left_pinkie': (255, 100, 100),    # 左手小指
            'left_ring': (255, 150, 100),      # 左手无名指
            'left_middle': (255, 200, 100),    # 左手中指
            'left_index': (255, 255, 100),     # 左手食指
            'left_thumb': (200, 255, 100),     # 左手拇指
            'right_thumb': (150, 255, 100),    # 右手拇指
            'right_index': (100, 255, 100),    # 右手食指
            'right_middle': (100, 255, 150),   # 右手中指
            'right_ring': (100, 255, 200),     # 右手无名指
            'right_pinkie': (100, 200, 255)    # 右手小指
        }
        
        # 按键到手指的映射
        self.key_to_finger = self._create_key_to_finger_map()
        
        # 字体 - 使用统一的字体加载器
        self.font = load_font(16, font_dir=config.FONTS_DIR)
        
        # 初始化键盘布局
        self._init_keyboard_layout()
    
    def _create_key_map(self):
        """创建按键映射"""
        # 按键映射，用于将pygame的按键常量映射到字符
        key_map = {
            pygame.K_a: 'a', pygame.K_b: 'b', pygame.K_c: 'c', pygame.K_d: 'd',
            pygame.K_e: 'e', pygame.K_f: 'f', pygame.K_g: 'g', pygame.K_h: 'h',
            pygame.K_i: 'i', pygame.K_j: 'j', pygame.K_k: 'k', pygame.K_l: 'l',
            pygame.K_m: 'm', pygame.K_n: 'n', pygame.K_o: 'o', pygame.K_p: 'p',
            pygame.K_q: 'q', pygame.K_r: 'r', pygame.K_s: 's', pygame.K_t: 't',
            pygame.K_u: 'u', pygame.K_v: 'v', pygame.K_w: 'w', pygame.K_x: 'x',
            pygame.K_y: 'y', pygame.K_z: 'z',
            
            pygame.K_0: '0', pygame.K_1: '1', pygame.K_2: '2', pygame.K_3: '3',
            pygame.K_4: '4', pygame.K_5: '5', pygame.K_6: '6', pygame.K_7: '7',
            pygame.K_8: '8', pygame.K_9: '9',
            
            pygame.K_SPACE: ' ', pygame.K_RETURN: 'Enter', pygame.K_TAB: 'Tab',
            pygame.K_BACKSPACE: 'Backspace', pygame.K_LSHIFT: 'Shift', pygame.K_RSHIFT: 'Shift',
            pygame.K_LCTRL: 'Ctrl', pygame.K_RCTRL: 'Ctrl',
            pygame.K_LALT: 'Alt', pygame.K_RALT: 'Alt',
            pygame.K_CAPSLOCK: 'Caps', pygame.K_ESCAPE: 'Esc',
            
            pygame.K_MINUS: '-', pygame.K_EQUALS: '=', pygame.K_LEFTBRACKET: '[',
            pygame.K_RIGHTBRACKET: ']', pygame.K_BACKSLASH: '\\',
            pygame.K_SEMICOLON: ';', pygame.K_QUOTE: "'", pygame.K_COMMA: ',',
            pygame.K_PERIOD: '.', pygame.K_SLASH: '/',
        }
        
        return key_map
    
    def _create_key_to_finger_map(self):
        """创建按键到手指的映射"""
        # 标准指法按键映射
        key_to_finger = {
            # 左手小指
            '1': 'left_pinkie', '2': 'left_pinkie', 'q': 'left_pinkie', 'w': 'left_pinkie',
            'a': 'left_pinkie', 's': 'left_pinkie', 'z': 'left_pinkie', 'x': 'left_pinkie',
            '`': 'left_pinkie', '~': 'left_pinkie',
            
            # 左手无名指
            '3': 'left_ring', 'e': 'left_ring', 'd': 'left_ring', 'c': 'left_ring',
            
            # 左手中指
            '4': 'left_middle', 'r': 'left_middle', 'f': 'left_middle', 'v': 'left_middle',
            
            # 左手食指
            '5': 'left_index', '6': 'left_index', 't': 'left_index', 'y': 'left_index',
            'g': 'left_index', 'h': 'left_index', 'b': 'left_index', 'n': 'left_index',
            
            # 左手拇指
            ' ': 'left_thumb',
            
            # 右手拇指
            ' ': 'right_thumb',
            
            # 右手食指
            '7': 'right_index', '8': 'right_index', 'u': 'right_index', 'i': 'right_index',
            'j': 'right_index', 'k': 'right_index', 'm': 'right_index', ',': 'right_index',
            
            # 右手中指
            '9': 'right_middle', 'o': 'right_middle', 'l': 'right_middle', '.': 'right_middle',
            
            # 右手无名指
            '0': 'right_ring', 'p': 'right_ring', ';': 'right_ring', ':': 'right_ring',
            '/': 'right_ring', '?': 'right_ring',
            
            # 右手小指
            '-': 'right_pinkie', '_': 'right_pinkie', '=': 'right_pinkie', '+': 'right_pinkie',
            '[': 'right_pinkie', '{': 'right_pinkie', ']': 'right_pinkie', '}': 'right_pinkie',
            '\\': 'right_pinkie', '|': 'right_pinkie', "'": 'right_pinkie', '"': 'right_pinkie',
            'Enter': 'right_pinkie', 'Shift': 'right_pinkie', 'Ctrl': 'right_pinkie',
            'Alt': 'right_pinkie', 'Caps': 'right_pinkie', 'Esc': 'right_pinkie',
            'Tab': 'left_pinkie', 'Backspace': 'right_pinkie',
            'Win': 'left_thumb', 'Fn': 'left_thumb',
        }
        
        return key_to_finger
    
    def _init_keyboard_layout(self):
        """初始化键盘布局"""
        # 定义键盘布局
        # 每个按键的格式: (字符, x位置, y位置, 宽度, 高度)
        self.keyboard_layout = [
            # 第一行
            [('`', 0, 0), ('1', 1, 0), ('2', 2, 0), ('3', 3, 0), ('4', 4, 0),
             ('5', 5, 0), ('6', 6, 0), ('7', 7, 0), ('8', 8, 0), ('9', 9, 0),
             ('0', 10, 0), ('-', 11, 0), ('=', 12, 0), ('Backspace', 13, 0, 2, 1)],
            
            # 第二行
            [('Tab', 0, 1, 1.5, 1), ('q', 1.5, 1), ('w', 2.5, 1), ('e', 3.5, 1),
             ('r', 4.5, 1), ('t', 5.5, 1), ('y', 6.5, 1), ('u', 7.5, 1),
             ('i', 8.5, 1), ('o', 9.5, 1), ('p', 10.5, 1), ('[', 11.5, 1),
             (']', 12.5, 1), ('\\', 13.5, 1)],
            
            # 第三行
            [('Caps', 0, 2, 1.75, 1), ('a', 1.75, 2), ('s', 2.75, 2), ('d', 3.75, 2),
             ('f', 4.75, 2), ('g', 5.75, 2), ('h', 6.75, 2), ('j', 7.75, 2),
             ('k', 8.75, 2), ('l', 9.75, 2), (';', 10.75, 2), ("'", 11.75, 2),
             ('Enter', 12.75, 2, 1.75, 1)],
            
            # 第四行
            [('Shift', 0, 3, 2.25, 1), ('z', 2.25, 3), ('x', 3.25, 3), ('c', 4.25, 3),
             ('v', 5.25, 3), ('b', 6.25, 3), ('n', 7.25, 3), ('m', 8.25, 3),
             (',', 9.25, 3), ('.', 10.25, 3), ('/', 11.25, 3), ('Shift', 12.25, 3, 2.25, 1)],
            
            # 第五行
            [('Ctrl', 0, 4, 1.25, 1), ('Win', 1.25, 4, 1.25, 1),
             ('Alt', 2.5, 4, 1.25, 1), (' ', 3.75, 4, 8, 1),
             ('Alt', 11.75, 4, 1.25, 1), ('Fn', 13, 4, 1.25, 1), ('Ctrl', 14.25, 4, 1.25, 1)]
        ]
        
        # 计算按键的实际位置和大小
        self.keys = []
        for row in self.keyboard_layout:
            for key_info in row:
                char = key_info[0]
                x_pos = key_info[1]
                y_pos = key_info[2]
                
                # 按键宽度和高度，默认为1个单位
                width = 1
                height = 1
                
                # 如果有指定宽度和高度，则使用指定的值
                if len(key_info) > 3:
                    width = key_info[3]
                if len(key_info) > 4:
                    height = key_info[4]
                
                # 计算实际的像素位置和大小
                x = self.keyboard_x + x_pos * (self.key_width + self.key_margin)
                y = self.keyboard_y + y_pos * (self.key_height + self.key_margin)
                w = width * self.key_width + (width - 1) * self.key_margin
                h = height * self.key_height + (height - 1) * self.key_margin
                
                # 添加到按键列表
                self.keys.append({
                    'char': char,
                    'rect': pygame.Rect(x, y, w, h),
                    'finger': self.key_to_finger.get(char.lower() if len(char) == 1 else char, None)
                })

        if self.keys:
            min_x = min(key['rect'].left for key in self.keys)
            max_x = max(key['rect'].right for key in self.keys)
            min_y = min(key['rect'].top for key in self.keys)
            max_y = max(key['rect'].bottom for key in self.keys)

            actual_width = max_x - min_x
            actual_height = max_y - min_y

            desired_x = (self.config.SCREEN_WIDTH - actual_width) // 2
            desired_y = (self.config.SCREEN_HEIGHT - actual_height) // 2

            dx = desired_x - min_x
            dy = desired_y - min_y

            for key in self.keys:
                key['rect'].move_ip(dx, dy)

            self.keyboard_x = desired_x
            self.keyboard_y = desired_y
            self.keyboard_width = actual_width
            self.keyboard_height = actual_height
    
    def render(self, screen):
        """
        渲染键盘
        
        参数:
        - screen: 游戏屏幕
        """
        # 渲染背景
        keyboard_rect = pygame.Rect(
            self.keyboard_x - 10,
            self.keyboard_y - 10,
            self.keyboard_width + 20,
            self.keyboard_height + 20
        )
        pygame.draw.rect(screen, (180, 180, 180), keyboard_rect, border_radius=10)
        
        # 渲染按键
        expired_keys = []
        for key in self.keys:
            # 确定按键颜色
            color = self.key_bg_color
            highlight = self.highlights.get(key['char'])
            if highlight:
                color = highlight['color']
                # 计时高亮递减
                if highlight['duration'] is not None:
                    highlight['duration'] -= 1
                    if highlight['duration'] <= 0:
                        expired_keys.append(key['char'])

            # 绘制按键
            pygame.draw.rect(screen, color, key['rect'], border_radius=5)
            pygame.draw.rect(screen, self.key_border_color, key['rect'], 2, border_radius=5)

        # 清理过期高亮
        for char in expired_keys:
            self.highlights.pop(char, None)

        # 绘制按键文本和指示（对所有按键）
        for key in self.keys:
            text_surface = self.font.render(key['char'], True, self.key_text_color)
            text_rect = text_surface.get_rect(center=key['rect'].center)
            screen.blit(text_surface, text_rect)


    
    def highlight_key(self, key_char, color=None, duration=30):
        """
        高亮显示指定按键
        
        参数:
        - key_char: 要高亮的按键字符
        - color: 高亮颜色，默认为None（使用默认高亮颜色）
        - duration: 高亮持续时间（帧数），None 表示持续
        """
        if key_char is None:
            return
        self.highlights[key_char] = {
            'color': color or self.key_highlight_color,
            'duration': duration
        }
    
    def clear_highlight(self, key_char=None):
        """清除高亮（单个或全部）"""
        if key_char:
            self.highlights.pop(key_char, None)
        else:
            self.highlights.clear()
    
    def highlight_finger_keys(self, finger, color=None, duration=30):
        """
        高亮显示指定手指对应的所有按键
        
        参数:
        - finger: 手指名称
        - color: 高亮颜色，默认为None（使用手指对应的颜色）
        - duration: 高亮持续时间（帧数）
        """
        if color is None:
            color = self.finger_colors.get(finger, self.key_highlight_color)
        
        for key in self.keys:
            if key['finger'] == finger:
                self.highlight_key(key['char'], color, duration)
    
    def get_key_by_char(self, char):
        """
        根据字符获取按键信息
        
        参数:
        - char: 按键字符
        
        返回:
        - 按键信息字典，如果未找到则返回None
        """
        for key in self.keys:
            if key['char'] == char:
                return key
        return None
    
    def get_key_by_position(self, pos):
        """
        根据位置获取按键信息
        
        参数:
        - pos: 位置坐标 (x, y)
        
        返回:
        - 按键信息字典，如果未找到则返回None
        """
        for key in self.keys:
            if key['rect'].collidepoint(pos):
                return key
        return None
    
    def get_finger_for_key(self, key_char):
        """
        获取按键对应的手指
        
        参数:
        - key_char: 按键字符
        
        返回:
        - 手指名称，如果未找到则返回None
        """
        # 对于单字符按键，转换为小写查找
        if len(key_char) == 1:
            return self.key_to_finger.get(key_char.lower(), None)
        else:
            # 对于特殊按键（如'Shift', 'Enter'等），直接查找
            return self.key_to_finger.get(key_char, None)
    
    def show_finger_guide(self, key_char):
        """
        显示按键对应的手指指导
        
        参数:
        - key_char: 按键字符
        """
        finger = self.get_finger_for_key(key_char)
        if finger:
            self.highlight_finger_keys(finger, duration=60)