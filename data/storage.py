#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
存储管理器，负责管理游戏数据的保存和读取
"""

import json
import os
import time

class StorageManager:
    """存储管理器类"""
    
    def __init__(self, config):
        """
        初始化存储管理器
        
        参数:
        - config: 游戏配置
        """
        self.config = config
        
        # 存档文件路径
        self.save_file = config.SAVE_FILE
        
        # 确保数据目录存在
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """确保数据目录存在"""
        data_dir = self.config.DATA_DIR
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def load_data(self):
        """
        加载游戏数据
        
        返回:
        - 游戏数据字典
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(self.save_file):
                # 文件不存在，返回默认数据
                return self.get_default_data()
            
            # 读取文件
            with open(self.save_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 确保数据结构完整
            return self.ensure_data_structure(data)
        
        except Exception as e:
            print(f"警告: 加载游戏数据失败: {e}")
            # 返回默认数据
            return self.get_default_data()
    
    def save_data(self, data):
        """
        保存游戏数据
        
        参数:
        - data: 游戏数据字典
        """
        try:
            # 确保数据结构完整
            data = self.ensure_data_structure(data)
            
            # 更新最后游戏时间
            data['last_played'] = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # 写入文件
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        
        except Exception as e:
            print(f"警告: 保存游戏数据失败: {e}")
            return False
    
    def get_default_data(self):
        """
        获取默认游戏数据
        
        返回:
        - 默认游戏数据字典
        """
        return {
            'player_name': '玩家',
            'total_sessions': 0,
            'last_played': time.strftime("%Y-%m-%d %H:%M:%S"),
            'modes': {
                'beginner': {
                    'best_score': 0,
                    'best_accuracy': 0.0,
                    'stars': 0,
                    'record_holder': '玩家',
                    'total_sessions': 0,
                    'recent_results': []
                },
                'intermediate': {
                    'levels': {
                        'words': {
                            'best_score': 0,
                            'best_accuracy': 0.0,
                            'best_time': float('inf'),
                            'best_speed': 0,
                            'stars': 0,
                            'record_holder': '玩家',
                            'total_sessions': 0
                        },
                        'phrases': {
                            'best_score': 0,
                            'best_accuracy': 0.0,
                            'best_time': float('inf'),
                            'best_speed': 0,
                            'stars': 0,
                            'record_holder': '玩家',
                            'total_sessions': 0
                        },
                        'sentences': {
                            'best_score': 0,
                            'best_accuracy': 0.0,
                            'best_time': float('inf'),
                            'best_speed': 0,
                            'stars': 0,
                            'record_holder': '玩家',
                            'total_sessions': 0
                        }
                    },
                    'total_sessions': 0,
                    'recent_results': []
                },
                'advanced': {
                    'best_score': 0,
                    'best_accuracy': 0.0,
                    'max_combo': 0,
                    'stars': 0,
                    'record_holder': '玩家',
                    'total_sessions': 0,
                    'recent_results': []
                },
                'master': {
                    'best_score': 0,
                    'best_accuracy': 0.0,
                    'max_combo': 0,
                    'stars': 0,
                    'record_holder': '玩家',
                    'total_sessions': 0,
                    'recent_results': []
                }
            }
        }
    
    def ensure_data_structure(self, data):
        """
        确保数据结构完整
        
        参数:
        - data: 游戏数据字典
        
        返回:
        - 完整的游戏数据字典
        """
        # 获取默认数据结构
        default_data = self.get_default_data()
        
        # 确保顶级键存在
        for key in default_data:
            if key not in data:
                data[key] = default_data[key]
        
        # 确保模式数据结构完整
        for mode in default_data['modes']:
            if mode not in data['modes']:
                data['modes'][mode] = default_data['modes'][mode]
            else:
                # 确保模式内的键存在
                for key in default_data['modes'][mode]:
                    if key not in data['modes'][mode]:
                        data['modes'][mode][key] = default_data['modes'][mode][key]
        
        # 确保中级模式的级别数据结构完整
        if 'intermediate' in data['modes']:
            if 'levels' not in data['modes']['intermediate']:
                data['modes']['intermediate']['levels'] = default_data['modes']['intermediate']['levels']
            else:
                for level in default_data['modes']['intermediate']['levels']:
                    if level not in data['modes']['intermediate']['levels']:
                        data['modes']['intermediate']['levels'][level] = default_data['modes']['intermediate']['levels'][level]
                    else:
                        # 确保级别内的键存在
                        for key in default_data['modes']['intermediate']['levels'][level]:
                            if key not in data['modes']['intermediate']['levels'][level]:
                                data['modes']['intermediate']['levels'][level][key] = default_data['modes']['intermediate']['levels'][level][key]
        
        return data
    
    def update_record(self, mode, level=None, record=None):
        """
        更新游戏记录
        
        参数:
        - mode: 游戏模式
        - level: 游戏级别（仅中级模式使用）
        - record: 记录字典
        
        返回:
        - 是否创造了新纪录
        """
        # 加载当前数据
        data = self.load_data()
        
        # 标记是否创造了新纪录
        is_new_record = False
        
        # 更新总游戏次数
        data['total_sessions'] += 1
        
        # 根据模式更新记录
        if mode == 'intermediate' and level:
            # 中级模式
            if level in data['modes']['intermediate']['levels']:
                level_data = data['modes']['intermediate']['levels'][level]
                
                # 更新级别游戏次数
                level_data['total_sessions'] = level_data.get('total_sessions', 0) + 1
                
                # 更新中级模式总游戏次数
                data['modes']['intermediate']['total_sessions'] = data['modes']['intermediate'].get('total_sessions', 0) + 1
                
                # 更新最佳分数
                if record and 'score' in record:
                    if record['score'] > level_data.get('best_score', 0):
                        level_data['best_score'] = record['score']
                        level_data['record_holder'] = data.get('player_name', '玩家')
                        is_new_record = True
                
                # 更新最佳准确率
                if record and 'accuracy' in record:
                    if record['accuracy'] > level_data.get('best_accuracy', 0):
                        level_data['best_accuracy'] = record['accuracy']
                
                # 更新最佳时间
                if record and 'time' in record:
                    if record['time'] < level_data.get('best_time', float('inf')):
                        level_data['best_time'] = record['time']
                
                # 更新最佳速度
                if record and 'speed' in record:
                    if record['speed'] > level_data.get('best_speed', 0):
                        level_data['best_speed'] = record['speed']
                
                # 更新星级
                if record and 'stars' in record:
                    if record['stars'] > level_data.get('stars', 0):
                        level_data['stars'] = record['stars']
                
                # 添加到最近结果
                if record:
                    if 'recent_results' not in data['modes']['intermediate']:
                        data['modes']['intermediate']['recent_results'] = []
                    
                    # 添加当前结果
                    result = {
                        'level': level,
                        'score': record.get('score', 0),
                        'accuracy': record.get('accuracy', 0.0),
                        'time': record.get('time', 0.0),
                        'speed': record.get('speed', 0),
                        'stars': record.get('stars', 0),
                        'date': time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    data['modes']['intermediate']['recent_results'].append(result)
                    
                    # 只保留最近10条记录
                    if len(data['modes']['intermediate']['recent_results']) > 10:
                        data['modes']['intermediate']['recent_results'] = data['modes']['intermediate']['recent_results'][-10:]
        else:
            # 其他模式
            if mode in data['modes']:
                mode_data = data['modes'][mode]
                
                # 更新模式游戏次数
                mode_data['total_sessions'] = mode_data.get('total_sessions', 0) + 1
                
                # 更新最佳分数
                if record and 'score' in record:
                    if record['score'] > mode_data.get('best_score', 0):
                        mode_data['best_score'] = record['score']
                        mode_data['record_holder'] = data.get('player_name', '玩家')
                        is_new_record = True
                
                # 更新最佳准确率
                if record and 'accuracy' in record:
                    if record['accuracy'] > mode_data.get('best_accuracy', 0):
                        mode_data['best_accuracy'] = record['accuracy']
                
                # 更新最大连击
                if record and 'max_combo' in record:
                    if record['max_combo'] > mode_data.get('max_combo', 0):
                        mode_data['max_combo'] = record['max_combo']
                
                # 更新星级
                if record and 'stars' in record:
                    if record['stars'] > mode_data.get('stars', 0):
                        mode_data['stars'] = record['stars']
                
                # 添加到最近结果
                if record:
                    if 'recent_results' not in mode_data:
                        mode_data['recent_results'] = []
                    
                    # 添加当前结果
                    result = {
                        'score': record.get('score', 0),
                        'accuracy': record.get('accuracy', 0.0),
                        'max_combo': record.get('max_combo', 0),
                        'stars': record.get('stars', 0),
                        'date': time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    mode_data['recent_results'].append(result)
                    
                    # 只保留最近10条记录
                    if len(mode_data['recent_results']) > 10:
                        mode_data['recent_results'] = mode_data['recent_results'][-10:]
        
        # 保存更新后的数据
        self.save_data(data)
        
        return is_new_record
    
    def get_best_record(self, mode, level=None):
        """
        获取最佳记录
        
        参数:
        - mode: 游戏模式
        - level: 游戏级别（仅中级模式使用）
        
        返回:
        - 最佳记录字典
        """
        # 加载数据
        data = self.load_data()
        
        # 根据模式获取最佳记录
        if mode == 'intermediate' and level:
            # 中级模式
            if level in data['modes']['intermediate']['levels']:
                return data['modes']['intermediate']['levels'][level]
        else:
            # 其他模式
            if mode in data['modes']:
                return data['modes'][mode]
        
        return None
    
    def set_player_name(self, name):
        """
        设置玩家名称
        
        参数:
        - name: 玩家名称
        """
        # 加载数据
        data = self.load_data()
        
        # 更新玩家名称
        data['player_name'] = name
        
        # 保存更新后的数据
        self.save_data(data)