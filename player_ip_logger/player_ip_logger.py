# -*- coding: utf-8 -*-
import re

from mcdreforged.api.all import *

config = None
game_server: PluginServerInterface = None

def on_load(server: PluginServerInterface, old):
    server.logger.info("Player IP Logger 插件正在加载...")

    global config, game_server
    game_server = server
    config = server.load_config_simple("config.json", {"users": {}})

    server.logger.info("Player IP Logger 插件已成功加载。")

def on_info(server: PluginServerInterface, info: Info):
    if config is None:
        return
    
    if "logged in with entity id" in info.content \
        or "lost connection" in info.content \
        or "Disconnecting" in info.content:
        handle_player_login(server, info)

def handle_player_login(server: PluginServerInterface, info: Info):

    player_name, player_ip = extract_player_info(info.content)
    
    # is player
    if player_name and player_ip:
        if player_name not in config["users"]:
            config["users"][player_name] = []
        
        if player_ip not in config["users"][player_name]:
            config["users"][player_name].append(player_ip)

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

#############################################################
# API
#############################################################
def ban_ip(ip: str):
    if config is not None:
        game_server.execute("ban-ip " + ip)

def ban_player(name: str):
    if config is not None:
        ips = get_player_ips(name)
        for ip in ips:
            ban_ip(ip)

def get_player_ips(name: str)->list:
    if config is not None:
        return config["users"].get(name, [])
    return []

def get_player_names(ip: str)->list:
    if config is not None:
        return [name for name, ips in config["users"].items() if ip in ips]
    return []

def is_player(name: str)->bool:
    if config is not None:
        return name in config["users"]
    return False