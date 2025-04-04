@echo off
REM Remove old report file if it exists
if exist report.html del report.html
REM Run pytest and generate an HTML report
pytest --html=report.html --self-contained-html
