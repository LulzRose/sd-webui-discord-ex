'''
Author: SpenserCai
Date: 2023-08-23 23:07:15
version: 
LastEditors: SpenserCai
LastEditTime: 2023-08-24 15:57:45
Description: file content
'''
from modules import script_callbacks, paths_internal
import gradio as gr
import tempfile
import os
import shutil
import json
from scripts import base
from scripts import process_ctrl
import time
import datetime

def load_config(key):
    jsonObject = {}
    config_path = os.path.join(base.get_bin_path(), "config.json")
    if os.path.isfile(config_path):
        with open(config_path, "r") as file:
            jsonObject = json.load(file)
    if key == "token":
        return jsonObject.get("discord", {}).get("token", "")
    elif key == "server_id":
        return jsonObject.get("discord", {}).get("server_id", "")
    elif key == "node_list":
        return jsonObject.get("sd_webui", {}).get("servers", [])
    
def get_desensitization_token(token):
    print(token)
    # 如果token不是<your token here>，则只保留开头和结尾各5个字符，如果总长度小于10，则全部替换为*
    if token != "<your token here>":
        if len(token) < 10:
            return "*" * len(token)
        return token[:5] + "*" * 10 + token[-5:]
    return token

def start_bot(log):
    process_ctrl.ProcessCtrl.LogData = log + "Starting...\n"
    process_ctrl.ProcessCtrl.start()
    while process_ctrl.ProcessCtrl.is_running():
        process_ctrl.ProcessCtrl.LogData += datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Running...\n"
        yield process_ctrl.ProcessCtrl.LogData
        time.sleep(1)

def stop_bot():
    if process_ctrl.ProcessCtrl.is_running():
        process_ctrl.ProcessCtrl.LogData += "Stopping...\n"
        process_ctrl.ProcessCtrl.stop()
        return process_ctrl.ProcessCtrl.LogData + "Stopped\n"
    return process_ctrl.ProcessCtrl.LogData + "Not Running\n"


def discord_tab():
    with gr.Blocks(analytics_enabled=False) as ui:
        with gr.Row():
            with gr.Column():
                j_data = {
                    "token": get_desensitization_token(load_config("token")),
                    "server_id": load_config("server_id")
                }
                gr.JSON(j_data, label="Discord Config")
                node_list = load_config("node_list")
                node_array = []
                for node in node_list:
                    node_array.append([node.get("name", ""), node.get("host", ""), node.get("max_concurrent", "")])
                n_dataframe = gr.Dataframe(headers=["Name","Host","MaxConcurrent"], type="array", label="Node List")
                n_dataframe.value = node_array
                
            with gr.Column():
                gr.Label("SD-WEBUI-DISCORD LOG")
                # 一个长文本框，显示日至，只读的
                log = gr.Textbox(lines=20,autofocus=True, readonly=True)
                # 一个启动按钮
                start_button = gr.Button("Start")
                stop_button = gr.Button("Stop")
                start_button.click(inputs=[log],outputs=[log],fn=start_bot)
                stop_button.click(inputs=[],outputs=[log],fn=stop_bot)
                



    return [(ui,"Discord","Discord")]

script_callbacks.on_ui_tabs(discord_tab)