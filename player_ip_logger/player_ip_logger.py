# -*- coding: utf-8 -*-
import re

from mcdreforged.api.all import *
from mcdreforged.api.command import SimpleCommandBuilder, Integer, Text, GreedyText

config = None
game_server: PluginServerInterface = None

def on_load(server: PluginServerInterface, old):
    server.logger.info("Player IP Logger 插件正在加载...")

    global config, game_server
    game_server = server
    config = server.load_config_simple("config.json", {"users": {}, "banned_player": [], "banned_ips": []})

    server.register_command(
        Literal("!!ip")
        .requires(lambda src: src.has_permission(3))
        .then(
            Literal('ban')
            .then(
                Text('player/ip').runs(ban)
            )
        )
        .then(
            Literal('pardon')
            .then(
                Text('player/ip').runs(pardon)
            )
        )
    )

    server.register_help_message('!!ip ban <player/ip>','禁止玩家登录')
    server.register_help_message('!!ip pardon <player/ip>', '解禁玩家')

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
def get_banned_ips(ip: str):
    return config.get("banned_ips", [])

def get_banned_player(name: str):
    return config.get("banned_player", [])

def get_player_ips(name: str)->list:
    if config:
        return config["users"].get(name, [])
    return []

def get_player_names(ip: str)->list:
    if config:
        return [name for name, ips in config["users"].items() if ip in ips]
    return []

def is_player(name: str)->bool:
    if config:
        return name in config["users"]
    return False

#############################################################
# ban/unban API
#############################################################
def ban(src, ctx)->None:
    player = ctx['player/ip']
    if is_ip(player):
        ban_ip(player)
    else:
        ban_player(player)

def ban_ip(ip: str)->None:
    if config:
        game_server.execute("ban-ip " + ip)
        if ip not in config.get('banned_ips'):
            config['banned_ips'].append(ip)

def ban_player(name: str)->None:
    if config:
        ips = get_player_ips(name)
        for ip in ips:
            ban_ip(ip)
        if name not in config.get('banned_player'):
            config['banned_player'].append(name)

def pardon(src, ctx)->None:
    player = ctx['player/ip']
    if is_ip(player):
        unban_ip(player)
    else:
        unban_player(player)

def unban_ip(ip: str)->None:
    if config and game_server:
        game_server.execute("pardon-ip " + ip)
        if ip in config.get("banned_ips", []):
            config['banned_ips'].remove(ip)

def unban_player(name: str)->None:
    if config and game_server:
        ips = get_player_ips(name)
        for ip in ips:
            unban_ip(ip)
        if name in config.get("banned_player", []):
            config['banned_player'].remove(name)

#############################################################
# helper
#############################################################
def is_ip(string:str)->bool:
    return '.' in string