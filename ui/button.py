#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
按钮组件
"""

import pygame
from font_loader import load_font

class Button:
    """按钮类"""
    
    def __init__(self, text, width, height, pos, bg_color, text_color, font_size, action=None, font_dir=None):
        """
        初始化按钮
        
        参数:
        - text: 按钮文本
        - width: 按钮宽度
        - height: 按钮高度
        - pos: 按钮位置 (x, y)
        - bg_color: 按钮背景颜色
        - text_color: 按钮文本颜色
        - font_size: 文本字体大小
        - action: 按钮点击时执行的函数
        - font_dir: 字体目录
        """
        self.text = text
        self.width = width
        self.height = height
        self.pos = pos
        self.bg_color = bg_color
        self.text_color = text_color
        self.font_size = font_size
        self.action = action
        
        # 按钮是否被按下
        self.is_pressed = False
        
        # 按钮是否被悬停
        self.is_hovered = False
        
        # 创建按钮矩形
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = pos
        
        # 加载字体 - 使用统一的字体加载器
        self.font = load_font(font_size, font_dir=font_dir)
        
        # 渲染文本
        self.render_text()
    
    def render_text(self):
        """渲染按钮文本"""
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=(self.width // 2, self.height // 2))
    
    def set_text(self, text):
        """设置按钮文本"""
        self.text = text
        self.render_text()
    
    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键点击
                if self.rect.collidepoint(event.pos):
                    self.is_pressed = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # 左键释放
                if self.is_pressed and self.rect.collidepoint(event.pos):
                    # 执行按钮动作
                    if self.action:
                        self.action()
                self.is_pressed = False
        
        elif event.type == pygame.MOUSEMOTION:
            # 检查鼠标是否悬停在按钮上
            self.is_hovered = self.rect.collidepoint(event.pos)
    
    def render(self, screen):
        """渲染按钮"""
        # 根据按钮状态选择颜色
        color = self.bg_color
        if self.is_pressed:
            # 按下状态，颜色变暗
            color = tuple(max(0, c - 30) for c in self.bg_color)
        elif self.is_hovered:
            # 悬停状态，颜色变亮
            color = tuple(min(255, c + 20) for c in self.bg_color)
        
        # 绘制按钮背景
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        
        # 绘制按钮边框
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=10)
        
        # 绘制按钮文本
        screen.blit(self.text_surface, (self.rect.x + self.text_rect.x, self.rect.y + self.text_rect.y))