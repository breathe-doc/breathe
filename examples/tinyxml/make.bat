@ECHO OFF

set DOXYGEN=doxygen
for /f "delims=" %%i in ('where doxygen') do set DOXYGEN=%%i

set PERL=perl
for /f "delims=" %%i in ('where perl') do set PERL=%%i

set HAVE_DOT=dot
for /f "delims=" %%i in ('where dot') do set HAVE_DOT=%%i

@REM echo DOXYGEN  : %DOXYGEN%
@REM echo PERL     : %PERL%
@REM echo HAVE_DOT : %HAVE_DOT%

if "%1" == "" (
    call :all
    goto end
)

if "%1" == "all" (
    call :all
    goto end
)

if "%1" == "clean" (
    call :clean
    goto end
)

goto end

:all
    call :doxygen tinyxml.cfg
    goto end

:clean
    call :rmdir tinyxml
    goto end

:doxygen
    set CFG=%~1
    echo Running doxygen: %CFG%
    "%DOXYGEN%" %CFG%
    goto end

:rmdir
    set DIR=%~1
    if exist "%DIR%" (
        echo Removing directory: %DIR%
        rmdir /s/q "%DIR%"
    )
    goto end

:end