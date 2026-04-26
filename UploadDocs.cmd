@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

rem Set values for your storage account
set subscription_id=76cec82d-497a-4606-ac2d-1611f7128004
set azure_storage_account=ataaitechtravel
set azure_storage_key=PV2DkhT+mofDzP03A+Wzm9/kHLMl0LavfNcUGAE9j50acC+eUtJ2najvQ4PVuq3s6pDG7o6vyvMd+AStF8hklw==


echo Creating container...
call az storage container create --account-name !azure_storage_account! --subscription !subscription_id! --name margies --auth-mode key --account-key !azure_storage_key! --output none

echo Uploading files...
call az storage blob upload-batch -d margies -s data --account-name !azure_storage_account! --auth-mode key --account-key !azure_storage_key!  --output none
