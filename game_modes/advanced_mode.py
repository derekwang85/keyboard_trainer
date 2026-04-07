#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
高级模式 - 字母下落切水果玩法
"""

import pygame
import random
import time
from .base_mode import BaseMode
from ui.text import Text
from effects.particle import ParticleSystem
from effects.cut_effect import CutEffect
from font_loader import load_font

class FallingLetter:
    """下落字母类"""
    
    def __init__(self, char, x, y, speed, config):
        """
        初始化下落字母
        
        参数:
        - char: 字母字符
        - x: x坐标
        - y: y坐标
        - speed: 下落速度
        - config: 游戏配置
        """
        self.char = char
        self.x = x
        self.y = y
        self.speed = speed
        self.config = config
        
        # 字母大小和颜色
        self.font_size = 36
        self.color = self._get_random_color()
        
        # 字体 - 使用统一的字体加载器
        self.font = load_font(self.font_size, font_dir=config.FONTS_DIR)
        
        # 是否被击中
        self.hit = False
        
        # 是否已经落地
        self.landed = False
        
        # 击中特效
        self.cut_effect = None
        
        # 计算碰撞区域
        self.update_rect()
    
    def _get_random_color(self):
        """获取随机颜色"""
        colors = [
            (255, 50, 50),   # 红色
            (50, 255, 50),   # 绿色
            (50, 50, 255),   # 蓝色
            (255, 255, 50),  # 黄色
            (255, 50, 255),  # 粉色
            (50, 255, 255),  # 青色
            (255, 150, 50),  # 橙色
            (150, 50, 255)   # 紫色
        ]
        return random.choice(colors)
    
    def update_rect(self):
        """更新碰撞区域"""
        # 渲染字母以获取大小
        text_surface = self.font.render(self.char, True, self.color)
        self.width = text_surface.get_width()
        self.height = text_surface.get_height()
        
        # 创建碰撞区域
        self.rect = pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )
    
    def update(self):
        """更新字母位置"""
        if not self.hit and not self.landed:
            # 更新位置
            self.y += self.speed
            
            # 检查是否落地
            if self.y > self.config.SCREEN_HEIGHT - 200:
                self.landed = True
            
            # 更新碰撞区域
            self.update_rect()
        
        # 更新击中特效
        if self.cut_effect:
            self.cut_effect.update()
            if self.cut_effect.finished:
                self.cut_effect = None
    
    def render(self, screen):
        """渲染字母"""
        if self.hit:
            # 渲染击中特效
            if self.cut_effect:
                self.cut_effect.render(screen)
        elif not self.landed:
            # 渲染字母
            text_surface = self.font.render(self.char, True, self.color)
            text_rect = text_surface.get_rect(center=(self.x, self.y))
            screen.blit(text_surface, text_rect)
            
            # 添加发光效果
            glow_rect = text_rect.inflate(10, 10)
            pygame.draw.rect(
                screen,
                self.color,
                glow_rect,
                2,
                border_radius=5
            )
    
    def check_hit(self, key_char):
        """
        检查是否被击中
        
        参数:
        - key_char: 按键字符
        
        返回:
        - 是否被击中
        """
        if not self.hit and not self.landed:
            if key_char.lower() == self.char.lower():
                self.hit = True
                # 创建切割特效
                self.cut_effect = CutEffect(self.x, self.y, self.color, self.config)
                return True
        return False

class AdvancedMode(BaseMode):
    """高级模式类"""
    
    def __init__(self, scene):
        """
        初始化高级模式
        
        参数:
        - scene: 游戏场景
        """
        super().__init__(scene)
        
        # 下落字母列表
        self.falling_letters = []
        
        # 游戏时间
        self.game_duration = self.config.ADVANCED_DURATION
        self.start_time = 0
        
        # 生成字母的间隔
        self.spawn_interval = 1.0
        self.last_spawn_time = 0
        
        # 字母下落速度
        self.base_speed = 2.0
        self.speed_increment = self.config.ADVANCED_SPEED_INCREMENT
        
        # 连击数
        self.combo = 0
        self.max_combo = 0
        
        # 漏失数
        self.missed = 0
        
        # 粒子系统
        self.particle_system = ParticleSystem(self.config)
        
        # 连击文本
        self.combo_text = None
        self.combo_timer = 0
        
        # 初始化游戏
        self.reset_game()
    
    def reset_game(self):
        """重置游戏"""
        # 重置游戏数据
        self.reset_game_data()
        
        # 清空下落字母列表
        self.falling_letters = []
        
        # 重置时间
        self.start_time = time.time()
        self.last_spawn_time = self.start_time
        
        # 重置速度
        self.current_speed = self.base_speed
        
        # 重置连击数
        self.combo = 0
        self.max_combo = 0
        
        # 重置漏失数
        self.missed = 0
        
        # 重置连击文本
        self.combo_text = None
        self.combo_timer = 0
    
    def start(self):
        """开始游戏"""
        super().start()
        self.reset_game()
    
    def update(self):
        """更新游戏状态"""
        super().update()
        
        # 检查游戏是否结束
        if self.game_time >= self.game_duration:
            self.end_game()
            return
        
        # 更新当前速度（随时间增加）
        self.current_speed = self.base_speed + (self.game_time / self.game_duration) * self.speed_increment
        
        # 生成新字母
        current_time = time.time()
        if current_time - self.last_spawn_time >= self.spawn_interval:
            self.spawn_letter()
            self.last_spawn_time = current_time
            
            # 随着游戏进行，减小生成间隔
            self.spawn_interval = max(0.3, 1.0 - (self.game_time / self.game_duration) * 0.7)
        
        # 更新下落字母
        for letter in self.falling_letters[:]:
            letter.update()
            
            # 检查是否落地
            if letter.landed:
                self.missed += 1
                self.combo = 0  # 重置连击
                self.falling_letters.remove(letter)
        
        # 更新粒子系统
        self.particle_system.update()
        
        # 更新连击文本
        if self.combo_text:
            self.combo_timer -= 1
            if self.combo_timer <= 0:
                self.combo_text = None
    
    def render(self, screen):
        """渲染游戏画面"""
        super().render(screen)
        
        # 渲染下落字母
        for letter in self.falling_letters:
            letter.render(screen)
        
        # 渲染游戏信息
        self.render_game_info(screen)
        
        # 渲染粒子效果
        self.particle_system.render(screen)
        
        # 渲染连击文本
        if self.combo_text:
            self.combo_text.render(screen)
    
    def render_game_info(self, screen):
        """渲染游戏信息"""
        # 使用统一的字体加载器
        font = load_font(24, font_dir=self.config.FONTS_DIR)
        
        # 渲染剩余时间
        remaining_time = max(0, int(self.game_duration - self.game_time))
        time_text = f"时间: {remaining_time}秒"
        time_surface = font.render(time_text, True, self.config.TEXT_COLOR)
        screen.blit(time_surface, (20, 120))
        
        # 渲染连击数
        combo_text = f"连击: {self.combo}"
        combo_surface = font.render(combo_text, True, self.config.TEXT_COLOR)
        screen.blit(combo_surface, (20, 150))
        
        # 渲染漏失数
        missed_text = f"漏失: {self.missed}"
        missed_surface = font.render(missed_text, True, self.config.TEXT_COLOR)
        screen.blit(missed_surface, (20, 180))
        
        # 渲染最大连击
        max_combo_text = f"最大连击: {self.max_combo}"
        max_combo_surface = font.render(max_combo_text, True, self.config.TEXT_COLOR)
        screen.blit(max_combo_surface, (self.config.SCREEN_WIDTH - 200, 120))
        
        # 渲染当前速度
        speed_text = f"速度: {self.current_speed:.1f}"
        speed_surface = font.render(speed_text, True, self.config.TEXT_COLOR)
        screen.blit(speed_surface, (self.config.SCREEN_WIDTH - 200, 150))
    
    def spawn_letter(self):
        """生成新的下落字母"""
        # 随机选择一个字母
        char = random.choice("abcdefghijklmnopqrstuvwxyz")
        
        # 随机生成x坐标
        x = random.randint(50, self.config.SCREEN_WIDTH - 50)
        
        # 生成下落字母
        letter = FallingLetter(char, x, -20, self.current_speed, self.config)
        self.falling_letters.append(letter)
    
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
        
        if key_char and len(key_char) == 1:
            # 检查是否击中任何下落字母
            hit_any = False
            
            for letter in self.falling_letters[:]:
                if letter.check_hit(key_char):
                    # 击中字母
                    hit_any = True
                    
                    # 更新游戏数据
                    self.correct_count += 1
                    self.total_count += 1
                    
                    # 增加连击数
                    self.combo += 1
                    self.max_combo = max(self.max_combo, self.combo)
                    
                    # 计算分数（基础分 + 连击奖励）
                    base_score = 10
                    combo_bonus = int(self.combo * self.config.COMBO_BONUS)
                    self.score += base_score + combo_bonus
                    
                    # 播放正确音效
                    self.play_correct_sound()
                    
                    # 生成粒子效果
                    self.particle_system.create_explosion(
                        letter.x,
                        letter.y,
                        letter.color
                    )
                    
                    # 显示连击文本
                    if self.combo >= 3:
                        self.show_combo_text(letter.x, letter.y)
                    
                    # 从列表中移除
                    self.falling_letters.remove(letter)
                    
                    # 只处理第一个击中的字母
                    break
            
            if not hit_any:
                # 没有击中任何字母
                self.total_count += 1
                self.combo = 0  # 重置连击
                self.play_error_sound()
    
    def show_combo_text(self, x, y):
        """显示连击文本"""
        combo_messages = {
            3: "不错!",
            5: "很好!",
            10: "太棒了!",
            15: "惊人!",
            20: "超级连击!",
            30: "连击大师!"
        }
        
        # 选择消息
        message = "继续!"
        for threshold, msg in sorted(combo_messages.items(), reverse=True):
            if self.combo >= threshold:
                message = msg
                break
        
        # 创建连击文本
        self.combo_text = Text(
            f"{message} {self.combo}!",
            36,
            (255, 215, 0),  # 金色
            (x, y - 50)
        )
        
        # 设置显示时间
        self.combo_timer = 30
    
    def calculate_accuracy(self):
        """计算准确率"""
        super().calculate_accuracy()
    
    def calculate_score(self):
        """计算得分"""
        # 基础分数
        base_score = self.score
        
        # 最大连击奖励
        combo_reward = int(self.max_combo * 2)
        
        # 准确率奖励
        accuracy_reward = int(self.accuracy * 50)
        
        # 总分
        self.score = base_score + combo_reward + accuracy_reward
    
    def get_max_score(self):
        """获取最大可能分数"""
        # 估算最大分数
        max_possible_letters = int(self.game_duration / 0.3)  # 假设最快0.3秒一个字母
        max_base_score = max_possible_letters * 10  # 每个字母10分
        max_combo_bonus = int(max_possible_letters * 1.5)  # 假设平均连击奖励
        max_combo_reward = 30 * 2  # 最大连击奖励
        max_accuracy_reward = 50  # 准确率奖励
        
        return max_base_score + max_combo_bonus + max_combo_reward + max_accuracy_reward
    
    def get_mode_name(self):
        """获取游戏模式名称"""
        return "高级模式"