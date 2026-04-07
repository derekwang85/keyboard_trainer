#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
切割效果，用于高级模式中击中字母时的特效
"""

import pygame
import random
import math

class CutEffect:
    """切割效果类"""
    
    def __init__(self, x, y, color, config):
        """
        初始化切割效果
        
        参数:
        - x: 切割中心x坐标
        - y: 切割中心y坐标
        - color: 切割线颜色
        - config: 游戏配置
        """
        self.x = x
        self.y = y
        self.color = color
        self.config = config
        
        # 切割线角度
        self.angle = random.uniform(0, math.pi)
        
        # 切割线长度
        self.length = 100
        
        # 切割线宽度
        self.width = 4
        
        # 切割线持续时间
        self.duration = 15
        self.max_duration = self.duration
        
        # 碎片粒子
        self.particles = []
        self.create_particles()
        
        # 效果是否完成
        self.finished = False
    
    def create_particles(self):
        """创建切割碎片粒子"""
        # 创建左侧碎片
        for _ in range(10):
            # 计算碎片位置（左侧）
            angle = self.angle + math.pi/2
            distance = random.uniform(0, self.length/2)
            x = self.x + math.cos(angle) * distance
            y = self.y + math.sin(angle) * distance
            
            # 创建粒子
            particle = {
                'x': x,
                'y': y,
                'vx': math.cos(angle - math.pi/4) * random.uniform(2, 5),
                'vy': math.sin(angle - math.pi/4) * random.uniform(2, 5),
                'size': random.randint(3, 8),
                'color': self.color,
                'life': random.randint(15, 30),
                'max_life': random.randint(15, 30),
                'alpha': 255
            }
            self.particles.append(particle)
        
        # 创建右侧碎片
        for _ in range(10):
            # 计算碎片位置（右侧）
            angle = self.angle - math.pi/2
            distance = random.uniform(0, self.length/2)
            x = self.x + math.cos(angle) * distance
            y = self.y + math.sin(angle) * distance
            
            # 创建粒子
            particle = {
                'x': x,
                'y': y,
                'vx': math.cos(angle + math.pi/4) * random.uniform(2, 5),
                'vy': math.sin(angle + math.pi/4) * random.uniform(2, 5),
                'size': random.randint(3, 8),
                'color': self.color,
                'life': random.randint(15, 30),
                'max_life': random.randint(15, 30),
                'alpha': 255
            }
            self.particles.append(particle)
    
    def update(self):
        """更新切割效果"""
        # 更新持续时间
        self.duration -= 1
        
        # 更新碎片粒子
        for particle in self.particles[:]:
            # 更新位置
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # 减速
            particle['vx'] *= 0.95
            particle['vy'] *= 0.95
            
            # 增加重力效果
            particle['vy'] += 0.2
            
            # 更新生命周期
            particle['life'] -= 1
            
            # 更新透明度
            particle['alpha'] = int(255 * (particle['life'] / particle['max_life']))
            
            # 移除死亡的粒子
            if particle['life'] <= 0:
                self.particles.remove(particle)
        
        # 检查效果是否完成
        if self.duration <= 0 and len(self.particles) == 0:
            self.finished = True
    
    def render(self, screen):
        """渲染切割效果"""
        # 渲染切割线
        if self.duration > 0:
            # 计算切割线端点
            start_x = self.x - math.cos(self.angle) * self.length / 2
            start_y = self.y - math.sin(self.angle) * self.length / 2
            end_x = self.x + math.cos(self.angle) * self.length / 2
            end_y = self.y + math.sin(self.angle) * self.length / 2
            
            # 计算透明度
            alpha = int(255 * (self.duration / self.max_duration))
            
            # 创建临时表面
            surface = pygame.Surface((self.length, self.width * 2), pygame.SRCALPHA)
            
            # 绘制切割线
            pygame.draw.line(
                surface,
                (*self.color, alpha),
                (0, self.width),
                (self.length, self.width),
                self.width
            )
            
            # 旋转表面
            rotated_surface = pygame.transform.rotate(surface, math.degrees(self.angle))
            
            # 绘制到屏幕
            screen.blit(
                rotated_surface,
                (
                    start_x - rotated_surface.get_width() / 2,
                    start_y - rotated_surface.get_height() / 2
                )
            )
        
        # 渲染碎片粒子
        for particle in self.particles:
            # 创建临时表面
            surface = pygame.Surface(
                (particle['size'] * 2, particle['size'] * 2),
                pygame.SRCALPHA
            )
            
            # 绘制粒子
            pygame.draw.rect(
                surface,
                (*particle['color'], particle['alpha']),
                (0, 0, particle['size'] * 2, particle['size'] * 2)
            )
            
            # 绘制到屏幕
            screen.blit(
                surface,
                (
                    particle['x'] - particle['size'],
                    particle['y'] - particle['size']
                )
            )