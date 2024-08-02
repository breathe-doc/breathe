@ECHO OFF

set GENERATED_MOD="breathe\_parser.py"

if "%1" == "html"               goto html
if "%1" == "pdf"                goto pdf
if "%1" == "data"               goto data
if "%1" == "clean"              goto clean
if "%1" == "distclean"          goto distclean
if "%1" == "test"               goto test
if "%1" == "dev-test"           goto dev-test
if "%1" == "flake8"             goto flake8
if "%1" == "black"              goto black
if "%1" == "type-check"         goto type-check
if "%1" == "version-check"      goto version-check
if "%1" == "%GENERATED_MOD%"    goto _parser
if "%1" == "all"                goto all
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
    if exist "%GENERATED_MOD%" (
        echo Removing file: %GENERATED_MOD%
        del "%DIR%"
    )
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
    call :_parser
    cd tests
    set PYTHONPATH=..\;%PYTHONPATH%
    python -m pytest -v
    cd ..
    goto end

:flake8
    flake8 breathe
    goto end

:black
    black --check .
    goto end

:type-check
    mypy --warn-redundant-casts --warn-unused-ignores breathe tests
    goto end

:version-check
    call :_parser
    set PYTHONPATH=..\;%PYTHONPATH%
    python scripts\version-check.py
    goto end

:_parser
    echo Generating %GENERATED_MOD% from xml_parser_generator\schema.json
    python xml_parser_generator\setuptools_builder.py
    goto end

:all
    call :html
    call :pdf
    goto end

:end