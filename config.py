#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
游戏配置文件，定义游戏的基本参数和常量
"""

import os

class Config:
    """游戏配置类"""
    
    def __init__(self):
        """初始化配置"""
        # 屏幕设置
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 768
        self.FPS = 60
        
        # 颜色设置 - 深色主题 (参考 type.fun 风格)
        # 背景色
        self.BACKGROUND_COLOR = (45, 52, 54)           # 深灰蓝 #2D3436
        self.CARD_BG_COLOR = (30, 35, 40)              # 卡片背景 #1E2328
        self.PANEL_BG_COLOR = (38, 45, 52)            # 面板背景 #263544
        
        # 主色调
        self.PRIMARY_COLOR = (236, 72, 153)            # 粉红 #EC4899 (当前键高亮)
        self.PRIMARY_LIGHT = (244, 114, 182)           # 浅粉 #F472B6
        self.SECONDARY_COLOR = (116, 185, 255)        # 天蓝 #74B9FF
        
        # 状态色
        self.SUCCESS_COLOR = (16, 185, 129)           # 翠绿 #10B981
        self.ERROR_COLOR = (239, 68, 68)              # 红色 #EF4444
        self.WARNING_COLOR = (251, 191, 36)           # 橙黄 #FBBF24
        
        # 文本色
        self.TEXT_COLOR = (226, 232, 240)             # 浅灰白 #E2E8F0
        self.TEXT_SECONDARY = (148, 163, 184)         # 次要文字 #94A3B8
        self.TEXT_MUTED = (100, 116, 139)             # 暗淡文字 #64748B
        self.LIGHT_TEXT = (255, 255, 255)             # 纯白 #FFFFFF
        
        # 键盘按键色
        self.KEY_DEFAULT_BG = (61, 79, 95)             # 按键默认 #3D4F5F
        self.KEY_DEFAULT_TEXT = (226, 232, 240)       # 按键文字 #E2E8F0
        self.KEY_BORDER = (75, 90, 110)               # 按键边框 #4B5A6E
        self.KEY_HIGHLIGHT = (236, 72, 153)           # 按键高亮 #EC4899
        self.KEY_HOME_POS = (16, 185, 129)            # 基准键位(F/J) #10B981
        self.KEY_PRESSED = (99, 102, 120)            # 按下状态 #636B78
        self.KEY_ERROR = (239, 68, 68)               # 错误 #EF4444
        self.KEYBOARD_BG = (26, 32, 38)              # 键盘背景 #1A2026
        
        # 键盘设置
        self.KEYBOARD_WIDTH = 800
        self.KEYBOARD_HEIGHT = 200
        self.KEYBOARD_POS_X = (self.SCREEN_WIDTH - self.KEYBOARD_WIDTH) // 2
        self.KEYBOARD_POS_Y = self.SCREEN_HEIGHT - self.KEYBOARD_HEIGHT - 20
        
        # 游戏模式设置
        self.BEGINNER_TRIALS = 100              # 初级模式按键次数
        self.ADVANCED_DURATION = 60             # 高级模式游戏时长(秒)
        self.MASTER_DURATION = 60               # 大师模式游戏时长(秒)
        
        # 难度设置
        self.ADVANCED_SPEED_INCREMENT = 0.5     # 高级模式速度增量
        self.MASTER_SPEED_INCREMENT = 0.3       # 大师模式速度增量
        
        # 分数设置
        self.CORRECT_KEY_SCORE = 1              # 正确按键得分
        self.COMBO_BONUS = 0.1                  # 连击奖励系数
        
        # 星级评价设置
        self.STAR_THRESHOLDS = [
            0,    # 0分以下
            40,   # 1星 (0-39分)
            60,   # 2星 (40-59分)
            80,   # 3星 (60-79分)
            90,   # 4星 (80-89分)
            100   # 5星 (90-100分)
        ]
        
        # 路径设置
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.RESOURCES_DIR = os.path.join(self.BASE_DIR, 'resources')
        self.SOUNDS_DIR = os.path.join(self.RESOURCES_DIR, 'sounds')
        self.FONTS_DIR = os.path.join(self.RESOURCES_DIR, 'fonts')
        self.DATA_DIR = os.path.join(self.BASE_DIR, 'data')
        
        # 存档文件路径
        self.SAVE_FILE = os.path.join(self.DATA_DIR, 'game_data.json')
        
        # 音效设置
        self.SOUND_VOLUME = 0.5
        self.MUSIC_VOLUME = 0.3
        
        # 字体设置
        # 使用系统字体列表，支持中文
        self.CHINESE_FONTS = [
            "hiraginosansgb",
            "pingfang",
            "stheitilight",
            "stheitimedium",
            "notosanscjk",
            "sourcehansans",
            "arialunicodems"
        ]
        self.TITLE_FONT_SIZE = 48
        self.HEADER_FONT_SIZE = 36
        self.NORMAL_FONT_SIZE = 24
        self.SMALL_FONT_SIZE = 18
        
        # 按钮设置
        self.BUTTON_WIDTH = 200
        self.BUTTON_HEIGHT = 60
        self.BUTTON_RADIUS = 10
        self.BUTTON_MARGIN = 20
        
        # 动画设置
        self.PARTICLE_DURATION = 30             # 粒子效果持续帧数
        self.HIGHLIGHT_DURATION = 10            # 按键高亮持续帧数
        self.STAR_ANIMATION_DURATION = 60       # 星级动画持续帧数