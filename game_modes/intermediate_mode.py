#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
中级模式 - 英文短句打字训练
"""

import pygame
import random
import time
from .base_mode import BaseMode
from ui.text import Text
from content.english_words import WORDS
from content.english_phrases import PHRASES
from content.english_sentences import SENTENCES
from font_loader import load_font

class IntermediateMode(BaseMode):
    """中级模式类"""
    
    def __init__(self, scene):
        """
        初始化中级模式
        
        参数:
        - scene: 游戏场景
        """
        super().__init__(scene)
        
        # 训练内容级别
        self.level = 0  # 0: 单词, 1: 短语, 2: 句子
        self.levels = ["单词", "短语", "句子"]
        
        # 训练内容
        self.content_list = []
        self.current_content = ""
        self.current_index = 0
        
        # 用户输入
        self.user_input = ""
        
        # 训练次数
        self.total_trials = 10
        self.current_trial = 0
        
        # 错误标记
        self.error_index = -1

        # 速度计算与统计
        self.start_input_time = 0
        self.total_input_time = 0
        self.characters_typed = 0  # 真实击键数（含错误）

        # 预加载字体与按键去抖
        self.title_font = load_font(32, font_dir=self.config.FONTS_DIR)
        self.content_font = load_font(28, font_dir=self.config.FONTS_DIR)
        self.input_font = load_font(28, font_dir=self.config.FONTS_DIR)
        self.info_font = load_font(24, font_dir=self.config.FONTS_DIR)

        self.last_key = None
        self.last_key_time = 0
        self.key_debounce_seconds = 0.12
        self.error_highlight_frames = 12

        # 初始化游戏
        self.reset_game()
    
    def reset_game(self):
        """重置游戏"""
        # 重置游戏数据
        self.reset_game_data()
        
        # 重置训练次数
        self.current_trial = 0
        
        # 重置输入统计
        self.total_input_time = 0
        self.characters_typed = 0
        
        # 加载训练内容
        self.load_content()
        
        # 设置第一个训练内容
        self.set_next_content()
    
    def load_content(self):
        """加载训练内容"""
        # 根据级别选择训练内容
        if self.level == 0:
            self.content_list = random.sample(WORDS, self.total_trials)
        elif self.level == 1:
            self.content_list = random.sample(PHRASES, self.total_trials)
        else:
            self.content_list = random.sample(SENTENCES, self.total_trials)
    
    def set_next_content(self):
        """设置下一个训练内容"""
        if self.current_trial < self.total_trials:
            self.current_content = self.content_list[self.current_trial]
            self.user_input = ""
            self.current_index = 0
            self.error_index = -1
            self.start_input_time = time.time()

            # 键盘提示当前目标键
            self.keyboard_renderer.clear_highlight()
            if len(self.current_content) > 0:
                self.highlight_target_key()
        else:
            # 所有训练内容完成
            self.keyboard_renderer.clear_highlight()
            self.end_game()
    
    def start(self):
        """开始游戏"""
        super().start()
        self.reset_game()
    
    def update(self):
        """更新游戏状态"""
        super().update()
        
        # 检查是否完成当前内容
        if self.current_index >= len(self.current_content):
            # 计算输入时间
            input_time = time.time() - self.start_input_time
            self.total_input_time += input_time
            self.start_input_time = time.time()
            
            # 进入下一个训练内容
            self.current_trial += 1
            self.set_next_content()
        else:
            # 保持目标键高亮
            self.highlight_target_key()
    
    def render(self, screen):
        """渲染游戏画面"""
        super().render(screen)
        
        # 渲染级别选择（如果还未开始）
        if not self.running:
            return
        
        # 渲染训练内容
        self.render_content(screen)
        
        # 渲染用户输入
        self.render_user_input(screen)
        
        # 渲染进度
        self.render_progress(screen)
        
        # 渲染速度信息
        self.render_speed_info(screen)
    
    def render_content(self, screen):
        """渲染训练内容"""
        # 渲染标题
        title_text = f"{self.levels[self.level]}训练"
        title_surface = self.title_font.render(title_text, True, self.config.PRIMARY_COLOR)
        title_rect = title_surface.get_rect(center=(self.config.SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)
        
        # 渲染训练内容（目标串）
        content_surface = self.content_font.render(self.current_content, True, self.config.TEXT_COLOR)
        content_rect = content_surface.get_rect(center=(self.config.SCREEN_WIDTH // 2, 190))
        screen.blit(content_surface, content_rect)
        
        # 已输入部分用成功色，单一光标位置计算
        if self.current_index > 0:
            completed_text = self.current_content[:self.current_index]
            completed_surface = self.content_font.render(completed_text, True, self.config.SUCCESS_COLOR)
            screen.blit(completed_surface, content_rect)
        
        # 当前目标字符简单底色高亮（单一光标）
        if self.current_index < len(self.current_content):
            prefix_width = self.content_font.size(self.current_content[:self.current_index])[0]
            current_char = self.current_content[self.current_index]
            char_width, char_height = self.content_font.size(current_char)
            char_center = (content_rect.left + prefix_width + char_width / 2, content_rect.centery)
            highlight_rect = pygame.Rect(0, 0, char_width + 8, char_height + 8)
            highlight_rect.center = char_center
            pygame.draw.rect(screen, self.config.PRIMARY_COLOR, highlight_rect, border_radius=3)
            char_surface = self.content_font.render(current_char, True, self.config.LIGHT_TEXT)
            char_rect = char_surface.get_rect(center=char_center)
            screen.blit(char_surface, char_rect)

    
    def render_user_input(self, screen):
        """渲染用户输入"""
        # 渲染用户输入
        input_surface = self.input_font.render(self.user_input, True, self.config.TEXT_COLOR)
        input_rect = input_surface.get_rect(center=(self.config.SCREEN_WIDTH // 2, 240))
        screen.blit(input_surface, input_rect)
        
        # 渲染光标（单一颜色）
        cursor_x = input_rect.left + self.input_font.size(self.user_input)[0]
        cursor_y = input_rect.top
        cursor_height = self.input_font.size("Tg")[1]
        pygame.draw.line(
            screen,
            self.config.PRIMARY_COLOR,
            (cursor_x, cursor_y),
            (cursor_x, cursor_y + cursor_height),
            2
        )
    
    def render_progress(self, screen):
        """渲染进度"""
        progress_text = f"进度: {self.current_trial}/{self.total_trials}"
        progress_surface = self.info_font.render(progress_text, True, self.config.TEXT_COLOR)
        screen.blit(progress_surface, (20, 120))
    
    def render_speed_info(self, screen):
        """渲染速度信息"""
        if self.total_input_time > 0:
            # 计算速度（字符/分钟）
            cpm = int(self.characters_typed / self.total_input_time * 60)
            
            speed_text = f"速度: {cpm} CPM"
            speed_surface = self.info_font.render(speed_text, True, self.config.TEXT_COLOR)
            screen.blit(speed_surface, (self.config.SCREEN_WIDTH - 200, 120))
    
    def handle_event(self, event):
        """处理游戏事件"""
        super().handle_event(event)
        
        # 处理键盘事件
        if event.type == pygame.KEYDOWN:
            self.handle_key_down(event.key)
    
    def handle_key_down(self, key):
        """处理键盘按下事件，带去抖和键盘提示"""
        now = time.time()
        if self.last_key == key and (now - self.last_key_time) < self.key_debounce_seconds:
            return
        self.last_key = key
        self.last_key_time = now

        # 处理特殊按键
        if key == pygame.K_BACKSPACE:
            if len(self.user_input) > 0:
                self.user_input = self.user_input[:-1]
                self.current_index = max(0, self.current_index - 1)
                self.error_index = -1
                self.highlight_target_key()
        
        elif key == pygame.K_RETURN:
            # 强制提交当前条目（按已输入/错误统计）
            input_time = time.time() - self.start_input_time
            self.total_input_time += input_time
            self.start_input_time = time.time()
            self.current_trial += 1
            self.set_next_content()
        
        elif key == pygame.K_TAB:
            self.level = (self.level + 1) % len(self.levels)
            self.reset_game()
        
        else:
            key_char = self._to_char(key)

            if key_char:
                if self.current_index < len(self.current_content):
                    expected_char = self.current_content[self.current_index]
                    if key_char == expected_char:
                        # 输入正确
                        self.user_input += key_char
                        self.current_index += 1
                        self.error_index = -1
                        self.correct_count += 1
                        self.total_count += 1
                        self.characters_typed += 1
                        self.play_correct_sound()
                        self.keyboard_renderer.clear_highlight()
                        if self.current_index < len(self.current_content):
                            self.highlight_target_key()
                        else:
                            self.keyboard_renderer.clear_highlight()
                    else:
                        # 输入错误：仅键盘提示，不移动光标
                        self.error_index = self.current_index
                        self.total_count += 1
                        self.characters_typed += 1
                        wrong_hl = self.normalize_highlight_char(key_char)
                        if wrong_hl:
                            self.keyboard_renderer.highlight_key(wrong_hl, self.config.ERROR_COLOR, self.error_highlight_frames)
                        self.highlight_target_key()
                        self.play_error_sound()
                else:
                    # 已完成，直接进入下一个
                    input_time = time.time() - self.start_input_time
                    self.total_input_time += input_time
                    self.start_input_time = time.time()
                    self.current_trial += 1
                    self.set_next_content()
    
    def calculate_accuracy(self):
        """计算准确率"""
        if self.total_count > 0:
            self.accuracy = self.correct_count / self.total_count
        else:
            self.accuracy = 0.0

    def calculate_score(self):
        """计算得分：扣分制，满分100，不超过100"""
        self.calculate_accuracy()
        self.score = int(self.accuracy * 100)
        self.score = max(0, min(100, self.score))

    def _to_char(self, key):
        """将pygame键值转换为字符，含shift符号"""
        shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
        if pygame.K_a <= key <= pygame.K_z:
            return chr(key - pygame.K_a + (ord('A') if shift_pressed else ord('a')))
        if pygame.K_0 <= key <= pygame.K_9:
            symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
            return symbols[key - pygame.K_0] if shift_pressed else chr(key)
        if key == pygame.K_SPACE:
            return ' '
        mapping = {
            pygame.K_MINUS: '_' if shift_pressed else '-',
            pygame.K_EQUALS: '+' if shift_pressed else '=',
            pygame.K_LEFTBRACKET: '{' if shift_pressed else '[',
            pygame.K_RIGHTBRACKET: '}' if shift_pressed else ']',
            pygame.K_BACKSLASH: '|' if shift_pressed else '\\',
            pygame.K_SEMICOLON: ':' if shift_pressed else ';',
            pygame.K_QUOTE: '"' if shift_pressed else "'",
            pygame.K_COMMA: '<' if shift_pressed else ',',
            pygame.K_PERIOD: '>' if shift_pressed else '.',
            pygame.K_SLASH: '?' if shift_pressed else '/',
        }
        return mapping.get(key)

    def normalize_highlight_char(self, ch):
        """将字符转换为键盘高亮字符"""
        if len(ch) == 1 and ch.isalpha():
            return ch.lower()
        return ch

    def highlight_target_key(self):
        if self.current_index < len(self.current_content):
            target_char = self.current_content[self.current_index]
            hl_char = self.normalize_highlight_char(target_char)
            if hl_char:
                self.keyboard_renderer.highlight_key(hl_char, duration=None)

    def calculate_score(self):
        """计算得分"""
        # 基础分数
        base_score = self.score
        
        # 速度奖励
        if self.total_input_time > 0:
            cpm = self.characters_typed / self.total_input_time * 60
            speed_bonus = min(int(cpm / 10), 30)
        else:
            speed_bonus = 0
        
        # 总分
        self.score = base_score + speed_bonus
    
    def get_max_score(self):
        """获取最大可能分数"""
        return self.total_trials * 10 + 30  # 基础分 + 速度奖励
    
    def get_mode_name(self):
        """获取游戏模式名称"""
        return f"中级模式 - {self.levels[self.level]}"