import logging
import tinytuya
import subprocess
import json
import os
from typing import Dict, Any

logger = logging.getLogger(__name__)


class TuyaController:
    @staticmethod
    async def scan_devices():
        try:
            result = subprocess.run(
                ["python", "-m", "tinytuya", "scan"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                logger.info("Device scan completed successfully")
                return await TuyaController.read_snapshot_devices()
            else:
                logger.error(f"Scan failed with return code {result.returncode}: {result.stderr}")
                raise Exception(f"Scan command failed: {result.stderr}")

        except subprocess.TimeoutExpired:
            logger.error("Device scan timed out")
            raise Exception("Device scan timed out after 30 seconds")
        except Exception as e:
            logger.error(f"Failed to scan devices: {e}")
            raise

    @staticmethod
    async def read_snapshot_devices(snapshot_path: str = "snapshot.json") -> Dict[str, Dict[str, Any]]:
        """
        Đọc file snapshot.json và trích xuất thông tin thiết bị

        Args:
            snapshot_path: Đường dẫn tới file snapshot.json

        Returns:
            Dict với device_id làm key và thông tin thiết bị làm value
        """
        try:
            if not os.path.exists(snapshot_path):
                logger.error(f"Snapshot file not found: {snapshot_path}")
                return {}

            with open(snapshot_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            devices_dict = {}
            devices = data.get('devices', [])

            for device in devices:
                device_id = device.get('id')
                if device_id:
                    devices_dict[device_id] = {
                        'device_id': device_id,
                        'device_ip': device.get('ip', ''),
                        'device_key': device.get('key', ''),
                        'device_version': float(device.get('ver', '3.5')),
                        'productKey': device.get('productKey', ''),
                        'name': device.get('name', ''),
                        'mac': device.get('mac', ''),
                        'active': device.get('active', 0),
                        'encrypt': device.get('encrypt', False)
                    }

            logger.info(f"Loaded {len(devices_dict)} devices from snapshot")
            return devices_dict

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in snapshot file: {e}")
            return {}
        except Exception as e:
            logger.error(f"Failed to read snapshot file: {e}")
            return {}

    @staticmethod
    async def _create_device(
        device_id: str, device_ip: str, device_key: str, device_version: float = 3.5
    ):
        try:
            device = tinytuya.Device(
                dev_id=device_id,
                address=device_ip,
                local_key=device_key,
                version=device_version,
            )
            logger.info(f"Created connection to Tuya device {device_id}")
            return device
        except Exception as e:
            logger.error(f"Failed to create device connection: {e}")
            raise

    @staticmethod
    async def get_status(
        device_id: str, device_ip: str, device_key: str, device_version: float = 3.5
    ) -> Dict[str, Any]:
        try:
            device = await TuyaController._create_device(
                device_id, device_ip, device_key, device_version
            )
            status = device.status()
            logger.info(f"Device {device_id} status retrieved: {status}")
            return {
                "success": True,
                "data": status,
                "message": "Status retrieved successfully",
                "device_id": device_id,
            }
        except Exception as e:
            logger.error(f"Failed to get device {device_id} status: {e}")
            return {
                "success": False,
                "data": None,
                "message": f"Failed to get status: {str(e)}",
                "device_id": device_id,
            }

    @staticmethod
    async def turn_on(
        device_id: str, device_ip: str, device_key: str, device_version: float = 3.5
    ) -> Dict[str, Any]:
        try:
            device = await TuyaController._create_device(
                device_id, device_ip, device_key, device_version
            )
            result = device.turn_on()
            logger.info(f"Device {device_id} turned on successfully")
            return {
                "success": True,
                "data": result,
                "message": "Device turned on successfully",
                "device_id": device_id,
            }
        except Exception as e:
            logger.error(f"Failed to turn on device {device_id}: {e}")
            return {
                "success": False,
                "data": None,
                "message": f"Failed to turn on: {str(e)}",
                "device_id": device_id,
            }

    @staticmethod
    async def turn_off(
        device_id: str, device_ip: str, device_key: str, device_version: float = 3.5
    ) -> Dict[str, Any]:
        try:
            device = await TuyaController._create_device(
                device_id, device_ip, device_key, device_version
            )
            result = device.turn_off()
            logger.info(f"Device {device_id} turned off successfully")
            return {
                "success": True,
                "data": result,
                "message": "Device turned off successfully",
                "device_id": device_id,
            }
        except Exception as e:
            logger.error(f"Failed to turn off device {device_id}: {e}")
            return {
                "success": False,
                "data": None,
                "message": f"Failed to turn off: {str(e)}",
                "device_id": device_id,
            }
