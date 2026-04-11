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
        
        # 字母大小和颜色（高对比）
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
        """获取随机颜色（高对比深色系）"""
        colors = [
            (220, 20, 60),    # 猩红
            (26, 115, 232),   # 深蓝
            (34, 139, 34),    # 深绿
            (255, 140, 0),    # 深橙
            (156, 39, 176),   # 紫
            (0, 121, 107),    # 青绿
            (0, 0, 0),        # 纯黑
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
        self.spawn_interval = 1.2
        self.last_spawn_time = 0
        
        # 字母下落速度（放缓初速）
        self.base_speed = 1.4
        self.speed_increment = self.config.ADVANCED_SPEED_INCREMENT * 0.6
        
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

        # 动态速度调节机制
        self.consecutive_errors = 0       # 连续错误计数
        self.speed_penalty = 1.0          # 速度惩罚因子（初始1.0，每2次连续错误乘以0.95）
        self.SPEED_PENALTY_THRESHOLD = 2   # 触发降速的连续错误次数
        self.SPEED_PENALTY_FACTOR = 0.95   # 每次降速的乘法因子
        self.SPEED_MIN_RATIO = 0.5         # 速度下限比例（相对于初始base_speed）
        
        # 指法均衡追踪
        self.finger_letter_count = {}  # {finger: {char: count}}
        self._init_finger_letter_mapping()

        # 初始化游戏
        self.reset_game()
    
    def _init_finger_letter_mapping(self):
        """初始化手指到字母的映射"""
        # 从键盘渲染器获取映射
        key_to_finger = self.keyboard_renderer.key_to_finger
        
        # 按手指分组字母
        self.finger_letter_map = {}
        for char in 'abcdefghijklmnopqrstuvwxyz':
            finger = key_to_finger.get(char, 'unknown')
            if finger not in self.finger_letter_map:
                self.finger_letter_map[finger] = []
            self.finger_letter_map[finger].append(char)
        
        # 初始化计数
        for finger in self.finger_letter_map:
            self.finger_letter_count[finger] = 0
    
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

        # 重置动态速度调节
        self.consecutive_errors = 0
        self.speed_penalty = 1.0
        
        # 重置指法统计
        for finger in self.finger_letter_count:
            self.finger_letter_count[finger] = 0
    
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
        
        # 更新基准速度（随时间增加）
        base_current_speed = self.base_speed + (self.game_time / self.game_duration) * self.speed_increment
        
        # 应用速度惩罚因子得到实际速度
        self.current_speed = base_current_speed * self.speed_penalty

        # 检查速度是否低于下限
        if self.current_speed < self.base_speed * self.SPEED_MIN_RATIO:
            self.end_game()
            return
        
        # 生成新字母
        current_time = time.time()
        if current_time - self.last_spawn_time >= self.spawn_interval:
            self.spawn_letter()
            self.last_spawn_time = current_time
            
            # 随着游戏进行，减小生成间隔（保留更多反应时间）
            self.spawn_interval = max(0.6, 1.2 - (self.game_time / self.game_duration) * 0.6)
        
        # 更新下落字母
        for letter in self.falling_letters[:]:
            letter.update()
            
            # 检查是否落地（落地也算错误）
            if letter.landed:
                self.missed += 1
                self.combo = 0  # 重置连击
                self.consecutive_errors += 1
                # 检查是否需要降速
                if self.consecutive_errors >= self.SPEED_PENALTY_THRESHOLD:
                    self.speed_penalty *= self.SPEED_PENALTY_FACTOR
                    self.consecutive_errors = 0
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
        
        # 渲染当前速度（带速度倍率）
        speed_ratio = self.speed_penalty * 100
        speed_text = f"速度: {self.current_speed:.1f} ({speed_ratio:.0f}%)"
        
        # 根据速度倍率选择颜色
        if speed_ratio <= self.SPEED_MIN_RATIO * 100:
            speed_color = (220, 20, 60)  # 红色：危险
        elif speed_ratio <= 75:
            speed_color = (255, 140, 0)  # 橙色：警告
        else:
            speed_color = self.config.TEXT_COLOR
        
        speed_surface = font.render(speed_text, True, speed_color)
        screen.blit(speed_surface, (self.config.SCREEN_WIDTH - 200, 150))

        # 渲染连续错误数
        error_text = f"连错: {self.consecutive_errors}/{self.SPEED_PENALTY_THRESHOLD}"
        error_surface = font.render(error_text, True, self.config.TEXT_COLOR)
        screen.blit(error_surface, (self.config.SCREEN_WIDTH - 200, 180))
    
    def spawn_letter(self):
        """
        生成新的下落字母 - 指法均衡算法
        
        优先选择使用次数最少的手指对应的字母，
        以确保每根手指都能得到均衡的练习
        """
        # 找出使用次数最少的手指
        min_count = min(self.finger_letter_count.values()) if self.finger_letter_count else 0
        
        # 找出所有使用次数等于最少的手指
        least_used_fingers = [
            finger for finger, count in self.finger_letter_count.items()
            if count == min_count and finger in self.finger_letter_map
        ]
        
        # 优先选择使用次数少的手指对应的字母
        if least_used_fingers:
            # 80%概率选择最少使用的手指，20%概率完全随机（增加多样性）
            if random.random() < 0.8:
                selected_finger = random.choice(least_used_fingers)
                char = random.choice(self.finger_letter_map[selected_finger])
            else:
                char = random.choice("abcdefghijklmnopqrstuvwxyz")
        else:
            char = random.choice("abcdefghijklmnopqrstuvwxyz")
        
        # 记录字母生成（用于指法统计）
        finger = self.keyboard_renderer.key_to_finger.get(char, 'unknown')
        if finger in self.finger_letter_count:
            self.finger_letter_count[finger] += 1
        
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

                    # 重置连续错误计数（击中成功）
                    self.consecutive_errors = 0
                    
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
                self.consecutive_errors += 1
                # 检查是否需要降速
                if self.consecutive_errors >= self.SPEED_PENALTY_THRESHOLD:
                    self.speed_penalty *= self.SPEED_PENALTY_FACTOR
                    self.consecutive_errors = 0
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