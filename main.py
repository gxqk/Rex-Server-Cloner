#!/usr/bin/env python3

import discord
import asyncio
import aiohttp
import json
import sys
import os
from typing import Optional, List, Dict, Any

try:
    import colorama
    colorama.init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

COLORS = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'purple': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'reset': '\033[0m'
}

def print_colored(message: str, color: str = 'white') -> None:
    if os.name == 'nt' and not COLORAMA_AVAILABLE:
        print(message)
    elif os.name == 'nt' and COLORAMA_AVAILABLE:
        color_code = COLORS.get(color, COLORS['white'])
        print(f"{color_code}{message}{COLORS['reset']}")
    else:
        color_code = COLORS.get(color, COLORS['white'])
        print(f"{color_code}{message}{COLORS['reset']}")

def print_error(message: str) -> None:
    print_colored(f"[X] {message}", 'red')

def print_success(message: str) -> None:
    print_colored(f"[+] {message}", 'green')

def print_warning(message: str) -> None:
    print_colored(f"[!] {message}", 'yellow')

def print_info(message: str) -> None:
    print_colored(f"[i] {message}", 'blue')

def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print_error("config.json file not found!")
        print_info("Create a config.json file with your Discord token.")
        sys.exit(1)
    except json.JSONDecodeError:
        print_error("Error in the format of the config.json file!")
        sys.exit(1)

CONFIG = load_config()
TOKEN = CONFIG.get('discord_token', '')
SETTINGS = CONFIG.get('settings', {})

ROLE_CREATE_DELAY = SETTINGS.get('role_create_delay', 1.0)
CHANNEL_CREATE_DELAY = SETTINGS.get('channel_create_delay', 0.5)
EMOJI_CREATE_DELAY = SETTINGS.get('emoji_create_delay', 1.0)
PERMISSION_UPDATE_DELAY = SETTINGS.get('permission_update_delay', 0.3)

def validate_discord_id(discord_id: str) -> bool:
    try:
        id_int = int(discord_id)
        return 17 <= len(discord_id) <= 19
    except ValueError:
        return False

def validate_token(token: str) -> bool:
    if not token or len(token) < 50:
        return False
    parts = token.split('.')
    return len(parts) >= 2

async def safe_sleep(duration: float) -> None:
    try:
        await asyncio.sleep(duration)
    except KeyboardInterrupt:
        print_warning("Interruption detected...")
        sys.exit(0)

def get_user_input(prompt: str, validator=None) -> str:
    while True:
        try:
            if os.name == 'nt' and not COLORAMA_AVAILABLE:
                user_input = input(prompt)
            else:
                user_input = input(f"{COLORS['cyan']}{prompt}{COLORS['reset']}")

            if validator and not validator(user_input):
                print_error("Invalid input, please try again.")
                continue

            return user_input.strip()
        except KeyboardInterrupt:
            print_warning("\nOperation canceled by the user.")
            sys.exit(0)
        except EOFError:
            print_error("Input reading error.")
            sys.exit(1)

def print_banner():
    banner = """

                    __
                   / _)      ██████╗ ███████╗██╗  ██╗    ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗
            .-^^^-/ /        ██╔══██╗██╔════╝╚██╗██╔╝    ██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
           /       /         ██████╔╝█████╗   ╚███╔╝     ███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
         <__.|_|-|_|         ██╔══██╗██╔══╝   ██╔██╗     ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
                             ██║  ██║███████╗██╔╝ ██╗    ███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
                             ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝

                              ██████╗██╗      ██████╗ ███╗   ██╗███████╗██████╗
                             ██╔════╝██║     ██╔═══██╗████╗  ██║██╔════╝██╔══██╗
                             ██║     ██║     ██║   ██║██╔██╗ ██║█████╗  ██████╔╝
                             ██║     ██║     ██║   ██║██║╚██╗██║██╔══╝  ██╔══██╗
                             ╚██████╗███████╗╚██████╔╝██║ ╚████║███████╗██║  ██║
                              ╚═════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝

                                                    Rex Server-Cloner 1.0
                                                    Created by gxqk_secours on discord :)
    """
    print_colored(banner, 'cyan')



class DiscordServerCloner:
    def __init__(self, token: str):
        self.token = token
        self.client = None
        self.source_guild = None
        self.target_guild = None

    def is_connected(self) -> bool:
        return self.client and self.client.user is not None

    async def get_guild(self, guild_id: int) -> Optional[discord.Guild]:
        try:
            guild = self.client.get_guild(guild_id)
            if guild:
                return guild

            try:
                guild = await self.client.fetch_guild(guild_id)
                return guild
            except discord.Forbidden:
                for g in self.client.guilds:
                    if g.id == guild_id:
                        return g
                print_error(f"No access to server {guild_id} or server not found")
                return None

        except discord.NotFound:
            print_error(f"Server {guild_id} not found")
            return None
        except discord.Forbidden:
            print_error(f"No access to server {guild_id}")
            return None
        except Exception as e:
            print_error(f"Error while fetching the server: {str(e)}")
            return None

    async def clone_roles(self) -> Dict[int, discord.Role]:
        print_info("Cloning roles...")
        role_mapping = {}

        roles_to_clone = sorted(
            [role for role in self.source_guild.roles if role.name != "@everyone"],
            key=lambda r: r.position
        )

        for role in roles_to_clone:
            try:
                new_role = await self.target_guild.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    color=role.color,
                    hoist=role.hoist,
                    mentionable=role.mentionable,
                    reason="Server cloning"
                )

                role_mapping[role.id] = new_role
                print_success(f"Role created: {role.name} (position: {role.position})")
                await safe_sleep(ROLE_CREATE_DELAY)

            except discord.Forbidden:
                print_warning(f"No permission to create the role: {role.name}")
            except discord.HTTPException as e:
                print_error(f"Error while creating the role {role.name}: {str(e)}")
            except Exception as e:
                print_error(f"Unexpected error for role {role.name}: {str(e)}")

        await self._reorder_roles(role_mapping)

        return role_mapping

    async def _reorder_roles(self, role_mapping: Dict[int, discord.Role]) -> None:
        print_info("Reordering roles according to hierarchy...")

        try:
            source_roles = sorted(
                [role for role in self.source_guild.roles if role.name != "@everyone"],
                key=lambda r: r.position,
                reverse=True
            )

            new_roles_ordered = []
            for source_role in source_roles:
                if source_role.id in role_mapping:
                    new_roles_ordered.append(role_mapping[source_role.id])

            if new_roles_ordered:
                await self.target_guild.edit_role_positions(
                    positions={role: len(new_roles_ordered) - i for i, role in enumerate(new_roles_ordered)},
                    reason="Hierarchical reordering of roles"
                )
                print_success("Role hierarchy restored!")
                await safe_sleep(1.0)

        except discord.Forbidden:
            print_warning("No permission to reorder roles")
        except discord.HTTPException as e:
            print_warning(f"Error while reordering roles: {str(e)}")
        except Exception as e:
            print_warning(f"Unexpected error during reordering: {str(e)}")

    async def _convert_overwrites(self, overwrites: Dict, role_mapping: Dict[int, discord.Role]) -> Dict:
        new_overwrites = {}

        for target, overwrite in overwrites.items():
            try:
                if isinstance(target, discord.Role):
                    if target.id in role_mapping:
                        new_overwrites[role_mapping[target.id]] = overwrite
                    elif target.name == "@everyone":
                        new_overwrites[self.target_guild.default_role] = overwrite

                elif isinstance(target, discord.Member):
                    member = self.target_guild.get_member(target.id)
                    if member:
                        new_overwrites[member] = overwrite

            except Exception:
                pass

        return new_overwrites

    async def clean_target_server(self) -> bool:
        print_info("Complete cleaning of the target server...")

        try:
            print_info("Deleting all channels...")
            all_channels = list(self.target_guild.channels)

            regular_channels = [ch for ch in all_channels if not isinstance(ch, discord.CategoryChannel)]
            categories = [ch for ch in all_channels if isinstance(ch, discord.CategoryChannel)]

            for channel in regular_channels:
                try:
                    await channel.delete(reason="Cleaning before cloning")
                    print_success(f"Channel deleted: {channel.name}")
                    await safe_sleep(0.3)
                except discord.Forbidden:
                    print_warning(f"No permission to delete: {channel.name}")
                except discord.HTTPException as e:
                    print_warning(f"Error while deleting {channel.name}: {str(e)}")
                except Exception as e:
                    print_warning(f"Unexpected error for {channel.name}: {str(e)}")

            print_info("Deleting categories...")
            for category in categories:
                try:
                    await category.delete(reason="Cleaning before cloning")
                    print_success(f"Category deleted: {category.name}")
                    await safe_sleep(0.3)
                except discord.Forbidden:
                    print_warning(f"No permission to delete category: {category.name}")
                except discord.HTTPException as e:
                    print_warning(f"Error while deleting category {category.name}: {str(e)}")
                except Exception as e:
                    print_warning(f"Unexpected error for category {category.name}: {str(e)}")

            print_info("Deleting roles...")
            roles_to_delete = [role for role in self.target_guild.roles if role.name != "@everyone"]

            roles_to_delete.sort(key=lambda r: r.position, reverse=True)

            for role in roles_to_delete:
                try:
                    await role.delete(reason="Cleaning before cloning")
                    print_success(f"Role deleted: {role.name}")
                    await safe_sleep(0.3)
                except discord.Forbidden:
                    print_warning(f"No permission to delete role: {role.name}")
                except discord.HTTPException as e:
                    print_warning(f"Error while deleting role {role.name}: {str(e)}")
                except Exception as e:
                    print_warning(f"Unexpected error for role {role.name}: {str(e)}")

            print_info("Deleting emojis...")
            emojis_to_delete = list(self.target_guild.emojis)
            for emoji in emojis_to_delete:
                try:
                    await emoji.delete(reason="Cleaning before cloning")
                    print_success(f"Emoji deleted: {emoji.name}")
                    await safe_sleep(0.2)
                except discord.Forbidden:
                    print_warning(f"No permission to delete emoji: {emoji.name}")
                except discord.HTTPException as e:
                    print_warning(f"Error while deleting emoji {emoji.name}: {str(e)}")
                except Exception as e:
                    print_warning(f"Unexpected error for emoji {emoji.name}: {str(e)}")

            print_success("Server cleaning finished!")
            return True

        except Exception as e:
            print_error(f"Error during cleaning: {str(e)}")
            return False

    async def clone_categories_and_channels(self, role_mapping: Dict[int, discord.Role]) -> None:
        print_info("Cloning categories and channels...")
        category_mapping = {}

        categories = [cat for cat in self.source_guild.categories]
        categories.sort(key=lambda c: c.position)

        for category in categories:
            try:
                overwrites = await self._convert_overwrites(category.overwrites, role_mapping)

                new_category = await self.target_guild.create_category(
                    name=category.name,
                    overwrites=overwrites,
                    reason="Server cloning"
                )

                category_mapping[category.id] = new_category
                print_success(f"Category created: {category.name}")
                await safe_sleep(CHANNEL_CREATE_DELAY)

            except Exception as e:
                print_error(f"Error while creating category {category.name}: {str(e)}")

        await self._clone_channels(category_mapping, role_mapping)

    async def _clone_channels(self, category_mapping: Dict[int, discord.CategoryChannel],
                            role_mapping: Dict[int, discord.Role]) -> None:
        channels = [ch for ch in self.source_guild.channels if not isinstance(ch, discord.CategoryChannel)]
        channels.sort(key=lambda c: c.position)

        for channel in channels:
            try:
                overwrites = await self._convert_overwrites(channel.overwrites, role_mapping)
                category = category_mapping.get(channel.category_id) if channel.category else None

                if isinstance(channel, discord.TextChannel):
                    await self._create_text_channel(channel, category, overwrites)
                elif isinstance(channel, discord.VoiceChannel):
                    await self._create_voice_channel(channel, category, overwrites)
                elif isinstance(channel, discord.StageChannel):
                    await self._create_stage_channel(channel, category, overwrites)

                await safe_sleep(CHANNEL_CREATE_DELAY)

            except Exception as e:
                print_error(f"Error while creating channel {channel.name}: {str(e)}")

    async def _create_text_channel(self, channel: discord.TextChannel,
                                 category: Optional[discord.CategoryChannel],
                                 overwrites: Dict) -> None:
        try:
            new_channel = await self.target_guild.create_text_channel(
                name=channel.name,
                topic=channel.topic,
                slowmode_delay=channel.slowmode_delay,
                nsfw=channel.nsfw,
                category=category,
                overwrites=overwrites,
                reason="Server cloning"
            )
            print_success(f"Text channel created: {channel.name}")

        except Exception as e:
            print_error(f"Error while creating text channel {channel.name}: {str(e)}")

    async def _create_voice_channel(self, channel: discord.VoiceChannel,
                                  category: Optional[discord.CategoryChannel],
                                  overwrites: Dict) -> None:
        try:
            new_channel = await self.target_guild.create_voice_channel(
                name=channel.name,
                bitrate=channel.bitrate,
                user_limit=channel.user_limit,
                category=category,
                overwrites=overwrites,
                reason="Server cloning"
            )
            print_success(f"Voice channel created: {channel.name}")

        except Exception as e:
            print_error(f"Error while creating voice channel {channel.name}: {str(e)}")

    async def _create_stage_channel(self, channel: discord.StageChannel,
                                  category: Optional[discord.CategoryChannel],
                                  overwrites: Dict) -> None:
        try:
            new_channel = await self.target_guild.create_stage_channel(
                name=channel.name,
                topic=getattr(channel, 'topic', None),
                category=category,
                overwrites=overwrites,
                reason="Server cloning"
            )
            print_success(f"Stage channel created: {channel.name}")

        except Exception as e:
            print_error(f"Error while creating stage channel {channel.name}: {str(e)}")



    async def clone_emojis(self) -> None:
        print_info("Cloning emojis...")

        for emoji in self.source_guild.emojis:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(emoji.url)) as resp:
                        if resp.status == 200:
                            emoji_data = await resp.read()

                            new_emoji = await self.target_guild.create_custom_emoji(
                                name=emoji.name,
                                image=emoji_data,
                                reason="Server cloning"
                            )

                            print_success(f"Emoji created: {emoji.name}")
                            await safe_sleep(EMOJI_CREATE_DELAY)
                        else:
                            print_warning(f"Could not download emoji: {emoji.name}")

            except discord.Forbidden:
                print_warning(f"No permission to create emoji: {emoji.name}")
            except discord.HTTPException as e:
                if "Maximum number of emojis reached" in str(e):
                    print_warning("Emoji limit reached in the target server")
                    break
                else:
                    print_error(f"Error while creating emoji {emoji.name}: {str(e)}")
            except Exception as e:
                print_error(f"Unexpected error for emoji {emoji.name}: {str(e)}")

    async def update_server_settings(self, clone_icon: bool = True) -> None:
        print_info("Updating server settings...")

        try:
            if self.source_guild.name != self.target_guild.name:
                await self.target_guild.edit(name=f"{self.source_guild.name} (Clone)")
                print_success("Server name updated")

            if clone_icon and self.source_guild.icon:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(str(self.source_guild.icon.url)) as resp:
                            if resp.status == 200:
                                icon_data = await resp.read()
                                await self.target_guild.edit(icon=icon_data)
                                print_success("Server icon copied")
                except Exception as e:
                    print_warning(f"Could not copy the icon: {str(e)}")
            elif not clone_icon:
                print_info("Server icon not cloned (option disabled)")

            if self.source_guild.banner:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(str(self.source_guild.banner.url)) as resp:
                            if resp.status == 200:
                                banner_data = await resp.read()
                                await self.target_guild.edit(banner=banner_data)
                                print_success("Server banner copied")
                except Exception as e:
                    print_warning(f"Could not copy the banner: {str(e)}")

        except discord.Forbidden:
            print_warning("No permission to modify server settings")
        except Exception as e:
            print_error(f"Error while updating settings: {str(e)}")

    async def clone_server(self, source_guild_id: int, target_guild_id: int, clone_icon: bool = True) -> bool:
        try:
            print_info(f"Starting clone: {source_guild_id} -> {target_guild_id}")

            if not self.is_connected():
                print_error("Discord client not connected")
                return False

            self.source_guild = await self.get_guild(source_guild_id)
            if not self.source_guild:
                return False

            self.target_guild = await self.get_guild(target_guild_id)
            if not self.target_guild:
                return False

            print_success(f"Source server: {self.source_guild.name}")
            print_success(f"Target server: {self.target_guild.name}")

            try:
                me = self.target_guild.get_member(self.client.user.id)
                if me and not me.guild_permissions.administrator:
                    print_warning("Warning: You may not have administrator permissions")
                    print_info("Cloning will continue but some operations may fail")
            except:
                print_info("Could not check permissions, cloning will continue")

            print_info("Starting the cloning process...")

            if not await self.clean_target_server():
                print_warning("Cleaning partially failed, but cloning continues...")

            role_mapping = await self.clone_roles()

            await self.clone_categories_and_channels(role_mapping)

            await self.clone_emojis()

            await self.update_server_settings(clone_icon)

            print_success("Cloning finished successfully!")
            return True

        except Exception as e:
            print_error(f"Error during cloning: {str(e)}")
            return False

    async def close(self) -> None:
        if self.client:
            await self.client.close()

def get_guild_ids():
    print_info("Server configuration")

    while True:
        source_id = get_user_input("[>] ID of the server to clone (source): ")

        if not validate_discord_id(source_id):
            print_error("Invalid Discord ID (must be 17-19 digits).")
            continue

        break

    while True:
        target_id = get_user_input("[<] ID of the destination server (target): ")

        if not validate_discord_id(target_id):
            print_error("Invalid Discord ID (must be 17-19 digits).")
            continue

        if target_id == source_id:
            print_error("The source and target servers cannot be the same.")
            continue

        break

    return int(source_id), int(target_id)

def get_clone_options():
    print_info("Cloning options")

    clone_icon = get_user_input("[?] Do you want to clone the server icon/picture? (yes/no): ")
    clone_server_icon = clone_icon.lower() in ['oui', 'o', 'yes', 'y']

    if clone_server_icon:
        print_success("The server icon will be cloned")
    else:
        print_info("The server icon will not be cloned")

    return clone_server_icon

def confirm_operation(source_id: int, target_id: int, clone_icon: bool):
    print_info("Operation summary")
    print(f"[>] Source server: {source_id}")
    print(f"[<] Target server: {target_id}")
    print(f"[?] Clone icon: {'Yes' if clone_icon else 'No'}")
    print()

    confirmation = get_user_input("[!] Are you sure you want to continue? (yes/no): ")

    if confirmation.lower() not in ['oui', 'o', 'yes', 'y']:
        print_warning("Operation canceled by the user.")
        sys.exit(0)

async def main():
    try:
        print_banner()

        if not TOKEN or TOKEN == "YOUR_TOKEN_HERE":
            print_error("Please configure your Discord token in config.json")
            sys.exit(1)

        if not validate_token(TOKEN):
            print_error("Invalid token format in config.json")
            sys.exit(1)

        source_guild_id, target_guild_id = get_guild_ids()

        clone_icon = get_clone_options()

        confirm_operation(source_guild_id, target_guild_id, clone_icon)

        print_info("Initializing the cloner...")

        cloner = DiscordServerCloner(TOKEN)

        print_info("Connecting to Discord...")

        try:
            cloner.client = discord.Client()

            @cloner.client.event
            async def on_ready():
                print_success(f"Connected as {cloner.client.user}")
                print_info(f"Connected to {len(cloner.client.guilds)} servers")

            await cloner.client.login(TOKEN)
            print_success("Authentication successful")

            print_info("Connecting...")

            connection_task = asyncio.create_task(cloner.client.connect())

            def handle_task_exception(task):
                try:
                    task.result()
                except Exception:
                    pass

            connection_task.add_done_callback(handle_task_exception)

            await safe_sleep(3.0)

            print_success("Connection established, starting clone!")

            success = await cloner.clone_server(source_guild_id, target_guild_id, clone_icon)

            connection_task.cancel()
            await cloner.close()

        except discord.LoginFailure:
            print_error("Invalid Discord token")
            return False
        except Exception as e:
            print_error(f"Connection error: {str(e)}")
            return False

        if success:
            print_info("Check your Discord server to see the results.")
        else:
            print_error("Cloning failed.")

        return success

    except KeyboardInterrupt:
        print_warning("\nOperation interrupted by the user.")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        return False

def run_cloner():
    try:
        if sys.version_info < (3, 7):
            print_error("Python 3.7 or higher required.")
            sys.exit(1)

        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

        success = asyncio.run(main())

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print_warning("\nProgram interrupted.")
        sys.exit(0)
    except Exception as e:
        print_error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_cloner()
