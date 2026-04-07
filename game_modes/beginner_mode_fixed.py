#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
初级模式 - 单键指法训练（修复版）
"""

import pygame
import random
import time
from .base_mode import BaseMode
from ui.text import Text
from effects.particle import ParticleSystem

class BeginnerMode(BaseMode):
    """初级模式类"""

    def __init__(self, scene):
        """
        初始化初级模式

        参数:
        - scene: 游戏场景
        """
        super().__init__(scene)

        # 训练按键集
        self.key_set = self._get_key_set()

        # 当前目标按键
        self.target_key = None

        # 训练次数
        self.total_trials = self.config.BEGINNER_TRIALS
        self.current_trial = 0

        # 粒子系统
        self.particle_system = ParticleSystem(self.config)

        # 鼓励文本
        self.encouragement_text = None
        self.encouragement_timer = 0

        # 初始化游戏
        self.reset_game()

    def _get_key_set(self):
        """获取训练按键集"""
        # 基础按键集，包含字母、数字和常用符号
        key_set = [
            'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'q', 'w', 'e', 'r', 't',
            'y', 'u', 'i', 'o', 'p', 'z', 'x', 'c', 'v', 'b', 'n', 'm',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            ' ', '-', '=', '[', ']', '\\', ';', "'", ',', '.', '/'
        ]

        return key_set

    def reset_game(self):
        """重置游戏"""
        # 重置游戏数据
        self.reset_game_data()

        # 重置训练次数
        self.current_trial = 0

        # 生成第一个目标按键
        self.generate_target_key()

    def start(self):
        """开始游戏"""
        super().start()
        self.reset_game()

    def generate_target_key(self):
        """生成目标按键"""
        # 随机选择一个按键
        self.target_key = random.choice(self.key_set)

        # 高亮显示目标按键
        self.keyboard_renderer.highlight_key(self.target_key)

        # 显示对应的手指指导
        finger = self.keyboard_renderer.get_finger_for_key(self.target_key)
        if finger:
            self.keyboard_renderer.highlight_finger_keys(finger)

    def update(self):
        """更新游戏状态"""
        super().update()

        # 更新粒子系统
        self.particle_system.update()

        # 更新鼓励文本
        if self.encouragement_text:
            self.encouragement_timer -= 1
            if self.encouragement_timer <= 0:
                self.encouragement_text = None

        # 检查是否完成所有训练
        if self.current_trial >= self.total_trials:
            self.end_game()

    def handle_event(self, event):
        """处理游戏事件"""
        super().handle_event(event)

        # 处理键盘事件
        if event.type == pygame.KEYDOWN:
            self.handle_key_down(event.key)

    def handle_key_down(self, key):
        """处理键盘按下事件"""
        # 获取按键字符
        key_char = self.keyboard_renderer.key_map.get(key, None)

        # 检查按键是否正确
        if key_char == self.target_key:
            # 按键正确
            self.handle_correct_key()
        else:
            # 按键错误
            self.handle_error_key(key)

    def handle_correct_key(self):
        """处理正确按键"""
        # 更新游戏数据
        self.correct_count += 1
        self.total_count += 1
        self.current_trial += 1
        self.score += 1

        # 播放正确音效
        self.play_correct_sound()

        # 显示鼓励文本
        self.show_encouragement()

        # 生成粒子效果
        self.particle_system.create_explosion(
            self.config.SCREEN_WIDTH // 2,
            self.config.SCREEN_HEIGHT // 2,
            self.config.SUCCESS_COLOR
        )

        # 高亮键盘上的目标按键
        self.keyboard_renderer.highlight_key(self.target_key, self.config.SUCCESS_COLOR, 10)

        # 检查是否完成所有训练
        if self.current_trial >= self.total_trials:
            # 游戏结束，进入计分环节
            self.end_game()
        else:
            # 生成下一个目标按键
            self.generate_target_key()

    def handle_error_key(self, pressed_key_code=None):
        """处理错误按键"""
        # 更新游戏数据
        self.total_count += 1

        # 播放错误音效
        self.play_error_sound()

        # 高亮错误按键（如果提供了按键代码）
        if pressed_key_code:
            key_char = self.keyboard_renderer.key_map.get(pressed_key_code, None)
            if key_char:
                self.keyboard_renderer.highlight_key(key_char, self.config.ERROR_COLOR, 10)

    def show_encouragement(self):
        """显示鼓励文本"""
        # 随机选择一个鼓励语
        encouragement = self.get_encouragement()

        # 创建鼓励文本
        self.encouragement_text = Text(
            encouragement,
            36,
            self.config.SUCCESS_COLOR,
            (
                random.randint(100, self.config.SCREEN_WIDTH - 100),
                random.randint(100, self.config.SCREEN_HEIGHT - 200)  # 避开键盘区域
            )
        )
        self.encouragement_timer = 60  # 显示60帧（约1秒）

    def get_encouragement(self):
        """获取鼓励语"""
        return random.choice(self.encouragements)

    def render(self, screen):
        """渲染游戏画面"""
        # 渲染键盘
        self.keyboard_renderer.render(screen)

        # 渲染目标按键提示（顶部中央，避开键盘区域）
        self.render_target_key(screen)

        # 渲染进度信息（右上角）
        self.render_progress(screen)

        # 渲染粒子效果
        self.particle_system.render(screen)

        # 渲染鼓励文本
        if self.encouragement_text:
            self.encouragement_text.render(screen)

    def render_target_key(self, screen):
        """渲染目标按键提示"""
        # 定义中文字体列表
        chinese_fonts = [
            "hiraginosansgb",
            "pingfang",
            "stheitilight",
            "stheitimedium",
            "notosanscjk",
            "sourcehansans",
            "arialunicodems"
        ]

        # 显示字符
        display_char = self.target_key.upper()

        # 如果是空格，显示为"空格"
        if self.target_key == ' ':
            display_char = '空格'

        # 大字体用于显示目标按键
        font_large = pygame.font.SysFont(chinese_fonts, 120)

        # 计算屏幕中心位置（上半部分，避开键盘区域）
        center_x = self.config.SCREEN_WIDTH // 2
        center_y = self.config.SCREEN_HEIGHT // 2 - 150  # 上移150像素

        # 渲染目标按键
        text_surface = font_large.render(display_char, True, self.config.PRIMARY_COLOR)
        text_rect = text_surface.get_rect(center=(center_x, center_y))
        screen.blit(text_surface, text_rect)

        # 渲染提示文本
        font_hint = pygame.font.SysFont(chinese_fonts, 24)
        hint_text = "请按上面的按键"
        hint_surface = font_hint.render(hint_text, True, self.config.TEXT_COLOR)
        hint_rect = hint_surface.get_rect(center=(center_x, center_y + 80))
        screen.blit(hint_surface, hint_rect)

    def render_progress(self, screen):
        """渲染进度信息"""
        # 定义中文字体列表
        chinese_fonts = [
            "hiraginosansgb",
            "pingfang",
            "stheitilight",
            "stheitimedium",
            "notosanscjk",
            "sourcehansans",
            "arialunicodems"
        ]

        font = pygame.font.SysFont(chinese_fonts, 24)

        # 计算进度百分比
        progress_percent = int((self.current_trial / self.total_trials) * 100)

        # 进度文本（右上角，不与按钮重叠）
        progress_text = f"进度: {self.current_trial}/{self.total_trials} ({progress_percent}%)"
        progress_surface = font.render(progress_text, True, self.config.TEXT_COLOR)

        # 放置在右上角，但偏左一些以避开退出按钮（退出按钮在SCREEN_WIDTH - 120, 20）
        progress_x = self.config.SCREEN_WIDTH - progress_surface.get_width() - 140
        progress_y = 20

        screen.blit(progress_surface, (progress_x, progress_y))

    def get_mode_name(self):
        """获取模式名称"""
        return "初级模式"
