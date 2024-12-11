@echo off

echo Limpando cache...
rd /s /q "cache"

timeout 1

start build/FXServer.exe +exec server.cfg

exit
