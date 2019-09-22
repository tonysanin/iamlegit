import keyboard
import pymem
from pymem import process
import time
from offsets import *
from multiprocessing import Process

_process = pymem.Pymem("csgo.exe")
_client = pymem.process.module_from_name(_process.process_handle, "client_panorama.dll").lpBaseOfDll


def Bhop():
    print("Bhop activated")
    while True:
        try:
            if keyboard.is_pressed("space"):
                player = _process.read_int(_client + dwLocalPlayer)
                jump = _client + dwForceJump
                player_state = _process.read_int(player + m_fFlags)
                if player_state == 257 or player_state == 263:  # 257 = on ground  263 = crouch
                    _process.write_int(jump, 5)
                    time.sleep(0.1)
                    _process.write_int(jump, 4)
        except pymem.exception.MemoryReadError:
            pass


def GlowESP():
    print("GlowESP activated")
    while True:
        glow_manager = _process.read_int(_client + dwGlowObjectManager)

        for i in range(1, 32):  # Entities 1-32 are reserved for players.
            entity = _process.read_int(_client + dwEntityList + i * 0x10)

            if entity:
                entity_team_id = _process.read_int(entity + m_iTeamNum)
                entity_glow = _process.read_int(entity + m_iGlowIndex)

                if entity_team_id == 2:  # Terrorist
                    _process.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(1))  # R
                    _process.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))  # G
                    _process.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))  # B
                    _process.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                    _process.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)  # Enable glow

                elif entity_team_id == 3:  # Counter-terrorist
                    _process.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0))  # R
                    _process.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))  # G
                    _process.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))  # B
                    _process.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                    _process.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)  # Enable glow


GlowESP()
