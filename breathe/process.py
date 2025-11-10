from __future__ import annotations

import os
from pathlib import Path
from shlex import quote
from typing import TYPE_CHECKING

from breathe.project import AutoProjectInfo, ProjectInfoFactory
from breathe.file_state_cache import MTimeError

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Callable

    from breathe.project import AutoProjectInfo, ProjectInfoFactory

AUTOCFG_TEMPLATE = r"""
PROJECT_NAME     = "{project_name}"
OUTPUT_DIRECTORY = {output_dir}
GENERATE_LATEX   = NO
GENERATE_MAN     = NO
GENERATE_RTF     = NO
CASE_SENSE_NAMES = NO
INPUT            = {input}
ENABLE_PREPROCESSING = YES
QUIET            = YES
JAVADOC_AUTOBRIEF = YES
JAVADOC_AUTOBRIEF = NO
GENERATE_HTML = NO
GENERATE_XML = YES
ALIASES = rst="\verbatim embed:rst"
ALIASES += endrst="\endverbatim"
ALIASES += inlinerst="\verbatim embed:rst:inline"
{extra}
""".strip()


class ProjectData:
    """Simple handler for the files and project_info for each project."""

    def __init__(self, auto_project_info: AutoProjectInfo, files: list[str]) -> None:
        self.auto_project_info = auto_project_info
        self.files = files

class AutoDoxygenCache:
    """Simple handler for the doxygen cache information."""
    
    @staticmethod
    def _getmtime(filename: str):
        try:
            return os.path.getmtime(filename)
        except OSError:
            raise MTimeError("Cannot find file: %s" % os.path.realpath(filename))

    def __init__(self) -> None:
        self._cache: dict[str, float] = {}

    def needs_update(self, info: AutoProjectInfo, files: list[str]) -> bool:
        """Check if any file is newer than the cached time for the provided project info."""
        if not files:
            return False  # No files to check, so no update needed?
        name = info.name()
        try:
             #TODO: Are project names unique?
            cached_time = self._cache[name]
        except KeyError:
            return True  # Project not cached yet

        full_paths = [str(info.abs_path_to_source_file(f)) for f in files]
        max_mtime = max(self._getmtime(file_) for file_ in full_paths)
        return max_mtime > cached_time

    def update_cache(self, info: AutoProjectInfo, files: list[str]) -> None:
        """Update the cache entry for the provided project info."""
        name = info.name()
        full_paths = [str(info.abs_path_to_source_file(f)) for f in files]
        if len(full_paths) == 0:
            self._cache[name] = 0.0
            return
        mtime = max(self._getmtime(file_) for file_ in full_paths)
        self._cache[name] = mtime

class AutoDoxygenProcessHandle:
    def __init__(
        self,
        run_process: Callable,
        write_file: Callable[[str | os.PathLike[str], str, str], None],
        project_info_factory: ProjectInfoFactory,
    ) -> None:
        self.run_process = run_process
        self.write_file = write_file
        self.project_info_factory = project_info_factory

    def generate_xml(
        self,
        projects_source: Mapping[str, tuple[str, list[str]]],
        doxygen_options: Mapping[str, str],
        doxygen_aliases: Mapping[str, str],
        doxygen_cache: AutoDoxygenCache,
    ) -> None:
        project_files: dict[str, ProjectData] = {}

        # First collect together all the files which need to be doxygen processed for each project
        for project_name, file_structure in projects_source.items():
            folder, contents = file_structure
            auto_project_info = self.project_info_factory.create_auto_project_info(
                project_name, folder
            )
            project_files[project_name] = ProjectData(auto_project_info, contents)

        # Iterate over the projects and generate doxygen xml output for the files for each one into
        # a directory in the Sphinx build area
        for project_name, data in project_files.items():
            project_path = self.process(
                data.auto_project_info, data.files, doxygen_options, doxygen_aliases, doxygen_cache
            )
            project_info = data.auto_project_info.create_project_info(project_path)
            self.project_info_factory.store_project_info_for_auto(project_name, project_info)

    def process(
        self,
        auto_project_info: AutoProjectInfo,
        files: list[str],
        doxygen_options: Mapping[str, str],
        doxygen_aliases: Mapping[str, str],
        doxygen_cache: AutoDoxygenCache,
    ) -> str:
        name = auto_project_info.name()
        full_paths = [str(auto_project_info.abs_path_to_source_file(f)) for f in files]

        options = "\n".join("%s=%s" % pair for pair in doxygen_options.items())
        aliases = "\n".join(
            f'ALIASES += {name}="{value}"' for name, value in doxygen_aliases.items()
        )

        cfg = AUTOCFG_TEMPLATE.format(
            project_name=name,
            output_dir=name,
            input=" ".join(full_paths),
            extra=f"{options}\n{aliases}",
        )

        build_dir = Path(auto_project_info.build_dir(), "breathe", "doxygen")
        project_path = os.path.join(build_dir, name, "xml")
        
        if not doxygen_cache.needs_update(auto_project_info, files): 
            #TODO: Should we also pass the config into the cache check, to see if that has changed?
            return project_path

        cfgfile = f"{name}.cfg"
        
        self.write_file(build_dir, cfgfile, cfg)

        # Shell-escape the cfg file name to try to avoid any issue where the name might include
        # malicious shell character - We have to use the shell=True option to make it work on
        # Windows. See issue #271
        self.run_process(f"doxygen {quote(cfgfile)}", cwd=build_dir, shell=True)

        doxygen_cache.update_cache(auto_project_info, files)
        return project_path
