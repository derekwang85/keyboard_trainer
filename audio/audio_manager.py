#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
音频管理器，负责管理游戏音效和音乐
"""

import pygame
import os
import random

class AudioManager:
    """音频管理器类"""
    
    def __init__(self, config):
        """
        初始化音频管理器
        
        参数:
        - config: 游戏配置
        """
        self.config = config
        
        # 音效字典
        self.sounds = {}
        
        # 音乐字典
        self.music = {}
        
        # 音量设置
        self.sound_volume = config.SOUND_VOLUME
        self.music_volume = config.MUSIC_VOLUME
        
        # 音效开关
        self.sound_enabled = True
        
        # 加载音效
        self.load_sounds()
    
    def load_sounds(self):
        """加载音效文件"""
        # 音效文件路径
        sound_files = {
            'correct': 'correct.wav',
            'error': 'error.wav',
            'encouragement': 'encouragement.wav',
            'game_over': 'game_over.wav',
            'new_record': 'new_record.wav',
            'button_click': 'button_click.wav',
            'level_up': 'level_up.wav',
            'combo': 'combo.wav'
        }
        
        # 尝试加载音效文件
        for name, filename in sound_files.items():
            try:
                # 构建音效文件路径
                sound_path = os.path.join(self.config.SOUNDS_DIR, filename)
                
                # 检查文件是否存在
                if os.path.exists(sound_path):
                    # 加载音效
                    sound = pygame.mixer.Sound(sound_path)
                    sound.set_volume(self.sound_volume)
                    self.sounds[name] = sound
                else:
                    # 文件不存在，创建一个空的音效对象
                    # 这是一个模拟，实际上不会产生声音
                    self.sounds[name] = None
                    print(f"警告: 音效文件 '{sound_path}' 不存在")
            except Exception as e:
                # 加载失败，创建一个空的音效对象
                self.sounds[name] = None
                print(f"警告: 加载音效 '{name}' 失败: {e}")
    
    def play_sound(self, sound_name):
        """
        播放音效
        
        参数:
        - sound_name: 音效名称
        """
        # 检查音效是否启用
        if not self.sound_enabled:
            return
        
        # 检查音效是否存在
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                # 播放音效
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"警告: 播放音效 '{sound_name}' 失败: {e}")
    
    def stop_sound(self, sound_name):
        """
        停止音效
        
        参数:
        - sound_name: 音效名称
        """
        # 检查音效是否存在
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                # 停止音效
                self.sounds[sound_name].stop()
            except Exception as e:
                print(f"警告: 停止音效 '{sound_name}' 失败: {e}")
    
    def play_music(self, music_name, loop=True):
        """
        播放音乐
        
        参数:
        - music_name: 音乐名称
        - loop: 是否循环播放
        """
        # 检查音效是否启用
        if not self.sound_enabled:
            return
        
        # 检查音乐是否存在
        if music_name in self.music and self.music[music_name]:
            try:
                # 停止当前音乐
                pygame.mixer.music.stop()
                
                # 设置音乐
                pygame.mixer.music.load(self.music[music_name])
                pygame.mixer.music.set_volume(self.music_volume)
                
                # 播放音乐
                if loop:
                    pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.play(0)
            except Exception as e:
                print(f"警告: 播放音乐 '{music_name}' 失败: {e}")
    
    def stop_music(self):
        """停止音乐"""
        try:
            pygame.mixer.music.stop()
        except Exception as e:
            print(f"警告: 停止音乐失败: {e}")
    
    def set_volume(self, volume):
        """
        设置音量
        
        参数:
        - volume: 音量值 (0.0 - 1.0)
        """
        # 限制音量范围
        volume = max(0.0, min(1.0, volume))
        
        # 更新音量设置
        self.sound_volume = volume
        self.music_volume = volume
        
        # 更新音效音量
        for sound in self.sounds.values():
            if sound:
                sound.set_volume(volume)
        
        # 更新音乐音量
        pygame.mixer.music.set_volume(volume)
    
    def set_sound_enabled(self, enabled):
        """
        设置音效开关
        
        参数:
        - enabled: 是否启用音效
        """
        self.sound_enabled = enabled
        
        # 如果禁用音效，停止所有声音
        if not enabled:
            # 停止所有音效
            for sound_name in self.sounds:
                self.stop_sound(sound_name)
            
            # 停止音乐
            self.stop_music()
    
    def play_random_encouragement(self):
        """播放随机鼓励音效"""
        # 鼓励音效列表
        encouragement_sounds = [
            'encouragement',
            'level_up',
            'combo'
        ]
        
        # 随机选择一个鼓励音效
        sound_name = random.choice(encouragement_sounds)
        self.play_sound(sound_name)