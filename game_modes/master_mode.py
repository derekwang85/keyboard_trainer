#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
大师模式 - 汉字下落+拼音输入
"""

import pygame
import random
import time
from .base_mode import BaseMode
from ui.text import Text
from effects.particle import ParticleSystem
from effects.explosion import ExplosionEffect
from content.chinese_chars import CHINESE_CHARS
from font_loader import load_font

class FallingChineseChar:
    """下落汉字类"""
    
    def __init__(self, char, pinyin, x, y, speed, config):
        """
        初始化下落汉字
        
        参数:
        - char: 汉字字符
        - pinyin: 拼音
        - x: x坐标
        - y: y坐标
        - speed: 下落速度
        - config: 游戏配置
        """
        self.char = char
        self.pinyin = pinyin
        self.x = x
        self.y = y
        self.speed = speed
        self.config = config
        
        # 汉字大小和颜色（高对比）
        self.font_size = 48
        self.color = self._get_random_color()
        
        # 字体 - 使用统一的字体加载器
        self.font = load_font(self.font_size, font_dir=config.FONTS_DIR)
        
        # 是否被击中
        self.hit = False
        
        # 是否已经落地
        self.landed = False
        
        # 爆炸特效
        self.explosion_effect = None
        
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
        # 渲染汉字以获取大小
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
        """更新汉字位置"""
        if not self.hit and not self.landed:
            # 更新位置
            self.y += self.speed
            
            # 检查是否落地
            if self.y > self.config.SCREEN_HEIGHT - 200:
                self.landed = True
            
            # 更新碰撞区域
            self.update_rect()
        
        # 更新爆炸特效
        if self.explosion_effect:
            self.explosion_effect.update()
            if self.explosion_effect.finished:
                self.explosion_effect = None
    
    def render(self, screen):
        """渲染汉字"""
        if self.hit:
            # 渲染爆炸特效
            if self.explosion_effect:
                self.explosion_effect.render(screen)
        elif not self.landed:
            # 渲染汉字
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
            
            # 渲染拼音提示（半透明）
            # 使用统一的字体加载器
            pinyin_font = load_font(16, font_dir=self.config.FONTS_DIR)
            pinyin_surface = pinyin_font.render(self.pinyin, True, (100, 100, 100))
            pinyin_rect = pinyin_surface.get_rect(center=(self.x, self.y + 30))
            
            # 创建半透明背景
            alpha_surface = pygame.Surface((pinyin_rect.width + 10, pinyin_rect.height + 5), pygame.SRCALPHA)
            alpha_surface.fill((255, 255, 255, 128))
            screen.blit(alpha_surface, (pinyin_rect.x - 5, pinyin_rect.y - 2))
            
            screen.blit(pinyin_surface, pinyin_rect)
    
    def check_hit(self, pinyin):
        """
        检查是否被击中
        
        参数:
        - pinyin: 输入的拼音
        
        返回:
        - 是否被击中
        """
        if not self.hit and not self.landed:
            if pinyin.lower() == self.pinyin.lower():
                self.hit = True
                # 创建爆炸特效
                self.explosion_effect = ExplosionEffect(self.x, self.y, self.color, self.config)
                return True
        return False

class MasterMode(BaseMode):
    """大师模式类"""
    
    def __init__(self, scene):
        """
        初始化大师模式
        
        参数:
        - scene: 游戏场景
        """
        super().__init__(scene)
        
        # 下落汉字列表
        self.falling_chars = []
        
        # 游戏时间
        self.game_duration = self.config.MASTER_DURATION
        self.start_time = 0
        
        # 生成汉字的间隔
        self.spawn_interval = 2.4
        self.last_spawn_time = 0

        # 按键去抖，避免一次敲击录入多次
        self.last_key = None
        self.last_key_time = 0
        self.key_debounce_seconds = 0.12
        
        # 汉字下落速度（放缓初速）
        self.base_speed = 0.9
        self.speed_increment = self.config.MASTER_SPEED_INCREMENT * 0.5
        
        # 用户输入的拼音
        self.user_pinyin = ""
        
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

        # 初始化游戏
        self.reset_game()
    
    def reset_game(self):
        """重置游戏"""
        # 重置游戏数据
        self.reset_game_data()
        
        # 清空下落汉字列表
        self.falling_chars = []
        
        # 重置时间
        self.start_time = time.time()
        self.last_spawn_time = self.start_time
        
        # 重置速度
        self.current_speed = self.base_speed
        
        # 重置用户输入
        self.user_pinyin = ""
        
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
        
        # 生成新汉字
        current_time = time.time()
        if current_time - self.last_spawn_time >= self.spawn_interval:
            self.spawn_chinese_char()
            self.last_spawn_time = current_time
            
            # 随着游戏进行，减小生成间隔（保留更长时间）
            self.spawn_interval = max(1.2, 2.4 - (self.game_time / self.game_duration) * 1.0)
        
        # 更新下落汉字
        for char in self.falling_chars[:]:
            char.update()
            
            # 检查是否落地（落地也算错误）
            if char.landed:
                self.missed += 1
                self.combo = 0  # 重置连击
                self.consecutive_errors += 1
                # 检查是否需要降速
                if self.consecutive_errors >= self.SPEED_PENALTY_THRESHOLD:
                    self.speed_penalty *= self.SPEED_PENALTY_FACTOR
                    self.consecutive_errors = 0
                self.falling_chars.remove(char)
        
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
        
        # 渲染下落汉字
        for char in self.falling_chars:
            char.render(screen)
        
        # 渲染游戏信息
        self.render_game_info(screen)
        
        # 渲染用户输入
        self.render_user_input(screen)
        
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
    
    def render_user_input(self, screen):
        """渲染用户输入"""
        # 使用统一的字体加载器
        hint_font = load_font(24, font_dir=self.config.FONTS_DIR)
        pinyin_font = load_font(36, font_dir=self.config.FONTS_DIR)
        
        # 渲染提示文本
        hint_text = "请输入拼音并按Enter确认:"
        hint_surface = hint_font.render(hint_text, True, self.config.TEXT_COLOR)
        hint_rect = hint_surface.get_rect(center=(self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT - 150))
        screen.blit(hint_surface, hint_rect)
        
        # 渲染用户输入的拼音
        pinyin_surface = pinyin_font.render(self.user_pinyin, True, self.config.PRIMARY_COLOR)
        pinyin_rect = pinyin_surface.get_rect(center=(self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT - 100))
        screen.blit(pinyin_surface, pinyin_rect)
        
        # 添加输入框效果
        input_rect = pinyin_rect.inflate(20, 10)
        pygame.draw.rect(
            screen,
            self.config.PRIMARY_COLOR,
            input_rect,
            2,
            border_radius=5
        )
        
        # 渲染光标
        if len(self.user_pinyin) > 0:
            cursor_x = pinyin_rect.left + pinyin_font.size(self.user_pinyin)[0]
        else:
            cursor_x = pinyin_rect.left
        
        cursor_y = pinyin_rect.top
        cursor_height = pinyin_font.size("Tg")[1]
        
        # 绘制光标
        pygame.draw.line(
            screen,
            self.config.PRIMARY_COLOR,
            (cursor_x, cursor_y),
            (cursor_x, cursor_y + cursor_height),
            2
        )
    
    def spawn_chinese_char(self):
        """生成新的下落汉字"""
        # 随机选择一个汉字和拼音
        char, pinyin = random.choice(list(CHINESE_CHARS.items()))
        
        # 随机生成x坐标
        x = random.randint(50, self.config.SCREEN_WIDTH - 50)
        
        # 生成下落汉字
        chinese_char = FallingChineseChar(char, pinyin, x, -20, self.current_speed, self.config)
        self.falling_chars.append(chinese_char)
    
    def handle_event(self, event):
        """处理游戏事件"""
        super().handle_event(event)
        
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

        # 处理特殊按键
        if key == pygame.K_BACKSPACE:
            if len(self.user_pinyin) > 0:
                self.user_pinyin = self.user_pinyin[:-1]
        
        elif key == pygame.K_RETURN:
            if self.user_pinyin:
                self.submit_pinyin()
        
        else:
            key_char = None
            if pygame.K_a <= key <= pygame.K_z:
                shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
                key_char = chr(key - pygame.K_a + (ord('A') if shift_pressed else ord('a')))
            if key_char:
                self.user_pinyin += key_char
    
    def submit_pinyin(self):
        """提交拼音"""
        if not self.user_pinyin:
            return
        
        # 检查是否击中任何下落汉字
        hit_any = False
        
        for char in self.falling_chars[:]:
            if char.check_hit(self.user_pinyin):
                # 击中汉字
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
                base_score = 20
                combo_bonus = int(self.combo * self.config.COMBO_BONUS * 2)  # 大师模式连击奖励更高
                self.score += base_score + combo_bonus
                
                # 播放正确音效
                self.play_correct_sound()
                
                # 生成粒子效果
                self.particle_system.create_explosion(
                    char.x,
                    char.y,
                    char.color
                )
                
                # 显示连击文本
                if self.combo >= 3:
                    self.show_combo_text(char.x, char.y)
                
                # 从列表中移除
                self.falling_chars.remove(char)
                
                # 只处理第一个击中的汉字
                break
        
        if not hit_any:
            # 没有击中任何汉字
            self.total_count += 1
            self.combo = 0  # 重置连击
            self.consecutive_errors += 1
            # 检查是否需要降速
            if self.consecutive_errors >= self.SPEED_PENALTY_THRESHOLD:
                self.speed_penalty *= self.SPEED_PENALTY_FACTOR
                self.consecutive_errors = 0
            self.play_error_sound()
        
        # 清空用户输入
        self.user_pinyin = ""
    
    def show_combo_text(self, x, y):
        """显示连击文本"""
        combo_messages = {
            3: "不错!",
            5: "很好!",
            10: "太棒了!",
            15: "惊人!",
            20: "超级连击!",
            30: "汉字大师!"
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
        combo_reward = int(self.max_combo * 3)  # 大师模式连击奖励更高
        
        # 准确率奖励
        accuracy_reward = int(self.accuracy * 100)  # 大师模式准确率奖励更高
        
        # 总分
        self.score = base_score + combo_reward + accuracy_reward
    
    def get_max_score(self):
        """获取最大可能分数"""
        # 估算最大分数
        max_possible_chars = int(self.game_duration / 0.8)  # 假设最快0.8秒一个汉字
        max_base_score = max_possible_chars * 20  # 每个汉字20分
        max_combo_bonus = int(max_possible_chars * 3)  # 假设平均连击奖励
        max_combo_reward = 30 * 3  # 最大连击奖励
        max_accuracy_reward = 100  # 准确率奖励
        
        return max_base_score + max_combo_bonus + max_combo_reward + max_accuracy_reward
    
    def get_mode_name(self):
        """获取游戏模式名称"""
        return "大师模式"