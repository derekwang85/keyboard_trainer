#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
大师模式 / 高级拼音模式共用实现
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

    def __init__(self, char, pinyin, x, y, speed, config, show_pinyin=True):
        self.char = char
        self.pinyin = pinyin
        self.x = x
        self.y = y
        self.speed = speed
        self.config = config
        self.show_pinyin = show_pinyin

        self.font_size = 48
        self.color = self._get_random_color()
        self.font = load_font(self.font_size, font_dir=config.FONTS_DIR)

        self.hit = False
        self.landed = False
        self.explosion_effect = None
        self.update_rect()

    def _get_random_color(self):
        """获取随机颜色（高对比深色系）"""
        colors = [
            (220, 20, 60),
            (26, 115, 232),
            (34, 139, 34),
            (255, 140, 0),
            (156, 39, 176),
            (0, 121, 107),
            (0, 0, 0),
        ]
        return random.choice(colors)

    def update_rect(self):
        """更新碰撞区域"""
        text_surface = self.font.render(self.char, True, self.color)
        self.width = text_surface.get_width()
        self.height = text_surface.get_height()
        self.rect = pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )

    def update(self, speed=None):
        """更新汉字位置"""
        if not self.hit and not self.landed:
            current_speed = speed if speed is not None else self.speed
            self.y += current_speed
            if self.y > self.config.SCREEN_HEIGHT - 200:
                self.landed = True
            self.update_rect()

        if self.explosion_effect:
            self.explosion_effect.update()
            if self.explosion_effect.finished:
                self.explosion_effect = None

    def render(self, screen):
        """渲染汉字"""
        if self.hit:
            if self.explosion_effect:
                self.explosion_effect.render(screen)
            return

        if self.landed:
            return

        text_surface = self.font.render(self.char, True, self.color)
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        screen.blit(text_surface, text_rect)

        glow_rect = text_rect.inflate(10, 10)
        pygame.draw.rect(screen, self.color, glow_rect, 2, border_radius=5)

        if self.show_pinyin:
            pinyin_font = load_font(16, font_dir=self.config.FONTS_DIR)
            pinyin_surface = pinyin_font.render(self.pinyin, True, (100, 100, 100))
            pinyin_rect = pinyin_surface.get_rect(center=(self.x, self.y + 30))
            alpha_surface = pygame.Surface((pinyin_rect.width + 10, pinyin_rect.height + 5), pygame.SRCALPHA)
            alpha_surface.fill((255, 255, 255, 128))
            screen.blit(alpha_surface, (pinyin_rect.x - 5, pinyin_rect.y - 2))
            screen.blit(pinyin_surface, pinyin_rect)

    def check_hit(self, user_input, input_mode="pinyin"):
        """检查是否被击中"""
        if self.hit or self.landed:
            return False

        normalized_input = user_input.strip()
        if input_mode == "char":
            is_match = normalized_input == self.char
        else:
            is_match = normalized_input.lower() == self.pinyin.lower()

        if is_match:
            self.hit = True
            self.explosion_effect = ExplosionEffect(self.x, self.y, self.color, self.config)
            return True
        return False


class MasterMode(BaseMode):
    """大师模式类"""

    def __init__(self, scene):
        super().__init__(scene)

        self.show_keyboard = False
        self.show_pinyin_hint = False
        self.mode_subtype = "master"
        self.input_mode = "char"
        self.input_prompt = "请输入汉字并按Enter确认:"
        self.mode_hint_text = "【大师汉字模式】"
        self.max_input_length = 4

        self.falling_chars = []
        self.game_duration = self.config.MASTER_DURATION
        self.start_time = 0
        self.spawn_interval = 2.4
        self.last_spawn_time = 0

        self.last_key = None
        self.last_key_time = 0
        self.key_debounce_seconds = 0.12

        self.base_speed = 0.9
        self.speed_increment = self.config.MASTER_SPEED_INCREMENT * 0.5
        self.user_input = ""

        self.combo = 0
        self.max_combo = 0
        self.missed = 0

        self.particle_system = ParticleSystem(self.config)
        self.combo_text = None
        self.combo_timer = 0

        self.consecutive_errors = 0
        self.speed_penalty = 1.0
        self.SPEED_PENALTY_THRESHOLD = 2
        self.SPEED_PENALTY_FACTOR = 0.95
        self.SPEED_MIN_RATIO = 0.5

        self.consecutive_correct = 0
        self.speed_bonus = 1.0
        self.SPEED_BONUS_THRESHOLD = self.config.SPEED_BONUS_THRESHOLD
        self.SPEED_BONUS_FIRST_STEP = self.config.SPEED_BONUS_FIRST_STEP
        self.SPEED_BONUS_CONTINUOUS_STEP = self.config.SPEED_BONUS_CONTINUOUS_STEP
        self.SPEED_BONUS_MAX = self.config.SPEED_BONUS_MAX

        self.set_variant("master")
        self.reset_game()

    def reset_game(self):
        """重置游戏"""
        self.reset_game_data()
        self.falling_chars = []
        self.start_time = time.time()
        self.last_spawn_time = self.start_time
        self.current_speed = self.base_speed
        self.user_input = ""
        self.combo = 0
        self.max_combo = 0
        self.missed = 0
        self.combo_text = None
        self.combo_timer = 0
        self.consecutive_errors = 0
        self.speed_penalty = 1.0
        self.consecutive_correct = 0
        self.speed_bonus = 1.0

    def start(self):
        """开始游戏"""
        super().start()
        self.reset_game()
        self._toggle_text_input(self.input_mode == "char")

    def end_game(self):
        """结束游戏前关闭文本输入"""
        self._toggle_text_input(False)
        super().end_game()

    def abort_game(self):
        """放弃游戏时关闭文本输入"""
        self._toggle_text_input(False)
        super().abort_game()

    def set_variant(self, variant):
        """设置大师模式的具体变体"""
        if variant == "advanced_pinyin":
            self.mode_subtype = "advanced_pinyin"
            self.input_mode = "pinyin"
            self.show_keyboard = True
            self.show_pinyin_hint = True
            self.input_prompt = "请输入拼音并按Enter确认:"
            self.mode_hint_text = "【高级拼音模式】"
            self.max_input_length = 12
        else:
            self.mode_subtype = "master"
            self.input_mode = "char"
            self.show_keyboard = False
            self.show_pinyin_hint = False
            self.input_prompt = "请输入汉字并按Enter确认:"
            self.mode_hint_text = "【大师汉字模式】"
            self.max_input_length = 4

    def _toggle_text_input(self, enabled):
        """按模式开启或关闭系统文本输入"""
        if not hasattr(pygame.key, "start_text_input"):
            return
        try:
            if enabled:
                pygame.key.start_text_input()
            else:
                pygame.key.stop_text_input()
        except pygame.error:
            pass

    def _apply_error_penalty(self):
        """处理连续错误带来的降速"""
        self.consecutive_errors += 1
        self.consecutive_correct = 0
        if self.consecutive_errors >= self.SPEED_PENALTY_THRESHOLD:
            self.speed_penalty *= self.SPEED_PENALTY_FACTOR
            self.consecutive_errors = 0

    def _apply_speed_bonus_progression(self):
        """按新的连续命中规则逐步加速"""
        if self.consecutive_correct == self.SPEED_BONUS_THRESHOLD:
            self.speed_bonus = min(self.SPEED_BONUS_MAX, self.speed_bonus + self.SPEED_BONUS_FIRST_STEP)
        elif self.consecutive_correct > self.SPEED_BONUS_THRESHOLD:
            self.speed_bonus = min(self.SPEED_BONUS_MAX, self.speed_bonus + self.SPEED_BONUS_CONTINUOUS_STEP)

    def update(self):
        """更新游戏状态"""
        super().update()

        if self.game_time >= self.game_duration:
            self.end_game()
            return

        base_current_speed = self.base_speed + (self.game_time / self.game_duration) * self.speed_increment
        self.current_speed = base_current_speed * self.speed_penalty * self.speed_bonus

        if self.current_speed < self.base_speed * self.SPEED_MIN_RATIO:
            self.end_game()
            return

        base_spawn_interval = max(1.2, 2.4 - (self.game_time / self.game_duration) * 1.0)
        self.spawn_interval = max(0.75, base_spawn_interval / max(1.0, self.speed_bonus))
        current_time = time.time()
        if current_time - self.last_spawn_time >= self.spawn_interval:
            self.spawn_chinese_char()
            self.last_spawn_time = current_time

        for char in self.falling_chars[:]:
            char.update(self.current_speed)
            if char.landed:
                self.missed += 1
                self.combo = 0
                self._apply_error_penalty()
                self.falling_chars.remove(char)

        self.particle_system.update()

        if self.combo_text:
            self.combo_timer -= 1
            if self.combo_timer <= 0:
                self.combo_text = None

    def render(self, screen):
        """渲染游戏画面"""
        if self.show_keyboard:
            super().render(screen)
        else:
            self.render_background(screen)

        for char in self.falling_chars:
            char.render(screen)

        self.render_game_info(screen)
        self.render_user_input(screen)
        self.particle_system.render(screen)

        if self.combo_text:
            self.combo_text.render(screen)

        if self.mode_subtype == "master":
            self._render_blind_mode_hint(screen)

    def render_background(self, screen):
        """渲染背景"""
        screen.fill(self.config.BACKGROUND_COLOR)

    def _render_blind_mode_hint(self, screen):
        """渲染模式提示"""
        hint_font = load_font(20, font_dir=self.config.FONTS_DIR)
        hint_surface = hint_font.render(self.mode_hint_text, True, self.config.PRIMARY_COLOR)
        hint_rect = hint_surface.get_rect(center=(self.config.SCREEN_WIDTH // 2, 20))
        screen.blit(hint_surface, hint_rect)

    def render_game_info(self, screen):
        """渲染游戏信息"""
        font = load_font(24, font_dir=self.config.FONTS_DIR)

        remaining_time = max(0, int(self.game_duration - self.game_time))
        time_surface = font.render(f"时间: {remaining_time}秒", True, self.config.TEXT_COLOR)
        screen.blit(time_surface, (20, 120))

        combo_surface = font.render(f"连击: {self.combo}", True, self.config.TEXT_COLOR)
        screen.blit(combo_surface, (20, 150))

        missed_surface = font.render(f"漏失: {self.missed}", True, self.config.TEXT_COLOR)
        screen.blit(missed_surface, (20, 180))

        max_combo_surface = font.render(f"最大连击: {self.max_combo}", True, self.config.TEXT_COLOR)
        screen.blit(max_combo_surface, (self.config.SCREEN_WIDTH - 200, 120))

        bonus_percent = max(0, int(round((self.speed_bonus - 1.0) * 100)))
        speed_text = f"速度: {self.current_speed:.1f} (+{bonus_percent}%)"
        if self.speed_penalty <= self.SPEED_MIN_RATIO:
            speed_color = (220, 20, 60)
        elif self.speed_penalty < 1.0:
            speed_color = (255, 140, 0)
        elif bonus_percent > 0:
            speed_color = (16, 185, 129)
        else:
            speed_color = self.config.TEXT_COLOR
        speed_surface = font.render(speed_text, True, speed_color)
        screen.blit(speed_surface, (self.config.SCREEN_WIDTH - 220, 150))

        if self.consecutive_correct >= self.SPEED_BONUS_THRESHOLD:
            status_text = f"连对: {self.consecutive_correct}  继续命中+3%"
            status_color = self.config.SUCCESS_COLOR
        elif self.consecutive_correct > 0:
            status_text = f"连对: {self.consecutive_correct}/{self.SPEED_BONUS_THRESHOLD}"
            status_color = self.config.SUCCESS_COLOR
        elif self.consecutive_errors > 0:
            status_text = f"连错: {self.consecutive_errors}/{self.SPEED_PENALTY_THRESHOLD}"
            status_color = self.config.WARNING_COLOR
        else:
            status_text = "连击准备中"
            status_color = self.config.TEXT_COLOR
        status_surface = font.render(status_text, True, status_color)
        screen.blit(status_surface, (self.config.SCREEN_WIDTH - 260, 180))

    def render_user_input(self, screen):
        """渲染用户输入"""
        hint_font = load_font(24, font_dir=self.config.FONTS_DIR)
        input_font = load_font(36, font_dir=self.config.FONTS_DIR)

        hint_surface = hint_font.render(self.input_prompt, True, self.config.TEXT_COLOR)
        hint_rect = hint_surface.get_rect(center=(self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT - 150))
        screen.blit(hint_surface, hint_rect)

        input_surface = input_font.render(self.user_input, True, self.config.PRIMARY_COLOR)
        input_rect_text = input_surface.get_rect(center=(self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT - 100))
        screen.blit(input_surface, input_rect_text)

        input_rect = input_rect_text.inflate(20, 10)
        pygame.draw.rect(screen, self.config.PRIMARY_COLOR, input_rect, 2, border_radius=5)

        if pygame.time.get_ticks() % 1000 < 500:
            if self.user_input:
                cursor_x = input_rect_text.left + input_font.size(self.user_input)[0]
            else:
                cursor_x = input_rect_text.left
            cursor_y = input_rect_text.top
            cursor_height = input_font.size("Tg")[1]
            pygame.draw.line(
                screen,
                self.config.PRIMARY_COLOR,
                (cursor_x, cursor_y),
                (cursor_x, cursor_y + cursor_height),
                2
            )

    def spawn_chinese_char(self):
        """生成新的下落汉字"""
        char, pinyin = random.choice(list(CHINESE_CHARS.items()))
        x = random.randint(50, self.config.SCREEN_WIDTH - 50)
        chinese_char = FallingChineseChar(
            char,
            pinyin,
            x,
            -20,
            self.current_speed,
            self.config,
            show_pinyin=self.show_pinyin_hint
        )
        self.falling_chars.append(chinese_char)

    def handle_event(self, event):
        """处理游戏事件"""
        if not self.running:
            return

        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_END):
            self.abort_game()
            return

        if event.type == pygame.TEXTINPUT and self.input_mode == "char":
            self._append_text_input(event.text)
            return

        if event.type == pygame.KEYDOWN:
            self.handle_key_down(event.key, getattr(event, "unicode", ""))

    def handle_key_down(self, key, unicode_char=""):
        """处理键盘按下事件，带去抖"""
        now = time.time()
        if self.last_key == key and (now - self.last_key_time) < self.key_debounce_seconds:
            return
        self.last_key = key
        self.last_key_time = now

        if key == pygame.K_BACKSPACE:
            if self.user_input:
                self.user_input = self.user_input[:-1]
        elif key == pygame.K_RETURN:
            if self.user_input:
                self.submit_input()
        elif self.input_mode == "pinyin":
            if unicode_char and unicode_char.isalpha() and len(self.user_input) < self.max_input_length:
                self.user_input += unicode_char.lower()
            elif pygame.K_a <= key <= pygame.K_z and len(self.user_input) < self.max_input_length:
                self.user_input += chr(key - pygame.K_a + ord('a'))

    def _append_text_input(self, text):
        """向输入框追加汉字内容"""
        if not text:
            return
        filtered = ''.join(ch for ch in text if '\u4e00' <= ch <= '\u9fff')
        if not filtered:
            return
        remaining = max(0, self.max_input_length - len(self.user_input))
        if remaining > 0:
            self.user_input += filtered[:remaining]

    def submit_input(self):
        """提交当前输入内容"""
        normalized_input = self.user_input.strip()
        if not normalized_input:
            return

        hit_any = False
        candidates = sorted(self.falling_chars, key=lambda item: item.y, reverse=True)
        for char in candidates:
            if char.check_hit(normalized_input, self.input_mode):
                hit_any = True
                self.consecutive_errors = 0
                self.consecutive_correct += 1
                self._apply_speed_bonus_progression()

                self.correct_count += 1
                self.total_count += 1
                self.combo += 1
                self.max_combo = max(self.max_combo, self.combo)

                base_score = 20
                combo_bonus = int(self.combo * self.config.COMBO_BONUS * 2)
                self.score += base_score + combo_bonus

                self.play_correct_sound()
                self.particle_system.create_explosion(char.x, char.y, char.color)

                if self.combo >= 3:
                    self.show_combo_text(char.x, char.y)

                if char in self.falling_chars:
                    self.falling_chars.remove(char)
                break

        if not hit_any:
            self.total_count += 1
            self.combo = 0
            self._apply_error_penalty()
            self.play_error_sound()

        self.user_input = ""

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

        message = "继续!"
        for threshold, msg in sorted(combo_messages.items(), reverse=True):
            if self.combo >= threshold:
                message = msg
                break

        self.combo_text = Text(
            f"{message} {self.combo}!",
            36,
            (255, 215, 0),
            (x, y - 50)
        )
        self.combo_timer = 30

    def calculate_accuracy(self):
        """计算准确率"""
        super().calculate_accuracy()

    def calculate_score(self):
        """计算得分"""
        base_score = self.score
        combo_reward = int(self.max_combo * 3)
        accuracy_reward = int(self.accuracy * 100)
        self.score = base_score + combo_reward + accuracy_reward

    def get_max_score(self):
        """获取最大可能分数"""
        max_possible_chars = int(self.game_duration / 0.8)
        max_base_score = max_possible_chars * 20
        max_combo_bonus = int(max_possible_chars * 3)
        max_combo_reward = 30 * 3
        max_accuracy_reward = 100
        return max_base_score + max_combo_bonus + max_combo_reward + max_accuracy_reward

    def get_mode_name(self):
        """获取游戏模式名称"""
        if self.mode_subtype == "advanced_pinyin":
            return "高级拼音"
        return "大师模式"
