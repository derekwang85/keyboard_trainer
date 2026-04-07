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
        
        # 速度计算
        self.start_input_time = 0
        self.total_input_time = 0
        self.characters_typed = 0
        
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
        else:
            # 所有训练内容完成
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
            
            # 更新字符数统计
            self.characters_typed += len(self.current_content)
            
            # 更新准确率
            correct_chars = sum(1 for i in range(len(self.current_content)) 
                              if i < len(self.user_input) and self.user_input[i] == self.current_content[i])
            self.correct_count += correct_chars
            self.total_count += len(self.current_content)
            
            # 增加分数
            accuracy = correct_chars / len(self.current_content)
            self.score += int(accuracy * 10)
            
            # 进入下一个训练内容
            self.current_trial += 1
            self.set_next_content()
    
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
        # 使用统一的字体加载器
        font = load_font(32, font_dir=self.config.FONTS_DIR)
        content_font = load_font(28, font_dir=self.config.FONTS_DIR)

        # 渲染标题
        title_text = f"{self.levels[self.level]}训练"
        title_surface = font.render(title_text, True, self.config.PRIMARY_COLOR)
        title_rect = title_surface.get_rect(center=(self.config.SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)
        
        # 渲染训练内容
        content_surface = content_font.render(self.current_content, True, self.config.TEXT_COLOR)
        content_rect = content_surface.get_rect(center=(self.config.SCREEN_WIDTH // 2, 200))
        screen.blit(content_surface, content_rect)
        
        # 高亮已输入部分
        if self.current_index > 0:
            # 创建已输入部分的文本
            completed_text = self.current_content[:self.current_index]
            completed_surface = content_font.render(completed_text, True, self.config.SUCCESS_COLOR)
            completed_rect = completed_surface.get_rect(center=content_rect.topleft)
            screen.blit(completed_surface, completed_rect)
        
        # 高亮当前字符
        if self.current_index < len(self.current_content):
            current_char_text = self.current_content[self.current_index]
            current_char_surface = content_font.render(current_char_text, True, self.config.PRIMARY_COLOR)
            current_char_rect = current_char_surface.get_rect(
                center=(
                    content_rect.left + content_font.size(self.current_content[:self.current_index])[0] + 
                    content_font.size(current_char_text)[0] // 2,
                    content_rect.centery
                )
            )
            
            # 添加高亮背景
            highlight_rect = current_char_rect.inflate(5, 5)
            pygame.draw.rect(
                screen,
                self.config.PRIMARY_COLOR,
                highlight_rect,
                border_radius=3
            )
            screen.blit(current_char_surface, current_char_rect)
        
        # 高亮错误字符
        if self.error_index >= 0 and self.error_index < len(self.user_input):
            error_char_text = self.user_input[self.error_index]
            error_char_surface = content_font.render(error_char_text, True, self.config.ERROR_COLOR)
            error_char_rect = error_char_surface.get_rect(
                center=(
                    content_rect.left + content_font.size(self.current_content[:self.error_index])[0] + 
                    content_font.size(error_char_text)[0] // 2,
                    content_rect.centery
                )
            )
            
            # 添加错误背景
            error_highlight_rect = error_char_rect.inflate(5, 5)
            pygame.draw.rect(
                screen,
                self.config.ERROR_COLOR,
                error_highlight_rect,
                border_radius=3
            )
            screen.blit(error_char_surface, error_char_rect)
    
    def render_user_input(self, screen):
        """渲染用户输入"""
        # 使用统一的字体加载器
        font = load_font(28, font_dir=self.config.FONTS_DIR)
        
        # 渲染用户输入
        input_surface = font.render(self.user_input, True, self.config.TEXT_COLOR)
        input_rect = input_surface.get_rect(center=(self.config.SCREEN_WIDTH // 2, 250))
        screen.blit(input_surface, input_rect)
        
        # 渲染光标
        if len(self.user_input) > 0:
            cursor_x = input_rect.left + font.size(self.user_input)[0]
        else:
            cursor_x = input_rect.left
        
        cursor_y = input_rect.top
        cursor_height = font.size("Tg")[1]
        
        # 绘制光标
        pygame.draw.line(
            screen,
            self.config.PRIMARY_COLOR,
            (cursor_x, cursor_y),
            (cursor_x, cursor_y + cursor_height),
            2
        )
    
    def render_progress(self, screen):
        """渲染进度"""
        # 使用统一的字体加载器
        font = load_font(24, font_dir=self.config.FONTS_DIR)
        progress_text = f"进度: {self.current_trial}/{self.total_trials}"
        progress_surface = font.render(progress_text, True, self.config.TEXT_COLOR)
        screen.blit(progress_surface, (20, 120))
    
    def render_speed_info(self, screen):
        """渲染速度信息"""
        if self.total_input_time > 0:
            # 计算速度（字符/分钟）
            cpm = int(self.characters_typed / self.total_input_time * 60)
            
            # 使用统一的字体加载器
            font = load_font(24, font_dir=self.config.FONTS_DIR)
            speed_text = f"速度: {cpm} CPM"
            speed_surface = font.render(speed_text, True, self.config.TEXT_COLOR)
            screen.blit(speed_surface, (self.config.SCREEN_WIDTH - 200, 120))
    
    def handle_event(self, event):
        """处理游戏事件"""
        super().handle_event(event)
        
        # 处理键盘事件
        if event.type == pygame.KEYDOWN:
            self.handle_key_down(event.key)
    
    def handle_key_down(self, key):
        """处理键盘按下事件"""
        # 处理特殊按键
        if key == pygame.K_BACKSPACE:
            # 退格键
            if len(self.user_input) > 0:
                self.user_input = self.user_input[:-1]
                self.current_index = max(0, self.current_index - 1)
                self.error_index = -1
        
        elif key == pygame.K_RETURN:
            # 回车键，完成当前内容
            if self.current_index < len(self.current_content):
                # 计算输入时间
                input_time = time.time() - self.start_input_time
                self.total_input_time += input_time
                
                # 更新字符数统计
                self.characters_typed += len(self.current_content)
                
                # 更新准确率
                correct_chars = sum(1 for i in range(min(len(self.current_content), len(self.user_input))) 
                                  if self.user_input[i] == self.current_content[i])
                self.correct_count += correct_chars
                self.total_count += len(self.current_content)
                
                # 增加分数
                accuracy = correct_chars / len(self.current_content)
                self.score += int(accuracy * 10)
                
                # 进入下一个训练内容
                self.current_trial += 1
                self.set_next_content()
            else:
                # 已经输入完所有字符，直接进入下一个
                self.current_trial += 1
                self.set_next_content()
        
        elif key == pygame.K_TAB:
            # Tab键，切换级别
            self.level = (self.level + 1) % len(self.levels)
            self.reset_game()
        
        else:
            # 普通按键
            # 获取按键字符
            key_char = None
            
            # 处理字母键
            if pygame.K_a <= key <= pygame.K_z:
                # 检查是否按下Shift键
                shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
                if shift_pressed:
                    key_char = chr(key - pygame.K_a + ord('A'))
                else:
                    key_char = chr(key - pygame.K_a + ord('a'))
            
            # 处理数字键
            elif pygame.K_0 <= key <= pygame.K_9:
                # 检查是否按下Shift键
                shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
                if shift_pressed:
                    # 上排符号
                    symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
                    key_char = symbols[key - pygame.K_0]
                else:
                    key_char = chr(key)
            
            # 处理空格键
            elif key == pygame.K_SPACE:
                key_char = ' '
            
            # 处理其他符号键
            elif key == pygame.K_MINUS:
                shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
                key_char = '_' if shift_pressed else '-'
            elif key == pygame.K_EQUALS:
                shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
                key_char = '+' if shift_pressed else '='
            elif key == pygame.K_LEFTBRACKET:
                shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
                key_char = '{' if shift_pressed else '['
            elif key == pygame.K_RIGHTBRACKET:
                shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
                key_char = '}' if shift_pressed else ']'
            elif key == pygame.K_BACKSLASH:
                shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
                key_char = '|' if shift_pressed else '\\'
            elif key == pygame.K_SEMICOLON:
                shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
                key_char = ':' if shift_pressed else ';'
            elif key == pygame.K_QUOTE:
                shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
                key_char = '"' if shift_pressed else "'"
            elif key == pygame.K_COMMA:
                shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
                key_char = '<' if shift_pressed else ','
            elif key == pygame.K_PERIOD:
                shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
                key_char = '>' if shift_pressed else '.'
            elif key == pygame.K_SLASH:
                shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
                key_char = '?' if shift_pressed else '/'
            
            # 如果获取到按键字符
            if key_char:
                # 检查是否是当前需要输入的字符
                if self.current_index < len(self.current_content):
                    expected_char = self.current_content[self.current_index]
                    
                    if key_char == expected_char:
                        # 输入正确
                        self.user_input += key_char
                        self.current_index += 1
                        self.error_index = -1
                        self.play_correct_sound()
                    else:
                        # 输入错误
                        self.user_input += key_char
                        self.error_index = self.current_index
                        self.current_index += 1
                        self.play_error_sound()
                else:
                    # 已经输入完所有字符，自动进入下一个
                    # 计算输入时间
                    input_time = time.time() - self.start_input_time
                    self.total_input_time += input_time
                    
                    # 更新字符数统计
                    self.characters_typed += len(self.current_content)
                    
                    # 更新准确率
                    correct_chars = sum(1 for i in range(len(self.current_content)) 
                                      if self.user_input[i] == self.current_content[i])
                    self.correct_count += correct_chars
                    self.total_count += len(self.current_content)
                    
                    # 增加分数
                    accuracy = correct_chars / len(self.current_content)
                    self.score += int(accuracy * 10)
                    
                    # 进入下一个训练内容
                    self.current_trial += 1
                    self.set_next_content()
    
    def calculate_accuracy(self):
        """计算准确率"""
        super().calculate_accuracy()
    
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