#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
打字姿势指导模块
提供正确的打字姿势要点和可视化指导
"""

import pygame
from font_loader import load_font


class PostureGuide:
    """打字姿势指导类"""
    
    # 姿势要点
    POSTURE_TIPS = [
        {
            'title': '坐姿',
            'points': [
                '背部挺直，微微后倾',
                '双脚平放在地面上',
                '膝盖与地面保持90度角',
                '肩膀放松，不要耸起'
            ]
        },
        {
            'title': '手臂',
            'points': [
                '上臂与键盘平行或略向下倾斜',
                '前臂与上臂保持90-110度角',
                '手腕轻轻放在键盘边缘或悬空',
                '避免手腕压在键盘上'
            ]
        },
        {
            'title': '手指',
            'points': [
                '手指自然弯曲，呈现弧形',
                '指尖轻触按键，不要用力敲击',
                '左手小指负责1、Q、A、Z键',
                '右手小指负责0、P、；、/键'
            ]
        },
        {
            'title': '基准键位',
            'points': [
                '左手食指放在F键上（F键有凸起指示）',
                '右手食指放在J键上（J键有凸起指示）',
                '其他手指依次放在相邻键位上',
                '拇指自然放在空格键上'
            ]
        }
    ]
    
    def __init__(self, config):
        """
        初始化姿势指导
        
        参数:
        - config: 游戏配置
        """
        self.config = config
        self.current_page = 0
        self.total_pages = len(self.POSTURE_TIPS)
        
        # 字体
        self.title_font = load_font(32, font_dir=config.FONTS_DIR)
        self.content_font = load_font(20, font_dir=config.FONTS_DIR)
        self.hint_font = load_font(16, font_dir=config.FONTS_DIR)
        
        # 颜色
        self.primary_color = config.PRIMARY_COLOR
        self.text_color = config.TEXT_COLOR
        self.text_secondary = config.TEXT_SECONDARY
        self.bg_color = config.CARD_BG_COLOR
        
        # 按钮区域
        self.next_button_rect = None
        self.prev_button_rect = None
        self.skip_button_rect = None
    
    def next_page(self):
        """下一页"""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            return True
        return False
    
    def prev_page(self):
        """上一页"""
        if self.current_page > 0:
            self.current_page -= 1
            return True
        return False
    
    def is_last_page(self):
        """是否最后一页"""
        return self.current_page == self.total_pages - 1
    
    def render(self, screen):
        """
        渲染姿势指导界面
        
        参数:
        - screen: 游戏屏幕
        
        返回:
        - 按钮区域字典
        """
        # 居中位置
        center_x = self.config.SCREEN_WIDTH // 2
        center_y = self.config.SCREEN_HEIGHT // 2
        
        # 卡片尺寸
        card_width = 600
        card_height = 420
        card_x = center_x - card_width // 2
        card_y = center_y - card_height // 2
        
        # 绘制遮罩背景
        overlay = pygame.Surface((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        
        # 绘制卡片背景
        card_surface = pygame.Surface((card_width, card_height), pygame.SRCALPHA)
        pygame.draw.rect(card_surface, (*self.bg_color, 250), 
                       (0, 0, card_width, card_height), border_radius=16)
        pygame.draw.rect(card_surface, self.primary_color,
                       (0, 0, card_width, card_height), 2, border_radius=16)
        screen.blit(card_surface, card_rect.topleft if 'card_rect' in dir() else (card_x, card_y))
        
        # 获取当前页面内容
        tip = self.POSTURE_TIPS[self.current_page]
        
        # 绘制标题
        title_y = card_y + 40
        title_text = f"{tip['title']}"
        title_surface = self.title_font.render(title_text, True, self.primary_color)
        title_rect = title_surface.get_rect(center=(center_x, title_y))
        screen.blit(title_surface, title_rect)
        
        # 绘制分隔线
        line_y = title_y + 45
        pygame.draw.line(screen, (80, 90, 110), (card_x + 40, line_y), 
                        (card_x + card_width - 40, line_y), 1)
        
        # 绘制要点列表
        points_y = line_y + 25
        line_height = 40
        for i, point in enumerate(tip['points']):
            # 绘制圆点
            dot_x = card_x + 60
            dot_y = points_y + i * line_height + 8
            pygame.draw.circle(screen, self.primary_color, (dot_x, dot_y), 5)
            
            # 绘制文字
            point_surface = self.content_font.render(point, True, self.text_color)
            screen.blit(point_surface, (dot_x + 20, points_y + i * line_height))
        
        # 绘制页码指示器
        dots_y = card_y + card_height - 70
        dot_spacing = 16
        total_dots_width = (self.total_pages - 1) * dot_spacing
        dots_start_x = center_x - total_dots_width // 2
        
        for i in range(self.total_pages):
            dot_x = dots_start_x + i * dot_spacing
            color = self.primary_color if i == self.current_page else self.text_secondary
            pygame.draw.circle(screen, color, (dot_x, dots_y), 6)
        
        # 绘制按钮
        button_width = 110
        button_height = 40
        button_y = card_y + card_height - 50
        
        # 上一步按钮
        self.prev_button_rect = None
        if self.current_page > 0:
            self.prev_button_rect = pygame.Rect(card_x + 40, button_y, button_width, button_height)
            self._draw_button(screen, self.prev_button_rect, "上一步", False)
        
        # 下一步/完成按钮
        is_last = self.is_last_page()
        btn_text = "开始练习" if is_last else "下一步"
        btn_x = card_x + card_width - button_width - 40
        self.next_button_rect = pygame.Rect(btn_x, button_y, button_width, button_height)
        self._draw_button(screen, self.next_button_rect, btn_text, True)
        
        # 跳过按钮
        skip_text = "跳过"
        skip_surface = self.hint_font.render(skip_text, True, self.text_secondary)
        skip_rect = skip_surface.get_rect(center=(center_x, button_y + 8))
        self.skip_button_rect = pygame.Rect(skip_rect.x - 12, skip_rect.y - 6, skip_rect.width + 24, skip_rect.height + 12)
        screen.blit(skip_surface, skip_rect)
        
        return {
            'next': self.next_button_rect,
            'prev': self.prev_button_rect,
            'skip': self.skip_button_rect
        }
    
    def _draw_button(self, screen, rect, text, is_primary):
        """绘制按钮"""
        bg_color = self.primary_color if is_primary else (55, 65, 75)
        text_color = (255, 255, 255) if is_primary else self.text_color
        
        pygame.draw.rect(screen, bg_color, rect, border_radius=8)
        
        text_surface = self.content_font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_click(self, pos):
        """处理点击事件"""
        if self.next_button_rect and self.next_button_rect.collidepoint(pos):
            return 'next'
        if self.prev_button_rect and self.prev_button_rect.collidepoint(pos):
            return 'prev'
        if self.skip_button_rect and self.skip_button_rect.collidepoint(pos):
            return 'skip'
        return None
