@ECHO OFF

if "%1" == "html"           goto html
if "%1" == "pdf"            goto pdf
if "%1" == "data"           goto data
if "%1" == "clean"          goto clean
if "%1" == "distclean"      goto distclean
if "%1" == "test"           goto test
if "%1" == "dev-test"       goto dev-test
if "%1" == "ruff"           goto ruff
if "%1" == "type-check"     goto type-check
if "%1" == "version-check"  goto version-check
if "%1" == "all"            goto all
goto end

:html
    call :data
    cd documentation
    call make.bat html
    cd ..
    goto end

:pdf
    call :data
    cd documentation
    call make.bat latexpdf
    cd ..
    goto end

:data
    cd examples\doxygen
    call make.bat all
    cd ..\..
    cd examples\tinyxml
    call make.bat all
    cd ..\..
    cd examples\specific
    call make.bat all
    cd ..\..
    goto end

:clean
    cd examples\doxygen
    call make.bat clean
    cd ..\..
    cd examples\tinyxml
    call make.bat clean
    cd ..\..
    cd examples\specific
    call make.bat clean
    cd ..\..
    goto end

:distclean
    call :clean
    cd documentation
    call make.bat clean
    cd ..
    goto end

:test
    cd tests
    python -m pytest -v
    cd ..
    goto end

:dev-test
    cd tests
    set PYTHONPATH=..\;%PYTHONPATH%
    python -m pytest -v
    cd ..
    goto end

:ruff
    ruff check
    ruff format
    goto end

:type-check
    mypy
    goto end

:version-check
    set PYTHONPATH=..\;%PYTHONPATH%
    python scripts\version-check.py
    goto end

:all
    call :html
    call :pdf
    goto end

:end