#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
存储管理器，负责管理游戏数据的保存和读取
"""

import copy
import json
import os
import time


class StorageManager:
    """存储管理器类"""

    BLACKLISTED_USERNAMES = {"admin", "tester"}
    MODE_ALIASES = {
        "基础模式": ("beginner", None),
        "高级模式": ("advanced", None),
        "大师模式": ("master", None),
        "高级拼音": ("advanced_pinyin", None),
        "intermediate_words": ("intermediate", "words"),
        "intermediate_phrases": ("intermediate", "phrases"),
        "intermediate_sentences": ("intermediate", "sentences"),
        "中级模式 - 单词": ("intermediate", "words"),
        "中级模式 - 短语": ("intermediate", "phrases"),
        "中级模式 - 句子": ("intermediate", "sentences"),
        "中级模式-单词": ("intermediate", "words"),
        "中级模式-短语": ("intermediate", "phrases"),
        "中级模式-句子": ("intermediate", "sentences"),
    }

    def __init__(self, config):
        self.config = config
        self.save_file = config.SAVE_FILE
        self.ensure_data_directory()

    def ensure_data_directory(self):
        """确保数据目录存在"""
        data_dir = self.config.DATA_DIR
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def load_data(self):
        """加载游戏数据"""
        try:
            if not os.path.exists(self.save_file):
                return self.get_default_data()

            with open(self.save_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return self.ensure_data_structure(data)
        except Exception as e:
            print(f"警告: 加载游戏数据失败: {e}")
            return self.get_default_data()

    def save_data(self, data):
        """保存游戏数据"""
        try:
            data = self.ensure_data_structure(data)
            data['last_played'] = time.strftime("%Y-%m-%d %H:%M:%S")
            data = self._sanitize_for_json(data)

            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"警告: 保存游戏数据失败: {e}")
            return False

    def _sanitize_for_json(self, data):
        """处理数据中的无穷值，转换为可序列化的值"""
        if isinstance(data, dict):
            return {k: self._sanitize_for_json(v) for k, v in data.items()}
        if isinstance(data, list):
            return [self._sanitize_for_json(item) for item in data]
        if isinstance(data, float):
            if data == float('inf'):
                return 999999
            if data == float('-inf'):
                return 0
        return data

    def get_default_data(self):
        """获取默认游戏数据"""
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
                    'recent_results': [],
                    'leaderboard': []
                },
                'intermediate': {
                    'levels': {
                        'words': {
                            'best_score': 0,
                            'best_accuracy': 0.0,
                            'best_time': 999999,
                            'best_speed': 0,
                            'stars': 0,
                            'record_holder': '玩家',
                            'total_sessions': 0,
                            'recent_results': [],
                            'leaderboard': []
                        },
                        'phrases': {
                            'best_score': 0,
                            'best_accuracy': 0.0,
                            'best_time': 999999,
                            'best_speed': 0,
                            'stars': 0,
                            'record_holder': '玩家',
                            'total_sessions': 0,
                            'recent_results': [],
                            'leaderboard': []
                        },
                        'sentences': {
                            'best_score': 0,
                            'best_accuracy': 0.0,
                            'best_time': 999999,
                            'best_speed': 0,
                            'stars': 0,
                            'record_holder': '玩家',
                            'total_sessions': 0,
                            'recent_results': [],
                            'leaderboard': []
                        }
                    },
                    'total_sessions': 0,
                    'recent_results': [],
                    'leaderboard': []
                },
                'advanced': {
                    'best_score': 0,
                    'best_accuracy': 0.0,
                    'max_combo': 0,
                    'stars': 0,
                    'record_holder': '玩家',
                    'total_sessions': 0,
                    'recent_results': [],
                    'leaderboard': []
                },
                'master': {
                    'best_score': 0,
                    'best_accuracy': 0.0,
                    'max_combo': 0,
                    'stars': 0,
                    'record_holder': '玩家',
                    'total_sessions': 0,
                    'recent_results': [],
                    'leaderboard': []
                },
                'advanced_pinyin': {
                    'best_score': 0,
                    'best_accuracy': 0.0,
                    'max_combo': 0,
                    'stars': 0,
                    'record_holder': '玩家',
                    'total_sessions': 0,
                    'recent_results': [],
                    'leaderboard': []
                }
            }
        }

    def ensure_data_structure(self, data):
        """确保数据结构完整，并迁移旧存档"""
        if not isinstance(data, dict):
            return self.get_default_data()

        default_data = self.get_default_data()

        if not isinstance(data.get('modes'), dict):
            data['modes'] = {}

        for key in ('player_name', 'total_sessions', 'last_played'):
            if key not in data:
                data[key] = copy.deepcopy(default_data[key])

        for mode, mode_default in default_data['modes'].items():
            if mode not in data['modes'] or not isinstance(data['modes'][mode], dict):
                data['modes'][mode] = copy.deepcopy(mode_default)
            else:
                self._merge_missing_keys(data['modes'][mode], mode_default)

        self._migrate_legacy_modes(data)
        self._normalize_all_mode_data(data)
        return data

    def _merge_missing_keys(self, target, template):
        """把模板中的缺失键补到目标结构里"""
        for key, value in template.items():
            if key not in target:
                target[key] = copy.deepcopy(value)
            elif isinstance(value, dict) and isinstance(target.get(key), dict):
                self._merge_missing_keys(target[key], value)

    def _normalize_mode_identifier(self, mode, level=None):
        """统一模式标识"""
        mode = (mode or 'beginner').strip()
        level = level.strip() if isinstance(level, str) else level

        if mode.startswith('intermediate_') and not level:
            level = mode.split('intermediate_', 1)[1]
            mode = 'intermediate'

        alias = self.MODE_ALIASES.get(mode)
        if alias:
            mode, alias_level = alias
            if not level:
                level = alias_level

        if mode == 'intermediate' and level not in ('words', 'phrases', 'sentences'):
            level = 'words'

        return mode, level

    def _get_mode_bucket(self, data, mode, level=None):
        """获取规范化后的模式数据桶"""
        mode, level = self._normalize_mode_identifier(mode, level)
        default_modes = self.get_default_data()['modes']

        if mode == 'intermediate':
            intermediate_bucket = data['modes'].setdefault('intermediate', copy.deepcopy(default_modes['intermediate']))
            self._merge_missing_keys(intermediate_bucket, default_modes['intermediate'])
            if level:
                level_bucket = intermediate_bucket['levels'].setdefault(level, copy.deepcopy(default_modes['intermediate']['levels'][level]))
                self._merge_missing_keys(level_bucket, default_modes['intermediate']['levels'][level])
                return level_bucket
            return intermediate_bucket

        bucket = data['modes'].setdefault(mode, copy.deepcopy(default_modes.get(mode, {
            'best_score': 0,
            'best_accuracy': 0.0,
            'stars': 0,
            'record_holder': '玩家',
            'total_sessions': 0,
            'recent_results': [],
            'leaderboard': []
        })))
        self._merge_missing_keys(bucket, default_modes.get(mode, {
            'best_score': 0,
            'best_accuracy': 0.0,
            'stars': 0,
            'record_holder': '玩家',
            'total_sessions': 0,
            'recent_results': [],
            'leaderboard': []
        }))
        return bucket

    def _merge_bucket_data(self, target, source):
        """合并旧数据桶到新数据桶"""
        if not isinstance(source, dict):
            return

        numeric_max_fields = ('best_score', 'best_accuracy', 'best_speed', 'max_combo', 'stars')
        for field in numeric_max_fields:
            target[field] = max(target.get(field, 0), source.get(field, 0))

        source_best_time = source.get('best_time', 999999)
        if 'best_time' in target:
            target['best_time'] = min(target.get('best_time', 999999), source_best_time)

        target['total_sessions'] = max(target.get('total_sessions', 0), source.get('total_sessions', 0))

        if source.get('best_score', 0) >= target.get('best_score', 0):
            source_holder = source.get('record_holder')
            if source_holder:
                target['record_holder'] = source_holder

        target['recent_results'] = self._normalize_recent_results(
            target.get('recent_results', []) + source.get('recent_results', [])
        )
        target['leaderboard'] = self._normalize_leaderboard(
            target.get('leaderboard', []) + source.get('leaderboard', [])
        )

    def _migrate_legacy_modes(self, data):
        """迁移旧版模式键和错误写入的排行榜路径"""
        for source_key in list(data.keys()):
            alias = self.MODE_ALIASES.get(source_key)
            if not alias:
                continue
            mode, level = alias
            source_bucket = data.pop(source_key, None)
            target_bucket = self._get_mode_bucket(data, mode, level)
            self._merge_bucket_data(target_bucket, source_bucket)

        for source_key in list(data['modes'].keys()):
            alias = self.MODE_ALIASES.get(source_key)
            if not alias:
                continue
            mode, level = alias
            source_bucket = data['modes'].pop(source_key, None)
            target_bucket = self._get_mode_bucket(data, mode, level)
            self._merge_bucket_data(target_bucket, source_bucket)

    def _normalize_recent_results(self, results):
        """规范 recent_results 结构"""
        if not isinstance(results, list):
            return []

        normalized = []
        for result in results:
            if isinstance(result, dict):
                normalized.append(result)
        return normalized[-10:]

    def _normalize_username(self, username):
        """规范用户名"""
        if username is None:
            return ''
        return str(username).strip()

    def _is_blacklisted_username(self, username):
        """检查用户名是否为黑名单"""
        normalized = self._normalize_username(username)
        return normalized.lower() in self.BLACKLISTED_USERNAMES

    def _normalize_leaderboard(self, leaderboard):
        """清理、去重并排序排行榜"""
        if not isinstance(leaderboard, list):
            return []

        deduped = []
        seen = set()
        for entry in leaderboard:
            if not isinstance(entry, dict):
                continue

            username = self._normalize_username(entry.get('username', ''))
            if not username or self._is_blacklisted_username(username):
                continue

            score = int(entry.get('score', 0))
            date = str(entry.get('date', ''))
            dedupe_key = (username.lower(), score, date)
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)
            deduped.append({
                'username': username,
                'score': score,
                'date': date
            })

        deduped.sort(key=lambda item: (item.get('score', 0), item.get('date', '')), reverse=True)
        return deduped[:10]

    def _normalize_all_mode_data(self, data):
        """统一清理所有模式数据"""
        for mode_key in ('beginner', 'advanced', 'master', 'advanced_pinyin'):
            bucket = self._get_mode_bucket(data, mode_key)
            bucket['recent_results'] = self._normalize_recent_results(bucket.get('recent_results', []))
            bucket['leaderboard'] = self._normalize_leaderboard(bucket.get('leaderboard', []))

        intermediate_bucket = self._get_mode_bucket(data, 'intermediate')
        intermediate_bucket['recent_results'] = self._normalize_recent_results(intermediate_bucket.get('recent_results', []))
        intermediate_bucket['leaderboard'] = self._normalize_leaderboard(intermediate_bucket.get('leaderboard', []))
        for level in ('words', 'phrases', 'sentences'):
            level_bucket = self._get_mode_bucket(data, 'intermediate', level)
            level_bucket['recent_results'] = self._normalize_recent_results(level_bucket.get('recent_results', []))
            level_bucket['leaderboard'] = self._normalize_leaderboard(level_bucket.get('leaderboard', []))

    def update_record(self, mode, level=None, record=None):
        """更新游戏记录"""
        data = self.load_data()
        mode, level = self._normalize_mode_identifier(mode, level)
        bucket = self._get_mode_bucket(data, mode, level)
        is_new_record = False

        data['total_sessions'] = data.get('total_sessions', 0) + 1
        if mode == 'intermediate' and level:
            parent_bucket = self._get_mode_bucket(data, 'intermediate')
            parent_bucket['total_sessions'] = parent_bucket.get('total_sessions', 0) + 1
        bucket['total_sessions'] = bucket.get('total_sessions', 0) + 1

        current_player = self._normalize_username(data.get('player_name', '玩家')) or '玩家'
        record = record or {}

        score = int(record.get('score', 0))
        if score > bucket.get('best_score', 0):
            bucket['best_score'] = score
            bucket['record_holder'] = current_player
            is_new_record = True

        accuracy = record.get('accuracy', 0.0)
        if accuracy > bucket.get('best_accuracy', 0.0):
            bucket['best_accuracy'] = accuracy

        if 'time' in record and 'best_time' in bucket:
            bucket['best_time'] = min(bucket.get('best_time', 999999), record.get('time', 999999))

        if 'speed' in record and 'best_speed' in bucket:
            bucket['best_speed'] = max(bucket.get('best_speed', 0), record.get('speed', 0))

        if 'max_combo' in record and 'max_combo' in bucket:
            bucket['max_combo'] = max(bucket.get('max_combo', 0), record.get('max_combo', 0))

        if 'stars' in record:
            bucket['stars'] = max(bucket.get('stars', 0), record.get('stars', 0))

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        if mode == 'intermediate' and level:
            result = {
                'level': level,
                'score': score,
                'accuracy': accuracy,
                'time': record.get('time', 0.0),
                'speed': record.get('speed', 0),
                'stars': record.get('stars', 0),
                'date': timestamp
            }
            bucket['recent_results'] = self._normalize_recent_results(bucket.get('recent_results', []) + [result])
            parent_bucket = self._get_mode_bucket(data, 'intermediate')
            parent_bucket['recent_results'] = self._normalize_recent_results(parent_bucket.get('recent_results', []) + [result])
        else:
            result = {
                'score': score,
                'accuracy': accuracy,
                'max_combo': record.get('max_combo', 0),
                'stars': record.get('stars', 0),
                'date': timestamp
            }
            bucket['recent_results'] = self._normalize_recent_results(bucket.get('recent_results', []) + [result])

        self.save_data(data)
        return is_new_record

    def get_best_record(self, mode, level=None):
        """获取最佳记录"""
        data = self.load_data()
        mode, level = self._normalize_mode_identifier(mode, level)
        return self._get_mode_bucket(data, mode, level)

    def set_player_name(self, name):
        """设置玩家名称"""
        data = self.load_data()
        data['player_name'] = self._normalize_username(name) or '玩家'
        self.save_data(data)

    def update_leaderboard(self, mode, username, score, level=None):
        """更新排行榜"""
        username = self._normalize_username(username)
        if not username or self._is_blacklisted_username(username):
            return

        data = self.load_data()
        mode, level = self._normalize_mode_identifier(mode, level)
        bucket = self._get_mode_bucket(data, mode, level)
        new_entry = {
            'username': username,
            'score': int(score),
            'date': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        bucket['leaderboard'] = self._normalize_leaderboard(bucket.get('leaderboard', []) + [new_entry])
        self.save_data(data)

    def get_leaderboard(self, mode, level=None):
        """获取排行榜"""
        data = self.load_data()
        mode, level = self._normalize_mode_identifier(mode, level)
        bucket = self._get_mode_bucket(data, mode, level)
        return bucket.get('leaderboard', [])
