#!/usr/bin/env python3
"""
Send file/image to Feishu chat
"""

import requests
import os
import sys

# Feishu credentials
APP_ID = "cli_a9138cd74ab8dbb6"
APP_SECRET = "DhZUdNkgMhTIcqmMGdlLHbhBAiN5orqv"
RECEIVE_ID = "oc_745fb284e1d23ff837f9c6cfc67e3ae8"

def get_tenant_token():
    """Get tenant access token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    data = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("tenant_access_token")
    else:
        print(f"Failed to get token: {response.text}")
        return None

def upload_image(token, image_path):
    """Upload image to Feishu"""
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    with open(image_path, 'rb') as f:
        files = {
            'image': (os.path.basename(image_path), f, 'image/jpeg')
        }
        data = {
            'image_type': 'message'
        }
        
        response = requests.post(url, headers=headers, files=files, data=data)
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                return result['data']['image_key']
            else:
                print(f"Upload failed: {result}")
                return None
        else:
            print(f"Upload error: {response.status_code} - {response.text}")
            return None

def send_image_message(token, image_key):
    """Send image message to chat"""
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    params = {
        "receive_id_type": "chat_id"
    }
    
    data = {
        "receive_id": RECEIVE_ID,
        "msg_type": "image",
        "content": json.dumps({
            "image_key": image_key
        })
    }
    
    response = requests.post(url, headers=headers, params=params, json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get('code') == 0:
            print("Image sent successfully!")
            return True
        else:
            print(f"Send failed: {result}")
            return False
    else:
        print(f"Send error: {response.status_code} - {response.text}")
        return False

if __name__ == "__main__":
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python feishu_send.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        sys.exit(1)
    
    print(f"Sending {image_path} to Feishu...")
    
    # Get token
    token = get_tenant_token()
    if not token:
        sys.exit(1)
    
    # Upload image
    image_key = upload_image(token, image_path)
    if not image_key:
        sys.exit(1)
    
    # Send message
    send_image_message(token, image_key)