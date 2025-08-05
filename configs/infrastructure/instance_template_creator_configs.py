import importlib.util
import sys

from typing import Any
from dataclasses import dataclass, field

from omegaconf import SI

module_name = "VMType"
module_path = "01-instance-template-creator.py"
spec = importlib.util.spec_from_file_location(module_name, module_path)
module = importlib.util.module_from_spec(spec)
sys.modules[module_name] = module
spec.loader.exec_module(module)
VMType = module.VMType

@dataclass
class BootDiskConfig:
    project_id: str = "ubuntu-os-cloud"
    name: str = "ubuntu-2004-jammy-v20230714"
    size_gb: int = 50
    labels: Any = SI("${..labels}")

@dataclass
class VMConfig:
    machine_type: str = "n1-standard-1"
    accelerator_count: int = 0
    accelerator_type: str = "nvidia-tesla-t4"
    vm_type: str = VMType.STANDARD
    disks: list[str] = field(default_factory=lambda: [])

@dataclass
class VMMetadataConfig:
    instance_group_name: str = SI("${infrastructure.instance_group_creator.name}")
    docker_image: str = SI("${docker_image}")
    zone: str = SI("${infrastructure.zone}")
    python_hash_seed: int = 42
    mlflow_tracking_uri: str = SI("${infrastructure.mlflow.mlflow_internal_tracking_uri}")
    node_count: int = SI("${infrastructure.instance_group_creator.node_count}")
    disks: list[str] = SI("${..vm_config.disks}")

@dataclass
class InstanceTemplateCreator:
    _target_: str = "instance_template_creator.InstanceTemplateCreator"
    scopes: list[str] = field(default_factory=lambda: [
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/cloud.useraccounts.readonly",
        "https://www.googleapis.com/auth/cloudruntimeconfig"
    ])
    network: str = SI("https://www.googleapis.com/compute/v1/projects/${.project_id}/global/networks/default")
    subnetwork: str = SI("https://www.googleapis.com/compute/v1/projects/${.project_id}/regions/europe-west4/subnetworks/default")
    startup_script_path: str = "../03-task-runner-startup_script.sh"
    vm_config: VMConfig = VMConfig()
    boot_disk_config: BootDiskConfig = BootDiskConfig()
    vm_metadata_config: VMMetadataConfig = VMMetadataConfig()
    template_name: str = SI("${infrastructure.instance_group_creator.name}")
    project_id: str = SI("${insfrastructure.project_id}")
    labels: dict[str, str] = field(default_factory=lambda:{
        "project": "cybulde"
    })