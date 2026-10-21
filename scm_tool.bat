@echo off
title SCM Automation Tool
python scm_tool.py %*
if "%1"=="" pause
