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
    call :doxygen class.cfg
    call :doxygen concept.cfg
    call :doxygen define.cfg
    call :doxygen enum.cfg
    call :doxygen file.cfg
    call :doxygen func.cfg
    call :doxygen page.cfg
    call :doxygen relates.cfg
    call :doxygen author.cfg
    call :doxygen par.cfg
    call :doxygen parblock.cfg
    call :doxygen overload.cfg
    call :doxygen example.cfg
    call :doxygen include.cfg
    call :doxygen qtstyle.cfg
    call :doxygen jdstyle.cfg
    call :doxygen structcmd.cfg
    call :doxygen autolink.cfg
    call :doxygen restypedef.cfg
    call :doxygen afterdoc.cfg
    call :doxygen templ.cfg
    call :doxygen tag.cfg
    call :doxygen group.cfg
    call :doxygen diagrams.cfg
    call :doxygen memgrp.cfg
    call :doxygen docstring.cfg
    call :doxygen pyexample.cfg
    call :doxygen manual.cfg
    call :doxygen interface.cfg
    goto end

:clean
    call :rmdir class
    call :rmdir concept
    call :rmdir define
    call :rmdir enum
    call :rmdir file
    call :rmdir func
    call :rmdir page
    call :rmdir relates
    call :rmdir author
    call :rmdir par
    call :rmdir parblock
    call :rmdir overload
    call :rmdir example
    call :rmdir include
    call :rmdir qtstyle
    call :rmdir jdstyle
    call :rmdir structcmd
    call :rmdir autolink
    call :rmdir restypedef
    call :rmdir afterdoc
    call :rmdir template
    call :rmdir tag
    call :rmdir group
    call :rmdir diagrams
    call :rmdir memgrp
    call :rmdir docstring
    call :rmdir pyexample
    call :rmdir manual
    call :rmdir interface
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