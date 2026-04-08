#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
初级模式 - 单键指法训练
"""

import pygame
import random
import time
from .base_mode import BaseMode
from ui.text import Text
from effects.particle import ParticleSystem
from font_loader import load_font

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

        # 预加载字体以避免每帧加载
        self.font_large = load_font(120, font_dir=self.config.FONTS_DIR)
        self.font_medium = load_font(48, font_dir=self.config.FONTS_DIR)
        self.hint_font = load_font(24, font_dir=self.config.FONTS_DIR)
        self.progress_font = load_font(24, font_dir=self.config.FONTS_DIR)

        # 按键去抖，避免一次按压触发多次计数
        self.last_key = None
        self.last_key_time = 0
        self.key_debounce_seconds = 0.12

        # 过渡控制
        self.pending_next_target = False
        self.next_target_delay = 0
        self.error_highlight_frames = 6
        
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

        # 清理高亮与过渡状态
        self.keyboard_renderer.clear_highlight()
        self.pending_next_target = False
        self.next_target_delay = 0
        
        # 生成第一个目标按键
        self.generate_target_key()
    
    def start(self):
        """开始游戏"""
        super().start()
        self.reset_game()
    
    def generate_target_key(self):
        """生成目标按键"""
        # 清除旧高亮
        self.keyboard_renderer.clear_highlight()

        # 随机选择一个按键
        self.target_key = random.choice(self.key_set)
        
        # 高亮显示目标按键（持续）
        self.keyboard_renderer.highlight_key(self.target_key, duration=None)
    
    def update(self):
        """更新游戏状态"""
        super().update()

        if not self.running:
            return

        # 更新粒子系统
        self.particle_system.update()

        # 更新鼓励文本
        if self.encouragement_text:
            self.encouragement_timer -= 1
            if self.encouragement_timer <= 0:
                self.encouragement_text = None

        # 处理错误后的延迟切换
        if self.pending_next_target:
            self.next_target_delay -= 1
            if self.next_target_delay <= 0:
                self.pending_next_target = False
                self.keyboard_renderer.clear_highlight()
                if self.current_trial >= self.total_trials:
                    self.end_game()
                    return
                else:
                    self.generate_target_key()
        else:
            # 检查是否完成所有训练
            if self.current_trial >= self.total_trials:
                self.end_game()
                return
    
    def handle_event(self, event):
        """处理游戏事件"""
        super().handle_event(event)

        if not self.running:
            return
        
        # 处理键盘事件
        if event.type == pygame.KEYDOWN:
            self.handle_key_down(event.key)
    
    def handle_key_down(self, key):
        """处理键盘按下事件，带去抖"""
        now = time.time()
        if self.last_key == key and (now - self.last_key_time) < self.key_debounce_seconds:
            return

        self.last_key = key
        self.last_key_time = now

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

        # 清除旧高亮并生成下一个
        self.keyboard_renderer.clear_highlight()
        if self.current_trial >= self.total_trials:
            self.end_game()
        else:
            self.generate_target_key()
    
    def handle_error_key(self, pressed_key_code=None):
        """处理错误按键"""
        # 更新游戏数据
        self.total_count += 1
        self.current_trial += 1

        # 播放错误音效
        self.play_error_sound()

        wrong_char = None
        if pressed_key_code:
            wrong_char = self.keyboard_renderer.key_map.get(pressed_key_code, None)

        # 高亮目标和错误按键，目标保持常亮，错误键短暂提示
        self.keyboard_renderer.clear_highlight()
        if self.target_key:
            self.keyboard_renderer.highlight_key(self.target_key, duration=None)
        if wrong_char:
            self.keyboard_renderer.highlight_key(wrong_char, self.config.ERROR_COLOR, self.error_highlight_frames)

        # 设置延迟切换到下一个目标
        self.pending_next_target = True
        self.next_target_delay = self.error_highlight_frames
    
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
                random.randint(100, self.config.SCREEN_HEIGHT - 100)
            )
        )
        self.encouragement_timer = 60
    
    def get_encouragement(self):
        """获取鼓励语"""
        return random.choice(self.encouragements)
    
    def render(self, screen):
        """渲染游戏画面"""
        # 先渲染键盘与基础信息
        super().render(screen)

        # 渲染进度
        self.render_progress(screen)

        # 渲染鼓励文本
        if self.encouragement_text:
            self.encouragement_text.render(screen)
    
    def render_target_key(self, screen, keyboard_y):
        """渲染目标按键提示"""
        # 计算中心位置（避开键盘区域）
        center_x = self.config.SCREEN_WIDTH // 2
        center_y = keyboard_y // 2 - 50
        
        # 渲染目标按键字符（大写显示）
        display_char = self.target_key.upper()
        
        # 如果是空格，显示为"空格"
        if display_char == ' ':
            display_char = '空格'
        
        # 渲染目标按键
        text_surface = self.font_large.render(display_char, True, self.config.PRIMARY_COLOR)
        text_rect = text_surface.get_rect(center=(center_x, center_y))
        screen.blit(text_surface, text_rect)
        
        # 渲染提示文本
        hint_text = "请按上面的按键"
        hint_surface = self.hint_font.render(hint_text, True, self.config.TEXT_COLOR)
        hint_rect = hint_surface.get_rect(center=(center_x, center_y + 80))
        screen.blit(hint_surface, hint_rect)
    
    def render_progress(self, screen):
        """渲染进度信息"""
        # 计算进度百分比
        progress_percent = int((self.current_trial / self.total_trials) * 100)
        
        # 进度文本（顶部功能区）
        progress_text = f"进度: {self.current_trial}/{self.total_trials}"
        progress_surface = self.progress_font.render(progress_text, True, self.config.TEXT_COLOR)
        progress_rect = progress_surface.get_rect(topleft=(20, 10))
        screen.blit(progress_surface, progress_rect)
        
        # 进度百分比（顶部功能区右侧）
        percent_text = f"{progress_percent}%"
        percent_surface = self.progress_font.render(percent_text, True, self.config.TEXT_COLOR)
        percent_rect = percent_surface.get_rect(topright=(self.config.SCREEN_WIDTH - 20, 10))
        screen.blit(percent_surface, percent_rect)
        
        # 渲染进度条（稍下方）
        bar_width = 320
        bar_height = 10
        bar_x = (self.config.SCREEN_WIDTH - bar_width) // 2
        bar_y = 36
        
        # 背景
        pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), border_radius=5)
        
        # 进度
        progress_width = int((self.current_trial / self.total_trials) * bar_width)
        progress_color = self.config.SUCCESS_COLOR if progress_percent >= 100 else self.config.PRIMARY_COLOR
        pygame.draw.rect(screen, progress_color, (bar_x, bar_y, progress_width, bar_height), border_radius=5)
