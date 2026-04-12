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
        
        # 按键大小和间距 - 优化为更大的圆角键帽
        self.key_width = 44
        self.key_height = 44
        self.key_margin = 4
        self.key_corner_radius = 8  # 圆角半径
        
        # 按键颜色 - 深色主题
        self.key_bg_color = config.KEY_DEFAULT_BG
        self.key_text_color = config.KEY_DEFAULT_TEXT
        self.key_border_color = config.KEY_BORDER
        self.key_highlight_color = config.KEY_HIGHLIGHT
        self.key_pressed_color = config.KEY_PRESSED
        self.key_error_color = config.KEY_ERROR
        self.keyboard_bg_color = config.KEYBOARD_BG
        self.key_home_pos_color = config.KEY_HOME_POS
        
        # 高亮状态：支持多键，duration=None 表示持续高亮
        self.highlights = {}
        
        # 闪烁状态：key_char -> {'blink_count': int, 'blink_frame': int, 'is_visible': bool}
        self.blink_keys = {}
        
        # 按键映射
        self.key_map = self._create_key_map()
        
        # 手指颜色映射（用于指法指导）- type.fun 风格配色
        self.finger_colors = {
            'left_pinkie': (239, 68, 68),       # 左手小指 - 红色 #EF4444
            'left_ring': (251, 146, 60),       # 左手无名指 - 橙色 #FB923C
            'left_middle': (234, 179, 8),       # 左手中指 - 黄色 #EAB308
            'left_index': (132, 204, 22),      # 左手食指 - 绿色 #84CC16
            'left_thumb': (16, 185, 129),      # 左手拇指 - 翠绿 #10B981
            'both_thumbs': (20, 184, 166),     # 双拇指 - 青绿 #14B8A6
            'right_thumb': (16, 185, 129),     # 右手拇指 - 翠绿 #10B981
            'right_index': (14, 165, 233),    # 右手食指 - 天蓝 #0EA5E9
            'right_middle': (99, 102, 241),    # 右手中指 - 靛蓝 #6366F1
            'right_ring': (168, 85, 247),     # 右手无名指 - 紫色 #A855F7
            'right_pinkie': (236, 72, 153)     # 右手小指 - 粉红 #EC4899
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
        r"""
        创建按键到手指的映射 - 修正为标准指法
        
        标准指法分配：
        - 左手小指: 1, Q, A, Z, Tab, CapsLock
        - 左手无名指: 2, W, S, X
        - 左手中指: 3, E, D, C
        - 左手食指: 4, 5, R, T, F, G, V, B
        - 右手食指: 6, 7, Y, U, H, J, N, M
        - 右手中指: 8, I, K, 逗号
        - 右手无名指: 9, O, L, 句号
        - 右手小指: 0, P, 分号, 斜杠, 减号等
        - 双拇指: 空格键 (双手拇指操作)
        """
        key_to_finger = {
            # ========== 左手区域 ==========
            # 左手小指 (最左列)
            '1': 'left_pinkie', 'q': 'left_pinkie', 'a': 'left_pinkie', 'z': 'left_pinkie',
            '`': 'left_pinkie', '~': 'left_pinkie',
            'Tab': 'left_pinkie', 'Caps': 'left_pinkie',  # Tab 和 CapsLock
            # 【修复】左手无名指 (2WSX) - 原错误映射到 left_pinkie
            '2': 'left_ring', 'w': 'left_ring', 's': 'left_ring', 'x': 'left_ring',
            # 【修复】左手中指 (3EDC) - 原错误映射到 left_ring
            '3': 'left_middle', 'e': 'left_middle', 'd': 'left_middle', 'c': 'left_middle',
            # 【修复】左手食指 (RFV TGB) - 原错误将 T Y G H 映射到 left_index
            '4': 'left_index', '5': 'left_index',  # 数字行的 4, 5
            'r': 'left_index', 'f': 'left_index', 'v': 'left_index',  # 左食指负责列
            't': 'left_index', 'g': 'left_index', 'b': 'left_index',  # 左食指上/下行
            # 左手拇指
            ' ': 'both_thumbs',  # 空格键由双手拇指操作
            
            # ========== 右手区域 ==========
            # 右手食指 (6YH NJM) - 右手基准键是 J 和 F
            '6': 'right_index', '7': 'right_index',
            'y': 'right_index', 'u': 'right_index',
            'h': 'right_index', 'j': 'right_index',  # J 是右手基准键
            'n': 'right_index', 'm': 'right_index',
            # 【修复】右手中指 (8IK ,) - 原错误将 I 映射到 right_index
            '8': 'right_middle', 'i': 'right_middle', 'k': 'right_middle', ',': 'right_middle',
            # 【修复】右手无名指 (9OL .) - 原错误将 0 映射到 right_ring
            '9': 'right_ring', 'o': 'right_ring', 'l': 'right_ring', '.': 'right_ring',
            # 右手小指 (0P;/ -[]\ 'Enter等)
            '0': 'right_pinkie', 'p': 'right_pinkie',
            ';': 'right_pinkie', ':': 'right_pinkie', '/': 'right_pinkie', '?': 'right_pinkie',
            '-': 'right_pinkie', '_': 'right_pinkie', '=': 'right_pinkie', '+': 'right_pinkie',
            '[': 'right_pinkie', '{': 'right_pinkie', ']': 'right_pinkie', '}': 'right_pinkie',
            '\\': 'right_pinkie', '|': 'right_pinkie', "'": 'right_pinkie', '"': 'right_pinkie',
            'Enter': 'right_pinkie', 'Shift': 'right_pinkie', 'Ctrl': 'right_pinkie',
            'Alt': 'right_pinkie', 'Esc': 'right_pinkie',
            'Backspace': 'right_pinkie', 'Win': 'right_pinkie', 'Fn': 'right_pinkie',
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
        渲染键盘 - 深色主题样式
        
        参数:
        - screen: 游戏屏幕
        """
        # 渲染键盘背景 - 深色半透明
        keyboard_rect = pygame.Rect(
            self.keyboard_x - 15,
            self.keyboard_y - 15,
            self.keyboard_width + 30,
            self.keyboard_height + 30
        )
        
        # 创建圆角键盘背景
        bg_surface = pygame.Surface((keyboard_rect.width, keyboard_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, (*self.keyboard_bg_color, 230), 
                         bg_surface.get_rect(), border_radius=12)
        screen.blit(bg_surface, keyboard_rect.topleft)
        
        # 渲染按键
        expired_keys = []
        expired_blinks = []
        for key in self.keys:
            # 确定按键颜色
            char_lower = key['char'].lower() if len(key['char']) == 1 else key['char']
            highlight = self.highlights.get(key['char'])
            blink = self.blink_keys.get(key['char'])
            
            # 处理闪烁状态更新
            if blink:
                blink['blink_frame'] += 1
                if blink['blink_frame'] >= blink['frames_per_toggle']:
                    blink['blink_frame'] = 0
                    blink['is_visible'] = not blink['is_visible']
                    if blink['is_visible']:
                        # 刚切换到可见，减少闪烁计数
                        blink['blink_count'] -= 1
                        if blink['blink_count'] <= 0:
                            expired_blinks.append(key['char'])
            
            # 确定颜色
            if blink and not blink['is_visible']:
                # 闪烁隐藏状态：使用较暗的颜色
                color = self.key_bg_color
            elif highlight:
                color = highlight['color']
                # 计时高亮递减
                if highlight['duration'] is not None:
                    highlight['duration'] -= 1
                    if highlight['duration'] <= 0:
                        expired_keys.append(key['char'])
            else:
                # 默认按键颜色 - 深色
                color = self.key_bg_color
            
            # 绘制圆角按键 - 带微妙渐变效果的边框
            pygame.draw.rect(screen, color, key['rect'], border_radius=self.key_corner_radius)
            
            # 绘制内阴影效果（按键顶部高光）
            highlight_rect = pygame.Rect(
                key['rect'].x + 2,
                key['rect'].y + 2,
                key['rect'].width - 4,
                key['rect'].height // 3
            )
            highlight_color = tuple(min(255, c + 20) for c in color)
            pygame.draw.rect(screen, highlight_color, highlight_rect, border_radius=6)
            
            # 绘制按键边框
            border_color = tuple(max(0, c - 30) for c in color)
            pygame.draw.rect(screen, border_color, key['rect'], 1, border_radius=self.key_corner_radius)

        # 清理过期高亮
        for char in expired_keys:
            self.highlights.pop(char, None)
        
        # 清理过期闪烁
        for char in expired_blinks:
            self.blink_keys.pop(char, None)

        # 绘制按键文本
        for key in self.keys:
            # 基准键(F/J)使用特殊颜色
            if key['char'].lower() in ['f', 'j']:
                text_color = self.key_home_pos_color
                # 为基准键添加底部指示条
                indicator_rect = pygame.Rect(
                    key['rect'].centerx - 8,
                    key['rect'].bottom - 6,
                    16, 3
                )
                pygame.draw.rect(screen, self.key_home_pos_color, indicator_rect, border_radius=2)
            else:
                text_color = self.key_text_color
            
            text_surface = self.font.render(key['char'], True, text_color)
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
    
    def blink_key(self, key_char, blink_count=1):
        """
        设置按键闪烁效果（用于重复目标键提示）
        
        参数:
        - key_char: 要闪烁的按键字符
        - blink_count: 闪烁次数（一亮一暗为一次）
        """
        if key_char is None:
            return
        self.blink_keys[key_char] = {
            'blink_count': max(1, blink_count),
            'blink_frame': 0,
            'is_visible': True,
            'frames_per_toggle': 4  # 缩短为一次快速闪烁
        }
    
    def clear_highlight(self, key_char=None):
        """清除高亮（单个或全部）"""
        if key_char:
            self.highlights.pop(key_char, None)
            self.blink_keys.pop(key_char, None)
        else:
            self.highlights.clear()
            self.blink_keys.clear()
    
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

    # ==================== 指法示意图渲染 ====================

    # 手指中文名称映射
    FINGER_NAMES_CN = {
        'left_pinkie': '左手小指',
        'left_ring': '左手无名指',
        'left_middle': '左手中指',
        'left_index': '左手食指',
        'left_thumb': '左手拇指',
        'both_thumbs': '双拇指',
        'right_thumb': '右手拇指',
        'right_index': '右手食指',
        'right_middle': '右手中指',
        'right_ring': '右手无名指',
        'right_pinkie': '右手小指',
    }

    # 手指默认颜色（未激活状态）- 深色主题下的暗淡颜色
    FINGER_INACTIVE_COLOR = (75, 85, 100)

    # 手掌/手形颜色 - 深色主题下使用轮廓线风格
    HAND_SKIN_COLOR = (60, 70, 85)
    HAND_BORDER_COLOR = (100, 115, 140)
    HAND_HIGHLIGHT_COLOR = (236, 72, 153)  # 激活手指时的高亮边框

    def render_finger_guide(self, screen, active_finger=None):
        """
        在键盘下方渲染指法示意图

        参数:
        - screen: 游戏屏幕
        - active_finger: 当前激活的手指名称（如'right_index'），None表示不高亮
        """
        # 计算示意图位置（键盘下方居中）
        guide_y = self.keyboard_y + self.keyboard_height + 15
        center_x = self.config.SCREEN_WIDTH // 2

        # 整体布局参数
        hand_width = 130       # 单只手掌宽度
        hand_height = 45       # 手掌高度
        finger_width = 12      # 手指宽度
        finger_length = 35     # 手指长度（不含手掌部分）
        thumb_width = 14       # 拇指宽度
        thumb_length = 20      # 拇指长度
        finger_gap = 6         # 手指间距
        palm_center_offset = 25  # 手掌中心到手指根部的偏移

        # 两只手之间的间距
        hands_gap = 40

        # 总宽度计算
        total_width = hand_width * 2 + hands_gap
        start_x = center_x - total_width // 2

        # ===== 绘制左手 =====
        left_hand_x = start_x
        self._draw_hand(
            screen,
            left_hand_x, guide_y,
            hand_width, hand_height,
            finger_width, finger_length,
            thumb_width, thumb_length,
            finger_gap, palm_center_offset,
            is_left=True,
            active_finger=active_finger
        )

        # ===== 绘制右手 =====
        right_hand_x = start_x + hand_width + hands_gap
        self._draw_hand(
            screen,
            right_hand_x, guide_y,
            hand_width, hand_height,
            finger_width, finger_length,
            thumb_width, thumb_length,
            finger_gap, palm_center_offset,
            is_left=False,
            active_finger=active_finger
        )

        # ===== 绘制激活手指的标签 =====
        if active_finger and active_finger in self.FINGER_NAMES_CN:
            self._draw_finger_label(screen, center_x, guide_y, active_finger)

    def _draw_hand(self, screen, x, y, hand_width, hand_height,
                   finger_width, finger_length, thumb_width, thumb_length,
                   finger_gap, palm_center_offset, is_left=True, active_finger=None):
        """
        绘制单只手（手掌+5个手指）- 深色主题风格
        
        激活手指使用填充色+发光效果
        未激活手指使用轮廓线风格

        参数:
        - screen: 游戏屏幕
        - x, y: 手掌左上角坐标
        - is_left: 是否为左手
        - active_finger: 当前激活的手指
        """
        # 四指与拇指分开处理，保证拇指位于手掌内侧、四指顺序真实
        if is_left:
            # 左手从左到右：小指、无名指、中指、食指，拇指单独在右侧
            finger_keys = ['left_pinkie', 'left_ring', 'left_middle', 'left_index']
            thumb_key = 'left_thumb'
        else:
            # 右手从左到右：食指、中指、无名指、小指，拇指单独在左侧
            finger_keys = ['right_index', 'right_middle', 'right_ring', 'right_pinkie']
            thumb_key = 'right_thumb'

        # 绘制手掌 - 深色主题使用填充矩形
        palm_rect = pygame.Rect(x, y + palm_center_offset, hand_width, hand_height)
        pygame.draw.rect(screen, self.HAND_SKIN_COLOR, palm_rect, border_radius=8)
        pygame.draw.rect(screen, self.HAND_BORDER_COLOR, palm_rect, 2, border_radius=8)

        # 计算4个手指的总宽度（不包括拇指）
        four_fingers_width = 4 * finger_width + 3 * finger_gap
        fingers_start_x = x + (hand_width - four_fingers_width) // 2

        # 绘制4个手指
        for i, finger_key in enumerate(finger_keys):
            fx = fingers_start_x + i * (finger_width + finger_gap)
            fy = y  # 指尖在上方

            # 确定手指颜色
            is_active = (finger_key == active_finger)
            color = self.finger_colors.get(finger_key, self.FINGER_INACTIVE_COLOR)
            
            # 绘制手指
            finger_rect = pygame.Rect(fx, fy, finger_width, finger_length)
            
            if is_active:
                # 激活状态：填充色 + 发光边框
                pygame.draw.ellipse(screen, color, finger_rect)
                # 发光效果（外圈）
                glow_rect = finger_rect.inflate(4, 4)
                glow_color = tuple(min(255, c + 60) for c in color)
                pygame.draw.ellipse(screen, glow_color, glow_rect, 2)
            else:
                # 未激活状态：仅轮廓线
                pygame.draw.ellipse(screen, self.HAND_BORDER_COLOR, finger_rect, 2)

        # 绘制拇指 - 修正位置，使其斜向手掌内侧下方
        is_active = (thumb_key == active_finger)
        color = self.finger_colors.get(thumb_key, self.FINGER_INACTIVE_COLOR)

        # 拇指位置优化：左手拇指在右侧，右手拇指在左侧，且拉开距离
        if is_left:
            # 左手拇指：移到手掌右侧边缘，并稍微向下
            thumb_x = x + hand_width - thumb_width - 10
            thumb_y = y + palm_center_offset + hand_height - thumb_length - 10
        else:
            # 右手拇指：移到手掌左侧边缘，并稍微向下
            thumb_x = x + 10
            thumb_y = y + palm_center_offset + hand_height - thumb_length - 10

        thumb_rect = pygame.Rect(thumb_x, thumb_y, thumb_width, thumb_length)
        
        if is_active:
            pygame.draw.ellipse(screen, color, thumb_rect)
            glow_rect = thumb_rect.inflate(4, 4)
            glow_color = tuple(min(255, c + 60) for c in color)
            pygame.draw.ellipse(screen, glow_color, glow_rect, 2)
        else:
            pygame.draw.ellipse(screen, self.HAND_BORDER_COLOR, thumb_rect, 2)

    def _draw_finger_label(self, screen, center_x, base_y, active_finger):
        """
        在手形下方绘制激活手指的中文名称标签 - 深色主题风格

        参数:
        - screen: 游戏屏幕
        - center_x: 中心x坐标
        - base_y: 示意图基准y坐标
        - active_finger: 激活的手指名称
        """
        label_text = self.FINGER_NAMES_CN.get(active_finger, '')
        if not label_text:
            return

        # 标签字体
        try:
            label_font = load_font(16, font_dir=self.config.FONTS_DIR)
        except Exception:
            label_font = None

        if label_font:
            text_surface = label_font.render(label_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect()

            # 标签位置（示意图下方居中）
            label_y = base_y + 85
            label_x = center_x - text_rect.width // 2

            # 背景框（半透明深色+手指颜色边框）
            padding = 10
            bg_rect = pygame.Rect(
                label_x - padding,
                label_y - padding,
                text_rect.width + padding * 2,
                text_rect.height + padding * 2
            )

            # 获取激活手指的颜色
            finger_color = self.finger_colors.get(active_finger, (236, 72, 153))
            
            # 创建半透明背景
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(bg_surface, (30, 35, 40, 240), bg_surface.get_rect(), border_radius=8)
            screen.blit(bg_surface, bg_rect.topleft)
            
            # 绘制手指颜色的边框
            pygame.draw.rect(screen, finger_color, bg_rect, 2, border_radius=8)

            # 绘制文字
            screen.blit(text_surface, (label_x, label_y))