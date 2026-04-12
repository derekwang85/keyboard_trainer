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
    """初级模式类 - 分阶段指法训练"""
    
    # 阶段定义：每个阶段包含按键集和过关条件
    TRAINING_STAGES = [
        # 阶段1: 基准键位入门 (ASDF JKL;)
        {
            'id': 1,
            'name': '基准键位',
            'description': '学习基准键位：ASDF JKL;',
            'keys': ['a', 's', 'd', 'f', 'j', 'k', 'l', ';'],
            'home_keys': ['f', 'j'],  # 基准键（带指示条）
            'required_count': 30,      # 该阶段需要完成的次数
            'min_accuracy': 0.7        # 最低准确率要求
        },
        # 阶段2: 左手无名指 (2WSX)
        {
            'id': 2,
            'name': '左手无名指',
            'description': '学习左手无名指：2WSX',
            'keys': ['a', 's', 'd', 'f', '2', 'w', 's', 'x'],
            'home_keys': ['f'],
            'required_count': 25,
            'min_accuracy': 0.65
        },
        # 阶段3: 左手中指 (3EDC)
        {
            'id': 3,
            'name': '左手中指',
            'description': '学习左手中指：3EDC',
            'keys': ['s', 'd', 'f', '3', 'e', 'd', 'c'],
            'home_keys': ['f'],
            'required_count': 25,
            'min_accuracy': 0.65
        },
        # 阶段4: 左手食指上排 (RTFV)
        {
            'id': 4,
            'name': '左手食指上',
            'description': '学习左手食指上排：RTFV',
            'keys': ['f', 'g', 'r', 't', 'v', 'b'],
            'home_keys': ['f'],
            'required_count': 25,
            'min_accuracy': 0.6
        },
        # 阶段5: 左手食指下排 (VGB)
        {
            'id': 5,
            'name': '左手食指下',
            'description': '学习左手食指下排：VGB',
            'keys': ['f', 'g', 'v', 'b', 'n'],
            'home_keys': ['f'],
            'required_count': 20,
            'min_accuracy': 0.6
        },
        # 阶段6: 右手食指下排 (HNM)
        {
            'id': 6,
            'name': '右手食指下',
            'description': '学习右手食指下排：HNM',
            'keys': ['j', 'h', 'n', 'm', 'b'],
            'home_keys': ['j'],
            'required_count': 20,
            'min_accuracy': 0.6
        },
        # 阶段7: 右手食指上排 (YUJ)
        {
            'id': 7,
            'name': '右手食指上',
            'description': '学习右手食指上排：YUJ',
            'keys': ['j', 'h', 'y', 'u', 'n', 'm'],
            'home_keys': ['j'],
            'required_count': 25,
            'min_accuracy': 0.6
        },
        # 阶段8: 右手中指 (I,K,)
        {
            'id': 8,
            'name': '右手中指',
            'description': '学习右手中指：IK,',
            'keys': ['j', 'k', 'l', 'i', 'k', ','],
            'home_keys': ['j'],
            'required_count': 25,
            'min_accuracy': 0.65
        },
        # 阶段9: 右手无名指 (OL.)
        {
            'id': 9,
            'name': '右手无名指',
            'description': '学习右手无名指：OL.',
            'keys': ['k', 'l', 'o', 'p', 'l', '.'],
            'home_keys': ['j'],
            'required_count': 25,
            'min_accuracy': 0.65
        },
        # 阶段10: 综合练习
        {
            'id': 10,
            'name': '综合练习',
            'description': '综合所有键位练习',
            'keys': ['a', 's', 'd', 'f', 'j', 'k', 'l', ';',
                    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
                    'z', 'x', 'c', 'v', 'b', 'n', 'm'],
            'home_keys': ['f', 'j'],
            'required_count': 50,
            'min_accuracy': 0.7
        },
    ]
    
    def __init__(self, scene):
        """
        初始化初级模式
        
        参数:
        - scene: 游戏场景
        """
        super().__init__(scene)
        
        # 阶段训练系统
        self.current_stage_index = 0
        self.stage_trial_count = 0      # 当前阶段的完成次数
        self.stage_correct_count = 0    # 当前阶段的正确次数
        
        # 当前目标按键
        self.target_key = None
        
        # 训练次数（全局，用于统计）
        self.total_trials = self.config.BEGINNER_TRIALS
        self.current_trial = 0
        
        # 粒子系统
        self.particle_system = ParticleSystem(self.config)
        
        # 鼓励文本
        self.encouragement_text = None
        self.encouragement_timer = 0

        # 预加载字体
        self.font_large = load_font(100, font_dir=self.config.FONTS_DIR)
        self.font_medium = load_font(48, font_dir=self.config.FONTS_DIR)
        self.font_small = load_font(20, font_dir=self.config.FONTS_DIR)
        self.hint_font = load_font(24, font_dir=self.config.FONTS_DIR)
        self.progress_font = load_font(24, font_dir=self.config.FONTS_DIR)
        self.stage_font = load_font(28, font_dir=self.config.FONTS_DIR)
        self.desc_font = load_font(18, font_dir=self.config.FONTS_DIR)

        # 按键去抖
        self.last_key = None
        self.last_key_time = 0
        self.key_debounce_seconds = 0.12

        # 过渡控制
        self.pending_next_target = False
        self.next_target_delay = 0
        self.error_highlight_frames = 6
        
        # 阶段切换动画
        self.stage_transition_timer = 0
        self.showing_stage_intro = False
        
        # 初始化游戏
        self.reset_game()
    
    def _get_key_set(self):
        """获取当前阶段的训练按键集"""
        stage = self.TRAINING_STAGES[self.current_stage_index]
        return stage['keys']
    
    @property
    def current_stage(self):
        """获取当前阶段"""
        return self.TRAINING_STAGES[self.current_stage_index]
    
    @property
    def total_stage_count(self):
        """获取总阶段数"""
        return len(self.TRAINING_STAGES)
    
    def reset_game(self):
        """重置游戏"""
        # 重置游戏数据
        self.reset_game_data()
        
        # 重置阶段
        self.current_stage_index = 0
        self.stage_trial_count = 0
        self.stage_correct_count = 0
        
        # 重置训练次数
        self.current_trial = 0

        # 清理高亮与过渡状态
        self.keyboard_renderer.clear_highlight()
        self.pending_next_target = False
        self.next_target_delay = 0
        
        # 显示阶段介绍
        self.showing_stage_intro = True
        self.stage_transition_timer = 90  # 显示1.5秒
        
        # 更新当前阶段的按键集
        self.key_set = self._get_key_set()
        
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

        # 使用当前阶段的按键集
        self.key_set = self._get_key_set()
        self.target_key = random.choice(self.key_set)
        
        # 高亮显示目标按键（持续）
        self.keyboard_renderer.highlight_key(self.target_key, 
            color=self.config.KEY_HIGHLIGHT, duration=None)
    
    def update(self):
        """更新游戏状态"""
        super().update()

        if not self.running:
            return

        # 处理阶段介绍动画
        if self.showing_stage_intro:
            self.stage_transition_timer -= 1
            if self.stage_transition_timer <= 0:
                self.showing_stage_intro = False
                # 阶段介绍结束后立即生成新目标按键高亮
                self.generate_target_key()
            return  # 阶段介绍期间不处理其他逻辑

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
                self.generate_next_target_after_error()
        else:
            # 检查是否完成当前阶段
            self._check_stage_progress()
    
    def _check_stage_progress(self):
        """检查阶段进度"""
        stage = self.current_stage
        
        # 检查是否满足当前阶段的完成条件
        if self.stage_trial_count >= stage['required_count']:
            # 计算当前阶段准确率
            stage_accuracy = (self.stage_correct_count / self.stage_trial_count 
                            if self.stage_trial_count > 0 else 0)
            
            # 检查是否达到最低准确率要求
            if stage_accuracy >= stage['min_accuracy']:
                # 阶段完成，进入下一阶段
                if self.current_stage_index < self.total_stage_count - 1:
                    self._advance_to_next_stage()
                else:
                    # 所有阶段完成，结束游戏
                    self.end_game()
            else:
                # 准确率不足，重新开始本阶段
                self._restart_current_stage()
    
    def _advance_to_next_stage(self):
        """进入下一阶段"""
        self.current_stage_index += 1
        self.stage_trial_count = 0
        self.stage_correct_count = 0
        self.key_set = self._get_key_set()
        
        # 显示阶段介绍
        self.showing_stage_intro = True
        self.stage_transition_timer = 90
        self.keyboard_renderer.clear_highlight()
    
    def _restart_current_stage(self):
        """重新开始当前阶段"""
        self.stage_trial_count = 0
        self.stage_correct_count = 0
        self.key_set = self._get_key_set()
        self.generate_target_key()
    
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
        self.stage_trial_count += 1
        self.stage_correct_count += 1
        self.score += 1
        
        # 播放正确音效
        self.play_correct_sound()
        
        # 显示鼓励文本
        self.show_encouragement()

        # 记录上一个目标键（用于重复按键闪烁）
        prev_target_key = self.target_key

        # 清除旧高亮并生成下一个
        self.keyboard_renderer.clear_highlight()
        self.generate_target_key()

        # 如果重复按键，触发一次快速闪烁提示
        if prev_target_key and self.target_key == prev_target_key:
            self.keyboard_renderer.blink_key(self.target_key, blink_count=1)
    
    def handle_error_key(self, pressed_key_code=None):
        """处理错误按键"""
        # 更新游戏数据
        self.total_count += 1
        self.current_trial += 1
        self.stage_trial_count += 1  # 计入阶段进度

        # 播放错误音效
        self.play_error_sound()

        wrong_char = None
        if pressed_key_code:
            wrong_char = self.keyboard_renderer.key_map.get(pressed_key_code, None)

        # 高亮目标和错误按键
        self.keyboard_renderer.clear_highlight()
        if self.target_key:
            self.keyboard_renderer.highlight_key(self.target_key, 
                color=self.config.KEY_HIGHLIGHT, duration=None)
        if wrong_char:
            self.keyboard_renderer.highlight_key(wrong_char, 
                self.config.ERROR_COLOR, self.error_highlight_frames)

        # 设置延迟切换到下一个目标（但保持正确按键高亮）
        self.pending_next_target = True
        self.next_target_delay = self.error_highlight_frames

    def generate_next_target_after_error(self):
        """错误延迟后生成下一个目标按键"""
        prev_target_key = self.target_key
        self.keyboard_renderer.clear_highlight()
        self.generate_target_key()

        # 如果重复按键，触发一次快速闪烁提示
        if prev_target_key and self.target_key == prev_target_key:
            self.keyboard_renderer.blink_key(self.target_key, blink_count=1)
    
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
        # 如果显示阶段介绍，先渲染介绍界面
        if self.showing_stage_intro:
            self._render_stage_intro(screen)
            return
        
        # 先渲染键盘与基础信息
        super().render(screen)

        # 渲染阶段信息
        self.render_stage_info(screen)

        # 渲染进度
        self.render_progress(screen)

        # 渲染目标按键提示
        self.render_target_key(screen, self.config.KEYBOARD_POS_Y)

        # 渲染鼓励文本
        if self.encouragement_text:
            self.encouragement_text.render(screen)

        # 渲染指法示意图（在键盘下方）
        if self.target_key:
            active_finger = self.keyboard_renderer.get_finger_for_key(self.target_key)
            if active_finger:
                self.keyboard_renderer.render_finger_guide(screen, active_finger)
    
    def _render_stage_intro(self, screen):
        """渲染阶段介绍界面"""
        # 深色半透明背景
        overlay = pygame.Surface((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        stage = self.current_stage
        center_x = self.config.SCREEN_WIDTH // 2
        center_y = self.config.SCREEN_HEIGHT // 2
        
        # 阶段标题
        stage_title = f"第 {stage['id']} 阶段"
        title_surface = self.font_medium.render(stage_title, True, self.config.PRIMARY_COLOR)
        title_rect = title_surface.get_rect(center=(center_x, center_y - 80))
        screen.blit(title_surface, title_rect)
        
        # 阶段名称
        name_surface = self.stage_font.render(stage['name'], True, self.config.TEXT_COLOR)
        name_rect = name_surface.get_rect(center=(center_x, center_y - 20))
        screen.blit(name_surface, name_rect)
        
        # 阶段描述
        desc_surface = self.desc_font.render(stage['description'], True, self.config.TEXT_SECONDARY)
        desc_rect = desc_surface.get_rect(center=(center_x, center_y + 30))
        screen.blit(desc_surface, desc_rect)
        
        # 按键提示
        keys_text = " ".join(k.upper() for k in stage['keys'][:8])
        if len(stage['keys']) > 8:
            keys_text += " ..."
        keys_surface = self.font_small.render(keys_text, True, self.config.PRIMARY_LIGHT)
        keys_rect = keys_surface.get_rect(center=(center_x, center_y + 80))
        screen.blit(keys_surface, keys_rect)
        
        # 倒计时提示
        countdown = self.stage_transition_timer // 60 + 1
        countdown_text = f"{countdown} 秒后开始..."
        countdown_surface = self.font_small.render(countdown_text, True, self.config.TEXT_MUTED)
        countdown_rect = countdown_surface.get_rect(center=(center_x, center_y + 140))
        screen.blit(countdown_surface, countdown_rect)
    
    def render_stage_info(self, screen):
        """渲染阶段信息"""
        stage = self.current_stage
        
        # 阶段名称（左侧）
        stage_text = f"第 {stage['id']}/{self.total_stage_count} 阶段: {stage['name']}"
        stage_surface = self.font_small.render(stage_text, True, self.config.TEXT_COLOR)
        screen.blit(stage_surface, (20, 50))
        
        # 阶段按键数（右侧）
        keys_text = f"按键: {' '.join(k.upper() for k in self.key_set[:6])}"
        if len(self.key_set) > 6:
            keys_text += "..."
        keys_surface = self.font_small.render(keys_text, True, self.config.TEXT_SECONDARY)
        keys_rect = keys_surface.get_rect(topright=(self.config.SCREEN_WIDTH - 20, 50))
        screen.blit(keys_surface, keys_rect)
    
    def render_target_key(self, screen, keyboard_y):
        """渲染目标按键提示"""
        # 计算中心位置（避开键盘区域）
        center_x = self.config.SCREEN_WIDTH // 2
        center_y = keyboard_y // 2 - 40
        
        # 渲染目标按键字符
        display_char = self.target_key.upper() if self.target_key else ''
        
        if display_char == ' ':
            display_char = '空格'
        
        # 渲染目标按键 - 使用主题色
        text_surface = self.font_large.render(display_char, True, self.config.PRIMARY_COLOR)
        text_rect = text_surface.get_rect(center=(center_x, center_y))
        screen.blit(text_surface, text_rect)
        
        # 渲染提示文本
        hint_text = "请按相应的按键"
        hint_surface = self.hint_font.render(hint_text, True, self.config.TEXT_SECONDARY)
        hint_rect = hint_surface.get_rect(center=(center_x, center_y + 70))
        screen.blit(hint_surface, hint_rect)
    
    def render_progress(self, screen):
        """渲染进度信息"""
        stage = self.current_stage
        
        # 计算当前阶段进度
        stage_progress = self.stage_trial_count / stage['required_count'] if stage['required_count'] > 0 else 0
        
        # 顶部进度条（阶段进度）
        bar_width = 400
        bar_height = 8
        bar_x = (self.config.SCREEN_WIDTH - bar_width) // 2
        bar_y = 28
        
        # 背景
        pygame.draw.rect(screen, (50, 55, 65), (bar_x, bar_y, bar_width, bar_height), border_radius=4)
        
        # 进度（使用渐变色）
        progress_width = int(stage_progress * bar_width)
        if progress_width > 0:
            pygame.draw.rect(screen, self.config.PRIMARY_COLOR, 
                           (bar_x, bar_y, progress_width, bar_height), border_radius=4)
        
        # 阶段内进度文字（顶部右侧）
        stage_text = f"阶段进度: {self.stage_trial_count}/{stage['required_count']}"
        stage_surface = self.progress_font.render(stage_text, True, self.config.TEXT_COLOR)
        stage_rect = stage_surface.get_rect(topleft=(20, 10))
        screen.blit(stage_surface, stage_rect)
        
        # 整体进度百分比（顶部右侧）
        total_progress = self.current_trial / 250  # 粗略估算
        total_text = f"总进度: {min(100, int(total_progress * 100))}%"
        total_surface = self.progress_font.render(total_text, True, self.config.TEXT_SECONDARY)
        total_rect = total_surface.get_rect(topright=(self.config.SCREEN_WIDTH - 20, 10))
        screen.blit(total_surface, total_rect)
