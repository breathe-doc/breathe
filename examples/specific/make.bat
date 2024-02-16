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
    @REM ---------------
    @REM General Pattern
    @REM ---------------
    call :doxygen nutshell.cfg
    call :doxygen alias.cfg
    call :doxygen rst.cfg
    call :doxygen inline.cfg
    call :doxygen namespacefile.cfg
    call :doxygen array.cfg
    call :doxygen inheritance.cfg
    call :doxygen members.cfg
    call :doxygen userdefined.cfg
    call :doxygen fixedwidthfont.cfg
    call :doxygen latexmath.cfg
    call :doxygen functionOverload.cfg
    call :doxygen image.cfg
    call :doxygen name.cfg
    call :doxygen union.cfg
    call :doxygen group.cfg
    call :doxygen struct.cfg
    call :doxygen struct_function.cfg
    call :doxygen qtsignalsandslots.cfg
    call :doxygen lists.cfg
    call :doxygen headings.cfg
    call :doxygen links.cfg
    call :doxygen parameters.cfg
    call :doxygen template_class.cfg
    call :doxygen template_class_non_type.cfg
    call :doxygen template_function.cfg
    call :doxygen template_type_alias.cfg
    call :doxygen template_specialisation.cfg
    call :doxygen enum.cfg
    call :doxygen define.cfg
    call :doxygen interface.cfg
    call :doxygen xrefsect.cfg
    call :doxygen tables.cfg
    call :doxygen cpp_anon.cfg
    call :doxygen cpp_concept.cfg
    call :doxygen cpp_enum.cfg
    call :doxygen cpp_union.cfg
    call :doxygen cpp_function.cfg
    call :doxygen cpp_friendclass.cfg
    call :doxygen cpp_inherited_members.cfg
    call :doxygen cpp_trailing_return_type.cfg
    call :doxygen cpp_constexpr_hax.cfg
    call :doxygen cpp_function_lookup.cfg
    call :doxygen c_file.cfg
    call :doxygen c_struct.cfg
    call :doxygen c_enum.cfg
    call :doxygen c_typedef.cfg
    call :doxygen c_macro.cfg
    call :doxygen c_union.cfg
    call :doxygen membergroups.cfg
    call :doxygen simplesect.cfg
    call :doxygen code_blocks.cfg
    call :doxygen dot_graphs.cfg
    @REM -------------
    @REM Special Cases
    @REM -------------
    call :doxygen programlisting.cfg
    call :doxygen decl_impl.cfg
    call :doxygen multifile.cfg
    call :doxygen auto.cfg
    call :doxygen class.cfg
    call :doxygen typedef.cfg
    goto end

:clean
    @REM ---------------
    @REM General Pattern
    @REM ---------------
    call :rmdir nutshell
    call :rmdir alias
    call :rmdir rst
    call :rmdir inline
    call :rmdir namespacefile
    call :rmdir array
    call :rmdir inheritance
    call :rmdir members
    call :rmdir userdefined
    call :rmdir fixedwidthfont
    call :rmdir latexmath
    call :rmdir functionOverload
    call :rmdir image
    call :rmdir name
    call :rmdir union
    call :rmdir group
    call :rmdir struct
    call :rmdir struct_function
    call :rmdir qtsignalsandslots
    call :rmdir lists
    call :rmdir headings
    call :rmdir links
    call :rmdir parameters
    call :rmdir template_class
    call :rmdir template_class_non_type
    call :rmdir template_function
    call :rmdir template_type_alias
    call :rmdir template_specialisation
    call :rmdir enum
    call :rmdir define
    call :rmdir interface
    call :rmdir xrefsect
    call :rmdir tables
    call :rmdir cpp_anon
    call :rmdir cpp_concept
    call :rmdir cpp_enum
    call :rmdir cpp_union
    call :rmdir cpp_function
    call :rmdir cpp_friendclass
    call :rmdir cpp_inherited_members
    call :rmdir cpp_trailing_return_type
    call :rmdir cpp_constexpr_hax
    call :rmdir cpp_function_lookup
    call :rmdir c_file
    call :rmdir c_struct
    call :rmdir c_enum
    call :rmdir c_typedef
    call :rmdir c_macro
    call :rmdir c_union
    call :rmdir membergroups
    call :rmdir simplesect
    call :rmdir code_blocks
    call :rmdir dot_graphs
    @REM -------------
    @REM Special Cases
    @REM -------------
    call :rmdir programlisting
    call :rmdir decl_impl
    call :rmdir multifilexml
    call :rmdir auto
    call :rmdir class
    call :rmdir typedef
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