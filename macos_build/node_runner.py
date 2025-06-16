#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Wrapper для запуска Node.js/TypeScript скриптов в macOS app bundle
Автоматически выбирает встроенный Node.js или системный
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Any

from .resource_utils import get_resource_path, is_app_bundle


class NodeRunner:
    """
    Универсальный runner для Node.js скриптов
    Автоматически определяет доступный Node.js runtime
    """
    
    def __init__(self):
        self.node_path = self._find_node_executable()
        self.npx_path = self._find_npx_executable()
    
    def _find_node_executable(self) -> str:
        """
        Находит исполняемый файл Node.js
        
        Returns:
            Путь к Node.js executable
        """
        if is_app_bundle():
            # В app bundle ищем встроенный Node.js
            embedded_node = get_resource_path('node/bin/node')
            if embedded_node.exists():
                return str(embedded_node)
        
        # Fallback к системному Node.js
        system_node = shutil.which('node')
        if system_node:
            return system_node
        
        raise RuntimeError("Node.js не найден ни в app bundle, ни в системе")
    
    def _find_npx_executable(self) -> str:
        """
        Находит исполняемый файл npx
        
        Returns:
            Путь к npx executable
        """
        if is_app_bundle():
            # В app bundle ищем встроенный npx
            embedded_npx = get_resource_path('node/bin/npx')
            if embedded_npx.exists():
                return str(embedded_npx)
        
        # Fallback к системному npx
        system_npx = shutil.which('npx')
        if system_npx:
            return system_npx
        
        # Если npx не найден, пробуем через node
        return None
    
    def run_typescript_script(self, script_dir: str, env_file: str = None) -> Dict[str, Any]:
        """
        Запускает TypeScript скрипт через ts-node
        
        Args:
            script_dir: Директория со скриптом (должна содержать index.ts)
            env_file: Путь к .env файлу (опционально)
            
        Returns:
            Результат выполнения скрипта
        """
        try:
            script_path = Path(script_dir)
            index_file = script_path / 'index.ts'
            
            if not index_file.exists():
                return {
                    'success': False,
                    'message': f"Файл index.ts не найден в {script_dir}"
                }
            
            # Подготавливаем команду
            if self.npx_path:
                cmd = [self.npx_path, 'ts-node', 'index.ts']
            else:
                # Пробуем запустить ts-node через node напрямую
                ts_node_path = self._find_ts_node()
                if ts_node_path:
                    cmd = [self.node_path, ts_node_path, 'index.ts']
                else:
                    return {
                        'success': False,
                        'message': "ts-node не найден"
                    }
            
            # Подготавливаем переменные окружения
            env = os.environ.copy()
            
            # Загружаем переменные из .env файла если указан
            if env_file and os.path.exists(env_file):
                self._load_env_file(env_file, env)
            
            # Запускаем процесс
            process = subprocess.Popen(
                cmd,
                cwd=str(script_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                env=env
            )
            
            # Ждем завершения
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                return {
                    'success': True,
                    'output': stdout,
                    'message': "Скрипт выполнен успешно"
                }
            else:
                return {
                    'success': False,
                    'message': f"Ошибка выполнения скрипта: {stderr or stdout}",
                    'error_code': process.returncode
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f"Критическая ошибка: {str(e)}"
            }
    
    def _find_ts_node(self) -> str:
        """
        Находит исполняемый файл ts-node
        
        Returns:
            Путь к ts-node или None
        """
        # Пробуем найти в node_modules
        if is_app_bundle():
            ts_node_path = get_resource_path('node_modules/.bin/ts-node')
            if ts_node_path.exists():
                return str(ts_node_path)
        
        # Пробуем системный ts-node
        system_ts_node = shutil.which('ts-node')
        if system_ts_node:
            return system_ts_node
        
        return None
    
    def _load_env_file(self, env_file: str, env_dict: dict):
        """
        Загружает переменные из .env файла в словарь окружения
        
        Args:
            env_file: Путь к .env файлу
            env_dict: Словарь переменных окружения для обновления
        """
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_dict[key.strip()] = value.strip()
        except Exception:
            # Игнорируем ошибки загрузки .env файла
            pass
    
    def check_dependencies(self) -> Dict[str, Any]:
        """
        Проверяет доступность Node.js и ts-node
        
        Returns:
            Информация о доступных зависимостях
        """
        result = {
            'node_available': False,
            'npx_available': False,
            'ts_node_available': False,
            'node_path': self.node_path,
            'npx_path': self.npx_path
        }
        
        # Проверяем Node.js
        try:
            process = subprocess.run(
                [self.node_path, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if process.returncode == 0:
                result['node_available'] = True
                result['node_version'] = process.stdout.strip()
        except:
            pass
        
        # Проверяем npx
        if self.npx_path:
            try:
                process = subprocess.run(
                    [self.npx_path, '--version'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if process.returncode == 0:
                    result['npx_available'] = True
            except:
                pass
        
        # Проверяем ts-node
        ts_node_path = self._find_ts_node()
        if ts_node_path:
            result['ts_node_available'] = True
            result['ts_node_path'] = ts_node_path
        
        return result 