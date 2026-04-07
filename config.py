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
        
        # 颜色设置
        self.BACKGROUND_COLOR = (240, 248, 255)  # 爱丽丝蓝
        self.PRIMARY_COLOR = (70, 130, 180)      # 钢蓝色
        self.SECONDARY_COLOR = (255, 165, 0)     # 橙色
        self.SUCCESS_COLOR = (50, 205, 50)       # 酸橙绿
        self.ERROR_COLOR = (220, 20, 60)         # 猩红色
        self.TEXT_COLOR = (30, 30, 30)           # 深灰色文本
        self.LIGHT_TEXT = (255, 255, 255)        # 白色文本
        
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