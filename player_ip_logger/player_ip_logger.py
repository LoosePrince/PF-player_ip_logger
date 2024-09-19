# -*- coding: utf-8 -*-
import re

from mcdreforged.api.all import *

config: dict = {}

def on_load(server: PluginServerInterface, old):
    server.logger.info("Player IP Logger 插件正在加载...")

    global config
    config = server.load_config_simple("config.json", {})

    server.logger.info("Player IP Logger 插件已成功加载。")

def on_info(server: PluginServerInterface, info: Info):
    if "logged in with entity id" in info.content \
        or "lost connection" in info.content \
        or "Disconnecting" in info.content:
        handle_player_login(server, info)

def handle_player_login(server: PluginServerInterface, info: Info):

    player_name, player_ip = extract_player_info(info.content)
    
    # is player
    if player_name and player_ip:
        if player_name not in config:
            config[player_name] = []
        
        if player_ip not in config[player_name]:
            config[player_name].append(player_ip)

            # Save the updated IP storage to the config file
            server.save_config_simple(config)

def extract_player_info(content: str):
    # 处理格式: Shusao[/127.0.0.1:25567] logged in with entity id 359776
    # 机器人格式: bot[/local] logged in with entity id 35977
    # 特殊格式: Disconnecting Shusao (/127.0.0.1:25567)
    # 特殊格式: Shusao (/127.0.0.1:25567) lost connection

    pattern = r'(\w+)\[/(.*?)\] logged in with entity id|Disconnecting (\w+) \(/(.*?)\)|(\w+) \(/(.*?)\) lost connection'
    match = re.search(pattern, content)
    if match:
        groups = match.groups()
        player_name = next((group for group in groups if group is not None), None)
        player_ip = next((group for group in groups[1:] if group is not None), None)
        if player_ip == "/local":
            return None, None
        return player_name, player_ip.split(":")[0]
    return None, None

def on_unload(server: PluginServerInterface):
    server.save_config_simple(config)

#############################################################
# API
#############################################################
def is_player(name: str)->bool:
    return name in config

def get_player_ips(name: str)->list:
    return config.get(name, [])