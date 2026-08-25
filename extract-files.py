#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import blob_fixup, blob_fixups_user_type
from extract_utils.fixups_lib import (
    lib_fixups as lib_fixups_default,
    lib_fixups_user_type,
)
from extract_utils.main import ExtractUtils, ExtractUtilsModule


system_ext_duplicate_libs = (
    'com.qualcomm.qti.imscmservice@1.0',
    'com.qualcomm.qti.imscmservice@2.0',
    'com.qualcomm.qti.imscmservice@2.1',
    'com.qualcomm.qti.imscmservice@2.2',
    'com.qualcomm.qti.uceservice@2.0',
    'com.qualcomm.qti.uceservice@2.1',
    'com.qualcomm.qti.uceservice@2.2',
    'com.qualcomm.qti.uceservice@2.3',
    'vendor.display.color@1.0',
    'vendor.display.color@1.1',
    'vendor.display.color@1.2',
    'vendor.display.color@1.3',
    'vendor.qti.hardware.data.dynamicdds@1.0',
    'vendor.qti.hardware.data.latency@1.0',
    'vendor.qti.hardware.fm@1.0',
    'vendor.qti.hardware.radio.ims@1.0',
    'vendor.qti.hardware.radio.ims@1.1',
    'vendor.qti.hardware.radio.ims@1.2',
    'vendor.qti.hardware.radio.ims@1.3',
    'vendor.qti.hardware.radio.ims@1.4',
    'vendor.qti.hardware.radio.ims@1.5',
    'vendor.qti.hardware.radio.ims@1.6',
    'vendor.qti.hardware.radio.ims@1.7',
    'vendor.qti.hardware.radio.internal.deviceinfo@1.0',
    'vendor.qti.hardware.vpp@1.1',
    'vendor.qti.ims.callcapability@1.0',
    'vendor.qti.ims.callinfo@1.0',
    'vendor.qti.ims.rcsconfig@1.0',
    'vendor.qti.ims.rcsconfig@1.1',
    'vendor.qti.ims.rcsconfig@2.0',
    'vendor.qti.ims.rcsconfig@2.1',
    'vendor.qti.imsrtpservice@3.0',
)


def lib_fixup_system_ext(lib: str, partition: str) -> str:
    return f'{lib}_system_ext' if partition == 'system_ext' else lib


lib_fixups: lib_fixups_user_type = {
    **lib_fixups_default,
    system_ext_duplicate_libs: lib_fixup_system_ext,
}


blob_fixups: blob_fixups_user_type = {
    (
        'product/etc/permissions/vendor.qti.hardware.data.connection-V1.0-java.xml',
        'product/etc/permissions/vendor.qti.hardware.data.connection-V1.1-java.xml',
    ): blob_fixup()
        .regex_replace('xml version="2.0"', 'xml version="1.0"'),
    'system_ext/etc/permissions/moto-telephony.xml': blob_fixup()
        .regex_replace('/system/framework/', '/system/system_ext/framework/'),
    (
        'system_ext/lib/lib-imsvideocodec.so',
        'system_ext/lib64/lib-imsvideocodec.so',
    ): blob_fixup()
        .add_needed('libgui_shim.so'),
    'vendor/lib64/libwvhidl.so': blob_fixup()
        .add_needed('libcrypto_shim.so'),
}  # fmt: skip


module = ExtractUtilsModule(
    'sm6150-common',
    'motorola',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=[
        'device/motorola/sm6150-common',
        'hardware/motorola',
        'hardware/qcom-caf/sm8150',
        'hardware/qcom-caf/wlan',
        'vendor/qcom/opensource/dataservices',
        'vendor/qcom/opensource/display',
    ],
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
